import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pandas as pd
import joblib

def train_global_model(X, y):
    """
    Trains a single Global LightGBM model across all products.
    
    Why: Allows learning shared patterns and handling Cold Start products.
    [cite: 187, 189]
    """
    # Split data (Time-based split is better for time series, but random for simplicity here)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # LightGBM Dataset
    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_val, label=y_val)
    
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'learning_rate': 0.05,
        'num_leaves': 31,
        'feature_fraction': 0.9,
        'verbose': -1
    }
    
    print("Training Global LightGBM model...")
    model = lgb.train(
        params,
        train_data,
        num_boost_round=1000,
        valid_sets=[val_data],
        callbacks=[lgb.early_stopping(stopping_rounds=50)]
    )
    
    return model

def save_model(model, path='models/global_lgbm.pkl'):
    joblib.dump(model, path)