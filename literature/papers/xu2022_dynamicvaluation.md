---
id: xu2022_dynamicvaluation
title: "Dynamic Valuation of Battery Lifetime"
authors: ["Xu, B."]
year: 2022
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "37(3):2177-2186"
doi: "10.1109/TPWRS.2021.3116130"
quartile: "Q1 (SJR 2025, IEEE Trans. Power Systems, SJR 4.217)"
group: "Bolun Xu (Columbia Univ., Earth & Environmental Engineering)"
lineage: "Xu = UW PhD 2018 (Kirschen group), MIT postdoc 2018-2019, Columbia faculty (Xu CV). Continues xu2018_cycleagingcost; Columbia students later extend (Zheng, Jaworski & Xu 2022 TPWRS variable-efficiency SDP — cross-ref S3)."
streams: [S4_degradation_operation, S1_foundations_value]
market_context: "NYISO real-time arbitrage 2010-2020 (WEST, NORTH, NYC, LONGIL) and PJM RegD frequency regulation 2016-2020"
method_class: "SDP/DP over state of health with piecewise-linear value function; daily convex dispatch with marginal degradation cost"
evidence_read: "full text (arXiv 2011.08425v2, https://arxiv.org/pdf/2011.08425v2)"
oa_link: "https://arxiv.org/abs/2011.08425"
---

## 1. Research question
What is the opportunity value of battery capacity (and hence the right marginal degradation cost) at each state of health over a project life, instead of the usual amortised replacement cost — and what is a second-life battery worth?

## 2. Setting & assumptions
- 0.5 MW / 1 MWh Li-ion (NMC), 85 % round-trip efficiency, pack cost $200/kWh, warranty to 80 % SoH; true end of life 50–75 % SoH; capacity constant within a day.
- Price-taker; historical prices used as scenarios.

## 3. Constraints that drove the model choice
Degradation acts on a multi-year timescale while dispatch is daily; replacement-cost-based marginal cost ignores that the value of remaining capacity depends on future market opportunities and project end date.

## 4. Model
- Cycle aging: rainflow with Φ(u) = 3.14e-4 u^2.03 (NMC, 1000 cycles @ 80 % depth, Laresgoiti et al. 2015); calendar D_cal = 0.2/1825 per day (20 % over 5 years).
- Bellman recursion over days n with SoH state E_n: V_n(E_n) = max_{p_n} [O_n(p_n) + γ V_{n+1}(E)], E = E_n − [D_cyc(p_n) + D_cal] E_0.
- Algorithm 1: backward recursion with piecewise-linear value function in E; each stage a convex daily dispatch problem.
- Algorithm 2 (non-anticipative): marginal degradation cost C_{i,n} = (v^s_{i,n+1} − v^s_{i+1,n+1}) / (E^s_i − E^s_{i+1}) from the value-function slope used as the daily cycle-cost price.

## 5. Data & processing
NYISO RT prices 2010–2020 (4 zones); PJM RegD 2016–2020 market data (avg. capacity payment ~ $550/day/MW), 2020 signal used for simulation.

## 6. Justification
DP optimality under the stated model; comparisons with amortised-cost approach; error of the within-day constant-capacity assumption ~0.01–0.03 %/day.

## 7. Key results
- Frequency regulation yields ~2× the revenue of arbitrage over the life.
- Second-life batteries retain > 50 % (≈ 60 % early → 95 % near project end) of the value of new ones; > $100/kWh surplus with ≥ 5 years remaining; > $200/kWh in LONGIL.
- In NYISO arbitrage, new batteries profitable only in the volatile LONGIL zone.
- Marginal value of capacity is state- and time-dependent (not a constant replacement cost). Explicit % improvement over amortised-cost dispatch not extracted.

## 8. Limitations (stated + your critical reading)
- Stated: constant calendar rate, C-rate neglected (0.5C), second-life logistics costs ignored, regulation signal from 2020 only, resale market assumed.
- Critical: perfect-foresight DP over historical years; calendar aging independent of SoC/T — exactly the coupling that market products with high SoC holding (e.g., reserves) would trigger.

## 9. Relevance to my study
Provides a principled, market-dependent degradation price (slope of the value function) that can be plugged into a daily MILP or used as an RL reward term; the gap between arbitrage and regulation value shows that the product set changes the value of lifetime.

## 10. Lineage links
- Builds on: xu2018_cycleagingcost, shi2019_cycleagingpfp, he2018_intertemporal (Lagrangian MBU idea).
- Related: Xu 2022 MRS Energy & Sustainability review "The role of modeling battery degradation in bulk power system optimizations" (review journal; not archived).

## 11. Verification log
- Crossref bibliographic query: "Dynamic Valuation of Battery Lifetime", B. Xu (Columbia), TPWRS 37(3):2177–2186, 2022, DOI 10.1109/TPWRS.2021.3116130.
- Xu CV lists same volume/pages.
- arXiv 2011.08425v2 full text read.
- SJR: scimagojr.com sourceid 28825 → Q1.
