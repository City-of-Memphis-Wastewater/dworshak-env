# tests/test_cli.py
"""
How can I make a test optional, like if only a certain pyproject.toml option dependency group is used?
"""
import pytest

typer = pytest.importorskip("typer")
from typer.testing import CliRunner
from dworshak_env.cli import app

runner = CliRunner()

@pytest.mark.typer
def test_version():
    cmd = ["--version"]
    result = runner.invoke(app,cmd)
    if result.exit_code != 0:
        print(f"\nCLI Error Output: {result.output}")  # This will show up with -s
    assert result.exit_code == 0

@pytest.mark.typer
def test_get():
    cmd = ["get","milk"]
    result = runner.invoke(app,cmd)
    if result.exit_code != 0:
        print(f"\nCLI Error Output: {result.output}")  # This will show up with -s
    assert result.exit_code == 0

@pytest.mark.typer
def test_set():
    cmd = ["set","milk","0","--overwrite"]
    result = runner.invoke(app,cmd)
    if result.exit_code != 0:
        print(f"\nCLI Error Output: {result.output}")  # This will show up with -s
    assert result.exit_code == 0

@pytest.mark.typer
def test_remove():
    cmd = ["remove","milk","--yes"]
    result = runner.invoke(app,cmd)
    if result.exit_code != 0:
        print(f"\nCLI Error Output: {result.output}")  # This will show up with -s
    assert result.exit_code == 0

@pytest.mark.typer
def test_list():
    cmd = ["list"]
    result = runner.invoke(app,cmd)
    if result.exit_code != 0:
        print(f"\nCLI Error Output: {result.output}")  # This will show up with -s
    assert result.exit_code == 0

