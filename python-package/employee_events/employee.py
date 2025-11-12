# Import the QueryBase class
from .query_base import QueryBase

import pandas as pd

# Define a subclass of QueryBase called Employee
class Employee(QueryBase):

    # Set the class attribute `name`
    # to the string "employee"
    name = "employee"

    # Return list of (full_name, employee_id) for all employees
    def names(self):
        sql = """
            SELECT (first_name || ' ' || last_name) AS full_name,
                   employee_id
            FROM employee
            ORDER BY last_name, first_name
        """
        rows = self.run_sql(sql)
        return [(r["full_name"], r["employee_id"]) for r in rows]

    # Return list with a single tuple (full_name,) for a given employee id
    def username(self, id):
        sql = f"""
            SELECT (first_name || ' ' || last_name) AS full_name
            FROM employee
            WHERE employee_id = {int(id)}
        """
        rows = self.run_sql(sql)
        return [(r["full_name"],) for r in rows]

    # Optional: events per day for charts — returns a pandas DataFrame
    def event_counts(self, id):
        sql = f"""
            SELECT event_date,
                   SUM(positive_events) AS positive,
                   SUM(negative_events) AS negative
            FROM employee_events
            WHERE employee_id = {int(id)}
            GROUP BY event_date
            ORDER BY event_date
        """
        rows = self.run_sql(sql)
        return pd.DataFrame(rows)

    # Optional: notes table — returns list of (note, note_date)
    def notes(self, id):
        sql = f"""
            SELECT note, note_date
            FROM notes
            WHERE employee_id = {int(id)}
            ORDER BY note_date DESC
        """
        rows = self.run_sql(sql)
        return [(r["note"], r["note_date"]) for r in rows]

    # ML features: return a pandas DataFrame with positive/negative sums
    def model_data(self, id):
        sql = f"""
            SELECT SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {int(id)}
        """
        rows = self.run_sql(sql)
        return pd.DataFrame(rows)
