# Backend API - Ärendehantering

Simple REST API built with FastAPI.

## Features
- Create cases
- Read all cases
- Read case by id
- Update case
- Delete case

## Case model
A case has the following fields:
- id (int)
- title (str)
- description (str)
- status (str, e.g. "öppen", "stängd")

## Tech stack
- Python
- FastAPI
- Pydantic v2
- In-memory repository (repository patern)

## Run locally
```bash
uvicorn backend_api.main:app --reload