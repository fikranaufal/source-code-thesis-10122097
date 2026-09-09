"""
Business and Technical Metrics Calculation Utility.
Calculates RMSLE, MAE, Directional Accuracy, Cost of Forecast Error (Holding, Stockout, Spoilage/Muda),
and Inventory Replenishment Parameters (Safety Stock, Reorder Point ROP).
"""

import numpy as np
import pandas as pd
from scipy import stats


def calc_rmsle(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate Root Mean Squared Logarithmic Error (RMSLE).
    Clips negative predictions and targets to zero.
    """
    y_true_clean = np.maximum(0, np.nan_to_num(y_true, nan=0.0))
    y_pred_clean = np.maximum(0, np.nan_to_num(y_pred, nan=0.0))
    return float(np.sqrt(np.mean((np.log1p(y_pred_clean) - np.log1p(y_true_clean)) ** 2)))


def calc_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate Mean Absolute Error (MAE).
    """
    y_true_clean = np.nan_to_num(y_true, nan=0.0)
    y_pred_clean = np.nan_to_num(y_pred, nan=0.0)
    return float(np.mean(np.abs(y_pred_clean - y_true_clean)))


def calc_direction_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate Directional Accuracy (%): whether the predicted delta direction (+ / -)
    matches the actual sales movement day-over-day.
    """
    if len(y_true) < 2:
        return 100.0
    true_diff = np.diff(y_true)
    pred_diff = np.diff(y_pred)
    matches = (true_diff * pred_diff) >= 0
    return float(np.mean(matches) * 100.0)


def calc_inventory_costs(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    holding_cost: float = 0.50,
    stockout_cost: float = 5.00,
    spoilage_rate: float = 10.0,
    profit_margin: float = 5.00,
    annual_multiplier: float = 6.0
) -> dict:
    """
    Simulate financial impact of forecast errors based on lean principles:
    - Over-forecasting: creates Overstock -> incurs Holding Cost + Perishable Spoilage (Muda Waste).
    - Under-forecasting: creates Stockout -> incurs Lost Sales Penalty + Profit Forfeiture.
    
    Parameters:
    -----------
    y_true : np.ndarray
        Ground truth actual sales units.
    y_pred : np.ndarray
        Forecasted sales units from the model.
    holding_cost : float
        Holding/carrying cost per unit/day ($) - capital, space, utilities.
    stockout_cost : float
        Stockout penalty cost per unit ($) - lost sale, goodwill, expediting.
    spoilage_rate : float
        Percentage (0-100) of overstocked units that spoil (Muda) for perishables.
    profit_margin : float
        Average profit margin earned per unit sold ($).
    annual_multiplier : float
        Multiplier to annualize the evaluated test window (e.g. 6x for 2-month window).
        
    Returns:
    --------
    dict with holding_cost, spoilage_cost, stockout_cost, total_cost,
    total_overstock_units, total_understock_units, lost_profit.
    """
    diff = y_pred - y_true
    
    # Over-forecasting (y_pred > y_true): Excess inventory sitting on shelves
    overstock_units = np.maximum(0, diff)
    total_overstock = float(np.sum(overstock_units))
    holding_cost_total = total_overstock * holding_cost * annual_multiplier
    
    # Spoilage / Muda waste: portion of overstocked perishable inventory thrown away
    spoilage_units = total_overstock * (spoilage_rate / 100.0)
    spoilage_cost_total = spoilage_units * (profit_margin + holding_cost) * annual_multiplier
    
    # Under-forecasting (y_pred < y_true): Shelves empty, customer demand turned away
    understock_units = np.maximum(0, -diff)
    total_understock = float(np.sum(understock_units))
    stockout_cost_total = total_understock * stockout_cost * annual_multiplier
    lost_profit_total = total_understock * profit_margin * annual_multiplier
    
    total_cost = holding_cost_total + spoilage_cost_total + stockout_cost_total
    
    return {
        "holding_cost": holding_cost_total,
        "spoilage_cost": spoilage_cost_total,
        "stockout_cost": stockout_cost_total,
        "total_cost": total_cost,
        "lost_profit": lost_profit_total,
        "total_overstock_units": total_overstock * annual_multiplier,
        "total_understock_units": total_understock * annual_multiplier,
        "spoilage_units": spoilage_units * annual_multiplier
    }


def calc_safety_stock_rop(
    forecast_series: np.ndarray,
    lead_time_days: int = 3,
    service_level_pct: float = 95.0
) -> dict:
    """
    Calculate statistical Safety Stock and Reorder Point (ROP) for Genba operations:
    - Safety Stock = Z * std_dev(daily demand) * sqrt(Lead Time)
    - Reorder Point (ROP) = (mean daily demand * Lead Time) + Safety Stock
    
    Parameters:
    -----------
    forecast_series : np.ndarray
        Forecasted sales trajectory over the upcoming horizon.
    lead_time_days : int
        Supplier fulfillment lead time in days.
    service_level_pct : float
        Target fulfillment probability (e.g. 95%).
        
    Returns:
    --------
    dict with daily_mean, daily_std, z_score, safety_stock, reorder_point, lead_time_demand.
    """
    clean_series = np.maximum(0, np.nan_to_num(forecast_series, nan=0.0))
    daily_mean = float(np.mean(clean_series))
    daily_std = float(np.std(clean_series)) if len(clean_series) > 1 else daily_mean * 0.2
    
    # Avoid zero std in uniform forecasts
    if daily_std == 0:
        daily_std = max(1.0, daily_mean * 0.15)
        
    # Standard normal quantile for target service level (e.g., 95% -> 1.645)
    z_score = float(stats.norm.ppf(service_level_pct / 100.0))
    
    # Lead time demand & standard deviation
    lead_time_demand = daily_mean * lead_time_days
    lead_time_std = daily_std * np.sqrt(lead_time_days)
    
    safety_stock = int(np.ceil(z_score * lead_time_std))
    reorder_point = int(np.ceil(lead_time_demand + safety_stock))
    
    return {
        "daily_mean": daily_mean,
        "daily_std": daily_std,
        "z_score": z_score,
        "safety_stock": safety_stock,
        "reorder_point": reorder_point,
        "lead_time_demand": lead_time_demand
    }
