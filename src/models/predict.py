import joblib
import pandas as pd

def load_model(path='models/global_lgbm.pkl'):
    return joblib.load(path)

def make_predictions(model, X):
    """
    Generates demand forecasts.
    """
    return model.predict(X)