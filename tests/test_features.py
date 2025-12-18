import pytest
import pandas as pd
import numpy as np
from src.features.cyclical import encode_cyclical_date_features

def test_month_encoding_continuity():
    """
    Ensures that December (12) and January (1) are close in vector space.
    """
    # Create a dummy dataframe with Dec and Jan
    df = pd.DataFrame({'date': ['2023-12-31', '2024-01-01']})
    
    df_transformed = encode_cyclical_date_features(df)
    
    # Check if cos component is similar (both near 1.0 for winter months)
    dec_cos = df_transformed.iloc[0]['month_cos']
    jan_cos = df_transformed.iloc[1]['month_cos']
    
    # They should be relatively close
    assert np.isclose(dec_cos, jan_cos, atol=0.2)

def test_sin_cos_range():
    """Ensures values are always between -1 and 1."""
    df = pd.DataFrame({'date': pd.date_range('2023-01-01', periods=100)})
    df = encode_cyclical_date_features(df)
    
    assert df['month_sin'].max() <= 1.0
    assert df['month_sin'].min() >= -1.0