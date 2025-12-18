import pytest
import pandas as pd
from src.data.uncensor import estimate_true_demand

def test_uncensoring_logic():
    """
    Ensures that when a stockout happens, Estimated Demand > Sales.
    """
    # Create fake data: 10 units sold, Stockout=True, Traffic=1000
    df = pd.DataFrame({
        'qty_sold': [10],
        'is_stockout': [1],
        'store_traffic': [1000]
    })
    
    df_processed = estimate_true_demand(df)
    
    # The adjusted demand should be HIGHER than 10 because we ran out of stock
    assert df_processed.iloc[0]['adjusted_demand_target'] > 10