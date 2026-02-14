# backend_api\repositories\inmemory.py
"""
In-memory implementation of the CaseRepository.

Used for:
- Early development
- Unit tests
- Fast feedback without external dependencies
"""

from typing import List, Optional
from backend_api.models import Case
from backend_api.repository import CaseRepository

class InMemoryCaseRepository(CaseRepository):
    """Simple in-memory repository implementation."""

    def __init__(self):
        self._cases: List[Case] = []
        self._next_id: int = 1

    def create(self, title: str, description: str, status: str) -> Case:
        case = Case(
            id=self._next_id,
            title=title,
            description=description,
            status=status,
        )
        self._next_id += 1
        self._cases.append(case)
        return case

    def get_all(self) -> List[Case]:
        return list(self._cases)
    
    def get_by_id(self, case_id: int) -> Optional[Case]:
        return next((c for c in self._cases if c.id == case_id), None)
    
    def update(
            self,
            case_id: int,
            title: str,
            description: str,
            status: str,
    ) -> Optional[Case]:
        case = self.get_by_id(case_id)
        if case is None:
            return None
        
        case.title = title
        case.description = description
        case.status = status
        return case
    
    def delete(self, case_id: int) -> bool:
        case = self.get_by_id(case_id)
        if case is None:
            return False
        
        self._cases.remove(case)
        return True