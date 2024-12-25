import pytest
from src.data_preprocessing import preprocess_data

def test_preprocess_data():
    data = preprocess_data('../data/raw/user_data.csv')
    assert data.isnull().sum().sum() == 0  # Check for missing values
