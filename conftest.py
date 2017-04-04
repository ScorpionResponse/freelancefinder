"""pytest global configuration."""

import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable db across all tests."""
    pass
