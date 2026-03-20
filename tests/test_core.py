#tests/test_core.py
from __future__ import annotations
import pytest
import os
from dworshak_env.core import DworshakEnv

@pytest.mark.core
def test_load_existing_value(env_mgr):
    # We defined EXISTING_KEY=old_value in the fixture
    assert env_mgr.get("EXISTING_KEY") == "old_value"

@pytest.mark.core
def test_set_new_value(env_mgr):
    env_mgr.set("NEW_KEY", "new_value")
    assert env_mgr.get("NEW_KEY") == "new_value"
    # Verify it actually hit the process environment too
    assert os.environ["NEW_KEY"] == "new_value"

@pytest.mark.core
def test_get_with_defaults():
    # Test the 'defaults' dict logic without a file
    mgr = DworshakEnv(path="non_existent.env", defaults={"PORT": "8080"})
    assert mgr.get("PORT") == "8080"

@pytest.mark.core
def test_remove_key(env_mgr):
    env_mgr.set("TO_DELETE", "gone_soon")
    assert env_mgr.remove("TO_DELETE") is True
    assert env_mgr.get("TO_DELETE") is None
