import numpy as np
import pandas as pd

def encode_cyclical_date_features(df, date_col='date'):
    """
    Transforms Month and DayOfWeek into Sin/Cos features.
    
    Why: To preserve continuity (e.g., Dec is close to Jan).
    """
    df = df.copy()
    
    # Ensure date column is datetime objects
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Month (1-12)
    df['month'] = df[date_col].dt.month
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    
    # Day of Week (0-6)
    df['day_of_week'] = df[date_col].dt.dayofweek
    df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    
    return df