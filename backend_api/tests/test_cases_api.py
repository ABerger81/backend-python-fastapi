# Test cases for backend_api main.py, not the repository
# directly
# Using FastAPI's TestClient to simulate API requests
# Integration-test ´light´
# Run the tests with:
# bash: pytest
# You should see:
# 6 passed in X.XXs
from binascii import Error
from enum import Enum
from sys import implementation
from fastapi import Request
from fastapi.testclient import TestClient
from backend_api.main import app

client = TestClient(app)

# Test 1 - POST /cases/
def test_create_case():
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
def test_get_all_cases():
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
def test_get_case_by_id():
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
def test_non_existing_case():
    response = client.get("/cases/9999")
    assert response.status_code == 404

    # This proves:
    # Error handling works
    # The API follows REST convention

# Test 5 - PUT /cases/{id}
def test_update_case():
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
def test_delete_case():
    response = client.delete("/cases/1")
    assert response.status_code == 204

    response = client.get("/cases/1")
    assert response.status_code == 404

    # This proves:
    # Deletion works
    # Integration of all parts works
    # End-to-end test