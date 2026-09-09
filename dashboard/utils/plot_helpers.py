"""
Plotly Chart Helper Functions with Executive Dark Theme and Dual Language Support.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Executive Dark Theme Color Palette
DARK_BG = "#0e1117"
CARD_BG = "#161b26"
GRID_COLOR = "#2d3748"
TEXT_COLOR = "#f7fafc"
MUTED_TEXT = "#a0aec0"

COLOR_ACTUAL = "#00f2fe"       # Cyan / Aqua
COLOR_BASELINE = "#f7971e"     # Amber / Orange (Individual LSTM)
COLOR_GLOBAL_LSTM = "#00e676"  # Emerald Green (Proposed Champion)
COLOR_NAIVE = "#ff416c"        # Coral Red (Seasonal Naive benchmark)
COLOR_ROP = "#ffd600"          # Gold (Reorder Point)
COLOR_SAFETY = "#ff5252"       # Crimson (Safety Stock)


def apply_executive_layout(
    fig: go.Figure,
    title: str = "",
    x_title: str = "",
    y_title: str = "",
    height: int = 420
) -> go.Figure:
    """Apply consistent executive dark styling to Plotly figures."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=15, color=TEXT_COLOR, family="Segoe UI, Inter, Roboto, Arial"),
            x=0.01,
            y=0.96
        ),
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, family="Segoe UI, Inter, Roboto, Arial"),
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=12, color=MUTED_TEXT)),
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=False,
            showline=True,
            linecolor=GRID_COLOR
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=12, color=MUTED_TEXT)),
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=False,
            showline=True,
            linecolor=GRID_COLOR
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=TEXT_COLOR),
            bgcolor="rgba(22, 27, 38, 0.6)"
        ),
        margin=dict(l=45, r=30, t=55, b=45),
        hovermode="x unified",
        height=height
    )
    return fig


def create_cost_waterfall_chart(baseline_cost: dict, global_cost: dict) -> go.Figure:
    """
    Render executive Waterfall chart showing the cost bridge:
    Baseline (Individual LSTM) -> Holding Savings -> Spoilage Savings -> Stockout Savings -> Proposed (Global LSTM).
    """
    diff_holding = baseline_cost["holding_cost"] - global_cost["holding_cost"]
    diff_spoilage = baseline_cost["spoilage_cost"] - global_cost["spoilage_cost"]
    diff_stockout = baseline_cost["stockout_cost"] - global_cost["stockout_cost"]
    
    x_labels = [
        "Biaya Baseline<br>(Individual LSTM)",
        "Efisiensi Simpan<br>(Holding Savings)",
        "Reduksi Basi/Muda<br>(Waste Elimination)",
        "Mitigasi Kehabisan<br>(Stockout Mitigation)",
        "Biaya Usulan<br>(Global LSTM)"
    ]
    
    # In waterfall, savings are negative deltas to step down cost
    y_values = [
        baseline_cost["total_cost"],
        -diff_holding,
        -diff_spoilage,
        -diff_stockout,
        global_cost["total_cost"]
    ]
    
    text_values = [
        f"${baseline_cost['total_cost']:,.0f}",
        f"-${diff_holding:,.0f}" if diff_holding >= 0 else f"+${abs(diff_holding):,.0f}",
        f"-${diff_spoilage:,.0f}" if diff_spoilage >= 0 else f"+${abs(diff_spoilage):,.0f}",
        f"-${diff_stockout:,.0f}" if diff_stockout >= 0 else f"+${abs(diff_stockout):,.0f}",
        f"${global_cost['total_cost']:,.0f}"
    ]
    
    fig = go.Figure(go.Waterfall(
        name="Cost Bridge",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=x_labels,
        textposition="outside",
        text=text_values,
        y=y_values,
        connector={"line": {"color": "#4a5568", "width": 1.5, "dash": "dot"}},
        decreasing={"marker": {"color": "#00e676"}},  # Emerald Green for cost reductions
        increasing={"marker": {"color": "#ff5252"}},  # Crimson if cost increased
        totals={"marker": {"color": "#00f2fe"}}        # Cyan for endpoint
    ))
    
    fig = apply_executive_layout(
        fig,
        title="Jembatan Penghematan Biaya Operasional (Operational Cost Savings Bridge)",
        x_title="",
        y_title="Total Biaya Operasional ($ USD)",
        height=450
    )
    fig.update_layout(hovermode="closest")
    return fig


