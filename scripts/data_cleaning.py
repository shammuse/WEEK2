import pandas as pd
import numpy as np

def load_data(file_path, file_type='csv'):
    """
    Load data from a specified file path.
    
    Parameters:
    - file_path (str): Path to the data file.
    - file_type (str): Type of the file (default is 'csv'). Options: 'csv', 'excel', 'json'.
    
    Returns:
    - pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    if file_type == 'csv':
        return pd.read_csv(file_path)
    elif file_type == 'excel':
        return pd.read_excel(file_path)
    elif file_type == 'json':
        return pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def handle_missing_values(df, strategy='mean', columns=None):
    """
    Handle missing values in the DataFrame.
    
    Parameters:
    - df (pd.DataFrame): DataFrame to clean.
    - strategy (str): Strategy to handle missing values ('mean', 'median', 'mode', 'drop').
    - columns (list): List of columns to apply the strategy to. If None, apply to all.
    
    Returns:
    - pd.DataFrame: Cleaned DataFrame.
    """
    if columns is None:
        columns = df.columns

    for col in columns:
        if df[col].isnull().sum() > 0:
            if strategy == 'mean':
                df[col].fillna(df[col].mean(), inplace=True)
            elif strategy == 'median':
                df[col].fillna(df[col].median(), inplace=True)
            elif strategy == 'mode':
                df[col].fillna(df[col].mode()[0], inplace=True)
            elif strategy == 'drop':
                df.dropna(subset=[col], inplace=True)
            else:
                raise ValueError(f"Unsupported strategy: {strategy}")
    return df

def remove_outliers(df, columns, method='zscore', threshold=3):
    """
    Remove outliers from specified columns in the DataFrame.
    
    Parameters:
    - df (pd.DataFrame): DataFrame to clean.
    - columns (list): List of columns to check for outliers.
    - method (str): Method to detect outliers ('zscore' or 'iqr').
    - threshold (float): Threshold for outlier detection. Default is 3 for 'zscore'.
    
    Returns:
    - pd.DataFrame: Cleaned DataFrame.
    """
    for col in columns:
        if method == 'zscore':
            from scipy.stats import zscore
            z_scores = zscore(df[col].dropna())
            abs_z_scores = np.abs(z_scores)
            df = df[abs_z_scores < threshold]
        elif method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[(df[col] >= (Q1 - 1.5 * IQR)) & (df[col] <= (Q3 + 1.5 * IQR))]
        else:
            raise ValueError(f"Unsupported method: {method}")
    return df

def standardize_columns(df):
    """
    Standardize column names by converting to lowercase and replacing spaces with underscores.
    
    Parameters:
    - df (pd.DataFrame): DataFrame to clean.
    
    Returns:
    - pd.DataFrame: Cleaned DataFrame with standardized column names.
    """
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    return df

def drop_duplicates(df):
    """
    Drop duplicate rows from the DataFrame.
    
    Parameters:
    - df (pd.DataFrame): DataFrame to clean.
    
    Returns:
    - pd.DataFrame: Cleaned DataFrame without duplicates.
    """
    return df.drop_duplicates()

def encode_categorical(df, columns, encoding_type='onehot'):
    """
    Encode categorical variables in the DataFrame.
    
    Parameters:
    - df (pd.DataFrame): DataFrame to clean.
    - columns (list): List of columns to encode.
    - encoding_type (str): Encoding method ('onehot' or 'label').
    
    Returns:
    - pd.DataFrame: Cleaned DataFrame with encoded categorical variables.
    """
    for col in columns:
        if encoding_type == 'onehot':
            onehot_encoded = pd.get_dummies(df[col], prefix=col)
            df = pd.concat([df, onehot_encoded], axis=1).drop(col, axis=1)
        elif encoding_type == 'label':
            from sklearn.preprocessing import LabelEncoder
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
        else:
            raise ValueError(f"Unsupported encoding type: {encoding_type}")
    return df

def save_cleaned_data(df, file_path, file_type='csv'):
    """
    Save the cleaned DataFrame to a file.
    
    Parameters:
    - df (pd.DataFrame): DataFrame to save.
    - file_path (str): Path to save the file.
    - file_type (str): File type to save as ('csv', 'excel', 'json').
    """
    if file_type == 'csv':
        df.to_csv(file_path, index=False)
    elif file_type == 'excel':
        df.to_excel(file_path, index=False)
    elif file_type == 'json':
        df.to_json(file_path, orient='records', lines=True)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
