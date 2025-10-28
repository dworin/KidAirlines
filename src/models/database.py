import sqlite3
from contextlib import contextmanager
from src.database import get_db_path


@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def execute_query(query, params=None):
    """Execute a query and return all results"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()


def execute_update(query, params=None):
    """Execute an update/insert query and return lastrowid"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor.lastrowid
