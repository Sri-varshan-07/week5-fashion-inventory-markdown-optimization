"""
Prescriptive Inventory Optimization Engine for Fashion Merchandising.
Implements Asymmetric Newsvendor Critical Fractile Models, 60/40 Split Pre-Commitments,
Multi-Echelon Safety Stock, and Dynamic Reorder Points.
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import norm


class FashionInventoryOptimizer:
    """
    Optimizes apparel inventory pre-commitments and agile replenishment buffers
    under lead-time asymmetry and non-linear demand uncertainty.
    """

    def __init__(self, catalog_df: pd.DataFrame):
        self.catalog = catalog_df.set_index("category").to_dict(orient="index")

    def calculate_newsvendor_allocation(
        self,
        category: str,
        predicted_mean: float,
        lower_80: float,
        upper_80: float,
        scale_factor: float = 100.0,
    ) -> dict:
        """
        Calculates optimal order quantity Q* based on asymmetric cost ratio.

        Parameters:
            category: Apparel category name
            predicted_mean: Point forecast demand index
            lower_80: 10th percentile forecast index
            upper_80: 90th percentile forecast index
            scale_factor: Physical unit conversion multiplier (e.g. 1 index pt = 100 units)
        """
        cat_info = self.catalog.get(category)
        if not cat_info:
            raise ValueError(f"Category '{category}' not found in catalog metadata.")

        retail_p = cat_info["retail_price"]
        unit_c = cat_info["unit_cost"]
        salvage_p = cat_info["salvage_price"]

        cost_underage_Cu = retail_p - unit_c
        cost_overage_Co = unit_c - salvage_p
        critical_fractile = cost_underage_Cu / (cost_underage_Cu + cost_overage_Co)

        # Estimate distribution standard deviation from 80% prediction interval
        # Interval width = 2 * Z(0.90) * sigma = 2 * 1.28155 * sigma
        sigma_idx = max((upper_80 - lower_80) / (2.0 * 1.28155), 1.0)

        # Optimal target index using inverse normal CDF
        z_score = norm.ppf(critical_fractile)
        optimal_idx = predicted_mean + z_score * sigma_idx

        # Convert to physical garment units
        mean_units = int(predicted_mean * scale_factor)
        optimal_units = int(optimal_idx * scale_factor)

        # 60/40 Split Rule Policy:
        # Commit 60% of baseline requirement 6-9 months prior
        pre_commit_units = int(0.60 * mean_units)
        # Agile nearshore chase buffer reserved for rapid response
        chase_buffer_units = max(optimal_units - pre_commit_units, 0)

        expected_gross_margin = (
            min(optimal_units, mean_units) * (retail_p - unit_c)
            - max(optimal_units - mean_units, 0) * (unit_c - salvage_p)
        )

        return {
            "category": category,
            "sku": cat_info["sku"],
            "retail_price": retail_p,
            "unit_cost": unit_c,
            "salvage_price": salvage_p,
            "critical_fractile": round(critical_fractile, 4),
            "expected_demand_units": mean_units,
            "optimal_order_quantity_Q": optimal_units,
            "pre_commitment_overseas_60pct": pre_commit_units,
            "agile_chase_buffer_40pct": chase_buffer_units,
            "expected_gross_margin_usd": round(expected_gross_margin, 2),
            "sigma_units": int(sigma_idx * scale_factor),
        }

    def compute_safety_stock_and_rop(
        self,
        category: str,
        weekly_demand_mean: float,
        weekly_demand_std: float,
        lead_time_weeks: int = 4,
        lead_time_std: float = 0.5,
        service_level: float = 0.90,
    ) -> dict:
        """
        Calculates dynamic safety stock and reorder point considering both
        demand volatility and supply chain lead time uncertainty.
        Formula: SS = Z * sqrt(L * sigma_D^2 + D^2 * sigma_L^2)
        """
        z_val = norm.ppf(service_level)
        variance_term = (lead_time_weeks * (weekly_demand_std ** 2)) + (
            (weekly_demand_mean ** 2) * (lead_time_std ** 2)
        )
        safety_stock = z_val * np.sqrt(variance_term)
        lead_time_demand = weekly_demand_mean * lead_time_weeks
        reorder_point = lead_time_demand + safety_stock

        return {
            "category": category,
            "service_level": service_level,
            "lead_time_weeks": lead_time_weeks,
            "lead_time_demand_units": int(lead_time_demand),
            "safety_stock_units": int(safety_stock),
            "reorder_point_units": int(reorder_point),
        }

    def run_full_allocation_pipeline(self, forecast_df: pd.DataFrame, base_path: str = ".") -> pd.DataFrame:
        """
        Runs prescriptive allocation across all categories and forecast weeks.
        """
        latest_forecasts = (
            forecast_df.groupby("category")
            .agg({
                "predicted_demand": "mean",
                "prediction_lower_80": "mean",
                "prediction_upper_80": "mean",
                "demand_adoption_index": "mean",
            })
            .reset_index()
        )

        allocations = []
        for _, row in latest_forecasts.iterrows():
            alloc = self.calculate_newsvendor_allocation(
                category=row["category"],
                predicted_mean=row["predicted_demand"],
                lower_80=row["prediction_lower_80"],
                upper_80=row["prediction_upper_80"],
                scale_factor=100.0,
            )
            # Add safety stock
            ss_info = self.compute_safety_stock_and_rop(
                category=row["category"],
                weekly_demand_mean=alloc["expected_demand_units"] / 16.0,
                weekly_demand_std=alloc["sigma_units"] / 4.0,
                lead_time_weeks=self.catalog[row["category"]]["chase_lead_time_weeks"],
                service_level=self.catalog[row["category"]]["target_service_level"],
            )
            alloc.update({
                "safety_stock_units": ss_info["safety_stock_units"],
                "reorder_point_units": ss_info["reorder_point_units"],
            })
            allocations.append(alloc)

        df_allocations = pd.DataFrame(allocations)
        out_path = os.path.join(base_path, "data", "processed", "prescriptive_inventory_allocations.csv")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        df_allocations.to_csv(out_path, index=False)
        return df_allocations
