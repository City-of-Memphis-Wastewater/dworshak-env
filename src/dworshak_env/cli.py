# src/dworshak_env/cli.py
import typer
from typer.models import OptionInfo
from rich.console import Console
import os
from pathlib import Path
from typing import Optional
try:
    from typer_helptree import add_typer_helptree
except:
    pass
from .core import DworshakEnv
from ._version import __version__


console = Console() # to be above the tkinter check, in case of console.print
app = typer.Typer()

# Force Rich to always enable colors, even when running from a .pyz bundle
os.environ["FORCE_COLOR"] = "1"
# Optional but helpful for full terminal feature detection
os.environ["TERM"] = "xterm-256color"

app = typer.Typer(
    name="dworshak-env",
    help=f"Store and retrieve plaintext, single-key configuration values to typical .env file. (v{__version__})",
    no_args_is_help=True,
    add_completion=False,
    context_settings={"ignore_unknown_options": True,
                      "help_option_names": ["-h", "--help"]},
)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context,
    version: Optional[bool] = typer.Option(
    None, "--version", is_flag=True, help="Show the version."
    )
    ):
    """
    Enable --version
    """
    if version:
        typer.echo(__version__)
        raise typer.Exit(code=0)

try:
    add_typer_helptree(app=app, console=console, version = __version__,hidden=True)
except:
    pass
@app.command()
def get(
    key: str = typer.Argument(..., help="The key key (e.g., port)."),
    value: str = typer.Option(None, "--value", help="Identify a value."),
    path: Path = typer.Option(None, "--path", help="Custom config file path."),
):
    """
    Get a .env configuration value (single-key).
    """
    env_mgr = DworshakEnv(path=path)
    value = env_mgr.get(key=key)
    
    if value is not None:
        # Just the value. No brackets, no labels.
        typer.echo(value)
    else:
        # Errors go to stderr so they don't get captured in variables
        typer.echo(f"Error: key '{key}' not found", err=True)
        raise typer.Exit(code=1)

@app.command()
def set(
    key: str = typer.Argument(..., help="The key key (e.g., port)."),
    value: str = typer.Option(None, "--value", help="Directly set a value."),
    path: Path = typer.Option(None, "--path", help="Custom config file path."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Force a new prompt.")
):
    """
    Store or update a .env configuration value (single-key).
    """
    if value is None:
        typer.echo(f"Provided: None. No value saved.", err=True)
        return
    env_mgr = DworshakEnv(path=path)
    existing_value = env_mgr.get(key=key)

    # If it exists and we aren't overwriting, print value and exit
    if existing_value is not None and not overwrite:
        # We still send 'Existing:' to stderr for context, but raw value to stdout
        typer.echo(existing_value)
        return

    # Trigger the prompt or the direct set
    final_value = env_mgr.set(
        key=key,
        value=value,
        overwrite=overwrite
    )

    if final_value is not None:
        # Status message goes to stderr
        typer.echo(f"Stored [{key}] successfully.", err=True)
        # ONLY the value goes to stdout
        typer.echo(final_value)
    else:
        # Error context to stderr
        typer.echo(f"Error: Failed to set value for [{key}]", err=True)
        
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

