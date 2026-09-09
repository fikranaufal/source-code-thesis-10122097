"""
Page 1: Dampak Bisnis, ROI & Asumsi Finansial (Business Impact, ROI & Assumptions)
The Primary Executive Landing Page. Translates forecast error into operational dollar impact
and Muda Elimination (Lean Manufacturing) without leading with technical deep learning metrics.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import numpy as np
import pandas as pd

from dashboard.utils.data_loader import load_timeseries_target
from dashboard.utils.metrics_calc import calc_inventory_costs
from dashboard.utils.plot_helpers import create_cost_waterfall_chart, create_cost_breakdown_bar

# Page configuration (guarded so it works standalone or in st.navigation)
try:
    st.set_page_config(
        page_title="Dampak Bisnis & ROI | Executive DSS",
        page_icon="💰",
        layout="wide"
    )
except Exception:
    pass

# Custom Executive Dark Styling
st.markdown("""
<style>
    .exec-hero {
        background: linear-gradient(135deg, #161b26 0%, #1a2234 100%);
        border: 1px solid #2d3748;
        border-left: 5px solid #00e676;
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.35);
    }
    .metric-card-kpi {
        background: linear-gradient(135deg, #161b26 0%, #111622 100%);
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 18px 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card-kpi:hover {
        transform: translateY(-3px);
        border-color: #00e676;
    }
    .metric-val-green {
        font-size: 2.1rem;
        font-weight: 800;
        color: #00e676;
        margin: 4px 0;
    }
    .metric-val-cyan {
        font-size: 2.1rem;
        font-weight: 800;
        color: #00f2fe;
        margin: 4px 0;
    }
    .metric-val-amber {
        font-size: 2.1rem;
        font-weight: 800;
        color: #f7971e;
        margin: 4px 0;
    }
    .metric-title-sub {
        font-size: 0.88rem;
        color: #a0aec0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-badge {
        font-size: 0.78rem;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
        margin-top: 4px;
    }
    .badge-green { background: rgba(0, 230, 118, 0.15); color: #00e676; }
    .badge-amber { background: rgba(247, 151, 30, 0.15); color: #f7971e; }
    .badge-cyan { background: rgba(0, 242, 254, 0.15); color: #00f2fe; }
    
    .assumption-card {
        background-color: #161b26;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 14px 16px;
        height: 100%;
    }
    .lean-box {
        background: linear-gradient(135deg, rgba(0, 230, 118, 0.05) 0%, rgba(0, 242, 254, 0.05) 100%);
        border-left: 4px solid #00e676;
        border-radius: 8px;
        padding: 20px 24px;
        margin-top: 25px;
        border-top: 1px solid #2d3748;
        border-right: 1px solid #2d3748;
        border-bottom: 1px solid #2d3748;
    }
</style>
""", unsafe_allow_html=True)

# Main Hero Header
st.markdown("""
<div class="exec-hero">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <h1 style="color: #ffffff; margin: 0; font-size: 2.1rem; font-weight: 800;">
                💰 Dampak Bisnis & ROI (Business Impact & Operational ROI)
            </h1>
            <p style="color: #00e676; font-weight: 600; font-size: 1.05rem; margin: 6px 0 0 0;">
                Sistem Pendukung Keputusan Eksekutif: Translasi Galat Prediksi ke Finansial & Eliminasi Pemborosan (Muda)
            </p>
            <p style="color: #a0aec0; font-size: 0.92rem; margin: 8px 0 0 0; max-width: 950px; line-height: 1.5;">
                Halaman ini menyajikan simulasi konversi akurasi model penjualan ritel ke dalam metrik finansial riil. 
                Membandingkan <b>Model Baseline (Individual LSTM)</b> hasil seminar proposal dengan <b>Model Usulan (Global LSTM)</b> 
                berdasarkan prinsip manufaktur ramping (*Lean Manufacturing / Kaizen*).
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Load cached time series data
ts_df = load_timeseries_target()

if ts_df.empty:
    st.error("⚠️ Data time-series tidak dapat dimuat. Silakan periksa file data pendukung.")
    st.stop()

# ==============================================================================
# SECTION 1: ASUMSI FINANSIAL & OPERASIONAL (ASSUMPTIONS SIDEBAR / SECTION)
# ==============================================================================
st.markdown("### ⚙️ Asumsi Variabel Bisnis & Operasional (Business Assumptions)")
st.caption("Tentukan parameter biaya untuk menghitung kerugian finansial akibat kesalahan peramalan (*Cost of Forecast Error*):")

col_a1, col_a2, col_a3, col_a4 = st.columns(4)

with col_a1:
    st.markdown("""
    <div class="assumption-card">
        <h5 style="color: #00f2fe; margin-top:0; margin-bottom:6px;">1. Profit Margin / Unit</h5>
        <p style="color: #a0aec0; font-size: 0.78rem; margin-bottom: 8px;">
            Margin keuntungan bersih rata-rata per unit yang diperoleh dari setiap penjualan sukses.
        </p>
    </div>
    """, unsafe_allow_html=True)
    margin_val = st.number_input(
        "Margin Keuntungan ($ USD):",
        min_value=0.50,
        max_value=50.00,
        value=5.00,
        step=0.50,
        key="param_margin"
    )

with col_a2:
    st.markdown("""
    <div class="assumption-card">
        <h5 style="color: #ffd600; margin-top:0; margin-bottom:6px;">2. Holding Cost / Unit / Hari</h5>
        <p style="color: #a0aec0; font-size: 0.78rem; margin-bottom: 8px;">
            <b>Biaya Over-forecasting:</b> Biaya modal tertahan, sewa gudang pendingin, utilitas, dan asuransi.
        </p>
    </div>
    """, unsafe_allow_html=True)
    holding_val = st.slider(
        "Biaya Simpan ($/unit/hari):",
        min_value=0.05,
        max_value=3.00,
        value=0.50,
        step=0.05,
        key="param_holding"
    )

with col_a3:
    st.markdown("""
    <div class="assumption-card">
        <h5 style="color: #ff5252; margin-top:0; margin-bottom:6px;">3. Stockout Penalty / Unit</h5>
        <p style="color: #a0aec0; font-size: 0.78rem; margin-bottom: 8px;">
            <b>Biaya Under-forecasting:</b> Hilangnya potensi penjualan (*lost sales*), degradasi loyalitas konsumen.
        </p>
    </div>
    """, unsafe_allow_html=True)
    stockout_val = st.slider(
        "Penalti Kehabisan ($/unit):",
        min_value=1.00,
        max_value=20.00,
        value=5.00,
        step=0.50,
        key="param_stockout"
    )

with col_a4:
    st.markdown("""
    <div class="assumption-card">
        <h5 style="color: #00e676; margin-top:0; margin-bottom:6px;">4. Spoilage Risk Rate (%)</h5>
        <p style="color: #a0aec0; font-size: 0.78rem; margin-bottom: 8px;">
            <b>Pemborosan (Muda):</b> Persentase barang segar (Daging, Telur, Ikan) yang membusuk & dibuang.
        </p>
    </div>
    """, unsafe_allow_html=True)
    spoilage_val = st.slider(
        "Tingkat Risiko Basi (%):",
        min_value=1,
        max_value=40,
        value=10,
        step=1,
        key="param_spoilage"
    )

# Scope Selector & Annual Multiplier
col_s1, col_s2 = st.columns([3, 1])

with col_s1:
    combos = ts_df[["store_nbr", "family"]].drop_duplicates().values
    combo_labels = ["Seluruh 8 Target Seri Utama (Aggregated Portfolio)"] + [f"Store {s} - {f}" for s, f in combos]
    selected_scope = st.selectbox("Cakupan Evaluasi Portofolio (Evaluation Scope):", combo_labels, index=0)

with col_s2:
    annual_mult = st.select_slider(
        "Skala Horison (Horizon Scale):",
        options=[1, 2, 4, 6, 12],
        value=6,
        format_func=lambda x: f"{x}x (Estimasi ~{x*2} Bulan)" if x < 6 else f"{x}x (Annualized 1 Tahun)"
    )

# Filter dataset based on selected scope
if "Aggregated" in selected_scope:
    eval_df = ts_df.copy()
else:
    s_id = int(selected_scope.split(" - ")[0].replace("Store ", ""))
    f_name = selected_scope.split(" - ")[1]
    eval_df = ts_df[(ts_df["store_nbr"] == s_id) & (ts_df["family"] == f_name)].copy()

# ==============================================================================
# SECTION 2: DYNAMIC ROI CALCULATOR
# ==============================================================================
# Baseline Model: Individual LSTM
cost_baseline = calc_inventory_costs(
    y_true=eval_df["actual"].values,
    y_pred=eval_df["individual_lstm"].values,
    holding_cost=holding_val,
    stockout_cost=stockout_val,
    spoilage_rate=float(spoilage_val),
    profit_margin=margin_val,
    annual_multiplier=float(annual_mult)
)

# Proposed Model: Global LSTM (Champion)
cost_global = calc_inventory_costs(
    y_true=eval_df["actual"].values,
    y_pred=eval_df["global_lstm"].values,
    holding_cost=holding_val,
    stockout_cost=stockout_val,
    spoilage_rate=float(spoilage_val),
    profit_margin=margin_val,
    annual_multiplier=float(annual_mult)
)

# Core Financial Deltas
total_savings = cost_baseline["total_cost"] - cost_global["total_cost"]
savings_pct = (total_savings / cost_baseline["total_cost"] * 100) if cost_baseline["total_cost"] > 0 else 0.0

waste_reduction_units = cost_baseline["spoilage_units"] - cost_global["spoilage_units"]
waste_reduction_pct = ((cost_baseline["spoilage_cost"] - cost_global["spoilage_cost"]) / cost_baseline["spoilage_cost"] * 100) if cost_baseline["spoilage_cost"] > 0 else 0.0

stockout_reduction_pct = ((cost_baseline["stockout_cost"] - cost_global["stockout_cost"]) / cost_baseline["stockout_cost"] * 100) if cost_baseline["stockout_cost"] > 0 else 0.0

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 3: LARGE EXECUTIVE METRIC CARDS
# ==============================================================================
st.markdown("### 📊 Ringkasan Finansial & Penghematan Biaya (Executive Financial Summary)")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Total Penghematan Biaya (Cost Savings)</div>
        <div class="metric-val-green">${total_savings:,.0f}</div>
        <div class="metric-badge badge-green">+{savings_pct:.1f}% Efisiensi Anggaran</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Eliminasi Pemborosan (Muda Waste)</div>
        <div class="metric-val-cyan">{waste_reduction_pct:.1f}%</div>
        <div class="metric-badge badge-cyan">~{waste_reduction_units:,.0f} Unit Basi Dihindari</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Biaya Usulan (Global LSTM Cost)</div>
        <div class="metric-val-green">${cost_global['total_cost']:,.0f}</div>
        <div class="metric-badge badge-green">Turun dari ${cost_baseline['total_cost']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Mitigasi Kehabisan Stok (Stockout Averted)</div>
        <div class="metric-val-amber">{stockout_reduction_pct:.1f}%</div>
        <div class="metric-badge badge-amber">Kepuasan Pelanggan Naik</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 4: VISUALIZATIONS (WATERFALL & BAR CHARTS)
# ==============================================================================
st.markdown("### 📈 Visualisasi Transparansi Biaya (Cost Transparency & Breakdown)")

tab_waterfall, tab_bar = st.tabs([
    "🌉 Jembatan Penghematan (Waterfall Cost Bridge)",
    "📊 Komparasi Komponen Biaya (Side-by-Side Breakdown)"
])

with tab_waterfall:
    fig_waterfall = create_cost_waterfall_chart(cost_baseline, cost_global)
    st.plotly_chart(fig_waterfall, use_container_width=True)
    st.caption("📌 **Cara Membaca:** Diagram Waterfall mengilustrasikan bagaimana perpindahan dari model Baseline Individual LSTM memotong biaya simpan, biaya bahan basi (Muda), dan denda kehabisan stok secara beruntun menuju total biaya operasional Model Global LSTM yang jauh lebih hemat.")

with tab_bar:
    fig_bar = create_cost_breakdown_bar(cost_baseline, cost_global)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption("📌 **Perbandingan Komponen:** Biaya Simpan (Holding), Biaya Makanan Segar Rusak/Basi (Spoilage Muda), dan Penalti Kehabisan Stok (Stockout).")

# ==============================================================================
# SECTION 5: LEAN MANUFACTURING & KAIZEN COMMENTARY BOX
# ==============================================================================
st.markdown(f"""
<div class="lean-box">
    <h4 style="color: #00e676; margin-top: 0; display: flex; align-items: center; gap: 8px;">
        <span>🌱</span> Kaizen & Eliminasi Muda dalam Rantai Pasok Ritel (Lean Supply Chain Impact)
    </h4>
    <div style="color: #e2e8f0; font-size: 0.92rem; line-height: 1.7;">
        Dalam filosofi manufaktur ramping Jepang (*Toyota Production System*), terdapat prinsip <b>Muda (無駄 - Pemborosan)</b> yang harus dieliminasi:
        <ul style="margin-top: 6px; margin-bottom: 8px; padding-left: 20px;">
            <li><b>Muda Pemborosan Inventaris (Excess Inventory):</b> Model Individual LSTM sering kali menghasilkan proyeksi berlebih (*over-forecast*) yang menyebabkan penumpukan stok di rak dan gudang. Hal ini membekukan modal kerja (*working capital*) dan memicu pembusukan produk segar (*perishables* seperti Daging dan Telur).</li>
            <li><b>Muda Cacat Pelayanan (Stockout / Under-forecast):</b> Ketika stok kosong, pelanggan beralih ke kompetitor dan margin penjualan langsung hangus.</li>
            <li><b>Solusi Berkelanjutan (Kaizen):</b> Model <b>Global LSTM</b> mentransformasikan rantai pasok menjadi sistem <i>Just-In-Time (JIT)</i>. Dengan mempelajari pola serempak lintas 54 toko, model mengurangi volatilitas proyeksi hingga menghemat <b>${total_savings:,.0f} ({savings_pct:.1f}%)</b> dan memangkas sampah makanan basi sebesar <b>{waste_reduction_pct:.1f}%</b>.</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)
