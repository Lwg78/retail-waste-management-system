import pandas as pd
import numpy as np

def run_shadow_simulation(df, model, legacy_system_predictions):
    """
    Compares AI Model vs Legacy System in "Shadow Mode".
    
    Does NOT execute orders. Just compares hypothetical waste/stockouts.
    [cite: 239, 246]
    """
    df = df.copy()
    
    # 1. AI Predictions
    # Note: In real life, we would prep features here first
    # For simulation, assuming df has features ready
    # df['ai_forecast'] = model.predict(df[features])
    
    # (Mocking AI prediction for script functionality)
    df['ai_forecast'] = df['adjusted_demand_target'] * np.random.normal(1.0, 0.1, len(df))
    
    # 2. Legacy Predictions (e.g., Moving Average) provided as input
    df['legacy_forecast'] = legacy_system_predictions
    
    # 3. Compare Metrics [cite: 241]
    
    # Waste Calculation: Order > Demand
    df['ai_waste'] = (df['ai_forecast'] - df['true_demand_hidden']).clip(lower=0)
    df['legacy_waste'] = (df['legacy_forecast'] - df['true_demand_hidden']).clip(lower=0)
    
    # Stockout Calculation: Demand > Order
    df['ai_lost_sales'] = (df['true_demand_hidden'] - df['ai_forecast']).clip(lower=0)
    df['legacy_lost_sales'] = (df['true_demand_hidden'] - df['legacy_forecast']).clip(lower=0)
    
    print("--- SHADOW MODE RESULTS ---")
    print(f"Total Waste (Legacy): {df['legacy_waste'].sum():.0f}")
    print(f"Total Waste (AI):     {df['ai_waste'].sum():.0f}")
    print(f"Lost Sales (Legacy):  {df['legacy_lost_sales'].sum():.0f}")
    print(f"Lost Sales (AI):      {df['ai_lost_sales'].sum():.0f}")
    
    return df