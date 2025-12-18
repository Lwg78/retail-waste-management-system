import pandas as pd
import numpy as np
from datetime import timedelta, datetime

def generate_synthetic_data(start_date='2023-01-01', days=365, n_products=50):
    """
    Generates synthetic retail data with "Censored Demand".
    
    Logic:
    1. True Demand is generated (unknown to the model).
    2. Inventory is set.
    3. Sales = min(True Demand, Inventory).
    4. If Demand > Inventory, we have a Stockout (Censored Data).
    """
    np.random.seed(42)
    dates = pd.date_range(start=start_date, periods=days)
    data = []

    for product_id in range(1, n_products + 1):
        # Base demand for the product
        base_demand = np.random.randint(20, 50)
        
        for date in dates:
            # Simulate seasonality (higher on weekends)
            is_weekend = date.weekday() >= 5
            demand_noise = np.random.normal(0, 5)
            true_demand = int(max(0, base_demand + (10 if is_weekend else 0) + demand_noise))
            
            # Simulate Inventory (Ordering Strategy)
            # Sometimes we under-order (creating the problem)
            inventory_stock = int(np.random.normal(true_demand - 2, 5)) 
            inventory_stock = max(0, inventory_stock)
            
            # The "Censored" Reality [cite: 56, 57]
            # We can only sell what we have.
            qty_sold = min(true_demand, inventory_stock)
            
            # Did we stock out? [cite: 130]
            stockout_flag = 1 if true_demand > inventory_stock else 0
            
            # We also simulate Store Traffic for the "Uncensoring" logic later [cite: 120]
            store_traffic = np.random.randint(500, 1000)

            data.append({
                'date': date,
                'product_id': product_id,
                'inventory_morning': inventory_stock,
                'qty_sold': qty_sold,             # This is what the junior data scientist sees
                'true_demand_hidden': true_demand, # This is the truth we want to predict
                'is_stockout': stockout_flag,
                'store_traffic': store_traffic
            })

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_synthetic_data()
    df.to_csv("data/raw/synthetic_sales.csv", index=False)
    print("Synthetic data generated with censored demand patterns.")