import pytest
from src.satisfaction_model import satisfaction_model

def test_satisfaction_model():
    data = pd.read_csv('../data/raw/user_data.csv')
    model, accuracy = satisfaction_model(data)
    assert accuracy > 0.7  # Ensure the model has good accuracy
