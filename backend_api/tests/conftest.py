# backend_api\tests\conftest.py
"""
Docstring for backend_api.tests.conftest
"""


import pytest
from backend_api.repositories.inmemory import InMemoryCaseRepository

@pytest.fixture
def test_repo():
    """
    Fresh in-memory repository for each test.
    Shared across integration and unit tests if needed.
    """
    return InMemoryCaseRepository()