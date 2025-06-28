import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from backend.neo4j_connector import Neo4jConnection
from backend.scope3_module import load_supplier_data, get_swap_suggestions
from backend.queries import (
    get_nodes_with_carbon,
    get_all_products,
    get_relationships_with_labels,
    get_donation_suggestions
)
from backend.predictor import train_model, predict_donation
from app.visualizer import show_graph, display_legend

# -------------------- 🔧 App Config -------------------------
st.set_page_config(page_title="Sustainable Twin", layout="wide")
st.title("🌿 Sustainable Digital Twin for Retail")

# -------------------- 🌐 Connect to Neo4j -------------------
conn = Neo4jConnection(
    uri="neo4j+s://80693212.databases.neo4j.io",
    user="neo4j",
    password="2NB6LSyOCRZgWKn7_tSMFLWu2lz0UEoJ0CZEBXswmFc"
)

# -------------------- 📌 Sidebar Navigation -----------------
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Select a feature:", [
    "📊 View Relationships",
    "🌡️ Carbon Emission Heatmap",
    "🤝 Donation Suggestions",
    "📂 Upload CSV & Predict",
    "🌍 Scope-3 Supplier Optimization Module"
])

# Shared Filter
products = get_all_products(conn)
selected_product = st.sidebar.selectbox("Filter by Product", ["All"] + products)

# Load filtered data
if selected_product == "All":
    data = get_relationships_with_labels(conn)
else:
    data = get_relationships_with_labels(conn, product=selected_product)

# -------------------- 🧭 Page Routing -----------------------

if page == "📊 View Relationships":
    st.subheader("📊 Relationship Table")
    st.dataframe(data)

elif page == "🌡️ Carbon Emission Heatmap":
    carbon_nodes = get_nodes_with_carbon(conn)
    st.subheader("🌡️ Carbon Emission Heatmap Graph")
    show_graph(data, carbon_nodes)
    display_legend()

elif page == "🤝 Donation Suggestions":
    st.subheader("🤝 Donation Suggestion Engine")
    donations = get_donation_suggestions(conn)
    if donations:
        st.dataframe(donations)
    else:
        st.info("No donation candidates found. Try a different filter.")

elif page == "📂 Upload CSV & Predict":
    st.subheader("📂 Upload Custom Product Data")
    uploaded_file = st.file_uploader("Upload CSV with columns: product, inventory, expiry_days, carbon_score", type="csv")

    if uploaded_file:
        df_uploaded = pd.read_csv(uploaded_file)
        st.write("📋 Uploaded Data Preview:")
        st.dataframe(df_uploaded)

        model = train_model()
        df_uploaded["donation_risk"] = df_uploaded.apply(
            lambda row: predict_donation(model, row['inventory'], row['expiry_days'], row['carbon_score']),
            axis=1
        )

        st.subheader("🔮 Prediction Results")
        st.dataframe(df_uploaded)

        st.download_button("📥 Download Results", df_uploaded.to_csv(index=False), file_name="predicted_donations.csv")
elif page == "🌍 Scope-3 Supplier Optimization Module":
    # ------------------🌍 Scope-3 Supplier Optimization Module --------------------------
    st.subheader("🌍 Scope-3 Supplier Optimization Module")

    try:
        df_suppliers = load_supplier_data("data/mock_supplier_emissions.csv")
        suggestions = get_swap_suggestions(df_suppliers)

    # Total carbon savings simulation
        total_savings = suggestions['Potential_Emission_Savings'].sum()
        st.success(f"🌱 If all swaps happen, total carbon emissions can be reduced by **{total_savings:.2f} units**.")

        st.write("🧾 Current Supplier Data (Color-Coded):")
        styled_df = df_suppliers.style.applymap(
            lambda val: 'background-color: red' if isinstance(val, (int, float)) and val > 70 else (
                        'background-color: yellow' if isinstance(val, (int, float)) and val > 40 else (
                        'background-color: green' if isinstance(val, (int, float)) else ''))
        , subset=['Carbon_Score'])
        st.dataframe(styled_df)

        st.write("🔁 Suggested Swaps with Impact:")
        st.dataframe(suggestions[[
            'Supplier', 'Product', 'Carbon_Score', 'Emission_Level', 'Distance_km',
            'Alternative_Supplier', 'Alt_Carbon_Score', 'Alt_Emission_Level',
            'Potential_Emission_Savings', 'Percent_Improvement'
        ]])

    except Exception as e:
        st.error(f"Something went wrong loading the Scope-3 module: {e}")

# -------------------- 🚪 Close DB -------------------------
conn.close()
