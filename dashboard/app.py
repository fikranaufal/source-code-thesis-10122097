"""
Executive Decision Support System (DSS) - Retail Sales Forecasting.
Multi-page Streamlit Application comparing Individual LSTM vs Global LSTM.
Entry point orchestrating modern navigation and executive dark aesthetics.
"""

import sys
import os

# Ensure repo root and dashboard directory are on sys.path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

import streamlit as st

# Configure global page properties
st.set_page_config(
    page_title="Retail Forecasting DSS | Global LSTM",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Executive Dark Styling
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    [data-testid="stSidebar"] {
        background-color: #121722;
        border-right: 1px solid #2d3748;
    }
    .sidebar-brand {
        padding: 16px 14px;
        background: linear-gradient(135deg, #161b26 0%, #1e2638 100%);
        border: 1px solid #2d3748;
        border-left: 4px solid #00e676;
        border-radius: 10px;
        margin-bottom: 16px;
    }
    .sidebar-info-box {
        background-color: #161b26;
        border: 1px dashed #2d3748;
        border-radius: 8px;
        padding: 12px 14px;
        font-size: 0.8rem;
        color: #a0aec0;
        line-height: 1.5;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Define pages relative to app.py
page_1 = st.Page(
    "pages/1_💰_Business_Impact_&_ROI.py",
    title="Dampak Bisnis & ROI (Business Impact)",
    icon="💰",
    default=True
)

page_2 = st.Page(
    "pages/2_📊_The_Kaizen_Story.py",
    title="Cerita Kaizen (The Kaizen Story)",
    icon="📊"
)

page_3 = st.Page(
    "pages/3_📦_Demand_Pattern_&_Reorder_Advisor.py",
    title="Pola Permintaan & ROP (Demand & Reorder)",
    icon="📦"
)

# Sidebar Header Branding
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff;">🏬 Retail DSS</div>
    <div style="font-size: 0.8rem; color: #00e676; font-weight: 600; margin-top: 3px;">Executive Decision Support System</div>
    <div style="font-size: 0.72rem; color: #a0aec0; margin-top: 4px;">Individual LSTM vs Global LSTM Research</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.caption("👨‍🔬 **Riset Skripsi:** Peramalan Penjualan Ritel Kaggle Store Sales (3+ Juta Transaksi)")

# Setup Navigation Menu
pg = st.navigation({
    "Navigasi Modul (Executive Navigation)": [page_1, page_2, page_3]
})

# Run selected page
pg.run()
