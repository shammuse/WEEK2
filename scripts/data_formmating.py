import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder

def drop_missing_values(data, threshold=0.5):
    """
    Drop columns with a high percentage of missing values.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - threshold (float): The fraction of allowed missing values (default is 0.5).

    Returns:
    - pd.DataFrame: Dataset with columns containing excessive missing values removed.
    """
    missing_fraction = data.isnull().mean()
    return data.loc[:, missing_fraction < threshold]

def fill_missing_values(data, strategy="mean", fill_value=None):
    """
    Fill missing values in the dataset.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - strategy (str): Filling strategy: "mean", "median", "mode", or "constant".
    - fill_value (any): Value to use if strategy is "constant".

    Returns:
    - pd.DataFrame: Dataset with missing values filled.
    """
    for column in data.select_dtypes(include=[np.number]).columns:
        if strategy == "mean":
            data[column] = data[column].fillna(data[column].mean())
        elif strategy == "median":
            data[column] = data[column].fillna(data[column].median())
        elif strategy == "mode":
            data[column] = data[column].fillna(data[column].mode()[0])
        elif strategy == "constant" and fill_value is not None:
            data[column] = data[column].fillna(fill_value)
        else:
            raise ValueError(f"Invalid strategy: {strategy}")
    return data

def normalize_data(data, columns=None):
    """
    Normalize numerical columns to a range of 0 to 1.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - columns (list): List of columns to normalize. Defaults to all numeric columns.

    Returns:
    - pd.DataFrame: Dataset with normalized columns.
    """
    scaler = MinMaxScaler()
    columns = columns or data.select_dtypes(include=[np.number]).columns
    data[columns] = scaler.fit_transform(data[columns])
    return data

def standardize_data(data, columns=None):
    """
    Standardize numerical columns to have zero mean and unit variance.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - columns (list): List of columns to standardize. Defaults to all numeric columns.

    Returns:
    - pd.DataFrame: Dataset with standardized columns.
    """
    scaler = StandardScaler()
    columns = columns or data.select_dtypes(include=[np.number]).columns
    data[columns] = scaler.fit_transform(data[columns])
    return data

def encode_categorical_columns(data, columns=None):
    """
    Encode categorical columns using Label Encoding.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - columns (list): List of columns to encode. Defaults to all object-type columns.

    Returns:
    - pd.DataFrame: Dataset with encoded columns.
    """
    le = LabelEncoder()
    columns = columns or data.select_dtypes(include=["object"]).columns
    for column in columns:
        data[column] = le.fit_transform(data[column])
    return data

def rename_columns(data, column_mapping):
    """
    Rename columns in the dataset.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - column_mapping (dict): Mapping of old column names to new ones.

    Returns:
    - pd.DataFrame: Dataset with renamed columns.
    """
    return data.rename(columns=column_mapping)

def format_dates(data, date_columns, format="%Y-%m-%d"):
    """
    Convert date columns to datetime format.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - date_columns (list): List of date columns.
    - format (str): Desired date format (default is "%Y-%m-%d").

    Returns:
    - pd.DataFrame: Dataset with formatted date columns.
    """
    for column in date_columns:
        data[column] = pd.to_datetime(data[column], format=format)
    return data

def aggregate_data(data, group_by_columns, aggregations):
    """
    Aggregate data by grouping and applying specified aggregation functions.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - group_by_columns (list): Columns to group by.
    - aggregations (dict): Aggregation functions for specific columns.

    Returns:
    - pd.DataFrame: Aggregated dataset.
    """
    return data.groupby(group_by_columns).agg(aggregations).reset_index()

def reorder_columns(data, column_order):
    """
    Reorder columns in the dataset.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - column_order (list): Desired order of columns.

    Returns:
    - pd.DataFrame: Dataset with reordered columns.
    """
    return data[column_order]

def detect_outliers(data, column, method="iqr"):
    """
    Detect outliers in a column using IQR or Z-score method.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - column (str): The column to analyze.
    - method (str): Outlier detection method ("iqr" or "zscore").

    Returns:
    - pd.Series: Boolean series indicating outliers.
    """
    if method == "iqr":
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return (data[column] < lower_bound) | (data[column] > upper_bound)
    elif method == "zscore":
        z_scores = (data[column] - data[column].mean()) / data[column].std()
        return (z_scores.abs() > 3)
    else:
        raise ValueError(f"Invalid method: {method}")
