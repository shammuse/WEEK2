# scripts/load_data.py

import os
import logging
from typing import Optional

import psycopg2
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from urllib.parse import quote_plus

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Fetch database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def load_data_from_postgres(query: str) -> Optional[pd.DataFrame]:
    """
    Connects to the PostgreSQL database and loads data based on the provided SQL query.

    :param query: SQL query to execute.
    :return: DataFrame containing the results of the query, or None if an error occurs.
    """
    try:
        # Establish a connection to the database
        with psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as connection:
            # Load data using pandas
            df = pd.read_sql_query(query, connection)

        return df

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None

@contextmanager
def get_sqlalchemy_engine() -> Engine:
    """
    Creates and yields an SQLAlchemy engine, ensuring proper cleanup.
    """
    print(f"Connecting to: {DB_HOST}:{DB_PORT}/{DB_NAME} as {DB_USER}")
    password = quote_plus(DB_PASSWORD)
    connection_string = f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
   
    engine = create_engine(connection_string)
    try:
        yield engine
    finally:
        engine.dispose()

def load_data_using_sqlalchemy(query: str) -> Optional[pd.DataFrame]:
    """
    Connects to the PostgreSQL database and loads data based on the provided SQL query using SQLAlchemy.

    :param query: SQL query to execute.
    :return: DataFrame containing the results of the query, or None if an error occurs.
    """
    try:
        with get_sqlalchemy_engine() as engine:
            # Load data into a pandas DataFrame
            df = pd.read_sql_query(query, engine)
        return df

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    test_query = "SELECT * FROM your_table LIMIT 5;"
    
    # Test psycopg2 method
    result_psycopg2 = load_data_from_postgres(test_query)
    if result_psycopg2 is not None:
        logger.info("Data loaded successfully using psycopg2")
        logger.info(result_psycopg2.head())
    else:
        logger.error("Failed to load data using psycopg2")
    
    # Test SQLAlchemy method
    result_sqlalchemy = load_data_using_sqlalchemy(test_query)
    if result_sqlalchemy is not None:
        logger.info("Data loaded successfully using SQLAlchemy")
        logger.info(result_sqlalchemy.head())
    else:
        logger.error("Failed to load data using SQLAlchemy")