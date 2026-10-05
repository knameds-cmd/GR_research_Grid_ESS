---
id: he2018_intertemporal
title: "An intertemporal decision framework for electrochemical energy storage management"
authors: ["He, G.", "Chen, Q.", "Moutis, P.", "Kar, S.", "Whitacre, J. F."]
year: 2018
journal: "Nature Energy"
volume_issue_pages: "3(5):404-412"
doi: "10.1038/s41560-018-0129-9"
quartile: "Q1 (SJR 2025, Nature Energy, SJR 20.769; Q1 in all four categories since 2017)"
group: "Whitacre & Kar (Carnegie Mellon Univ.) with Qixin Chen (Tsinghua Univ.)"
lineage: "G. He: Tsinghua PhD (Kang/Chen group, cf. he2016_pbrcyclelife) -> CMU postdoc with Whitacre (affiliations on paper: CMU + Tsinghua). Follow-up: He, Ciez, Moutis, Kar, Whitacre 2020 Applied Energy 'The economic end of life of electrochemical energy storage'."
streams: [S4_degradation_operation, S1_foundations_value]
market_context: "CAISO 2016: day-ahead energy arbitrage and frequency regulation (capacity + mileage); price-taker"
method_class: "Lagrangian decomposition (life-cycle problem -> marginal cost of usage) + convex short-term scheduling; grid search over multiplier"
evidence_read: "full text (author PDF, https://www.cmu.edu/ceic/assets/docs/publications/published-papers/2017-and-2018/he-et-al-2018.pdf)"
oa_link: "https://www.cmu.edu/ceic/assets/docs/publications/published-papers/2017-and-2018/he-et-al-2018.pdf"
---

## 1. Research question
How should degradation be priced in day-to-day storage operation so as to maximise life-cycle (not daily) profit, and is the common practice of pricing degradation by capital/replacement cost (levelised cost of degradation, LCOD) appropriate?

## 2. Setting & assumptions
- Price-taker; perfect price knowledge over the life (sensitivity to bias studied); 50 MW / 200 MWh Li-ion, 90 % efficiency, EoL at 70 % capacity after 3000 full cycles (≈1.2 TWh throughput), calendar loss ≈ 0.5 %/yr, discount rate 7 %.
- Degradation assumed Markov (depends only on current state/decision) so it aggregates additively across periods.

## 3. Constraints that drove the model choice
Life-cycle profit maximisation over ~15 years is intractable as one problem; daily schedulers need a scalar "degradation price". Capital cost is sunk and should not drive operational decisions; the right price is the shadow price of the total degradation budget.

## 4. Model
- Life-cycle problem: max Σ_t δ_t B_t(d_t, λ_t) s.t. Σ_t d_t ≤ D (total degradation budget), d_t ≥ C_t (calendar floor).
- Degradation: cycle life N = N_0·DOD^k; per-period degradation d_t = 2E_max Σ n_DOD · DOD^k + C_t (throughput-equivalent plus calendar).
- Lagrangian: multiplier μ on the budget = life-cycle **marginal benefit of usage (MBU)** [$/MWh throughput]; discounted DMBU_t = μ/δ_t is the operating threshold in short-term scheduling (dispatch only when marginal revenue ≥ DMBU).
- **Average benefit of usage** ABU = LB_max / D, used for investment (compare with average capital cost of degradation).
- Algorithm: simulate short-term convex scheduling for a grid of μ, build life-cycle benefit curve, pick optimal μ; update DMBU quarterly/annually.

## 5. Data & processing
CAISO 2016 day-ahead energy prices; CAISO regulation capacity and mileage prices; real-time regulation mileage data; prices repeated/projected over life.

## 6. Justification
KKT optimality when short-term benefit is concave in degradation; comparison with LCOD-based degradation pricing; sensitivity to ±20 % degradation-model bias.

## 7. Key results
- Arbitrage only: optimal MBU ≈ $5/MWh throughput vs. LCOD ≈ $17–25/MWh; life-cycle revenue ≈ $8.3 M (MBU) vs. ≈ $1.9 M (LCOD) — LCOD pricing loses most of the value (paper's reported ~337 % gain).
- Arbitrage + regulation: optimal MBU ≈ $25/MWh, ABU ≈ $35/MWh, life-cycle revenue ≈ $42 M; LCOD loses ≥ 12 %.
- 20 % degradation-estimation bias costs little compared with ignoring degradation or using LCOD.
(Numbers as extracted from the author PDF; re-check tables before citing.)

## 8. Limitations (stated + your critical reading)
- Stated: perfect forecasts; Markov degradation (no path dependence); constant calendar aging (T, SoC fixed); market-revenue view only; grid search cost.
- Critical: degradation is essentially throughput-based with a DOD power law — no SoC/temperature dependence; optimal μ depends on the 15-year price path, which is the real uncertainty.

## 9. Relevance to my study
Key conceptual argument for any market-rule study: the degradation "cost" should be an opportunity cost (shadow price of the life budget) that is **endogenous to the market product set** — a new product (e.g., a fast reserve) changes μ. Provides a cheap outer loop (grid search over μ) wrappable around an RL or MILP bidder.

## 10. Lineage links
- Builds on: he2016_pbrcyclelife (same first author; cycle-life bidding); Lagrangian resource-budget ideas.
- Parallel/related: xu2022_dynamicvaluation (DP over SoH, same "opportunity value" idea); collath2023_lifetimeprofit (empirical tuning of aging cost via lifetime simulation).

## 11. Verification log
- Nature page (nature.com/articles/s41560-018-0129-9): authors, affiliations CMU + Tsinghua, vol 3 pp. 404–412, May 2018, DOI.
- Full text read from CMU CEIC author PDF; funding DOE grant DE-EE0007165.
- SJR: scimagojr.com sourceid 21100812579 → Q1 (2025, SJR 20.769).
- 2026-10-06 independent verifier: added missing issue number (5) to volume_issue_pages; OpenAlex gives Nature Energy 3(5):404-412, 2018 (https://api.openalex.org/works/doi:10.1038/s41560-018-0129-9). Title/authors/year/DOI confirmed.
