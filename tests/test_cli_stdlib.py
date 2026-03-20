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
'''
@pytest.mark.argparse
def test_missing_argument_usage_error():
    """
    ASSURE: Running the CLI without commands (get, set, etc.) fails gracefully.
    STABILIZE: Ensures the user is prompted with usage info rather than a 
    Python stack trace when no arguments are provided.
    """
    from dworshak_env.cli_stdlib import main
    
    # Argparse usually exits with code 2 for usage errors (missing arguments)
    with pytest.raises(SystemExit) as excinfo:
        main([]) # Passing empty list to simulate no CLI input
        #main() # Passing empty list to simulate no CLI input
        
    assert excinfo.value.code != 0
'''
'''
@pytest.mark.argparse
def test_invalid_argument_error(capsys):
    """
    ASSURE: Providing an unrecognized command results in a non-zero exit.
    STABILIZE: Ensures the user is notified of a 'choice error' 
    rather than the program silently doing nothing.
    """
    from dworshak_env.cli_stdlib import main
    
    # We pass an invalid command 'NOT-A-COMMAND'
    with pytest.raises(SystemExit) as excinfo:
        main(["NOT-A-COMMAND"])
        
    # Argparse exit code 2 is standard for command-line syntax errors
    assert excinfo.value.code != 0
    
    captured = capsys.readouterr()
    assert "invalid choice" in captured.err.lower()
'''
'''
def test_missing_argument_usage_error():
    from dworshak_env.cli_stdlib import main
    
    # Since main() now returns an int instead of calling sys.exit,
    # we just check the return value.
    exit_code = main([]) 
    assert exit_code != 0
'''
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