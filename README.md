# Backend API - Case Management (FastAPI)

A simple backend API built with **FastAPI** to handle issues (cases).
The project is part of my training in backen and fullstack development.

## Important!
- Uses in-memory storage (no database yet)

## Functionality

The API supports basic CRUD operations for cases:

- Create case
- Get all cases
- Get a specific case by ID
- Update case
- Delete case

Each case contains:
- id
- title
- description
- status (`open` / `closed`)

## Case model
A case has the following fields:
- id (int)
- title (str)
- description (str)
- status (str, e.g. "open", "closed")

## Tech stack
- Python 3
- FastAPI
- Pydantic v2
- Uvicorn

## Run locally

1. Clone the repository
```bash
git clone <repo-url>
cd backend-api

2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Start the server
uvicorn backend_api.main:app --reload

The API is running on:
- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
