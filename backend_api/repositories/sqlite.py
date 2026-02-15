# backend_api\repositories\sqlite.py
"""
SQLite implementation of the CaseRepository.

Purpose: persistence logic only
"""

import sqlite3
from typing import List, Optional, Callable, ContextManager
from backend_api.models import Case
from backend_api.repository_contract import CaseRepository


class SQLiteCaseRepository(CaseRepository):
    def __init__(
        self,
        connection_factory: Callable[[], ContextManager[sqlite3.Connection]],
    ):
        self._connection_factory = connection_factory
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        # Schema creation must also use a local connection
        with self._connection_factory() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def _row_to_case(self, row: sqlite3.Row) -> Case:
        return Case(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=row["status"],
        )

    def create(self, title: str, description: str, status: str) -> Case:
        with self._connection_factory() as conn:
            cursor = conn.execute(
                "INSERT INTO cases (title, description, status) VALUES (?, ?, ?)",
                (title, description, status),
            )
            conn.commit()

            return Case(
                id=cursor.lastrowid,
                title=title,
                description=description,
                status=status,
            )

    def get_all(self) -> List[Case]:
        with self._connection_factory() as conn:
            rows = conn.execute(
                "SELECT id, title, description, status FROM cases"
            ).fetchall()

            return [self._row_to_case(row) for row in rows]

    def get_by_id(self, case_id: int) -> Optional[Case]:
        with self._connection_factory() as conn:
            row = conn.execute(
                "SELECT id, title, description, status FROM cases WHERE id = ?",
                (case_id,),
            ).fetchone()

            return self._row_to_case(row) if row else None

    def update(
        self,
        case_id: int,
        title: str,
        description: str,
        status: str,
    ) -> Optional[Case]:
        with self._connection_factory() as conn:
            cursor = conn.execute(
                """
                UPDATE cases
                SET title = ?, description = ?, status = ?
                WHERE id = ?
                """,
                (title, description, status, case_id),
            )
            conn.commit()

            if cursor.rowcount == 0:
                return None

            row = conn.execute(
                "SELECT id, title, description, status FROM cases WHERE id = ?",
                (case_id,),
            ).fetchone()

            return self._row_to_case(row) if row else None

    def delete(self, case_id: int) -> bool:
        with self._connection_factory() as conn:
            cursor = conn.execute(
                "DELETE FROM cases WHERE id = ?",
                (case_id,),
            )
            conn.commit()
            return cursor.rowcount > 0
