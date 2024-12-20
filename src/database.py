from sqlalchemy import create_engine
import pandas as pd

def connect_to_postgres(user, password, host, port, dbname):
    """Establish a connection to the PostgreSQL database."""
    try:
        connection_str = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
        engine = create_engine(connection_str)
        connection = engine.connect()
        print("Connection to PostgreSQL established successfully.")
        return connection
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def load_data_from_postgres(connection, query):
    """Load data from PostgreSQL using a SQL query."""
    try:
        data = pd.read_sql(query, connection)
        return data
    except Exception as e:
        print(f"Error loading data from PostgreSQL: {e}")
        return None
