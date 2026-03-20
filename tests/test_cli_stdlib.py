# tests/test_cli_stdlib.py
import pytest
from dworshak_env._version import __version__

@pytest.mark.argparse
def test_parser_version_exit(capsys):
    """
    ASSURE: The --version flag correctly triggers the version display and exits.
    DEMONSTRATE: Argparse handles --version by printing to stdout and calling 
    sys.exit(0). We catch SystemExit to prevent the test runner from crashing.
    """
    from dworshak_env.cli_stdlib import build_parser
    parser = build_parser()
    
    # We expect argparse to stop execution immediately upon seeing --version
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_args(["--version"])

    # Capture the output that was printed before the exit
    captured = capsys.readouterr()
    
    # This is better documentation: it proves the CLI matches the package version
    assert __version__ in captured.out

    # If you want to be strict about SemVer (x.y.z)
    assert captured.out.strip().count(".") >= 2

    # Exit code 0 indicates a successful, intended termination
    assert excinfo.value.code == 0

@pytest.mark.argparse
def test_missing_argument_usage_status():
    """
    ASSURE: The CLI identifies 'no command' as an incomplete request.
    STABILIZE: Ensures the return code is non-zero so scripts can detect 
    that no action was taken.
    """
    from dworshak_env.cli_stdlib import main
    result = main([])
    assert result != 0