from typing import Any
import pandas as pd
from django.db import connection

class DatabaseConnection:
    """
    Execute raw SQL queries using Django's configured database
    connection and return the result as a Pandas DataFrame.
    
    """
    def execute_query(
        self,
        query,
        params=None,
    ) -> pd.DataFrame:

        if params is None:
            params = []

        with connection.cursor() as cursor:
            cursor.execute(
                query,
                params,
            )

            columns = [
                column[0]
                for column in cursor.description
            ]

            rows = cursor.fetchall()

        return pd.DataFrame(
            rows,
            columns=columns,
        )