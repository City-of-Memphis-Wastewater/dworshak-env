# tests/conftest.py
import pytest
from pathlib import Path
from dworshak_env.core import DworshakEnv
import os

@pytest.fixture
def env_mgr(tmp_path, monkeypatch):
    """
    Provides a DworshakEnv instance pointed at a temporary file.
    Also ensures os.environ changes are reverted after every test.
    """
    # Create a dummy .env in a temp directory
    test_env_file = tmp_path / ".env"
    #test_env_file.write_text("TEST_KEY=test_value\n", encoding="utf-8")
    test_env_file.write_text("EXISTING_KEY=old_value\n", encoding="utf-8")

    # Isolate os.environ so tests don't pollute your actual terminal session.
    # Use monkeypatch to isolate environment variable changes.
    # This prevents tests from leaking keys into your shell session.
    monkeypatch.setattr(os, "environ", os.environ.copy())

    return DworshakEnv(path=test_env_file)