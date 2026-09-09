"""
Page 3: Pola Permintaan & Penasihat Pemesanan (Demand Pattern & Reorder Advisor)
Acts as the frontline Genba (現場) operational replenishment tool for retail store managers.
Features the Syntetos-Boylan 4-Quadrant Demand Matrix, dynamic 14-day What-If scenario simulations
(promotions, payday effects), and automated Reorder Point (ROP) & Safety Stock recommendations.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import numpy as np
import pandas as pd

from dashboard.utils.data_loader import load_descriptive_stats, load_timeseries_target
from dashboard.utils.metrics_calc import calc_safety_stock_rop
from dashboard.utils.plot_helpers import create_demand_matrix_scatter, create_whatif_forecast_chart

# Page configuration (guarded so it works standalone or in st.navigation)
try:
    st.set_page_config(
        page_title="Pola Permintaan & Reorder Advisor | Executive DSS",
        page_icon="📦",
        layout="wide"
    )
except Exception:
    pass

# Custom Executive Dark Styling
st.markdown("""
<style>
    .exec-hero-purple {
        background: linear-gradient(135deg, #161b26 0%, #1d1933 100%);
        border: 1px solid #2d3748;
        border-left: 5px solid #a855f7;
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
        border-color: #ffd600;
    }
    .metric-val-yellow {
        font-size: 2.0rem;
        font-weight: 800;
        color: #ffd600;
        margin: 4px 0;
    }
    .metric-val-red {
        font-size: 2.0rem;
        font-weight: 800;
        color: #ff5252;
        margin: 4px 0;
    }
    .metric-val-cyan {
        font-size: 2.0rem;
        font-weight: 800;
        color: #00f2fe;
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
    .badge-yellow { background: rgba(255, 214, 0, 0.15); color: #ffd600; }
    .badge-red { background: rgba(255, 82, 82, 0.15); color: #ff5252; }
    .badge-green { background: rgba(0, 230, 118, 0.15); color: #00e676; }
    .badge-cyan { background: rgba(0, 242, 254, 0.15); color: #00f2fe; }

    .quadrant-card {
        background-color: #161b26;
        border-radius: 8px;
        padding: 14px 16px;
        border: 1px solid #2d3748;
        height: 100%;
    }
    .genba-card {
        background: linear-gradient(135deg, rgba(255, 214, 0, 0.05) 0%, rgba(0, 230, 118, 0.05) 100%);
        border-left: 4px solid #ffd600;
        border-radius: 8px;
        padding: 20px 24px;
        margin-top: 25px;
        border-top: 1px solid #2d3748;
        border-right: 1px solid #2d3748;
        border-bottom: 1px solid #2d3748;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="exec-hero-purple">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <h1 style="color: #ffffff; margin: 0; font-size: 2.1rem; font-weight: 800;">
                📦 Pola Permintaan & Penasihat Pemesanan (Demand Pattern & Reorder Advisor)
            </h1>
            <p style="color: #a855f7; font-weight: 600; font-size: 1.05rem; margin: 6px 0 0 0;">
                Alat Operasional Lapangan (Genba 現場): Klasifikasi Pola Syntetos-Boylan, Skenario What-If & Kalkulasi ROP Otomatis
            </p>
            <p style="color: #a0aec0; font-size: 0.92rem; margin: 8px 0 0 0; max-width: 950px; line-height: 1.5;">
                Modul ini ditujukan bagi kepala toko (*Store Managers*) dan staf logistik untuk menerjemahkan proyeksi model ke dalam tindakan nyata. 
                Mengidentifikasi jenis permintaan barang, mensimulasikan dampak promosi / gajian 14 hari ke depan, 
                serta menghitung titik pemesanan ulang (<b>Reorder Point - ROP</b>) dan batas aman stok (<b>Safety Stock</b>).
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Load data
stats_df = load_descriptive_stats()
ts_df = load_timeseries_target()

if stats_df.empty or ts_df.empty:
    st.error("⚠️ Data deskriptif atau time-series tidak dapat dimuat.")
    st.stop()

# ==============================================================================
# SECTION 1: SYNTETOS-BOYLAN DEMAND PATTERN MATRIX
# ==============================================================================
st.markdown("### 🧭 Matriks Pola Permintaan Syntetos-Boylan (Syntetos-Boylan Matrix)")
st.caption("Klasifikasi 1.782 deret waktu toko-produk berdasarkan keteraturan interval permintaan (ADI) dan variabilitas volume transaksi (CV²):")

# Quadrant explanation cards
q_col1, q_col2, q_col3, q_col4 = st.columns(4)

with q_col1:
    st.markdown("""
    <div class="quadrant-card" style="border-top: 3px solid #00e676;">
        <h5 style="color: #00e676; margin-top:0;">🟢 Smooth (Permintaan Halus)</h5>
        <p style="color: #a0aec0; font-size: 0.78rem; margin-bottom: 4px;"><b>ADI &le; 1.32, CV² &le; 0.49</b></p>
        <p style="color: #cbd5e0; font-size: 0.82rem; line-height: 1.4;">
            Permintaan reguler dan volume stabil (Telur, Daging, Susu). Paling optimal untuk <i>Global Complex LSTM</i> dan prinsip <i>Just-In-Time</i>.
        </p>
    </div>
    """, unsafe_allow_html=True)

with q_col2:
    st.markdown("""
    <div class="quadrant-card" style="border-top: 3px solid #ffd600;">
        <h5 style="color: #ffd600; margin-top:0;">🟡 Intermittent (Berselang)</h5>
        <p style="color: #a0aec0; font-size: 0.78rem; margin-bottom: 4px;"><b>ADI > 1.32, CV² &le; 0.49</b></p>
        <p style="color: #cbd5e0; font-size: 0.82rem; line-height: 1.4;">
            Banyak periode transaksi nol, namun jumlah barang seragam saat terjual. Diuntungkan oleh fitur multivariat promosi dan kalender.
        </p>
    </div>
    """, unsafe_allow_html=True)

with q_col3:
    st.markdown("""
    <div class="quadrant-card" style="border-top: 3px solid #ff9100;">
        <h5 style="color: #ff9100; margin-top:0;">🟠 Erratic (Fluktuatif)</h5>
        <p style="color: #a0aec0; font-size: 0.78rem; margin-bottom: 4px;"><b>ADI &le; 1.32, CV² > 0.49</b></p>
        <p style="color: #cbd5e0; font-size: 0.82rem; line-height: 1.4;">
            Transaksi terjadi hampir setiap hari, tetapi ukuran pesanan sangat liar (Hardware, Taman). Model <i>Simple MV LSTM</i> mencegah overfit.
        </p>
    </div>
    """, unsafe_allow_html=True)

with q_col4:
    st.markdown("""
    <div class="quadrant-card" style="border-top: 3px solid #ff5252;">
        <h5 style="color: #ff5252; margin-top:0;">🔴 Lumpy (Sporadis Bergumpal)</h5>
        <p style="color: #a0aec0; font-size: 0.78rem; margin-bottom: 4px;"><b>ADI > 1.32, CV² > 0.49</b></p>
        <p style="color: #cbd5e0; font-size: 0.82rem; line-height: 1.4;">
            Paling menantang: jarang dibeli dan kuantitasnya acak. Membutuhkan buffer stok aman (*safety stock*) yang lebih besar.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Category Filter for Scatter Plot
f_col1, f_col2 = st.columns([2, 3])
with f_col1:
    cat_filter = st.selectbox(
        "Filter Tampilan Kuadran Matriks:",
        ["All", "Smooth", "Intermittent", "Erratic", "Lumpy"],
        index=0
    )
with f_col2:
    if cat_filter == "All":
        st.info(f"📊 Menampilkan seluruh <b>{len(stats_df):,}</b> deret waktu toko-kategori di 54 cabang toko ritel.")
    else:
        filtered_n = len(stats_df[stats_df["category"] == cat_filter]) if "category" in stats_df.columns else 0
        st.info(f"📍 Menampilkan <b>{filtered_n:,}</b> kombinasi deret waktu pada kuadran <b>{cat_filter}</b>.")

# Scatter Plot
fig_scatter = create_demand_matrix_scatter(stats_df, filter_cat=cat_filter)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("<br><hr style='border-color: #2d3748;'><br>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 2: WHAT-IF SCENARIO & REORDER POINT ADVISOR
# ==============================================================================
st.markdown("### 🔮 Simulator Skenario What-If & Penasihat Stok Ulang (14-Day Reorder Advisor)")
st.caption("Pilih toko dan kelompok produk untuk memproyeksikan kebutuhan stok selama 14 hari ke depan berdasarkan variabel situasional:")

# Store & Product Selection for Reorder Simulation
combos = ts_df[["store_nbr", "family"]].drop_duplicates().values
combo_options = [f"Store {s} - {f}" for s, f in combos]

col_cs1, col_cs2 = st.columns([2, 3])
with col_cs1:
    selected_target = st.selectbox("Pilih Seri Toko & Produk Target:", combo_options, index=0)
    selected_store_nbr = int(selected_target.split(" - ")[0].replace("Store ", ""))
    selected_family_name = selected_target.split(" - ")[1]

# Extract 14-day horizon from time series
series_slice = ts_df[(ts_df["store_nbr"] == selected_store_nbr) & (ts_df["family"] == selected_family_name)].copy()
if len(series_slice) >= 14:
    eval_slice = series_slice.iloc[-14:].copy()
else:
    eval_slice = series_slice.copy()

dates_14d = eval_slice["date"].tolist()
base_forecast_14d = eval_slice["global_lstm"].values.copy()

with col_cs2:
    st.markdown(f"**Target Terpilih:** Cabang **Store {selected_store_nbr}** | Kategori **{selected_family_name}**")
    st.caption(f"Horison proyeksi: {dates_14d[0] if dates_14d else 'N/A'} s/d {dates_14d[-1] if dates_14d else 'N/A'} (14 Hari Mendatang)")

# Levers for What-If
st.markdown("#### 🎛️ Tuas Simulasi Skenario Pasar (What-If Levers)")
w_col1, w_col2, w_col3, w_col4 = st.columns(4)

with w_col1:
    promo_count = st.slider(
        "Promosi Mendatang (Items on Promo):",
        min_value=0,
        max_value=30,
        value=8,
        step=1,
        help="Jumlah barang sejenis yang masuk katalog diskon/promosi."
    )

with w_col2:
    payday_active = st.toggle(
        "Siklus Gajian (Payday / Quincena):",
        value=True,
        help="Aktifkan lonjakan daya beli pada tanggal 15 dan akhir bulan."
    )

with w_col3:
    lead_time_val = st.slider(
        "Waktu Tunggu Supplier (Lead Time - Hari):",
        min_value=1,
        max_value=14,
        value=3,
        step=1,
        help="Lama waktu pengiriman dari gudang pusat/supplier ke rak toko."
    )

with w_col4:
    service_level_val = st.slider(
        "Target Layanan Konsumen (Service Level %):",
        min_value=85,
        max_value=99,
        value=95,
        step=1,
        help="Probabilitas ketersediaan stok tanpa kehabisan (95% adalah standar ritel modern)."
    )

# Dynamic What-If adjustments on 14-day forecast
simulated_forecast = base_forecast_14d.copy()

# Promotion uplift (approx 2.5% increase per promo item)
promo_factor = 1.0 + (promo_count * 0.025)
simulated_forecast = simulated_forecast * promo_factor

# Payday uplift (30% increase on quincena dates 15, 30, 31)
if payday_active:
    for idx, d_str in enumerate(dates_14d):
        try:
            day_num = int(d_str.split("-")[2])
            if day_num in [15, 30, 31]:
                simulated_forecast[idx] *= 1.30
        except Exception:
            pass

# Calculate statistical Safety Stock & Reorder Point (ROP)
inv_metrics = calc_safety_stock_rop(
    forecast_series=simulated_forecast,
    lead_time_days=lead_time_val,
    service_level_pct=float(service_level_val)
)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 3: REORDER KPI CARDS
# ==============================================================================
st.markdown("#### 📦 Rekomendasi Parameter Persediaan Toko (Inventory Replenishment Parameters)")

rk1, rk2, rk3, rk4 = st.columns(4)

with rk1:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Rata-rata Permintaan Harian</div>
        <div class="metric-val-cyan">{inv_metrics['daily_mean']:.1f} unit</div>
        <div class="metric-badge badge-cyan">{((promo_factor - 1.0)*100):+.1f}% Efek Promosi</div>
    </div>
    """, unsafe_allow_html=True)

with rk2:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Puncak Permintaan 14 Hari</div>
        <div class="metric-val-green">{np.max(simulated_forecast):.1f} unit</div>
        <div class="metric-badge badge-green">Puncak Terdeteksi</div>
    </div>
    """, unsafe_allow_html=True)

with rk3:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Batas Keamanan (Safety Stock)</div>
        <div class="metric-val-red">{inv_metrics['safety_stock']} unit</div>
        <div class="metric-badge badge-red">Service Level: {service_level_val}%</div>
    </div>
    """, unsafe_allow_html=True)

with rk4:
    st.markdown(f"""
    <div class="metric-card-kpi">
        <div class="metric-title-sub">Titik Pemesanan (Reorder Point)</div>
        <div class="metric-val-yellow">{inv_metrics['reorder_point']} unit</div>
        <div class="metric-badge badge-yellow">Lead Time: {lead_time_val} Hari</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# SECTION 4: INTERACTIVE WHAT-IF FORECAST PLOT
# ==============================================================================
st.markdown("#### 📈 Visualisasi Kurva Proyeksi 14 Hari & Garis Batas ROP")
fig_whatif = create_whatif_forecast_chart(
    dates=dates_14d,
    baseline_pred=base_forecast_14d,
    scenario_pred=simulated_forecast,
    safety_stock=inv_metrics["safety_stock"],
    reorder_point=inv_metrics["reorder_point"]
)
st.plotly_chart(fig_whatif, use_container_width=True)

# ==============================================================================
# SECTION 5: GENBA OPERATIONAL GUIDELINE (現場 ACTION)
# ==============================================================================
st.markdown(f"""
<div class="genba-card">
    <h4 style="color: #ffd600; margin-top: 0; display: flex; align-items: center; gap: 8px;">
        <span>📋</span> Standar Operasional Genba Toko (Store Frontline Action Guideline)
    </h4>
    <div style="color: #e2e8f0; font-size: 0.93rem; line-height: 1.7;">
        <ol style="margin-top: 6px; margin-bottom: 8px; padding-left: 20px;">
            <li><b>Triger Pemesanan Otomatis (Purchase Order Trigger):</b> Ketika sisa stok fisik di rak toko menyentuh 
                <b style="color: #ffd600;">Reorder Point (ROP: {inv_metrics['reorder_point']} unit)</b>, 
                sistem ERP toko harus otomatis menerbitkan Purchase Order (PO) ke gudang logistik pusat sebesar proyeksi kebutuhan siklus berikutnya.</li>
            <li><b>Fungsi Penyangga Batas Keamanan (Safety Stock Buffer: {inv_metrics['safety_stock']} unit):</b> 
                Stok penyangga ini menjamin bahwa pelanggan tidak akan menghadapi rak kosong jika terjadi keterlambatan armada truk supplier selama 
                <b>{lead_time_val} hari</b> atau terjadi lonjakan pembeli tak terduga, dengan tingkat jaminan <b>{service_level_val}% Service Level</b>.</li>
            <li><b>Pencegahan Overstock & Limbah (Zero Waste / Kaizen):</b> Jangan memesan melebihi kuantitas ROP yang direkomendasikan model, 
                khususnya untuk produk segar berkategori <i>Smooth</i> (seperti {selected_family_name}), guna menghindari pembusukan barang di ruang penyimpanan.</li>
        </ol>
    </div>
</div>
""", unsafe_allow_html=True)
