from __future__ import annotations

from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Absolute path to the packaged SQLite DB
db_path = Path(__file__).resolve().parent / "employee_events.db"


# OPTION 1: MIXIN
class QueryMixin:
    """Provides helper methods for executing SQL queries."""

    def pandas_query(self, sql_query: str) -> pd.DataFrame:
        """Execute the SQL query and return a pandas DataFrame."""
        with connect(db_path) as conn:
            return pd.read_sql_query(sql_query, conn)

    def query(self, sql_query: str):
        """Execute the SQL query and return a list of tuples."""
        with connect(db_path) as conn:
            cur = conn.cursor()
            rows = cur.execute(sql_query).fetchall()
        return rows


# OPTION 2: DECORATOR (available if you want to use it)
def query(func):
    """Decorator that runs a standard SQL execution and returns a list of tuples."""
    @wraps(func)
    def run_query(*args, **kwargs):
        sql = func(*args, **kwargs)
        with connect(db_path) as conn:
            cur = conn.cursor()
            rows = cur.execute(sql).fetchall()
        return rows
    return run_query


# Backwards-compat alias: some modules import SQLiteMixin
SQLiteMixin = QueryMixin
