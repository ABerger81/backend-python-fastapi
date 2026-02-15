# backend_api\tests\integration\test_cases_api_negative.py

def test_create_case_missing_title(client):
    response = client.post(
        "/cases/",
        json={
            "description": "Missing title",
            "status": "open",
        },
    )

    # 422 = FastAPI validation error
    assert response.status_code == 422

def test_create_case_invalid_status(client):
    response = client.post(
        "/cases/",
        json={
            "title": "Test",
            "description": "Invalid status",
            "status": "invalid",
        },
    )

    assert response.status_code == 422

def test_get_case_not_found(client):
    response = client.get("/cases/999")

    assert response.status_code == 404

def test_update_case_not_found(client):
    response = client.put(
        "/cases/999",
        json={
            "title": "Updated",
            "description": "Updated",
            "status": "open",
        },
    )

    assert response.status_code == 404

def test_delete_case_not_found(client):
    response = client.delete("/cases/999")

    assert response.status_code == 404