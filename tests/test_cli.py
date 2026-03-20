# tests/test_cli.py
"""
How can I make a test optional, like if only a certain pyproject.toml option dependency group is used?
"""
import pytest

typer = pytest.importorskip("typer")
from typer.testing import CliRunner
from dworshak_env.cli import app
from dworshak_env._version import __version__

runner = CliRunner()

@pytest.mark.typer
def test_version(capsys):
    cmd = ["--version"]
    result = runner.invoke(app,cmd)
    if result.exit_code != 0:
        print(f"\nCLI Error Output: {result.output}")  # This will show up with -s
    
    # Capture the output that was printed before the exit
    captured = capsys.readouterr()
    
    # This is better documentation: it proves the CLI matches the package version
    assert __version__ in captured.out

    # If you want to be strict about SemVer (x.y.z)
    assert captured.out.strip().count(".") >= 2

    # Exit code 0 indicates a successful, intended termination
    with pytest.raises(SystemExit) as excinfo:
        assert excinfo.value.code == 0

@pytest.mark.typer
def test_list():
    cmd = ["list"]
    result = runner.invoke(app,cmd)
    if result.exit_code != 0:
        print(f"\nCLI Error Output: {result.output}")  # This will show up with -s
    assert result.exit_code == 0

@pytest.mark.typer
def test_lifecycle():
    """Test the full lifecycle of a key to ensure state doesn't break individual tests."""
    # 1. SET the value
    set_result = runner.invoke(app, ["set", "milk", "white", "--overwrite"])
    assert set_result.exit_code == 0

    # 2. GET the value
    get_result = runner.invoke(app, ["get", "milk"])
    assert get_result.exit_code == 0
    assert "white" in get_result.output

    # 3. REMOVE the value
    remove_result = runner.invoke(app, ["remove", "milk", "--yes"])
    assert remove_result.exit_code == 0
