# Retail Waste Minimization AI 🛒

**A "System Design" approach to optimizing supermarket inventory using LightGBM and Censored Demand Estimation.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LightGBM](https://img.shields.io/badge/Model-LightGBM-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

## 📖 The Business Problem
Supermarkets face a "Perishable Inventory" dilemma:
1.  **Over-order:** Food rots (Waste Cost).
2.  **Under-order:** Shelves go empty (Stockout Cost + Customer Churn).

**The Trap:** Traditional models train on *Sales Data*. But when an item goes out of stock, sales drop to zero while *True Demand* remains high. Training on raw sales data causes models to underestimate demand, leading to a "Death Spiral" of shrinking inventory.

**The Solution:** This system implements a **Censored Demand Estimator** to reconstruct true customer intent and a **Shadow Deployment** strategy for safe rollout.

---

## 🏗️ System Architecture

### 1. The "Uncensoring" Logic (Data Engineering)
* **Input:** Historical Sales + Inventory Snapshots + Store Traffic.
* **Logic:**
    * If `Inventory > 0`: Assume `Demand = Sales`.
    * If `Inventory = 0`: Assume `Demand = Sales + Estimated_Lost_Potential` (derived from traffic data).
* **Result:** A corrected target variable that prevents the model from learning "zero sales" as "zero demand."

### 2. Global Forecasting Model (ML Strategy)
* **Approach:** Single Global LightGBM Regressor.
* **Why Global?** Training one model across all products (using `product_id` as a feature) allows the system to:
    * Handle **Cold Start** products (new items with no history) by leveraging category patterns.
    * Capture shared seasonality (e.g., "Weekend Peaks") robustly.
* **Features:**
    * **Cyclical Time:** Sin/Cos transformations for Month/Day (preserving Dec-Jan continuity).
    * **Interaction:** "Halo Effect" features (store traffic intensity).

### 3. Human-in-the-Loop "Shadow Mode" (Deployment)
* **Safety First:** The model does *not* immediately control orders.
* **Shadow Mode:** It runs in parallel to the Legacy System. We compare:
    * Legacy Waste vs. AI Simulated Waste.
    * Legacy Stockouts vs. AI Simulated Stockouts.
* **Ghost Variables:** A Streamlit dashboard allows managers to inject "invisible" context (e.g., "Competitor Price Cut") via temporary demand multipliers with **Auto-Expiry** to prevent stale configurations.

---

## 📂 Repository Structure

    retail-waste-management-system/
    ├── app/                  # Streamlit Dashboard for Manager Overrides
    ├── data/                 # Raw and Processed Data (GitIgnored)
    ├── notebooks/            # Story-driven analysis
    │   ├── 01_eda...         # Visualizing the "Stockout Trap"
    │   ├── 02_feature...     # Engineering Cyclical & Halo features
    │   └── 03_modeling...    # Training the Global LightGBM
    ├── src/                  # Production-grade source code
    │   ├── data/             # Synthetic generation & Uncensoring logic
    │   ├── features/         # Math-heavy transformations (Sin/Cos)
    │   ├── models/           # Training & Inference pipelines
    │   └── deployment/       # Shadow Mode & Override logic
    └── tests/                # Unit tests for critical math logic

---

## 🚀 Getting Started

### 1. Installation

    git clone [https://github.com/yourusername/retail-waste-management-system.git](https://github.com/yourusername/retail-waste-management-system.git)
    cd retail-waste-management-system
    pip install -r requirements.txt

### 2. Generate Data & Train
Since this is a portfolio project, we use a robust synthetic generator to simulate the "Censored Demand" phenomenon.

    # 1. Generate synthetic sales & stockout logs
    python -m src.data.generator

    # 2. Run the analysis notebooks
    jupyter notebook notebooks/

### 3. Run the Dashboard
Simulate the Store Manager interface:

    streamlit run app/dashboard.py

---

## 📊 Key Results

| Metric | Legacy System (Moving Avg) | AI Model (Global LightGBM) |
| :--- | :--- | :--- |
| **MAE (Error)** | High (Biased by stockouts) | **4.89 Units** (Unbiased) |
| **Stockout Risk** | Critical (Death Spiral) | **Minimized** (Service Level > 95%) |
| **Adaptability** | Low (Reactive) | **High** (Predictive seasonality) |

## 🛠️ Tech Stack
* **Core:** Python 3.10, Pandas, NumPy
* **ML:** LightGBM, Scikit-Learn
* **Viz:** Matplotlib, Seaborn, Plotly
* **App:** Streamlit