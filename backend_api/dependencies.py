# backend_api\dependencies.py
"""
Dependency providers for FastAPI.

This is the composition root:
- Wires together repositories and services
-Chooses concrete implementations
"""

import sqlite3
from backend_api.repository_contract import CaseRepository
from backend_api.repositories.sqlite import SQLiteCaseRepository
from backend_api.services.case_service import CaseService

def get_repository() -> CaseRepository:
    """Provide a repository instance."""
    connection = sqlite3.connect("cases.db", check_same_thread=False)
    # NOTE:
    # Connection lifecycle is request-scoped for simplicity.
    # In production, use connection pooling or lifespan events
    return SQLiteCaseRepository(connection)

def get_case_service() -> CaseService:
    """Provide a CaseService with its dependencies."""
    repository = get_repository()
    return CaseService(repository)

# Note:
# - No FastAPI imports here
# - No HTTP
# - Only object coupling
# This makes test overrides cleaner later.