# repository.py
"""
Responsibilities:
- Define the persistence contract for Case objects
- Contain NO storage logic
- Allow multiple implementations (in-memory, database, etc.)
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from backend_api.models import Case


class CaseRepository(ABC):
    """Abstract base class for Case persistance."""

    @abstractmethod
    def create(self, title: str, description: str, status: str) -> Case:
        pass

    @abstractmethod
    def get_all(self) -> List[Case]:
        pass

    @abstractmethod
    def get_by_id(self, case_id: int) -> Optional[Case]:
        pass

    @abstractmethod
    def update(
        self,
        case_id: int,
        title: str,
        description: str,
        status: str,
    ) -> Optional[Case]:
        pass

    @abstractmethod
    def delete(self, case_id: int) -> bool:
        pass

    def __init__(self):
        # Internal storage of cases
        self._cases: List[Case] = []
        self._next_id: int = 1

    def create(self, title: str, description: str, status: str) -> Case: 
        # Create a new Case and store it
        case = Case(
            id=self._next_id,
            title=title,
            description=description,
            status=status
            )
        self._next_id += 1
        self._cases.append(case)
        return case

    def get_all(self) -> List[Case]:
        # Return all stored cases
        return self._cases
    
    def get_by_id(self, case_id: int) -> Optional[Case]:
        # Return case by ID or None if not found
        return next((c for c in self._cases if c.id == case_id), None)
    
    def update(self, case_id: int, title: str, description: str, status: str) -> Optional[Case]:
        # Update an existing case, return updated case or None
        # if not found
        case = self.get_by_id(case_id)
        if case is None:
            return None
        
        case.title = title
        case.description = description
        case.status = status
        return case

    def delete(self, case_id: int) -> bool:
        # Delete a case by ID, return True if deleted,
        # False if not found
        case = self.get_by_id(case_id)
        if case is None:
            return False
        
        self._cases.remove(case)
        return True
    
