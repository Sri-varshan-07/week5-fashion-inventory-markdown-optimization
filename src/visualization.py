"""
Publication-Quality Visualization Suite for Week 5 Inventory & Markdown Optimization.
Generates 4 high-resolution diagnostic and operational decision figures.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Set global aesthetics
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#CBD5E0"
plt.rcParams["axes.linewidth"] = 0.8


def plot_inventory_allocation(df_alloc: pd.DataFrame, save_path: str):
    """
    Figure 1: Prescriptive Inventory Allocation Breakdown (60% Pre-Commitment + 40% Chase Buffer)
    with Safety Stock and Critical Fractiles.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={"width_ratios": [2.2, 1]})

    categories = df_alloc["category"]
    x = np.arange(len(categories))
    width = 0.55

    p1 = ax1.bar(
        x,
        df_alloc["pre_commitment_overseas_60pct"],
        width,
        label="60% Pre-Commitment (Overseas Lead Time: 24-28w)",
        color="#1E3A8A",
        alpha=0.9,
    )
    p2 = ax1.bar(
        x,
        df_alloc["agile_chase_buffer_40pct"],
        width,
        bottom=df_alloc["pre_commitment_overseas_60pct"],
        label="40% Agile Chase Buffer (Nearshore Lead Time: 3-4w)",
        color="#3B82F6",
        alpha=0.85,
    )

    # Add safety stock markers
    ax1.scatter(
        x,
        df_alloc["optimal_order_quantity_Q"] + df_alloc["safety_stock_units"],
        color="#DC2626",
        s=90,
        zorder=5,
        marker="D",
        label="Total Reorder Point (Q* + Safety Stock)",
    )

    # Value labels
    for i in range(len(categories)):
        tot = df_alloc["optimal_order_quantity_Q"].iloc[i]
        ax1.text(
            x[i],
            tot + 250,
            f"Q*={tot:,}\nUnits",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color="#1F2937",
        )

    ax1.set_title("Prescriptive Apparel Order Quantities & Agile Buffering Strategy", fontsize=13, fontweight="bold", pad=12)
    ax1.set_ylabel("Garment Volume (Units)", fontsize=11, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=10, fontweight="bold")
    ax1.legend(loc="upper left", frameon=True, fontsize=9.5)
    ax1.set_ylim(0, max(df_alloc["optimal_order_quantity_Q"]) * 1.35)

    # Panel 2: Critical Fractile vs Target Service Level
    colors = ["#4338CA", "#059669", "#D97706", "#4B5563"]
    fractiles = df_alloc["critical_fractile"]
    bars = ax2.barh(categories, fractiles, color=colors, height=0.5, alpha=0.85)

    for bar in bars:
        w = bar.get_width()
        ax2.text(
            w + 0.02,
            bar.get_y() + bar.get_height() / 2,
            f"{w:.1%}",
            ha="left",
            va="center",
            fontweight="bold",
            fontsize=10,
        )

    ax2.set_xlim(0, 1.0)
    ax2.set_xlabel("Critical Fractile (Cu / [Cu + Co])", fontsize=10, fontweight="bold")
    ax2.set_title("Asymmetric Risk Ratio", fontsize=12, fontweight="bold", pad=12)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_markdown_trajectory(markdown_sim_res: dict, save_path: str):
    """
    Figure 2: Dynamic Markdown Timing vs Traditional Late Liquidation Trajectory.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    weeks = np.arange(1, 17)
    trad = markdown_sim_res["traditional"]
    dyn = markdown_sim_res["algorithmic_dynamic"]

    # Panel 1: Price Trajectories
    ax1.step(weeks, trad["weekly_prices"], where="mid", label="Traditional Policy (Cliff Markdown @ W13: -60%)", color="#DC2626", linewidth=2.5, linestyle="--")
    ax1.step(weeks, dyn["weekly_prices"], where="mid", label="Algorithmic Policy (Stage 1 @ W8: -15%, Stage 2 @ W12: -35%)", color="#059669", linewidth=2.5)

    ax1.set_title("Price Trajectory over 16-Week Lifecycle", fontsize=12, fontweight="bold", pad=12)
    ax1.set_xlabel("Lifecycle Week", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Unit Selling Price ($)", fontsize=10, fontweight="bold")
    ax1.set_xticks(weeks)
    ax1.legend(loc="lower left", fontsize=9.5)

    # Panel 2: Cumulative Revenue Recovery
    cum_trad_rev = np.cumsum(np.array(trad["weekly_units_sold"]) * np.array(trad["weekly_prices"]))
    cum_dyn_rev = np.cumsum(np.array(dyn["weekly_units_sold"]) * np.array(dyn["weekly_prices"]))

    ax2.plot(weeks, cum_trad_rev, label=f"Traditional Revenue (${trad['total_revenue']:,.0f})", color="#DC2626", linewidth=2.5, marker="o", markersize=4)
    ax2.plot(weeks, cum_dyn_rev, label=f"Algorithmic Revenue (${dyn['total_revenue']:,.0f})", color="#059669", linewidth=2.5, marker="s", markersize=4)

    # Fill profit delta
    ax2.fill_between(weeks, cum_trad_rev, cum_dyn_rev, color="#10B981", alpha=0.25, label=f"Margin Lift: +{markdown_sim_res['gross_profit_lift_pct']:.1f}%")

    ax2.set_title("Cumulative Gross Revenue Recovery", fontsize=12, fontweight="bold", pad=12)
    ax2.set_xlabel("Lifecycle Week", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Cumulative Revenue ($)", fontsize=10, fontweight="bold")
    ax2.set_xticks(weeks)
    ax2.legend(loc="upper left", fontsize=9.5)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_monte_carlo_distributions(raw_distributions: dict, category: str, save_path: str):
    """
    Figure 3: Monte Carlo Gross Profit Distribution & Value-at-Risk (VaR) Analysis.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    trad_profits = raw_distributions[category]["trad"] / 1000.0  # in $k
    ml_profits = raw_distributions[category]["ml"] / 1000.0

    sns.kdeplot(trad_profits, ax=ax, label="Traditional Heuristic", color="#EF4444", fill=True, alpha=0.3, linewidth=2.2)
    sns.kdeplot(ml_profits, ax=ax, label="Prescriptive ML Merchandising", color="#10B981", fill=True, alpha=0.35, linewidth=2.2)

    # VaR 95% lines
    var95_trad = np.percentile(trad_profits, 5)
    var95_ml = np.percentile(ml_profits, 5)

    ax.axvline(var95_trad, color="#B91C1C", linestyle="--", linewidth=1.8, label=f"Trad 95% VaR: ${var95_trad:,.1f}k")
    ax.axvline(var95_ml, color="#047857", linestyle="--", linewidth=1.8, label=f"ML 95% VaR: ${var95_ml:,.1f}k")

    mean_trad = np.mean(trad_profits)
    mean_ml = np.mean(ml_profits)
    ax.axvline(mean_trad, color="#DC2626", linestyle=":", linewidth=2, label=f"Trad Mean: ${mean_trad:,.1f}k")
    ax.axvline(mean_ml, color="#059669", linestyle=":", linewidth=2, label=f"ML Mean: ${mean_ml:,.1f}k")

    ax.set_title(f"1,000-Run Monte Carlo Profit Distribution: {category}", fontsize=13, fontweight="bold", pad=14)
    ax.set_xlabel("Total Realized Gross Profit ($ thousands)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Probability Density", fontsize=11, fontweight="bold")
    ax.legend(loc="upper left", frameon=True, fontsize=9.5)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_early_warning_matrix(alerts_df: pd.DataFrame, save_path: str):
    """
    Figure 4: Operational Early Warning Matrix & Decision Boundaries.
    """
    fig, ax = plt.subplots(figsize=(11, 7))

    # Scatter plot of velocity change vs search momentum
    color_map = {
        "HEALTHY": "#2563EB",
        "VIRAL_SURGE_ALERT": "#7C3AED",
        "EARLY_DECAY_WARNING": "#F59E0B",
        "SEVERE_DECAY_CRITICAL": "#DC2626",
    }

    for alert_type, color in color_map.items():
        sub = alerts_df[alerts_df["alert_level"] == alert_type]
        if not sub.empty:
            ax.scatter(
                sub["search_momentum_4w"],
                sub["velocity_change_2w_pct"],
                label=f"{alert_type} ({len(sub)} events)",
                color=color,
                s=80,
                alpha=0.85,
                edgecolors="none",
            )

    # Decision boundary thresholds
    ax.axhline(0, color="#9CA3AF", linestyle="-", linewidth=0.8)
    ax.axvline(0, color="#9CA3AF", linestyle="-", linewidth=0.8)

    ax.axhline(-10, color="#F59E0B", linestyle="--", linewidth=1.2, label="Early Decay Velocity Threshold (-10%)")
    ax.axhline(-20, color="#DC2626", linestyle="--", linewidth=1.2, label="Severe Decay Velocity Threshold (-20%)")
    ax.axvline(10, color="#7C3AED", linestyle=":", linewidth=1.4, label="Viral Surge Momentum Threshold (+10%)")

    ax.set_title("Operational Early Warning Matrix: Search Momentum vs Velocity Deceleration", fontsize=12, fontweight="bold", pad=14)
    ax.set_xlabel("4-Week Search Interest Momentum Index (ΔSearch)", fontsize=10, fontweight="bold")
    ax.set_ylabel("2-Week Rolling Demand Velocity Change (ΔVelocity %)", fontsize=10, fontweight="bold")
    ax.legend(loc="lower right", frameon=True, fontsize=9)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
