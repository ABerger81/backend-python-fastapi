# repositories/sqlite.py
"""
SQLite implementation of the CaseRepository.

Responsibilities:
- Persist cases using SQLite
- Translate rows <-> domain models
- Hide SQL details from the service layer
"""

import sqlite3
from typing import List, Optional
from backend_api.models import Case
from backend_api.repository import CaseRepository


class SQLiteCaseRepository(CaseRepository):
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create database schema if it does not exist."""
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        self._conn.commit()
    
    def create(self, title: str, description: str, status: str) -> Case:
        cursor = self._conn.execute(
            "INSERT INTO cases (title, description, status) VALUES (?, ?, ?)",
            (title, description, status),
        )
        self._conn.commit()

        return Case(
            id=cursor.lastrowid,
            title=title,
            description=description,
            status=status,
        )
    
    def get_all(self) -> List[Case]:
        rows = self._conn.execute(
            "SELECT id, title, description, status FROM cases"
        ).fetchall()

        return [
            Case(id=row[0], title=row[1], description=row[2], status=row[3])
            for row in rows
        ]
    
    def get_by_id(self, case_id: int) -> Optional[Case]:
        row = self._conn.execute(
            "SELECT id, title, description, status FROM cases WHERE id = ?",
            (case_id,),
        ).fetchone()

        if row is None:
            return None
        
        return Case(id=row[0], title=row[1], description=row[2], status=row[3])
    
    def update(
            self,
            case_id: int,
            title: str,
            description: str,
            status: str,
    ) -> Optional[Case]:
        cursor = self._conn.execute(
            """
            UPDATE cases
            SET title = ?, description = ?, status = ?
            WHERE id = ?
            """,
            (title, description, status, case_id),
        )
        self._conn.commit()

        if cursor.rowcount == 0:
            return None
        
        return self.get_by_id(case_id)
    
    def delete(self, case_id: int) -> bool:
        cursor = self._conn.execute(
            "DELETE FROM cases WHERE id = ?",
            (case_id,),
        )
        self._conn.commit()
        return cursor.rowcount > 0