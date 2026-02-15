# backend_api\tests\integration\conftest.py

import sqlite3
import pytest
from fastapi.testclient import TestClient

from backend_api.main import app
from backend_api.dependencies import get_case_service
from backend_api.repositories.sqlite import SQLiteCaseRepository
from backend_api.services.case_service import CaseService


@pytest.fixture
def client():
    """
    Integration test client with a shared, thread-safe in-memory SQLite database.
    """

    # ONE shared connection for the whole test
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # Create schema once
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

    # Always return the same connection
    def connection_factory():
        return conn

    def get_test_case_service() -> CaseService:
        repository = SQLiteCaseRepository(connection_factory)
        return CaseService(repository)

    app.dependency_overrides[get_case_service] = get_test_case_service

    with TestClient(app) as test_client:
        yield test_client

    conn.close()
    app.dependency_overrides.clear()
