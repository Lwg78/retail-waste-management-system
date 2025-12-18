import pandas as pd

def calculate_halo_effects(df):
    """
    Creates features to capture cross-product interactions.
    
    Scenario: If a complementary product is on high sales/promotion, 
    this product's demand might spike. [cite: 184]
    """
    df = df.copy()
    
    # For this synthetic example, we simulate a "category" level feature.
    # In reality, this would check specific complementary product IDs.
    
    # Calculate daily total sales volume for the whole store (proxy for 'store busyness')
    daily_store_sales = df.groupby('date')['qty_sold'].transform('sum')
    
    # Feature: relative_store_volume
    # If the store is busy (lots of items selling), individual items sell more (Halo).
    df['store_halo_activity'] = daily_store_sales
    
    return df