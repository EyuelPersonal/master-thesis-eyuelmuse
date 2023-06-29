import json
import os

user_name = password = account = database = warehouse = role = None

def get_secret(file_name: str = 'settings.json'):
    # Documentation: https://docs.snowflake.com/en/user-guide/python-connector-example.html
    """
    Get the secret from the settings.json file. 
    """
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, file_name)
    global user_name, password, account, database, warehouse, role, region
    with open(path, 'r') as f:
        settings = json.load(f)
    user_name = settings["snowflake_db"]['user']
    password = settings["snowflake_db"]['password']
    account = settings["snowflake_db"]['account']
    database = settings["snowflake_db"]['database']
    warehouse = settings["snowflake_db"]['warehouse']
    role = settings["snowflake_db"]['role']