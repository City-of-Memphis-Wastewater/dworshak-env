# tests/test_cli_stdlib.py

import pytest
from dworshak_env._version import __version__

@pytest.mark.argparse
def test_parser():
    from dworshak_env.cli_stdlib import build_parser
    parser = build_parser()
    argument = ["--version"]
    args = parser.parse_args(argument)
    assert args.version == __version__

@pytest.mark.argparse
def test_missing_argument():
    from dworshak_env.cli_stdlib import main
    with pytest.raises(SystemExit):
        main()
