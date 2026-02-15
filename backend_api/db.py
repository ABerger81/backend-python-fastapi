# backend_api\db.py

"""
Purpose: provide a safe connection factory
Rule: no FastAPI imports, no globals, no shared connections
"""

import sqlite3
from contextlib import contextmanager


@contextmanager
def connection_factory():
    """
    Create a SQLite connection that is:
    - Created and used in the same thread
    - Properly closed after use
    """
    conn = sqlite3.connect("cases.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
