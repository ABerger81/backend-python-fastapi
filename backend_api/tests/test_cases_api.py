# test_cases_api.py
# # Test cases for backend_api main.py, not the repository
# directly
# Using FastAPI's TestClient to simulate API requests
# Integration-test ´light´
# Run the tests with:
# ```bash pytest -> 6 passed in X.XXs

from fastapi.testclient import TestClient
import pytest


from backend_api.main import app, get_case_repository
from backend_api.repository import CaseRepository

@pytest.fixture
def test_repo():
    # Create a fresh repository for each test
    return CaseRepository()

@pytest.fixture
def client(test_repo):
    # Override the dependency to use the test repository
    def override_get_case_repository():
        return test_repo
    
    app.dependency_overrides[get_case_repository] = override_get_case_repository

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

# Test 1 - POST /cases/
def test_create_case(client):
    # Arrange & Act
    response = client.post(
        "/cases/",
        json={
            "title": "Test case",
            "description": "Testing POST",
            "status": "open"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test case"
    assert data["description"] == "Testing POST"
    assert data["status"] == "open"
    
    # What this test proves:
    # Request → schema → repo → response works
    # Enum validation works
    # ID is created correctly

# Test 2 - GET /cases/
def test_get_all_cases(client):
    # Arrange - create a case first
    client.post(
        "/cases/",
        json={
            "title": "Test case",
            "description": "Testing GET all",
            "status": "open"
        }
    )
    response = client.get("/cases/")
    assert response.status_code == 200
    # Get JSON data
    data = response.json()
    # Response is a list
    assert isinstance(data, list)
    # At least one case created in previous test
    assert len(data) >= 1

    # Deliberately simple testing
    # We test behavior, not implementation

# Test 3 - GET /cases/
def test_get_case_by_id(client):
    # Arrange - create a case first
    client.post(
        "/cases/",
        json={
            "title": "Another case",
            "description": "Testing GET by id",
            "status": "open"
        }
    )
    response = client.get("/cases/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

    # What this test proves:
    # GET by id works
    # ID mapping works
    # Schema validation works
    # Dependency Injection works
    # Repository works
    # Integration of all parts works
    # End-to-end test

# Test 4 - GET non existing id -> 404
def test_non_existing_case(client):
    # Arrange - create no case
    client.post(
        "/cases/",
        json={
            "title": "Another case",
            "description": "Testing GET non-existing id",
            "status": "open"
        }
    )
    response = client.get("/cases/9999")
    assert response.status_code == 404

    # This proves:
    # Error handling works
    # The API follows REST convention

# Test 5 - PUT /cases/{id}
def test_update_case(client):
    # Arrange - update existing case
    client.post(
        "/cases/",
        json={
            "title": "Case to update",
            "description": "Testing PUT",
            "status": "open"
        }
    )
    response = client.put(
        "/cases/1",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "status": "closed"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "closed"

    # This proves:
    # Update works
    # Object mutation works
    # Enum validation works
    # Integration of all parts works
    # End-to-end test

# Test 6 - DELETE /cases/{id}
def test_delete_case(client):
    # Arrange - delete excisting case
    client.post(
        "/cases/",
        json={
            "title": "Case to delete",
            "description": "Testing DELETE",
            "status": "open"
        }
    )
    response = client.delete("/cases/1")
    assert response.status_code == 204

    response = client.get("/cases/1")
    assert response.status_code == 404

    # This proves:
    # Deletion works
    # Integration of all parts works
    # End-to-end test