import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- MOCK BACKEND CONNECTION ---
# In a real app, this would import from src.models or load a .pkl file
def get_mock_predictions(product_id):
    """Generates fake prediction data for the demo."""
    dates = pd.date_range(start=datetime.today(), periods=14)
    base_demand = np.random.randint(50, 100)
    
    # Simulate a pattern
    predictions = [base_demand + np.random.randint(-10, 10) for _ in range(14)]
    
    return pd.DataFrame({
        'Date': dates,
        'AI_Forecast': predictions
    })

# --- UI LAYOUT ---
st.set_page_config(page_title="Retail Waste Manager", layout="wide")

st.title("🛒 Inventory Command Center")
st.markdown("**System Status:** Shadow Mode (AI Recommendations Active)")

# Sidebar: Context
st.sidebar.header("Filter Context")
selected_store = st.sidebar.selectbox("Select Store", ["Store #001 (Orchard)", "Store #002 (Tampines)"])
selected_product = st.sidebar.selectbox("Select Product", ["Fresh Milk 1L", "Burger Buns", "Salmon Fillet"])

# --- MAIN LOGIC ---
st.subheader(f"Forecast Overview: {selected_product}")

# 1. Load Data
df = get_mock_predictions(selected_product)

# 2. Human-in-the-Loop Controls
col1, col2 = st.columns([1, 2])

with col1:
    st.info("💡 **Ghost Variable Detected**\nCompetitor price drop suspected.")
    
    # The "Override" Slider
    override_multiplier = st.slider(
        "Adjust Demand Multiplier", 
        min_value=0.5, 
        max_value=1.5, 
        value=1.0, 
        help="Use 1.2x to increase order by 20%"
    )
    
    # [cite_start]The "Auto-Expiry" Feature [cite: 269]
    expiry_days = st.number_input("Override Duration (Days)", min_value=1, max_value=14, value=7)
    
    if st.button("Apply Override"):
        st.success(f"Override of {override_multiplier}x applied for {expiry_days} days. Logged for retraining.")

with col2:
    # 3. Visualization (Plotly)
    df['Adjusted_Forecast'] = df['AI_Forecast'] * override_multiplier
    
    fig = px.line(df, x='Date', y=['AI_Forecast', 'Adjusted_Forecast'], 
                  title="AI Baseline vs. Manager Adjusted",
                  color_discrete_map={"AI_Forecast": "gray", "Adjusted_Forecast": "blue"})
    st.plotly_chart(fig, use_container_width=True)

# 4. Impact Simulation
waste_risk = np.random.randint(2, 8)
st.metric(label="Estimated Daily Waste Risk", value=f"{waste_risk}%", delta="-1.2%" if override_multiplier < 1.0 else "+0.5%")