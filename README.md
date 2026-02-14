# Backend API - Case Management (FastAPI)

A backend API built with **FastAPI** demonstrating clean architecture,
dependency injection, and automated testing.

This project is developed as part of my training in backend development,
with a focus on structure, testability, and maintainability.

---

## Project scope (current)

- Backend-only application
- Repository abstraction with multiple implementations
- In-memory repository for unit tests
- SQLite-backed repository for integration testing and development
- Fully tested API endpoints

---

## Functionality

The API provides basic CRUD operations for managing cases:

- Create case
- Retreive all cases
- Retrieve a specific case by ID
- Update a case
- Delete a case

Each case contains:
- `id`
- `title`
- `description`
- `status` (`open` / `closed`)

---

## Architecture overview

The application follows a layered architechture:

- **API layer**
    FastAPI endpoints and request/response validation

- **Service layer**
    Business logic and domain rules

- **Repository layer**
    Data access abstraction (currently in-memory storage)

This separation allows the storage mechanism to be replaced (e.g. with a database)
without changing the API or business logic.

### Repository implementations

The repository layer is defined as an abstract contract and has multiple implementations:

- **InMemoryCaseRepository**
    Used for unit tests and fast, isolated execution.

- ** SQLiteCaseRepository**
    Used for integration tests and local development, providing real persistence.

This allows switching storage mechanisms without modifying business logic or API code.

---

## Running the application locally

1. Clone the repository
```bash
git clone <repo-url>
cd backend-api
```

2. Create and activate virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Start the development server
```bash
uvicorn backend_api.main:app --reload
```

The API will be available at:
- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

---

## Testing
Automated tests are written using pytest and FastAPI's 

API tests are written using `pytest` and FastAPI's `TestClient`.

To run the test suite:

```bash
pytest
```

Tests include:
- API integration tests
- Repository unit tests
- Service layer unit tests

---

## Future direction
This project is intended to evolve into a fullstack application.
Planned architectural improvements include:
- Introducing a repository contract to support multiple storage implementations
- Adding persistent storage (SQLite -> ORM later)
- Strengthening integration tests with real infrastructure
- Authentication and authorization
- Frontend client
- CI/CD pipeline