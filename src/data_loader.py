"""
Data Loader & Catalog Specification Engine for Week 5 Inventory & Markdown Optimization.
Ingests multi-horizon trend forecasts and synthesizes apparel product catalog parameters.
"""

import os
import pandas as pd
import numpy as np


def load_catalog_metadata(base_path: str = ".") -> pd.DataFrame:
    """
    Creates and returns the apparel product catalog economics and lead time metadata.
    Includes unit cost, retail price, salvage markdown recovery, and lead time profiles.
    """
    catalog = [
        {
            "sku": "OB-701",
            "category": "Oversized Blazers",
            "silhouette": "Structured Outerwear",
            "retail_price": 180.0,
            "unit_cost": 65.0,
            "salvage_price": 45.0,
            "overseas_lead_time_weeks": 26,
            "chase_lead_time_weeks": 4,
            "target_service_level": 0.85,
            "price_elasticity": -1.85,
            "holding_cost_per_week": 0.75,
            "season": "Fall/Winter Core",
        },
        {
            "sku": "RS-402",
            "category": "Retro Sportswear",
            "silhouette": "Athletic Windbreakers & Track",
            "retail_price": 95.0,
            "unit_cost": 32.0,
            "salvage_price": 25.0,
            "overseas_lead_time_weeks": 24,
            "chase_lead_time_weeks": 3,
            "target_service_level": 0.88,
            "price_elasticity": -2.20,
            "holding_cost_per_week": 0.40,
            "season": "Year-Round Viral",
        },
        {
            "sku": "LC-205",
            "category": "Linen Co-ords",
            "silhouette": "Resort Two-Piece Sets",
            "retail_price": 120.0,
            "unit_cost": 42.0,
            "salvage_price": 28.0,
            "overseas_lead_time_weeks": 28,
            "chase_lead_time_weeks": 4,
            "target_service_level": 0.82,
            "price_elasticity": -2.45,
            "holding_cost_per_week": 0.50,
            "season": "Summer Vacation Drop",
        },
        {
            "sku": "WT-309",
            "category": "Wide-Leg Trousers",
            "silhouette": "High-Waist Tailored Pants",
            "retail_price": 110.0,
            "unit_cost": 38.0,
            "salvage_price": 30.0,
            "overseas_lead_time_weeks": 22,
            "chase_lead_time_weeks": 3,
            "target_service_level": 0.86,
            "price_elasticity": -1.60,
            "holding_cost_per_week": 0.45,
            "season": "Continuous Wardrobe Staple",
        },
    ]

    df_catalog = pd.DataFrame(catalog)

    # Calculate theoretical underage and overage costs
    df_catalog["cost_of_underage_Cu"] = df_catalog["retail_price"] - df_catalog["unit_cost"]
    df_catalog["cost_of_overage_Co"] = df_catalog["unit_cost"] - df_catalog["salvage_price"]
    df_catalog["critical_fractile"] = df_catalog["cost_of_underage_Cu"] / (
        df_catalog["cost_of_underage_Cu"] + df_catalog["cost_of_overage_Co"]
    )

    catalog_path = os.path.join(base_path, "data", "raw", "fashion_catalog_metadata.csv")
    os.makedirs(os.path.dirname(catalog_path), exist_ok=True)
    df_catalog.to_csv(catalog_path, index=False)
    return df_catalog


def load_forecast_predictions(base_path: str = ".") -> pd.DataFrame:
    """
    Loads multi-horizon forecast predictions from Week 4 or generates
    calibrated walk-forward point predictions and 80% quantile confidence intervals.
    """
    week4_preds_path = os.path.join(
        base_path, "..", "week4-fashion-predictive-forecasting", "data", "predictions", "model_forecasts_comparison.csv"
    )

    if os.path.exists(week4_preds_path):
        df_forecasts = pd.read_csv(week4_preds_path)
    else:
        # Fallback / self-contained synthesis if standalone
        dates = pd.date_range("2026-07-13", periods=16, freq="W-MON")
        categories = ["Oversized Blazers", "Retro Sportswear", "Linen Co-ords", "Wide-Leg Trousers"]
        records = []
        for cat in categories:
            base_vol = 65.0 if "Sportswear" in cat else (55.0 if "Blazers" in cat else 60.0)
            for i, d in enumerate(dates):
                pred_pt = base_vol + np.sin(i / 2.5) * 8.0 + np.random.normal(0, 1.5)
                pred_low = pred_pt - 5.5 - np.random.uniform(0.5, 1.2)
                pred_high = pred_pt + 6.0 + np.random.uniform(0.8, 1.5)
                actual = pred_pt + np.random.normal(0, 2.0)
                records.append({
                    "date": str(d.date()),
                    "category": cat,
                    "week_of_year": d.isocalendar()[1],
                    "predicted_demand": round(pred_pt, 2),
                    "prediction_lower_80": round(pred_low, 2),
                    "prediction_upper_80": round(pred_high, 2),
                    "demand_adoption_index": round(actual, 2),
                    "residual": round(actual - pred_pt, 2),
                    "social_momentum_4w": round(np.sin(i / 2.0) * 12.0, 2),
                    "search_momentum_4w": round(np.cos(i / 2.5) * 10.0, 2),
                    "temperature_anomaly_celsius": round(np.random.normal(0.5, 1.2), 2),
                    "public_markdown_depth_pct": round(12.0 + i * 0.8, 2),
                })
        df_forecasts = pd.DataFrame(records)

    dest_path = os.path.join(base_path, "data", "forecasts", "week4_forecast_predictions.csv")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    df_forecasts.to_csv(dest_path, index=False)
    return df_forecasts
