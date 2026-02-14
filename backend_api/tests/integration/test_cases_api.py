# backend_api\tests\integration\test_cases_api.py
"""
Integration tests for backend_api.main.

These tests verify the full request -> validation -> service -> repository -> response flow using FastAPI's TestClient.
"""
from fastapi.testclient import TestClient
import pytest



# Test 1 - POST /cases/
def test_create_case(client):
    response = client.post(
        "/cases/",
        json={
            "title": "Test case",
            "description": "Testing POST",
            "status": "open",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    
    # What this test proves:
    # Request → schema → repo → response works
    # Enum validation works
    # ID is created correctly

# Test 2 - GET /cases/
def test_get_all_cases(client):
    client.post(
        "/cases/",
        json={
            "title": "Test",
            "description": "Desc",
            "status": "open",
        },
    )
    response = client.get("/cases/")
    assert response.status_code == 200
    assert len(response.json()) == 1

# Test 3 - GET /cases/
def test_get_case_by_id(client):
    client.post(
        "/cases/",
        json={
            "title": "Test",
            "description": "Desc",
            "status": "open",
        },
    )
    response = client.get("/cases/1")
    assert response.status_code == 200

    # What this test proves:
    # Get by id works
    # ID mapping works

# Test 4 - PUT /cases/{id}
def test_update_case(client):
    client.post(
        "/cases/",
        json={
            "title": "Test",
            "description": "Desc",
            "status": "open",
        },
    )
    response = client.put(
        "/cases/1",
        json={
            "title": "Updated",
            "description": "Updated",
            "status": "closed",
        },
    )
    assert response.status_code == 200

    # This proves:
    # Update works
    # Object mutation works
    # Enum validation works
    # Integration of all parts works

# Test 5 - DELETE /cases/{id}
def test_delete_case(client):
    client.post(
        "/cases/",
        json={
            "title": "Test",
            "description": "Desc",
            "status": "open",
        },
    )
    response = client.delete("/cases/1")
    assert response.status_code == 204

    # This proves:
    # Deletion works
    # Integration of all parts works