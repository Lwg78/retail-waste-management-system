# Run this in Python to fix the test file
content = """import pytest
import pandas as pd
from src.data.uncensor import estimate_true_demand

def test_uncensoring_logic():
    \"\"\"
    Ensures that when a stockout happens, Estimated Demand > Sales.
    \"\"\"
    # We need TWO rows:
    # 1. A "Normal Day" (is_stockout=0) to establish the baseline conversion rate.
    # 2. A "Stockout Day" (is_stockout=1) that we want to test.
    df = pd.DataFrame({
        'qty_sold': [100, 10],       # Day 1: 100 sold, Day 2: 10 sold
        'is_stockout': [0, 1],       # Day 1: Normal,   Day 2: Stockout
        'store_traffic': [1000, 1000] # Same traffic for both
    })
    
    df_processed = estimate_true_demand(df)
    
    # Check the Stockout Day (Index 1)
    # Day 1 Conversion = 100 / 1000 = 10%
    # Day 2 Estimate = 1000 * 10% = 100
    # Adjusted Demand (100) > Recorded Sales (10)
    adjusted_val = df_processed.iloc[1]['adjusted_demand_target']
    
    assert adjusted_val > 10
"""

with open("tests/test_uncensor.py", "w") as f:
    f.write(content)

print("✅ File tests/test_uncensor.py has been updated successfully!")

import pytest
import pandas as pd
from src.data.uncensor import estimate_true_demand

def test_uncensoring_logic():
    """
    Ensures that when a stockout happens, Estimated Demand > Sales.
    """
    # We need TWO rows:
    # 1. A "Normal Day" (is_stockout=0) to establish the baseline conversion rate (e.g., 10%).
    # 2. A "Stockout Day" (is_stockout=1) that we want to test.
    df = pd.DataFrame({
        'qty_sold': [100, 10],       # Day 1: 100 sold, Day 2: 10 sold
        'is_stockout': [0, 1],       # Day 1: Normal,   Day 2: Stockout
        'store_traffic': [1000, 1000] # Same traffic for both
    })
    
    df_processed = estimate_true_demand(df)
    
    # Check the Stockout Day (Index 1)
    adjusted_val = df_processed.iloc[1]['adjusted_demand_target']
    
    # Logic:
    # Day 1 Conversion = 100 / 1000 = 10%
    # Day 2 Estimate = 1000 * 10% = 100
    # So the Adjusted Demand (100) should be greater than the Recorded Sales (10)
    assert adjusted_val > 10
EOF
