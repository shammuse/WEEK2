import pandas as pd
import numpy as np
from sklearn.preprocessing import PowerTransformer, PolynomialFeatures
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, chi2, f_classif

def apply_log_transformation(data, columns):
    """
    Apply log transformation to specified columns.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - columns (list): List of columns to transform.

    Returns:
    - pd.DataFrame: Dataset with transformed columns.
    """
    for column in columns:
        data[column] = np.log1p(data[column])  # log(1 + x) to handle zero values
    return data

def apply_power_transformation(data, columns, method='yeo-johnson'):
    """
    Apply power transformation to specified columns.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - columns (list): List of columns to transform.
    - method (str): The power transformation method ('yeo-johnson' or 'box-cox').

    Returns:
    - pd.DataFrame: Dataset with transformed columns.
    """
    pt = PowerTransformer(method=method)
    data[columns] = pt.fit_transform(data[columns])
    return data

def generate_polynomial_features(data, columns, degree=2, interaction_only=False):
    """
    Generate polynomial features from specified columns.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - columns (list): List of columns to transform.
    - degree (int): The degree of the polynomial features.
    - interaction_only (bool): If True, only interaction terms are included.

    Returns:
    - pd.DataFrame: Dataset with polynomial features added.
    """
    poly = PolynomialFeatures(degree=degree, interaction_only=interaction_only, include_bias=False)
    poly_features = poly.fit_transform(data[columns])
    feature_names = poly.get_feature_names_out(columns)
    poly_df = pd.DataFrame(poly_features, columns=feature_names, index=data.index)
    data = pd.concat([data, poly_df], axis=1).drop(columns=columns)
    return data

def reduce_dimensions_with_pca(data, n_components=2):
    """
    Reduce dimensions using Principal Component Analysis (PCA).

    Parameters:
    - data (pd.DataFrame): The dataset.
    - n_components (int): Number of principal components to keep.

    Returns:
    - pd.DataFrame: Dataset with reduced dimensions.
    """
    pca = PCA(n_components=n_components)
    reduced_data = pca.fit_transform(data)
    columns = [f'PC{i+1}' for i in range(n_components)]
    return pd.DataFrame(reduced_data, columns=columns, index=data.index)

def select_k_best_features(data, target, k=10, score_func=f_classif):
    """
    Select the top K best features based on a scoring function.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - target (pd.Series): The target variable.
    - k (int): Number of top features to select.
    - score_func (function): Scoring function (e.g., chi2, f_classif).

    Returns:
    - pd.DataFrame: Dataset with the top K features selected.
    """
    selector = SelectKBest(score_func=score_func, k=k)
    selected_features = selector.fit_transform(data, target)
    selected_columns = data.columns[selector.get_support()]
    return data[selected_columns]

def one_hot_encode(data, columns):
    """
    Apply one-hot encoding to specified columns.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - columns (list): List of categorical columns to encode.

    Returns:
    - pd.DataFrame: Dataset with one-hot encoded columns.
    """
    return pd.get_dummies(data, columns=columns, drop_first=True)

def scale_data_range(data, columns, feature_range=(0, 1)):
    """
    Scale data to a specified range.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - columns (list): List of columns to scale.
    - feature_range (tuple): Desired range of transformed data.

    Returns:
    - pd.DataFrame: Dataset with scaled columns.
    """
    scaler = MinMaxScaler(feature_range=feature_range)
    data[columns] = scaler.fit_transform(data[columns])
    return data

def bin_numerical_column(data, column, bins, labels=None):
    """
    Bin a numerical column into categories.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - column (str): The column to bin.
    - bins (list): Bin edges.
    - labels (list): Labels for the bins.

    Returns:
    - pd.DataFrame: Dataset with binned column.
    """
    data[column + '_binned'] = pd.cut(data[column], bins=bins, labels=labels)
    return data

def create_lagged_features(data, column, lags):
    """
    Create lagged features for a specified column.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - column (str): The column to create lagged features for.
    - lags (int): Number of lagged features to create.

    Returns:
    - pd.DataFrame: Dataset with lagged features added.
    """
    for lag in range(1, lags + 1):
        data[f'{column}_lag{lag}'] = data[column].shift(lag)
    return data

def calculate_rolling_statistics(data, column, window, stats=['mean', 'std']):
    """
    Calculate rolling statistics for a specified column.

    Parameters:
    - data (pd.DataFrame): The dataset.
    - column (str): The column to calculate rolling statistics for.
    - window (int): Window size for the rolling calculations.
    - stats (list): List of statistics to calculate (default: mean, std).

    Returns:
    - pd.DataFrame: Dataset with rolling statistics added.
    """
    for stat in stats:
        if stat == 'mean':
            data[f'{column}_rolling_mean'] = data[column].rolling(window).mean()
        elif stat == 'std':
            data[f'{column}_rolling_std'] = data[column].rolling(window).std()
        elif stat == 'min':
            data[f'{column}_rolling_min'] = data[column].rolling(window).min()
        elif stat == 'max':
            data[f'{column}_rolling_max'] = data[column].rolling(window).max()
    return data
