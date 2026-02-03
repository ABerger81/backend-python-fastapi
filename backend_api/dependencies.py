# dependencies.py
# Responsibilities:
# - Create and connect objects
# - Does not contain endpoints
# - Does not contain business logic

from backend_api.repository import CaseRepository
from backend_api.services.case_service import CaseService

def get_case_repository() -> CaseRepository:
    return CaseRepository()

def get_case_service() -> CaseService:
    repository = get_case_repository()
    return CaseService(repository)

# Note:
# - No FastAPI imports here
# - No HTTP
# - Only object coupling
# This makes test overrides cleaner later.