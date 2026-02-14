# backend_api\dependencies.py
"""
Dependency providers for FastAPI.

This is the composition root:
- Wires together repositories and services
_Chooses concrete implementations
"""

import sqlite3
from backend_api.repository import CaseRepository
from backend_api.repositories.sqlite import SQLiteCaseRepository
from backend_api.services.case_service import CaseService

def get_repository() -> CaseRepository:
    """Provide a repository instance."""
    connection = sqlite3.connect("cases.db", check_same_thread=False)
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