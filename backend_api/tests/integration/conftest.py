# backend_api\tests\integration\conftest.py

import sqlite3
import pytest
from fastapi.testclient import TestClient

from backend_api.main import app
from backend_api.dependencies import get_repository
from backend_api.repositories.sqlite import SQLiteCaseRepository

@pytest.fixture
def client():
    connection = sqlite3.connect(":memory:")
    repository = SQLiteCaseRepository(connection)

    app.dependency_overrides[get_repository] = lambda: repository

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()