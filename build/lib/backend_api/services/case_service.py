# backend_api/services/case_service.py
"""
Service layer for Case Domain.

Responsibilities:
- Enforce business rules
- Orchestrate repository access
- Remain free of HTTP concerns
"""

from backend_api.repository import CaseRepository

class CaseService:
    def __init__(self, repository: CaseRepository):
        self._repository = repository

    def create_case(self, title: str, description: str, status: str):
        if not title or not title.strip():
            raise ValueError("Case title cannot be empty")
        
        return self._repository.create(
            title=title.strip(),
            description=description,
            status=status,
        )
    
    def get_case(self, case_id: int):
        return self._repository.get_by_id(case_id)
    
    def get_all_cases(self):
        return self._repository.get_all()
    
    def update_case(self, case_id: int, title: str, description: str, status: str):
        case = self._repository.get_by_id(case_id)
        if case is None:
            return None
        
        if case.status.lower == "closed":
            raise ValueError("Cannot update a closed case")
        
        if not title or not title.strip():
            raise ValueError("Case title cannot be empty")
        
        return self._repository.update(
            case_id,
            title=title.strip(),
            description=description,
            status=status,
        )
    
    def delete_case(self, case_id: int) -> bool:
        case = self._repository.get_by_id(case_id)
        if case is None:
            return False
        
        if case.status == "closed":
            raise ValueError("Closed cases cannot be deleted")
        
        return self._repository.delete(case_id)