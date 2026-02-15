# backend_api\dependencies.py
"""
Dependency providers for FastAPI.

Purpose: composition root
Rule: FastAPI allowed here, nowhere else
- This is the composition root for the application
- Uses FastAPI dependency injection
- Wires infrastructure -> repository -> service
- Keeps business logic framework-agnostic
"""


from backend_api.db import connection_factory
from backend_api.repositories.sqlite import SQLiteCaseRepository
from backend_api.services.case_service import CaseService


def get_case_service() -> CaseService:
    """
    Provide a CaseService with its concrete dependencies.
    """
    repository = SQLiteCaseRepository(connection_factory)
    return CaseService(repository)
