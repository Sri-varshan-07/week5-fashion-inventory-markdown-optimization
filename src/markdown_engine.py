"""
Algorithmic Dynamic Markdown & Trend Decay Decision Engine.
Implements early velocity decay detection, price elasticity yield modeling,
and multi-stage markdown schedules to salvage gross margins.
"""

import os
import numpy as np
import pandas as pd


class DynamicMarkdownEngine:
    """
    Optimizes markdown timing, depth, and promotional triggers
    based on trend velocity deceleration and price elasticity of demand.
    """

    def __init__(self, catalog_df: pd.DataFrame):
        self.catalog = catalog_df.set_index("category").to_dict(orient="index")

    def detect_trend_decay_alerts(self, forecast_df: pd.DataFrame) -> pd.DataFrame:
        """
        Monitors weekly social velocity, search momentum, and inventory sell-through
        to identify micro-trend inflection points and early decay signals.
        """
        df = forecast_df.sort_values(["category", "date"]).copy()

        alerts = []
        for cat, group in df.groupby("category"):
            elasticity = self.catalog[cat]["price_elasticity"]
            group = group.reset_index(drop=True)

            for i in range(2, len(group)):
                current = group.iloc[i]
                prev = group.iloc[i - 1]
                prev_2 = group.iloc[i - 2]

                # Rolling velocity change
                vel_change_2w = (current["predicted_demand"] - prev_2["predicted_demand"]) / max(prev_2["predicted_demand"], 1.0)
                search_mom = current.get("search_momentum_4w", 0.0)
                social_mom = current.get("social_momentum_4w", 0.0)

                # Flag triggers
                is_viral_surge = (social_mom > 10.0) or (vel_change_2w > 0.15)
                is_early_decay = (vel_change_2w < -0.10) and (search_mom < -5.0)
                is_severe_decay = (vel_change_2w < -0.20) or (search_mom < -15.0)

                alert_level = "HEALTHY"
                recommended_markdown = 0.0
                action = "Maintain full price and standard buffer"

                if is_viral_surge:
                    alert_level = "VIRAL_SURGE_ALERT"
                    recommended_markdown = 0.0
                    action = "Trigger nearshore chase capacity (+25% buffer)"
                elif is_severe_decay:
                    alert_level = "SEVERE_DECAY_CRITICAL"
                    recommended_markdown = 0.35
                    action = "Execute Stage 2 Clearance Markdown (-35%)"
                elif is_early_decay:
                    alert_level = "EARLY_DECAY_WARNING"
                    recommended_markdown = 0.15
                    action = "Initiate Stage 1 Promotional Discount (-15%)"

                alerts.append({
                    "date": current["date"],
                    "category": cat,
                    "week_of_year": current["week_of_year"],
                    "predicted_demand": current["predicted_demand"],
                    "velocity_change_2w_pct": round(vel_change_2w * 100, 2),
                    "search_momentum_4w": round(search_mom, 2),
                    "social_momentum_4w": round(social_mom, 2),
                    "alert_level": alert_level,
                    "recommended_markdown_pct": round(recommended_markdown * 100, 1),
                    "recommended_action": action,
                    "price_elasticity": elasticity,
                })

        return pd.DataFrame(alerts)

    def simulate_markdown_revenue_yield(
        self,
        category: str,
        initial_stock: int = 6000,
        weeks: int = 16,
    ) -> dict:
        """
        Simulates unit sell-through and revenue recovery under two contrasting policies:
        1. Traditional Late Markdown (wait until week 13, discount 60%)
        2. Algorithmic Early Dynamic Markdown (Stage 1 at week 8: -15%, Stage 2 at week 12: -35%)
        """
        cat_info = self.catalog[category]
        p0 = cat_info["retail_price"]
        c0 = cat_info["unit_cost"]
        s0 = cat_info["salvage_price"]
        elasticity = cat_info["price_elasticity"]

        # Base weekly organic demand trajectory with natural trend decay
        t = np.arange(weeks)
        decay_curve = np.exp(-0.08 * t)  # natural seasonal drop
        base_demand_per_week = (initial_stock / 14.0) * decay_curve

        # --- Policy 1: Traditional Merchandising ---
        trad_stock = initial_stock
        trad_revenue = 0.0
        trad_units_sold = []
        trad_prices = []

        for w in range(weeks):
            price = p0 if w < 12 else p0 * 0.40  # 60% terminal dump at week 13
            discount_pct = (p0 - price) / p0
            elasticity_multiplier = 1.0 + (abs(elasticity) * discount_pct)
            effective_demand = base_demand_per_week[w] * elasticity_multiplier
            sold = min(effective_demand, trad_stock)
            trad_stock -= sold
            trad_revenue += sold * price
            trad_units_sold.append(sold)
            trad_prices.append(price)

        # Salvage remainder
        trad_revenue += trad_stock * s0

        # --- Policy 2: Algorithmic Dynamic Markdown ---
        dyn_stock = initial_stock
        dyn_revenue = 0.0
        dyn_units_sold = []
        dyn_prices = []

        for w in range(weeks):
            if w < 7:
                price = p0  # Full price
            elif w < 11:
                price = p0 * 0.85  # Early -15% soft promo
            elif w < 14:
                price = p0 * 0.65  # -35% clearance
            else:
                price = p0 * 0.45  # -55% final sweep

            discount_pct = (p0 - price) / p0
            elasticity_multiplier = 1.0 + (abs(elasticity) * discount_pct)
            effective_demand = base_demand_per_week[w] * elasticity_multiplier
            sold = min(effective_demand, dyn_stock)
            dyn_stock -= sold
            dyn_revenue += sold * price
            dyn_units_sold.append(sold)
            dyn_prices.append(price)

        dyn_revenue += dyn_stock * s0

        total_cost = initial_stock * c0
        trad_gross_profit = trad_revenue - total_cost
        dyn_gross_profit = dyn_revenue - total_cost
        margin_lift_pct = ((dyn_gross_profit - trad_gross_profit) / abs(trad_gross_profit)) * 100.0

        return {
            "category": category,
            "initial_stock": initial_stock,
            "unit_cost": c0,
            "full_retail_price": p0,
            "traditional": {
                "total_revenue": round(trad_revenue, 2),
                "gross_profit": round(trad_gross_profit, 2),
                "gross_margin_pct": round((trad_gross_profit / trad_revenue) * 100, 2),
                "unsold_terminal_units": int(trad_stock),
                "weekly_units_sold": [int(x) for x in trad_units_sold],
                "weekly_prices": [round(x, 2) for x in trad_prices],
            },
            "algorithmic_dynamic": {
                "total_revenue": round(dyn_revenue, 2),
                "gross_profit": round(dyn_gross_profit, 2),
                "gross_margin_pct": round((dyn_gross_profit / dyn_revenue) * 100, 2),
                "unsold_terminal_units": int(dyn_stock),
                "weekly_units_sold": [int(x) for x in dyn_units_sold],
                "weekly_prices": [round(x, 2) for x in dyn_prices],
            },
            "gross_profit_lift_pct": round(margin_lift_pct, 2),
            "terminal_waste_reduction_units": int(trad_stock - dyn_stock),
        }

    def run_all_markdown_evaluations(self, forecast_df: pd.DataFrame, base_path: str = ".") -> pd.DataFrame:
        """
        Executes dynamic decay alerts and revenue comparisons across all catalog lines.
        """
        alerts_df = self.detect_trend_decay_alerts(forecast_df)
        alerts_path = os.path.join(base_path, "data", "processed", "trend_decay_early_warning_alerts.csv")
        os.makedirs(os.path.dirname(alerts_path), exist_ok=True)
        alerts_df.to_csv(alerts_path, index=False)

        summary_records = []
        for cat in self.catalog.keys():
            sim = self.simulate_markdown_revenue_yield(category=cat, initial_stock=6000)
            summary_records.append({
                "category": cat,
                "full_retail_price": sim["full_retail_price"],
                "unit_cost": sim["unit_cost"],
                "traditional_gross_profit": sim["traditional"]["gross_profit"],
                "algorithmic_gross_profit": sim["algorithmic_dynamic"]["gross_profit"],
                "profit_lift_usd": sim["algorithmic_dynamic"]["gross_profit"] - sim["traditional"]["gross_profit"],
                "profit_lift_pct": sim["gross_profit_lift_pct"],
                "traditional_leftover_units": sim["traditional"]["unsold_terminal_units"],
                "algorithmic_leftover_units": sim["algorithmic_dynamic"]["unsold_terminal_units"],
                "terminal_waste_reduction_pct": round(
                    ((sim["traditional"]["unsold_terminal_units"] - sim["algorithmic_dynamic"]["unsold_terminal_units"]) /
                     max(sim["traditional"]["unsold_terminal_units"], 1)) * 100, 2
                ),
            })

        df_summary = pd.DataFrame(summary_records)
        sum_path = os.path.join(base_path, "data", "processed", "markdown_policy_benchmark_summary.csv")
        df_summary.to_csv(sum_path, index=False)
        return df_summary
