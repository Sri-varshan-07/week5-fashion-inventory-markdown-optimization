# Prescriptive Inventory Framework & Asymmetric Sourcing Optimization

## 1. Context & Business Rationale
Traditional fashion apparel supply chains rely on fixed annual commitments placed 6 to 9 months before customer delivery. Under volatile micro-trend shifts, this results in the classic inventory mismatch:
- Hot trends stock out, forfeiting lucrative full-price sales.
- Sluggish trends accumulate excess stock, requiring margin-destroying clearance liquidations.

## 2. Mathematical Foundation
To optimize order quantities under uncertainty, we formulate the **Asymmetric Newsvendor Problem**:
- Let $P$ be retail selling price.
- Let $C$ be unit production/landed cost.
- Let $S$ be salvage price ($P > C > S$).
- Cost of Underage ($C_u$): $P - C$ (unrealized profit margin).
- Cost of Overage ($C_o$): $C - S$ (depreciation loss).

The critical fractile is:
$$\tau^* = \frac{C_u}{C_u + C_o}$$

Using the calibrated 80% forecast interval from Week 4 $[Q_{10}, Q_{90}]$:
$$\sigma \approx \frac{Q_{90} - Q_{10}}{2.563}$$
$$Q^* = \mu + Z_{\tau^*} \cdot \sigma$$

## 3. The 60/40 Dual Sourcing Execution
1. **Overseas Core Allocation (60% of baseline demand):**
   - Booked 24–28 weeks in advance with long lead-time offshore suppliers at lowest unit manufacturing cost.
2. **Agile Chase Buffer (40% of baseline requirement):**
   - Retained as flexible production capacity with nearshore or domestic CMT (Cut-Make-Trim) facilities (lead time: 3–4 weeks).
   - Triggered only when leading indicators (social velocity growth $>15\%$ or search momentum $>+10.0$) confirm viral demand acceleration.

## 4. Multi-Echelon Safety Stock
$$\text{SS} = Z_{\alpha} \cdot \sqrt{L \cdot \sigma_D^2 + D^2 \cdot \sigma_L^2}$$
Protects against both demand volatility and port/freight delays.
