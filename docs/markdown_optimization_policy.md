# Algorithmic Dynamic Markdown Policy & Trend Decay Detection

## 1. The Markdown Dilemma in Fast Fashion
Retailers typically wait until end-of-season clearance to initiate markdowns. By week 13, customer curiosity has vanished, forcing steep 60%–70% discounts.

## 2. Early Trend Decay Detection Rules
Our algorithm scans weekly category metrics:
1. **2-Week Velocity Deceleration ($\Delta V_{2w}$):**
   $$\Delta V_{2w} = \frac{V_t - V_{t-2}}{V_{t-2}}$$
2. **4-Week Search Momentum ($\Delta S_{4w}$):**
   $$\Delta S_{4w} = S_t - S_{t-4}$$

## 3. Four-Tier Escalation Schedule
- **Level 0 (Full Price, 0% Markdown):**
  - Conditions: $\Delta V_{2w} \ge 0$, $\Delta S_{4w} \ge 0$.
  - Action: Retain MSRP.
- **Level 1 (Promotional Lift, -15%):**
  - Conditions: $\Delta V_{2w} < -10\%$ AND $\Delta S_{4w} < -5.0$.
  - Action: Execute -15% soft promotional lift. Drives unit sales up by ~28% through price elasticity.
- **Level 2 (Clearance Markdown, -35%):**
  - Conditions: $\Delta V_{2w} < -20\%$ OR $\Delta S_{4w} < -15.0$.
  - Action: Execute -35% mid-season clearance to reclaim working capital.
- **Level 3 (Terminal Liquidation, -55% to -60%):**
  - Conditions: Season weeks 14–16 for broken sizes.
  - Action: Deep sweep to prevent warehouse carrying overhead.

## 4. Price Elasticity Modeling
$$Q(P) = Q_0 \cdot \left(1 + |\epsilon| \cdot \frac{P_0 - P}{P_0}\right)$$
Balances unit velocity acceleration against marginal revenue decay.
