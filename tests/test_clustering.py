import pytest
from scripts.data_cleaning import perform_clustering, load_data

@pytest.fixture
def data():
    return load_data('data/processed/cleaned_data.csv')

def test_clustering(data):
    clustered_data = perform_clustering(data)
    assert 'cluster' in clustered_data.columns
    assert clustered_data['cluster'].nunique() == 3  # Check if there are 3 clusters
