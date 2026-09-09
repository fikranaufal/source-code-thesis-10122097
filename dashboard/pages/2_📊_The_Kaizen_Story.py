"""
Page 2: Cerita Kaizen (The Kaizen Story - Technical Model Performance)
Demonstrates the technical superiority of the Proposed Global LSTM over the Baseline Individual LSTM.
Features interactive store & product filters, time-series visualization, error metrics (RMSLE, MAE),
and an in-depth explanation of cross-learning dynamics that eliminate overfitting.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import numpy as np
import pandas as pd

from dashboard.utils.data_loader import load_timeseries_target, load_target_experiments_summary
from dashboard.utils.metrics_calc import calc_rmsle, calc_mae, calc_direction_accuracy
from dashboard.utils.plot_helpers import create_kaizen_comparison_chart

# Page configuration (guarded so it works standalone or in st.navigation)
try:
    st.set_page_config(
        page_title="Cerita Kaizen | Model Performance",
        page_icon="📊",
        layout="wide"
    )
except Exception:
    pass

# Custom Executive Dark Styling
st.markdown("""
<style>
    .exec-hero-blue {
        background: linear-gradient(135deg, #161b26 0%, #1a2234 100%);
        border: 1px solid #2d3748;
        border-left: 5px solid #00f2fe;
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
        transition: transform 0.2s ease;
    }
    .metric-card-kpi:hover {
        transform: translateY(-3px);
        border-color: #00f2fe;
    }
    .metric-val-cyan {
        font-size: 2.0rem;
        font-weight: 800;
        color: #00f2fe;
        margin: 4px 0;
    }
    .metric-val-amber {
        font-size: 2.0rem;
        font-weight: 800;
        color: #f7971e;
        margin: 4px 0;
    }
    .metric-val-green {
        font-size: 2.0rem;
        font-weight: 800;
        color: #00e676;
        margin: 4px 0;
    }
    .metric-title-sub {
        font-size: 0.85rem;
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

    .insight-card {
        background-color: #161b26;
        border-left: 4px solid #00e676;
        border-radius: 8px;
        padding: 20px 24px;
        margin-top: 20px;
        border-top: 1px solid #2d3748;
        border-right: 1px solid #2d3748;
        border-bottom: 1px solid #2d3748;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="exec-hero-blue">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <h1 style="color: #ffffff; margin: 0; font-size: 2.1rem; font-weight: 800;">
                📊 Cerita Kaizen: Kinerja & Evaluasi Model (The Kaizen Story)
            </h1>
            <p style="color: #00f2fe; font-weight: 600; font-size: 1.05rem; margin: 6px 0 0 0;">
                Evolusi Pemodelan Deep Learning: Mengatasi Overfitting Model Individual Menuju Generalisasi Model Global
            </p>
            <p style="color: #a0aec0; font-size: 0.92rem; margin: 8px 0 0 0; max-width: 950px; line-height: 1.5;">
                Halaman ini membuktikan keunggulan teknis arsitektur <b>Global LSTM</b> dibandingkan <b>Individual LSTM</b> 
                (model per-toko hasil seminar proposal). Eksperimen berfokus pada kategori permintaan halus (*Smooth Demand*) 
                seperti Telur, Daging, dan Makanan Siap Saji.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Load data
ts_df = load_timeseries_target()
summary_df = load_target_experiments_summary()

if ts_df.empty:
    st.error("⚠️ Data time-series belum tersedia. Silakan periksa data pendukung.")
    st.stop()

# ==============================================================================
# SECTION 1: INTERACTIVE FILTERS
# ==============================================================================
st.markdown("### 🔍 Filter Toko & Kategori Produk (Store & Product Selection)")
st.caption("Pilih toko dan kelompok produk untuk memvisualisasikan dinamika deret waktu penjualan aktual vs prediksi model:")

# Unique stores and product families
available_stores = sorted(ts_df["store_nbr"].unique().tolist())
available_families = sorted(ts_df["family"].unique().tolist())

# Priority smooth categories
priority_smooth = [f for f in ["EGGS", "MEATS", "PREPARED FOODS", "SEAFOOD", "GROCERY I"] if f in available_families]
other_families = [f for f in available_families if f not in priority_smooth]
ordered_families = priority_smooth + other_families

col_f1, col_f2, col_f3 = st.columns([2, 3, 2])

with col_f1:
    selected_store = st.selectbox(
        "Pilih Nomor Toko (Store Number):",
        available_stores,
        index=0,
        help="Pilih nomor cabang toko ritel di Ekuador."
    )

with col_f2:
    selected_family = st.selectbox(
        "Pilih Kategori Produk (Product Family):",
        ordered_families,
        index=0,
        help="Direkomendasikan memilih kategori dengan pola permintaan halus (Smooth) seperti Telur, Daging, dll."
    )

with col_f3:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    show_benchmark_naive = st.checkbox("Tampilkan Baseline Naive (Benchmark)", value=False)

# Filter dataset for selected combo
curr_df = ts_df[(ts_df["store_nbr"] == selected_store) & (ts_df["family"] == selected_family)].copy()

# Fallback if combo not found
if curr_df.empty:
    st.warning(f"Kombinasi Store {selected_store} - {selected_family} tidak memiliki data spesifik. Menampilkan kombinasi default (Store 23 - EGGS).")
    curr_df = ts_df[(ts_df["store_nbr"] == 23) & (ts_df["family"] == "EGGS")].copy()
    selected_store = 23
    selected_family = "EGGS"

# ==============================================================================
# SECTION 2: PERFORMANCE METRIC CARDS
# ==============================================================================
actual_vals = curr_df["actual"].values
indiv_vals = curr_df["individual_lstm"].values
global_vals = curr_df["global_lstm"].values
naive_vals = curr_df["naive"].values if "naive" in curr_df.columns else actual_vals

rmsle_indiv = calc_rmsle(actual_vals, indiv_vals)
rmsle_global = calc_rmsle(actual_vals, global_vals)
mae_indiv = calc_mae(actual_vals, indiv_vals)
mae_global = calc_mae(actual_vals, global_vals)
dir_acc_global = calc_direction_accuracy(actual_vals, global_vals)

improvement_rmsle = ((rmsle_indiv - rmsle_global) / rmsle_indiv * 100) if rmsle_indiv > 0 else 0.0
improvement_mae = ((mae_indiv - mae_global) / mae_indiv * 100) if mae_indiv > 0 else 0.0

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"#### 🎯 Metrik Akurasi untuk: **Store {selected_store} — {selected_family}**")

m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Baseline Individual LSTM</div>
        <div class="metric-val-amber">{rmsle_indiv:.4f}</div>
        <div class="metric-badge badge-amber">RMSLE (Model Lama Sempro)</div>
    </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Proposed Global LSTM</div>
        <div class="metric-val-green">{rmsle_global:.4f}</div>
        <div class="metric-badge badge-green">RMSLE (Model Usulan)</div>
    </div>
    """, unsafe_allow_html=True)

with m_col3:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Penurunan Galat (Error Reduction)</div>
        <div class="metric-val-cyan">-{improvement_rmsle:.1f}%</div>
        <div class="metric-badge badge-cyan">Peningkatan Presisi RMSLE</div>
    </div>
    """, unsafe_allow_html=True)

with m_col4:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Akurasi Arah Tren (Directional)</div>
        <div class="metric-val-green">{dir_acc_global:.1f}%</div>
        <div class="metric-badge badge-green">Kesesuaian Arah Fluktuasi</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 3: INTERACTIVE PLOTLY TIME-SERIES CHART
# ==============================================================================
st.markdown("### 📈 Visualisasi Deret Waktu (Time-Series Trajectory)")
fig_ts = create_kaizen_comparison_chart(curr_df, show_naive=show_benchmark_naive)
st.plotly_chart(fig_ts, use_container_width=True)

# ==============================================================================
# SECTION 4: INSIGHT BOX (CROSS-LEARNING & OVERFITTING ELIMINATION)
# ==============================================================================
st.markdown(f"""
<div class="insight-card">
    <h4 style="color: #00e676; margin-top: 0; display: flex; align-items: center; gap: 8px;">
        <span>💡</span> Analisis Cross-Learning: Mengapa Model Global Mengeliminasi Overfitting Model Individual?
    </h4>
    <div style="color: #e2e8f0; font-size: 0.93rem; line-height: 1.7;">
        <p style="margin-bottom: 10px;">
            Pada seminar proposal (Sempro), model <b>Individual LSTM</b> dilatih secara terisolasi per kombinasi toko-produk. 
            Hal ini memicu fenomena <b>Sample Starvation</b>: satu deret waktu lokal hanya memiliki sekitar 1.684 observasi harian. 
            Akibatnya, arsitektur LSTM dengan kapasitas parameter besar dengan mudah <i>menghafal derau lokal (noise memorization)</i>, 
            sehingga gagal melakukan generalisasi saat berhadapan dengan data pengujian (terlihat dari garis jingga yang berfluktuasi liar atau mengalami lag 1 hari).
        </p>
        <p style="margin-bottom: 0;">
            Sebaliknya, model <b>Global LSTM</b> menerapkan paradigma <b>Cross-Learning</b> melintasi <b>54 toko ritel dan 3.000.888 data transaksi</b>. 
            Mekanisme ini memungkinkan representasi bobot tersembunyi (*hidden states*) mempelajari pola universal: 
            pola musiman mingguan (lonjakan akhir pekan), siklus gajian dua mingguan (<i>Quincena</i> tanggal 15 dan akhir bulan), 
            serta elastisitas promosi tanpa terdistorsi oleh anomali stok lokal. 
            Inilah wujud nyata perbaikan berkelanjutan (<b>Kaizen</b>) yang menjamin stabilitas prediksi tingkat produksi.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 5: THESIS EXPERIMENT SUMMARY TABLE
# ==============================================================================
st.markdown("### 📋 Rangkuman Eksperimen 8 Kombinasi Target Utama (Thesis Research Findings)")
st.caption("Hasil komparasi arsitektur Simple vs Complex, Univariat vs Multivariat pada kategori Smooth dan Erratic:")

if not summary_df.empty:
    display_df = summary_df.copy()
    st.dataframe(
        display_df.style.highlight_min(
            subset=["RMSLE Simple UV", "RMSLE Complex UV", "RMSLE Simple MV", "RMSLE Complex MV"],
            color="#004d40",
            axis=1
        ).format({
            "RMSLE Naive": "{:.4f}",
            "RMSLE Individual LSTM": "{:.4f}",
            "RMSLE Simple UV": "{:.4f}",
            "RMSLE Complex UV": "{:.4f}",
            "RMSLE Simple MV": "{:.4f}",
            "RMSLE Complex MV": "{:.4f}",
            "Best RMSLE": "{:.4f}",
            "Improvement vs Naive (%)": "+{:.1f}%"
        }),
        use_container_width=True
    )
    st.caption("🟢 **Sorotan Hijau Tua:** Arsitektur Global LSTM terbaik pada setiap baris kombinasi target.")
