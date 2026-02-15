# Backend API - Case Management (FastAPI)

A backend API built with **FastAPI** demonstrating clean architechture,
dependency injection, and automated testing.

This project is developed as part of my training in backend development,
with a focus on structure, testability, and maintainability.

---

## Project scope (current)

- Backend-only application
- Clear separation between API, service, and repository layers
- Repository abstraction with multiple implementations
- Automated unit and integration testing
- SQLite-backed persistence for development and integration tests

---

## Functionality
The API provides basic CRUD operations for managing cases:

- Create case
- Retreive all cases
- Retreive a specific case by ID
- Update a case
- Delete a case

Each case contains:
- `id`
- `title`
- `description`
- `status` (`open` / `closed`)

---

## Architechture overview
The application follows a layered architechture:

### API layer
- FastAPI endpoints
- Request and response validation
- Translation of domain errors to HTTP responses

### Service layer
- Business logic
- Domain rules
- Independent of HTTP and persistence concerns

### Repository layer
- Abstract repository contract
- Concrete implementation for different storage mechanisms

This separation allows the storage mechanism to be replaced
without changing the API or business logic code.

---

## Repository implementations
The repository layer is defined as an abstract contract and has multiple implementations:

- **InMemoryCaseRepository**
    - Used for unit tests
    - Fast, isolated and deterministic

- **SQLiteCaseRepository**
    - Used for integration tests and local development
    - Provides real persistence using SQLite
    - Uses in-memory SQLite databases during tests

The active repository implementaion is selected using FastAPI dependency injection.

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
Automated tests are written using pytest and FastAPI's **TestClient** 

To run the full test suite:

```bash
pytest
```
## Test Structure
- **Unit tests**
    - Service layer logic
    - Repository implementation using in-memory storage
    - No HTTP or database dependencies
- **Integration tests**
    - Full API requests via HTTP
    - Real SQLite database (in-memory)
    - Dependency overrides to ensure test validation
This approach ensures fast feedback while still validating real system behavior.

---

## Error handling strategy
- Business rule violations raise domain-level errors in the service layer
- The API layer translates domain errors into appropriate HTTP responses
- The persistence layer contains no HTTP or validation logic

---

## Future direction
This project is intended to evolve into a fullstack application.
Planned architectural improvements include:
- Stronger request validation and error contracts
- Authenticaton and authorization
- Frontend client
- CI/CD pipeline

---

## Development notes
- Build artifacts and test caches are excluded from version control
- Dependency injection is used to swap repository implementations in tests
- SQLite is used for integration testing via in-memory databases