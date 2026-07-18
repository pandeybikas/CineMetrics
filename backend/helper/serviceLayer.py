from helper.db_connection import DatabaseConnection
from helper.constant import TABLE1, TABLE2
import pandas as pd

class DatabaseQueryResult(DatabaseConnection):
    def get_top_5_movies(self, year:int) -> pd.DataFrame:
        """
    Contains raw SQL queries used by CineMetrics APIs.
    """
        table_name= TABLE1
        query = f"""
            SELECT
                id,
                title,
                release_date,
                budget,
                revenue,
                vote_average,
                vote_count
            FROM {table_name}
            WHERE EXTRACT(YEAR FROM release_date) = %s
            AND revenue IS NOT NULL
            AND revenue > 0
            ORDER BY revenue DESC
            LIMIT 5
        """
        
        df = self.execute_query(
            query=query,
            params=[year],
        )

        return df