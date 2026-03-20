# src/dworshak_env/cli_stdlib.py
from __future__ import annotations
import sys
import argparse
import traceback
from pathlib import Path
import pprint
from typing import Optional

from .core import DworshakEnv
from ._version import __version__

TYPER_ONLY = ["helptree"]

def stdlib_notify(msg: str):
    """Print to stderr so it doesn't break shell piping."""
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()

def stdlib_notify_redirect(command: str):
    """Notification for Typer-only commands."""
    msg = [
        f"dworshak-env [lite]: The '{command}' command is only available in the full CLI.",
        "",
        "To enable the full interface, install the required extras:",
        "  pip install 'dworshak-env[typer]'",
        ""
    ]
    sys.stderr.write("\n".join(msg) + "\n")
    sys.stderr.flush()

def build_parser():
    parser = argparse.ArgumentParser(
        prog="dworshak-env",
        description=f"Store and retrieve plaintext, single-key configuration values to a Pythonic .env file v{__version__})",
        add_help=False
    )

    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--debug", action="store_true", help="Enable diagnostic stack traces")

    #subparsers = parser.add_subparsers(dest="command", title="Commands")
    subparsers = parser.add_subparsers(dest="command", title="Commands", required=True)

    # --- GET Command ---
    get_p = subparsers.add_parser("get", help="Retrieve a .env value", add_help=False)
    get_p.add_argument("key", help="The environment variable key")
    get_p.add_argument("--path","-p", type=Path, help="Custom config file path")
    get_p.add_argument("-h", "--help", action="help", help="Show this help")

    # --- SET Command ---
    set_p = subparsers.add_parser("set", help="Store an .env value", add_help=False)
    set_p.add_argument("key", help="The environment variable key")
    set_p.add_argument("value", help="The value to store")
    set_p.add_argument("--path","-p", type=Path, help="Custom .env file path")
    set_p.add_argument("--overwrite", action="store_true", help="Force overwrite existing value")
    set_p.add_argument("-h", "--help", action="help", help="Show this help")

    # --- LIST Command ---
    list_p = subparsers.add_parser("list", help="Show the contents of the target .env file.", add_help=False)
    list_p.add_argument("--path","-p", type=Path, help="Custom .env file path")
    list_p.add_argument("-h", "--help", action="help", help="Show this help")

    # --- LIST Command ---
    remove_p = subparsers.add_parser("remove", help="Remove a key and value from the target .env file.", add_help=False)
    remove_p.add_argument("key", help="The environment variable key")
    remove_p.add_argument("--path","-p", type=Path, help="Custom .env file path")
    remove_p.add_argument("--fail",action="store_true", help="Raise error if config not found"),
    remove_p.add_argument("--yes","-y",action="store_true",help="Skip confirmation prompt (useful in scripts or automation"),
    remove_p.add_argument("-h", "--help", action="help", help="Show this help")
    
    # --- Typer-Only Commands ---
    for cmd in TYPER_ONLY:
        subparsers.add_parser(cmd, help=f"[Requires Typer] Full version of {cmd}", add_help=False)
        
    return parser
    
def main(args=None) -> int:
    parser = build_parser()
    args = parser.parse_args(args)

    if not args.command:
        parser.print_help()
        return 2

    if args.command in TYPER_ONLY:
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
            
        elif args.command == "list":
            data = env_mgr.load()
            pprint.pprint(data)
        
        elif args.command == "remove":
            
            if not args.yes:
                stdlib_notify("Operation cancelled.")
                stdlib_notify("To remove value, please input the '--yes' flag.")
                return 0
            
            deleted = env_mgr.remove(args.key)
            if deleted:
                stdlib_notify(f"Removed value for key: {args.key}")
            else:
                if args.fail:
                    raise KeyError(f"No value found for key: {args.key}")
                stdlib_notify(f"No value found for key: {args.key}")


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
