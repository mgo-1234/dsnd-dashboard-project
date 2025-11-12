# Import any dependencies needed to execute sql queries
from __future__ import annotations
from .sql_execution import SQLiteMixin
import pandas as pd

# Define a class called QueryBase
# Use inheritance to add methods
# for querying the employee_events database.
class QueryBase(SQLiteMixin):

    # Create a class attribute called `name`
    # set the attribute to an empty string
    name: str = ""
    events_table: str = "employee_events"

    # Define a `names` method that receives
    # no passed arguments
    def names(self):
        # Return an empty list
        return []


    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    def event_counts(self, id):
        # Determine which id column to filter on (employee_id or team_id)
        id_col = f"{self.name}_id".strip("_")  # handles empty name safely

        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column
        sql = f"""
            SELECT
                event_date,
                SUM(positive_events) AS positive_events,
                SUM(negative_events) AS negative_events
            FROM {self.events_table}
            WHERE {id_col} = ?
            GROUP BY event_date
            ORDER BY date(event_date) ASC
        """
        rows = self.run_sql(sql, [id])
        return pd.DataFrame(rows)
            
    

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    def notes(self, id):
        # Pick the correct id column based on subclass name
        id_col = f"{self.name}_id".strip("_")

        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        sql = f"""
            SELECT
                note_date,
                note
            FROM notes
            WHERE {id_col} = ?
            ORDER BY date(note_date) DESC
        """
        rows = self.run_sql(sql, [id])
        return pd.DataFrame(rows)

