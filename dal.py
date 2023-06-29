import json
import constants
import os

import pandas as pd
import snowflake.connector
from snowflake.connector import DictCursor
from snowflake.connector.connection import SnowflakeConnection


class SnowflakeRunner:
    # Documentation: https://docs.snowflake.com/en/user-guide/python-connector-example.html
    """
    This class is used to connect to Snowflake and run queries.
    """
    def __init__(self) -> None:
        constants.get_secret()
        self.__conn = snowflake.connector.connect(
            user=constants.user_name,
            password=constants.password,
            account=constants.account,
            database=constants.database,
            warehouse=constants.warehouse,
            role=constants.role,
        )
    
    def get_data_raw(self, query_name: str) -> dict:
        folder = os.path.dirname(os.path.abspath(__file__))
        query_path = os.path.join(folder, query_name)
        with open(query_path, 'r') as data:
            query = data.read()
        cs = self.__conn.cursor(DictCursor)
        cs.execute(query)
        results = cs.fetchall()
        return results
    
    def get_data_frame(self, query_name: str) -> pd.DataFrame:
        folder = os.path.dirname(os.path.abspath(__file__))
        query_path = os.path.join(folder, query_name)
        with open(query_path, 'r') as data:
            query = data.read()
        cs = self.__conn.cursor(DictCursor)
        cs.execute(query)
        results = cs.fetchall()
        return pd.DataFrame(results)