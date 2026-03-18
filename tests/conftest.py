# tests/conftest.py
import pytest
import tempfile
from pathlib import Path
from dworshak_env.core import DworshakEnv

@pytest.fixture
def temp_env_file():
    """Creates a temporary .env file and cleans it up after the test."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as tmp:
        tmp.write("EXISTING_KEY=old_value\n")
        tmp_path = tmp.name
    
    yield Path(tmp_path)
    
    # Cleanup after test is done
    path = Path(tmp_path)
    if path.exists():
        path.unlink()

@pytest.fixture
def env_mgr(temp_env_file):
    """Provides a DworshakEnv instance pointing to the temp file."""
    return DworshakEnv(path=temp_env_file)
