# backend_api\tests\conftest.py
"""
Docstring for backend_api.tests.conftest
"""

import sqlite3
import pytest
from contextlib import contextmanager
from fastapi.testclient import TestClient

from backend_api.main import app
from backend_api.dependencies import get_case_service
from backend_api.repositories.sqlite import SQLiteCaseRepository
from backend_api.services.case_service import CaseService


@contextmanager
def test_connection_factory():
    """
    SQLite in-memory database for tests.
    One connection per operation, same thread.
    """
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    # Create schema once per connection
    conn.executescript(
        """
        CREATE TABLE cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL
        );
        """
    )

    try:
        yield conn
    finally:
        conn.close()


def get_test_case_service() -> CaseService:
    repository = SQLiteCaseRepository(test_connection_factory)
    return CaseService(repository)


@pytest.fixture
def client():
    app.dependency_overrides[get_case_service] = get_test_case_service

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
