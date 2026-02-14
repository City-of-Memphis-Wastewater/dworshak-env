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
    Get or set a .env configuration value (single-key).
    """
    env_mgr = DworshakEnv(path=path)
    
    value = env_mgr.get(
        key=key,
    )
    if value:
        # Only print the value to stdout for piping/capture
        typer.echo(f"[{key}] = {value}")

@app.command()
def set(
    key: str = typer.Argument(..., help="The key key (e.g., port)."),
    value: str = typer.Option(None, "--value", help="Directly set a value."),
    message: str = typer.Option(None, "--message", help="Custom prompt message."),
    path: Path = typer.Option(None, "--path", help="Custom config file path."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Force a new prompt.")
):
    """
    Get or set a .env configuration value (single-key).
    """
    env_mgr = DworshakEnv(path=path)
    
    exisiting_value = env_mgr.get(
        key=key,
    )
    if exisiting_value is not None :
        env_mgr.get_value(key, value)
        display_existing_val = value
        typer.echo(f"Existing: [{key}] = {display_existing_val}")

    if (exisiting_value is None) or (exisiting_value is not None and overwrite):
        value = env_mgr.set(
            key=key,
            prompt_message=message,
            overwrite=overwrite
        )
    else:
        value =  exisiting_value
    
    if value:
        # Only print the value to stdout for piping/capture
        typer.echo(f"[{key}] = {value}")

if __name__ == "__main__":
    app()