def create_cost_breakdown_bar(baseline_cost: dict, global_cost: dict) -> go.Figure:
    """
    Side-by-side grouped bar chart comparing inventory cost components for Baseline vs Proposed.
    """
    categories = [
        "Biaya Simpan<br>(Holding Cost)",
        "Biaya Basi/Rusak<br>(Spoilage / Muda)",
        "Penalti Kehabisan<br>(Stockout Cost)",
        "Total Biaya<br>(Total Cost)"
    ]
    
    baseline_vals = [
        baseline_cost.get("holding_cost", 0),
        baseline_cost.get("spoilage_cost", 0),
        baseline_cost.get("stockout_cost", 0),
        baseline_cost.get("total_cost", 0)
    ]
    
    global_vals = [
        global_cost.get("holding_cost", 0),
        global_cost.get("spoilage_cost", 0),
        global_cost.get("stockout_cost", 0),
        global_cost.get("total_cost", 0)
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories,
        y=baseline_vals,
        name="Baseline Model (Individual LSTM)",
        marker_color=COLOR_BASELINE,
        text=[f"${v:,.0f}" for v in baseline_vals],
        textposition="outside"
    ))
    fig.add_trace(go.Bar(
        x=categories,
        y=global_vals,
        name="Proposed Model (Global LSTM)",
        marker_color=COLOR_GLOBAL_LSTM,
        text=[f"${v:,.0f}" for v in global_vals],
        textposition="outside"
    ))
    
    fig = apply_executive_layout(
        fig,
        title="Komparasi Komponen Biaya Operasional (Cost Breakdown Comparison)",
        x_title="",
        y_title="Estimasi Biaya ($ USD)",
        height=450
    )
    fig.update_layout(barmode="group")
    return fig


def create_kaizen_comparison_chart(df: pd.DataFrame, show_naive: bool = False) -> go.Figure:
    """
    Render time-series line chart comparing Actual vs Baseline Individual LSTM vs Proposed Global LSTM.
    """
    fig = go.Figure()
    
    # Ground Truth Actual Sales
    if "actual" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["actual"],
            name="Penjualan Aktual (Ground Truth)",
            mode="lines+markers",
            marker=dict(size=4, color=COLOR_ACTUAL),
            line=dict(color=COLOR_ACTUAL, width=2.5)
        ))
    
    # Baseline Individual LSTM (Sempro / TA-1)
    if "individual_lstm" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["individual_lstm"],
            name="Baseline Model (Individual LSTM)",
            mode="lines",
            line=dict(color=COLOR_BASELINE, width=2, dash="dash")
        ))
        
    # Proposed Global LSTM (Champion)
    if "global_lstm" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["global_lstm"],
            name="Proposed Model (Global LSTM)",
            mode="lines",
            line=dict(color=COLOR_GLOBAL_LSTM, width=3)
        ))
        
    # Optional Seasonal Naive Benchmark
    if show_naive and "naive" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["naive"],
            name="Seasonal Naive (Benchmark)",
            mode="lines",
            line=dict(color=COLOR_NAIVE, width=1.5, dash="dot")
        ))
    
    return apply_executive_layout(
        fig,
        title="Kinerja Deret Waktu: Aktual vs Baseline vs Model Global (Time-Series Comparison)",
        x_title="Tanggal Evaluasi (Date)",
        y_title="Unit Penjualan (Sales Units)",
        height=430
    )


