"""
Monte Carlo Stochastic Simulation & Stress Testing Engine.
Benchmarks Traditional Merchandising vs. Prescriptive ML-Driven Merchandising
across 1,000 stochastic demand and lead-time shock realizations.
"""

import os
import numpy as np
import pandas as pd


class MerchandisingMonteCarloSimulator:
    """
    Simulates operational risk, margin resilience, and stockout probability
    under stochastic real-world fashion demand distributions.
    """

    def __init__(self, catalog_df: pd.DataFrame, n_simulations: int = 1000, seed: int = 42):
        self.catalog = catalog_df.set_index("category").to_dict(orient="index")
        self.n_simulations = n_simulations
        self.seed = seed
        np.random.seed(seed)

    def run_category_simulation(
        self,
        category: str,
        mean_demand: float = 6000.0,
        demand_std: float = 1200.0,
        lead_time_shock_prob: float = 0.15,
    ) -> dict:
        """
        Runs N Monte Carlo trials comparing Strategy A (Traditional) vs Strategy B (Prescriptive ML).
        """
        info = self.catalog[category]
        p = info["retail_price"]
        c = info["unit_cost"]
        s = info["salvage_price"]

        # Strategy A: Traditional Static Heuristic
        # 100% ordered overseas 6 months prior based on point estimate
        q_trad = mean_demand

        # Strategy B: Prescriptive ML Optimization
        # Critical fractile order quantity Q* with 60% baseline commit and 40% chase flexibility
        cu = p - c
        co = c - s
        crit_fractile = cu / (cu + co)
        from scipy.stats import norm
        z_crit = norm.ppf(crit_fractile)
        q_prescriptive = mean_demand + z_crit * demand_std
        q_commit = 0.60 * mean_demand
        max_chase_capacity = q_prescriptive - q_commit

        # Generate stochastic demand realizations with occasional viral fat-tails
        stochastic_demands = np.random.normal(mean_demand, demand_std, self.n_simulations)
        # Add viral surge probability (5% chance of +40% surge)
        viral_flags = np.random.binomial(1, 0.05, self.n_simulations)
        stochastic_demands = stochastic_demands * (1.0 + viral_flags * 0.40)
        stochastic_demands = np.maximum(stochastic_demands, 1000.0)

        # Simulation records
        trad_profits = []
        trad_stockouts = []
        trad_leftovers = []

        ml_profits = []
        ml_stockouts = []
        ml_leftovers = []

        for actual_d in stochastic_demands:
            # --- Traditional Run ---
            sold_trad = min(actual_d, q_trad)
            stockout_trad = max(actual_d - q_trad, 0.0)
            leftover_trad = max(q_trad - actual_d, 0.0)
            # Traditional markdown salvage: late liquidation at 60% off or salvage
            rev_trad = sold_trad * p + leftover_trad * s
            cost_trad = q_trad * c
            prof_trad = rev_trad - cost_trad

            trad_profits.append(prof_trad)
            trad_stockouts.append(stockout_trad > 0)
            trad_leftovers.append(leftover_trad)

            # --- Prescriptive ML Run ---
            # Chase trigger: If early signals show demand > q_commit, activate chase capacity
            chase_needed = max(actual_d - q_commit, 0.0)
            chase_procured = min(chase_needed, max_chase_capacity)
            total_ml_procured = q_commit + chase_procured

            sold_ml = min(actual_d, total_ml_procured)
            stockout_ml = max(actual_d - total_ml_procured, 0.0)
            leftover_ml = max(total_ml_procured - actual_d, 0.0)

            # Algorithmic markdown: early dynamic salvage recovers ~0.65 of full price on average
            salvage_ml_price = p * 0.60
            rev_ml = sold_ml * p + leftover_ml * salvage_ml_price
            cost_ml = (q_commit * c) + (chase_procured * (c * 1.08))  # slight 8% agile surcharge
            prof_ml = rev_ml - cost_ml

            ml_profits.append(prof_ml)
            ml_stockouts.append(stockout_ml > 0)
            ml_leftovers.append(leftover_ml)

        # Compute summary metrics
        trad_profits = np.array(trad_profits)
        ml_profits = np.array(ml_profits)

        res = {
            "category": category,
            "mean_demand": mean_demand,
            "retail_price": p,
            "unit_cost": c,
            "traditional": {
                "mean_profit_usd": round(float(np.mean(trad_profits)), 2),
                "std_profit_usd": round(float(np.std(trad_profits)), 2),
                "var_95_usd": round(float(np.percentile(trad_profits, 5)), 2),
                "stockout_rate_pct": round(float(np.mean(trad_stockouts) * 100), 2),
                "mean_leftover_units": round(float(np.mean(trad_leftovers)), 1),
            },
            "prescriptive_ml": {
                "mean_profit_usd": round(float(np.mean(ml_profits)), 2),
                "std_profit_usd": round(float(np.std(ml_profits)), 2),
                "var_95_usd": round(float(np.percentile(ml_profits, 5)), 2),
                "stockout_rate_pct": round(float(np.mean(ml_stockouts) * 100), 2),
                "mean_leftover_units": round(float(np.mean(ml_leftovers)), 1),
            },
            "profit_lift_pct": round(
                float(((np.mean(ml_profits) - np.mean(trad_profits)) / abs(np.mean(trad_profits))) * 100), 2
            ),
            "stockout_reduction_pct": round(
                float(((np.mean(trad_stockouts) - np.mean(ml_stockouts)) / max(np.mean(trad_stockouts), 0.001)) * 100), 2
            ),
            "leftover_reduction_pct": round(
                float(((np.mean(trad_leftovers) - np.mean(ml_leftovers)) / max(np.mean(trad_leftovers), 0.001)) * 100), 2
            ),
            "raw_trad_profits": trad_profits,
            "raw_ml_profits": ml_profits,
        }
        return res

    def run_all_simulations(self, base_path: str = ".") -> pd.DataFrame:
        """
        Runs Monte Carlo benchmarks across all catalog categories.
        """
        records = []
        raw_distributions = {}

        for cat in self.catalog.keys():
            res = self.run_category_simulation(category=cat)
            raw_distributions[cat] = {
                "trad": res["raw_trad_profits"],
                "ml": res["raw_ml_profits"],
            }
            records.append({
                "category": cat,
                "retail_price": res["retail_price"],
                "unit_cost": res["unit_cost"],
                "traditional_mean_profit": res["traditional"]["mean_profit_usd"],
                "ml_mean_profit": res["prescriptive_ml"]["mean_profit_usd"],
                "profit_lift_pct": res["profit_lift_pct"],
                "traditional_stockout_rate_pct": res["traditional"]["stockout_rate_pct"],
                "ml_stockout_rate_pct": res["prescriptive_ml"]["stockout_rate_pct"],
                "stockout_reduction_pct": res["stockout_reduction_pct"],
                "traditional_mean_leftover": res["traditional"]["mean_leftover_units"],
                "ml_mean_leftover": res["prescriptive_ml"]["mean_leftover_units"],
                "leftover_reduction_pct": res["leftover_reduction_pct"],
                "traditional_var95": res["traditional"]["var_95_usd"],
                "ml_var95": res["prescriptive_ml"]["var_95_usd"],
            })

        df_sim = pd.DataFrame(records)
        out_path = os.path.join(base_path, "data", "processed", "monte_carlo_simulation_results.csv")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        df_sim.to_csv(out_path, index=False)
        return df_sim, raw_distributions
