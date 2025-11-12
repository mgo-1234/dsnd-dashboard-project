from __future__ import annotations

from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Absolute path to the packaged SQLite DB
db_path = Path(__file__).resolve().parent / "employee_events.db"

class QueryMixin:
    """Provides helper methods for executing SQL queries."""

    def pandas_query(self, sql_query: str) -> pd.DataFrame:
        """Execute the SQL query and return a pandas DataFrame."""
        with connect(db_path) as conn:
            return pd.read_sql_query(sql_query, conn)

    def run_sql(self, sql_query: str):
        """Execute the SQL query and return a list of dicts (column names preserved)."""
        with connect(db_path) as conn:
            cur = conn.cursor()
            rows = cur.execute(sql_query).fetchall()
            cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in rows]

# Optional decorator (not required by the project, but harmless to keep)
def query(func):
    @wraps(func)
    def run_query(*args, **kwargs):
        sql = func(*args, **kwargs)
        with connect(db_path) as conn:
            cur = conn.cursor()
            rows = cur.execute(sql).fetchall()
        return rows
    return run_query

# Backwards-compat alias: some code may import SQLiteMixin
SQLiteMixin = QueryMixin