def create_demand_matrix_scatter(df: pd.DataFrame, filter_cat: str = "All") -> go.Figure:
    """
    Create Syntetos-Boylan 4-quadrant scatter plot (ADI vs CV²).
    Standard cutoff thresholds: ADI = 1.32, CV² = 0.49.
    """
    plot_df = df.copy()
    if filter_cat and filter_cat != "All" and "category" in plot_df.columns:
        plot_df = plot_df[plot_df["category"] == filter_cat]
        
    color_map = {
        "Smooth": "#00e676",        # Emerald
        "Intermittent": "#ffd600",  # Gold
        "Erratic": "#ff9100",       # Orange
        "Lumpy": "#ff3d00",         # Red-Orange
        "No Sales": "#78909c"       # Grey
    }
    
    fig = px.scatter(
        plot_df,
        x="adi",
        y="cv2",
        color="category",
        color_discrete_map=color_map,
        hover_data=["store_nbr", "family", "mean", "cv2", "adi"],
        opacity=0.8
    )
    
    # Quadrant Threshold Lines
    fig.add_vline(
        x=1.32,
        line_width=1.5,
        line_dash="dash",
        line_color="#90caf9",
        annotation_text="Ambang ADI (1.32)",
        annotation_position="top left",
        annotation_font=dict(color="#90caf9", size=10)
    )
    fig.add_hline(
        y=0.49,
        line_width=1.5,
        line_dash="dash",
        line_color="#90caf9",
        annotation_text="Ambang CV² (0.49)",
        annotation_position="bottom right",
        annotation_font=dict(color="#90caf9", size=10)
    )
    
    fig.update_traces(marker=dict(size=7, line=dict(width=0.4, color="#ffffff")))
    
    return apply_executive_layout(
        fig,
        title="Matriks Pola Permintaan Syntetos-Boylan (Demand Pattern Matrix)",
        x_title="Average Demand Interval (ADI - Selang Waktu Permintaan)",
        y_title="Squared Coefficient of Variation (CV² - Variansi Ukuran Pesanan)",
        height=450
    )


def create_whatif_forecast_chart(
    dates: list,
    baseline_pred: np.ndarray,
    scenario_pred: np.ndarray,
    safety_stock: int,
    reorder_point: int
) -> go.Figure:
    """
    Visualizes future 14-day/30-day forecast comparing baseline vs simulated what-if condition,
    with Reorder Point and Safety Stock threshold indicators.
    """
    fig = go.Figure()
    
    # Baseline Model Forecast
    fig.add_trace(go.Scatter(
        x=dates,
        y=baseline_pred,
        name="Proyeksi Dasar (Baseline Global Forecast)",
        mode="lines",
        line=dict(color="#90caf9", width=2, dash="dash")
    ))
    
    # Simulated What-If Forecast
    fig.add_trace(go.Scatter(
        x=dates,
        y=scenario_pred,
        name="Proyeksi Skenario (Simulated What-If Demand)",
        mode="lines+markers",
        marker=dict(size=6, color=COLOR_GLOBAL_LSTM),
        line=dict(color=COLOR_GLOBAL_LSTM, width=3)
    ))
    
    # Reorder Point (ROP) horizontal line
    fig.add_hline(
        y=reorder_point,
        line_width=2,
        line_dash="dot",
        line_color=COLOR_ROP,
        annotation_text=f"Reorder Point (ROP): {reorder_point} unit",
        annotation_position="top right",
        annotation_font=dict(color=COLOR_ROP, size=11)
    )
    
    # Safety Stock horizontal line
    fig.add_hline(
        y=safety_stock,
        line_width=2,
        line_dash="dot",
        line_color=COLOR_SAFETY,
        annotation_text=f"Safety Stock: {safety_stock} unit",
        annotation_position="bottom right",
        annotation_font=dict(color=COLOR_SAFETY, size=11)
    )
    
    return apply_executive_layout(
        fig,
        title="Simulasi Proyeksi Permintaan & Penasihat ROP (What-If Demand & Reorder Advisor)",
        x_title="Tanggal Proyeksi (Forecast Horizon)",
        y_title="Estimasi Kebutuhan Unit (Units)",
        height=450
    )
