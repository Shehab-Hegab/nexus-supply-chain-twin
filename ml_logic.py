import random

def train_predict_risk(df):
    """
    Simulates training a risk prediction model.
    Returns metrics dict and a dummy model object.
    """
    # Simulate processing time
    # In a real scenario, we would train XGBoost or similar here
    
    metrics = {
        'accuracy': 87.5,
        'risk_percentage': random.randint(15, 35)
    }
    
    model = "DummyModel"
    
    return metrics, model
