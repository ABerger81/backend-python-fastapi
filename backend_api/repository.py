# backend_api/repository.py
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
        """Create and return a new case."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Case]:
        """Return all cases."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, case_id: int) -> Optional[Case]:
        """Return a case by ID, or None if not found."""
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        case_id: int,
        title: str,
        description: str,
        status: str,
    ) -> Optional[Case]:
        """Update a case and return it, or None if not found."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, case_id: int) -> bool:
        """Delete a case. Return True if deleted, False otherwise."""
        raise NotImplementedError