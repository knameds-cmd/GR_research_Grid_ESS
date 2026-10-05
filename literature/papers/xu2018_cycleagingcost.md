---
id: xu2018_cycleagingcost
title: "Factoring the Cycle Aging Cost of Batteries Participating in Electricity Markets"
authors: ["Xu, B.", "Zhao, J.", "Zheng, T.", "Litvinov, E.", "Kirschen, D. S."]
year: 2018
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "33(2):2248-2259"
doi: "10.1109/TPWRS.2017.2733339"
quartile: "Q1 (SJR 2025, IEEE Trans. Power Systems, SJR 4.217; Q1 Electrical & Electronic Eng. and Energy Eng. & Power Tech.)"
group: "Kirschen (Univ. of Washington) with ISO New England (Litvinov, Zheng, Zhao)"
lineage: "Xu = UW PhD 2018 (Xu CV), Kirschen senior author; ISO-NE market-design co-authors -> formulation targeted at market-clearing integration. Continues xu2018_degradationmodel."
streams: [S4_degradation_operation, S7_market_design]
market_context: "ISO-NE (SE-MASS zone) 2015, day-ahead hourly, real-time hourly and real-time 5-min energy + reserve; price-taker with perfect foresight"
method_class: "MILP (piecewise-linear cycle-depth cost, binary for charge/discharge exclusivity)"
evidence_read: "full text (arXiv 1707.04567, https://arxiv.org/pdf/1707.04567)"
oa_link: "https://arxiv.org/abs/1707.04567"
---

## 1. Research question
How can the (rainflow-based, non-analytical) cycle-aging cost of a battery be represented in a form that a market participant can bid and that an ISO can put into a market-clearing optimisation, and how much does it change profit and lifetime?

## 2. Setting & assumptions
- Price-taker, perfect price foresight (historical prices), one year 2015, ISO-NE SE-MASS.
- 20 MW / 12.5 MWh Li-ion (NMC 18650 cells), 95 % charge and discharge efficiency, SoC ∈ [15 %, 95 %].
- Products: energy + reserve (NERC-style 1-h reserve sustainability constraint).
- Cycle aging only in the optimiser; calendar aging added ex post as constant 10 %/yr ("shelf life 10 years").
- Charging half-cycles assumed to cause no aging; discharging half-cycles age like full cycles of same depth; C-rate effects neglected (BES > 15 min duration).

## 3. Constraints that drove the model choice
Rainflow counting is non-analytical, cannot be written as constraints. Market clearing engines require convex, linear (or piecewise-linear) offer curves. Hence: a convex piecewise-linear cost on discharge power partitioned into SoC/"cycle-depth" segments that an ISO can embed like a multi-segment offer.

## 4. Model
- Cycle depth stress function (NMC lab data, Laresgoiti et al.): Φ(δ) = 5.24e-4 · δ^2.03; life loss L = Σ_i Φ(δ_i) over rainflow cycles.
- Piecewise-linear upper approximation with J equal depth segments; marginal cost of segment j:
  c_j = (R / η^dis) · J · [Φ(j/J) − Φ((j−1)/J)], R = cell replacement cost (300 000 $/MWh).
- Energy stored is split into segments e_{t,j} ∈ [0, E/J]; discharge from segment j costs c_j; cost C = Σ_t Σ_j M c_j p^dis_{t,j}.
- Objective: max Σ_t M[λ^e_t (g_t − d_t) + λ^q_t q_t] − C.
- Constraints: power limits, segment SoC dynamics with η^ch/η^dis, charge/discharge exclusivity via binary v_t, reserve sustainability S(g_t + q_t − d_t) ≤ Σ_j e_{t,j}.
- Theorem 1: with convex Φ, the optimiser discharges cheaper (shallower) segments first (greedy order holds without extra binaries). Theorem 2: as J → ∞ the model converges to rainflow cycle cost.
- Solver: GAMS/CPLEX.

## 5. Data & processing
- ISO-NE 2015 DA hourly, RT hourly (5-min averaged) and RT 5-min LMPs + reserve prices (SE-MASS).
- Cycle-life spec: 3000 cycles at 80 % DoD; NMC stress function from literature cell tests.
- Ex-post evaluation: dispatched SoC profile → rainflow → life loss; prorated profit = revenue − life-loss × replacement cost (incl. calendar).

## 6. Justification
Convergence proof (J → ∞) and convexity/greedy-order proof; numerical modelling error vs. exact rainflow < 5 % at 16 segments; comparison against (i) no-cost and (ii) single-segment (constant marginal cost) baselines.

## 7. Key results
RT 5-min market (Table I):
| Model | Annual revenue | Annual life loss | Prorated profit | Life |
|---|---|---|---|---|
| No aging cost | $789.3k | 77 % | −$2 101.3k | 1.1 yr |
| 1-segment | $303.8k | 2.2 % | $222.5k | 8.2 yr |
| 16-segment | $372.3k | 2.6 % | $276.3k | 8.0 yr |
- 16-segment model yields ~24 % higher prorated profit than the constant-cost model at similar life; ignoring aging destroys the asset in ~1 year.

## 8. Limitations (stated + your critical reading)
- Stated: perfect foresight / price-taker; calendar aging not co-optimised; ideal BMS / uniform cell aging; C-rate neglected; asymmetric half-cycle assumption.
- Critical: segment-based SoC representation only approximates rainflow for monotone SoC paths within the horizon; cycles spanning horizon boundaries are lost (rolling application undercounts). Replacement-cost pricing (R) is itself a modelling choice (see he2018_intertemporal, xu2022_dynamicvaluation for opportunity-cost alternatives).

## 9. Relevance to my study
Default "market-compatible" degradation representation: a market-rule study can use the J-segment cost directly in MILP benchmarks and as a reward-shaping term in RL; the Table I protocol (no cost / constant cost / segmented, evaluated ex post with rainflow) is a minimal ablation to copy.

## 10. Lineage links
- Builds on: xu2018_degradationmodel; Laresgoiti et al. 2015 (stress function).
- Built upon by: shi2019_cycleagingpfp, xu2022_dynamicvaluation; CAISO/ISO-NE storage participation model discussions (Xu FERC 2020 tech conference slides); many RL bidding papers using segment cost (cross-ref RL stream).

## 11. Verification log
- OpenAlex (doi:10.1109/TPWRS.2017.2733339): title, 5 authors (UW; ISO New England), vol 33(2) pp. 2248–2259; online 2017, issue 2018.
- arXiv 1707.04567 full text read (equations, Table I, assumptions).
- Xu CV confirms citation.
- SJR: scimagojr.com sourceid 28825 → Q1 (2025, SJR 4.217).
