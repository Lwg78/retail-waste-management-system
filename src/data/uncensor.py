import pandas as pd
import numpy as np

def estimate_true_demand(df):
    """
    Adjusts the target variable `qty_sold` to account for lost sales during stockouts.
    
    Strategy:
    If stockout occurred, Estimate Demand = Sales + Unmet Demand.
    Unmet Demand is estimated using traffic/conversion rates or simple heuristic.
    [cite: 124, 126]
    """
    df = df.copy()
    
    # Calculate simple conversion rate from non-stockout days
    # (Sales / Traffic)
    # In a real system, this would be more granular.
    avg_conversion = df[df['is_stockout'] == 0]['qty_sold'].sum() / \
                     df[df['is_stockout'] == 0]['store_traffic'].sum()
    
    def adjust_demand(row):
        if row['is_stockout'] == 0:
            return row['qty_sold']
        else:
            # If we stocked out, how much MORE would we have sold?
            # Heuristic: We assume we missed about 20% of the day's potential 
            # or derive it from remaining traffic. 
            # Here we use a traffic-based estimation:
            estimated_total_potential = row['store_traffic'] * avg_conversion
            
            # We take the higher of actual sales or estimated potential to be safe
            return max(row['qty_sold'], estimated_total_potential)

    df['adjusted_demand_target'] = df.apply(adjust_demand, axis=1)
    
    return df