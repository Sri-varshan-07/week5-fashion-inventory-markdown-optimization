# Risk Profiling, Monte Carlo Simulation & Scenario Planning

## 1. Fashion Supply Chain Risk Vectors
Apparel merchandising faces three major operational vulnerabilities:
1. **Viral Surge Risk:** Social media algorithms trigger unexpected viral spikes (+40% demand in 2 weeks).
2. **Weather Anomalies:** Delayed winter or unseasonal summer rain disrupt seasonal drop relevance.
3. **Logistics & Supplier Shocks:** Port congestion, customs delays, or raw fabric shortages.

## 2. Monte Carlo Methodology (1,000 Iterations)
- **Demand Realization:**
  $$D \sim \mathcal{N}(\mu, \sigma) \times (1 + \mathbb{I}_{\text{viral}} \times 0.40)$$
- **Value-at-Risk (95% VaR):**
  Represents the 5th percentile gross profit threshold:
  $$\text{VaR}_{95\%} = F_{\text{profit}}^{-1}(0.05)$$

## 3. Benchmark Results
- Traditional Static Ordering suffers a **52.8% stockout rate** under stochastic shocks due to rigid overseas commitments.
- Prescriptive ML Merchandising slashes stockouts to **11.8%--18.2%** (-69.4% average reduction) while boosting total realized profit by **+7.3%**.
- 95% VaR increases significantly, demonstrating downside capital protection.
