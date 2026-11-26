"""
Master Orchestration Pipeline for Week 5 Fashion Inventory & Markdown Optimization.
Executes data ingestion, prescriptive inventory allocation, dynamic markdown evaluation,
Monte Carlo simulation, and publication-quality figure generation.
"""

import os
import sys
import pandas as pd
import numpy as np

# Set local imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.data_loader import load_catalog_metadata, load_forecast_predictions
from src.inventory_engine import FashionInventoryOptimizer
from src.markdown_engine import DynamicMarkdownEngine
from src.simulation import MerchandisingMonteCarloSimulator
from src.visualization import (
    plot_inventory_allocation,
    plot_markdown_trajectory,
    plot_monte_carlo_distributions,
    plot_early_warning_matrix,
)


def run():
    print("================================================================================")
    print("  WEEK 5: PRESCRIPTIVE INVENTORY OPTIMIZATION & DYNAMIC MARKDOWN ENGINE         ")
    print("================================================================================")

    base_dir = os.path.abspath(os.path.dirname(__file__))

    # 1. Ingestion
    print("\n[Step 1/5] Loading Catalog Economics & Multi-Horizon Trend Forecasts...")
    catalog_df = load_catalog_metadata(base_path=base_dir)
    forecast_df = load_forecast_predictions(base_path=base_dir)
    print(f"  -> Catalog loaded: {len(catalog_df)} product silhouettes.")
    print(f"  -> Forecast observations: {len(forecast_df)} category-week data points.")

    # 2. Prescriptive Inventory Allocation
    print("\n[Step 2/5] Computing Newsvendor Critical Fractiles & 60/40 Split Buffers...")
    inv_optimizer = FashionInventoryOptimizer(catalog_df)
    alloc_df = inv_optimizer.run_full_allocation_pipeline(forecast_df, base_path=base_dir)
    for _, row in alloc_df.iterrows():
        print(
            f"  -> {row['category']:<20} | Q*={row['optimal_order_quantity_Q']:>5} | "
            f"Pre-commit (60%): {row['pre_commitment_overseas_60pct']:>5} | "
            f"Chase (40%): {row['agile_chase_buffer_40pct']:>5} | "
            f"Safety Stock: {row['safety_stock_units']:>4} | Fractile: {row['critical_fractile']:.2%}"
        )

    # 3. Dynamic Markdown & Decay Detection
    print("\n[Step 3/5] Evaluating Dynamic Markdown Yields & Trend Decay Early Warnings...")
    md_engine = DynamicMarkdownEngine(catalog_df)
    md_summary_df = md_engine.run_all_markdown_evaluations(forecast_df, base_path=base_dir)
    alerts_df = pd.read_csv(os.path.join(base_dir, "data", "processed", "trend_decay_early_warning_alerts.csv"))
    print(f"  -> Generated {len(alerts_df)} weekly trend velocity diagnostic alerts.")
    for _, row in md_summary_df.iterrows():
        print(
            f"  -> {row['category']:<20} | Traditional Profit: ${row['traditional_gross_profit']:>9,.0f} | "
            f"Algorithmic Profit: ${row['algorithmic_gross_profit']:>9,.0f} | "
            f"Profit Lift: +{row['profit_lift_pct']:>5.1f}% | Waste Cut: -{row['terminal_waste_reduction_pct']:.1f}%"
        )

    # 4. Monte Carlo Simulation
    print("\n[Step 4/5] Running 1,000-Iteration Monte Carlo Stochastic Demand Simulation...")
    sim_engine = MerchandisingMonteCarloSimulator(catalog_df, n_simulations=1000, seed=42)
    sim_summary_df, raw_distributions = sim_engine.run_all_simulations(base_path=base_dir)
    for _, row in sim_summary_df.iterrows():
        print(
            f"  -> {row['category']:<20} | Profit Lift: +{row['profit_lift_pct']:>5.1f}% | "
            f"Stockout Rate: {row['traditional_stockout_rate_pct']:>4.1f}% -> {row['ml_stockout_rate_pct']:>4.1f}% "
            f"(-{row['stockout_reduction_pct']:.1f}%) | 95% VaR: ${row['ml_var95']:>8,.0f}"
        )

    # 5. Publication Visualizations
    print("\n[Step 5/5] Generating Publication-Quality Figures & Diagnostic Plots...")
    figs_dir = os.path.join(base_dir, "reports", "figures")
    os.makedirs(figs_dir, exist_ok=True)

    fig1_path = os.path.join(figs_dir, "figure1_prescriptive_inventory_and_chase_allocation.png")
    plot_inventory_allocation(alloc_df, fig1_path)
    print(f"  -> Saved {fig1_path}")

    single_md_sim = md_engine.simulate_markdown_revenue_yield("Linen Co-ords", initial_stock=6000)
    fig2_path = os.path.join(figs_dir, "figure2_dynamic_markdown_trajectory_and_yield.png")
    plot_markdown_trajectory(single_md_sim, fig2_path)
    print(f"  -> Saved {fig2_path}")

    fig3_path = os.path.join(figs_dir, "figure3_monte_carlo_profit_distribution_var.png")
    plot_monte_carlo_distributions(raw_distributions, "Oversized Blazers", fig3_path)
    print(f"  -> Saved {fig3_path}")

    fig4_path = os.path.join(figs_dir, "figure4_operational_early_warning_matrix.png")
    plot_early_warning_matrix(alerts_df, fig4_path)
    print(f"  -> Saved {fig4_path}")

    print("\n================================================================================")
    print("  WEEK 5 PIPELINE COMPLETED SUCCESSFULLY! READY FOR REPORT GENERATION          ")
    print("================================================================================")


if __name__ == "__main__":
    run()
