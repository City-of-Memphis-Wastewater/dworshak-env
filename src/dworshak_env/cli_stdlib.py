# src/dworshak_env/cli_stdlib.py
from __future__ import annotations
import sys
import argparse
import traceback
from pathlib import Path
from typing import Optional

from .core import DworshakEnv
from ._version import __version__

def stdlib_notify(msg: str):
    """Print to stderr so it doesn't break shell piping."""
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()

def stdlib_notify_redirect(command: str):
    """Notification for Typer-only commands."""
    msg = [
        f"dworshak-env [lite]:: The '{command}' command is only available in the full CLI.",
        "",
        "To enable the full interface, install the required extras:",
        "  pip install 'dworshak-env[typer]'",
        ""
    ]
    sys.stderr.write("\n".join(msg) + "\n")
    sys.stderr.flush()

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="dworshak-env",
        description=f"Store and retrieve plaintext, single-key configuration values to a Pythonic .env file v{__version__})",
        add_help=False
    )

    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--debug", action="store_true", help="Enable diagnostic stack traces")

    subparsers = parser.add_subparsers(dest="command", title="Commands")

    # --- GET Command ---
    get_p = subparsers.add_parser("get", help="Retrieve a .env value", add_help=False)
    get_p.add_argument("key", help="The environment variable key")
    get_p.add_argument("--path", type=Path, help="Custom config file path")
    get_p.add_argument("-h", "--help", action="help", help="Show this help")

    # --- SET Command ---
    set_p = subparsers.add_parser("set", help="Store an .env value", add_help=False)
    set_p.add_argument("key", help="The environment variable key")
    set_p.add_argument("value", help="The value to store")
    set_p.add_argument("--path", type=Path, help="Custom .env file path")
    set_p.add_argument("--overwrite", action="store_true", help="Force overwrite existing value")
    set_p.add_argument("-h", "--help", action="help", help="Show this help")

    # --- Typer-Only Commands ---
    typer_only = ["helptree"]
    for cmd in typer_only:
        subparsers.add_parser(cmd, help=f"[Requires Typer] Full version of {cmd}", add_help=False)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command in typer_only:
        stdlib_notify_redirect(args.command)
        return 1

    try:
        env_mgr = DworshakEnv(path=args.path)

        if args.command == "get":
            value = env_mgr.get(args.key)
            if value is not None:
                # RAW stdout for automation
                print(value)
                return 0
            else:
                stdlib_notify(f"Error: key '{args.key}' not found.")
                return 1

        elif args.command == "set_":
            if args.value is None:
                stdlib_notify("Error: No value provided for set command.")
                return 1

            existing_value = env_mgr.get(args.key)
            
            # Match Typer CLI: if exists and no overwrite, just print existing and exit
            if existing_value is not None and not args.overwrite:
                print(existing_value)
                return 0

            final_value = env_mgr.set(args.key, args.value, overwrite=args.overwrite)
            
            if final_value is not None:
                stdlib_notify(f"Stored [{args.key}] successfully.")
                print(final_value) # Raw stdout
                return 0
            else:
                stdlib_notify(f"Error: Failed to set value for [{args.key}]")
                return 1
            

        elif args.command == "set":
            existing_value = env_mgr.get(args.key)
            
            # Use stderr to tell the human what's happening
            if existing_value is not None and not args.overwrite:
                stdlib_notify(f"Key [{args.key}] already exists. Use --overwrite to change it.")
                print(existing_value) # Data still goes to stdout for scripts
                return 0

            final_value = env_mgr.set(args.key, args.value, overwrite=args.overwrite)
            
            if final_value is not None:
                stdlib_notify(f"Stored [{args.key}] successfully.")
                print(final_value)
                return 0

    except KeyboardInterrupt:
        stdlib_notify("\nInterrupted.")
        return 130
    except Exception as e:
        stdlib_notify(f"Error: {e}")
        if args.debug:
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())