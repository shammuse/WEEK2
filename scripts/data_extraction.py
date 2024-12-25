import pandas as pd
import requests
import sqlite3

def extract_from_csv(file_path):
    """
    Extract data from a CSV file.

    Parameters:
    - file_path (str): Path to the CSV file.

    Returns:
    - pd.DataFrame: Data loaded from the CSV file.
    """
    return pd.read_csv(file_path)

def extract_from_excel(file_path, sheet_name=None):
    """
    Extract data from an Excel file.

    Parameters:
    - file_path (str): Path to the Excel file.
    - sheet_name (str): Specific sheet to extract. Defaults to the first sheet.

    Returns:
    - pd.DataFrame: Data loaded from the Excel file.
    """
    return pd.read_excel(file_path, sheet_name=sheet_name)

def extract_from_json(file_path):
    """
    Extract data from a JSON file.

    Parameters:
    - file_path (str): Path to the JSON file.

    Returns:
    - pd.DataFrame: Data loaded from the JSON file.
    """
    return pd.read_json(file_path)

def extract_from_api(url, params=None, headers=None):
    """
    Extract data from an API endpoint.

    Parameters:
    - url (str): The API endpoint.
    - params (dict): Query parameters for the API call.
    - headers (dict): Headers for the API call.

    Returns:
    - dict or list: Parsed JSON response from the API.
    """
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def extract_from_database(db_path, query):
    """
    Extract data from a SQLite database.

    Parameters:
    - db_path (str): Path to the SQLite database.
    - query (str): SQL query to execute.

    Returns:
    - pd.DataFrame: Data loaded from the database.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def save_raw_data(data, file_path, file_type='csv'):
    """
    Save raw data to a file.

    Parameters:
    - data (pd.DataFrame or dict or list): Data to save.
    - file_path (str): Path to save the file.
    - file_type (str): File type ('csv', 'json', 'excel').

    Returns:
    - None
    """
    if isinstance(data, pd.DataFrame):
        if file_type == 'csv':
            data.to_csv(file_path, index=False)
        elif file_type == 'excel':
            data.to_excel(file_path, index=False)
        elif file_type == 'json':
            data.to_json(file_path, orient='records', lines=True)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    elif isinstance(data, (dict, list)) and file_type == 'json':
        import json
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    else:
        raise ValueError("Unsupported data type for saving.")

def extract_sample_data(data, sample_size=100, random_state=42):
    """
    Extract a sample from a DataFrame.

    Parameters:
    - data (pd.DataFrame): The DataFrame to sample from.
    - sample_size (int): Number of rows to sample.
    - random_state (int): Random seed for reproducibility.

    Returns:
    - pd.DataFrame: Sampled DataFrame.
    """
    return data.sample(n=sample_size, random_state=random_state)
