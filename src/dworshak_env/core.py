# src/dworshak_env/core.py
from __future__ import annotations
import os
import tempfile
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("dworshak_env")

class DworshakEnv:
    def __init__(
        self, 
        path: str | Path | None = None, 
        defaults: Optional[Dict[str, str]] = None
    ):
        """
        Manages environment variables with fallback to a .env file.
        
        Args:
            path: Path to the .env file. Defaults to '.env' in the current directory.
            defaults: Hardcoded fallbacks if key is missing from os.environ and file.
        """
        self.path = Path(path) if path else Path(".env")
        self.defaults = defaults or {}

    def _load_dotenv(self) -> Dict[str, str]:
        """
        Parses the .env file into a dictionary.
        Supports basic KEY=VALUE pairs, skipping comments and empty lines.
        """
        env_dict = {}
        if not self.path.exists():
            return env_dict
        
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    
                    k, v = line.split("=", 1)
                    # Handle basic quoting and whitespace
                    k = k.strip()
                    v = v.strip().strip("'").strip('"')
                    env_dict[k] = v
        except Exception as e:
            logger.warning(f"Failed to read .env at {self.path}: {e}")
            
        return env_dict

    def _save_dotenv(self, env_dict: Dict[str, str]):
        """
        Writes the dictionary to the .env file using an atomic write pattern.
        This prevents file corruption during power loss or application crashes.
        """
        dir_name = self.path.parent
        dir_name.mkdir(parents=True, exist_ok=True)

        # Create a temporary file in the same directory to ensure it's on the same partition
        with tempfile.NamedTemporaryFile(
            mode="w", 
            dir=dir_name, 
            delete=False, 
            encoding="utf-8"
        ) as tf:
            for k, v in env_dict.items():
                tf.write(f"{k}={v}\n")
            temp_path = Path(tf.name)

        try:
            # Atomic rename (replace)
            temp_path.replace(self.path)
        except Exception as e:
            logger.error(f"Atomic write failed for {self.path}: {e}")
            if temp_path.exists():
                temp_path.unlink()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a value based on priority: 
        1. os.environ
        2. .env file
        3. Local defaults dictionary
        4. Method 'default' argument
        """
        val = os.getenv(key)
        if val is not None:
            return val
        
        file_values = self._load_dotenv()
        if key in file_values:
            return file_values[key]
        
        if key in self.defaults:
            return self.defaults[key]
            
        return default

    def set(
        self, 
        key: str, 
        value: Optional[str] = None, 
        prompt_message: Optional[str] = None,
        overwrite: bool = False
    ) -> str | None:
        """
        Updates the .env file with the provided value. 
        If value is None, triggers dworshak_ask to prompt the user.
        """
        current_val = self.get(key)
        
        if value is None:
            if current_val is None or overwrite:
                from dworshak_prompt import dworshak_ask
                msg = prompt_message or f"Enter value for {key}"
                value = dworshak_ask(message=msg, default=current_val)
            else:
                value = current_val

        if value is not None:
            data = self._load_dotenv()
            data[key] = str(value)
            self._save_dotenv(data)
            # Synchronize current process environment
            os.environ[key] = str(value)
            
        return value

def dworshak_env(key: str, default: Any = None, **kwargs) -> Any:
    """
    Functional wrapper for DworshakEnv.get.
    Usage: val = dworshak_env("API_KEY", path="/path/to/.env")
    """
    return DworshakEnv(**kwargs).get(key, default=default)
