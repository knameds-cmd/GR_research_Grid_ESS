---
id: xu2018_regdparticipation
title: "Optimal Battery Participation in Frequency Regulation Markets"
authors: ["Xu, B.", "Shi, Y.", "Kirschen, D.S.", "Zhang, B."]
year: 2018
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "33(6):6715-6725"
doi: "10.1109/TPWRS.2018.2846774"
quartile: "Q1 (SJR 2018, Electrical and Electronic Engineering; Energy Engineering and Power Technology)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Daniel Kirschen & Baosen Zhang, University of Washington EE"
lineage: "Bolun Xu = Kirschen PhD (UW, 2018; widely documented, not re-verified here); Yuanyuan Shi = Baosen Zhang student (UW). Companion to shi2019_cycleagingpfp and xu2018_cycleagingcost."
streams: [S6_ancillary_products]
market_context: "PJM RegD performance-based regulation (capability + mileage payment, performance score)"
method_class: "online threshold control policy with regret bound + bidding policy (SDP-like analytical)"
evidence_read: "full text (arXiv 1710.10514v2, https://arxiv.org/pdf/1710.10514v2)"
oa_link: "https://arxiv.org/abs/1710.10514"
---

## 1. Research question
How should a battery bid regulation capacity and control its SoC in PJM's performance-based regulation market to maximise market income minus cycle-ageing cost, while meeting the performance-score requirement?

## 2. Setting & assumptions
- PJM RegD: hourly settlement; payment = performance score × (capability price + mileage price × mileage) × capacity; minimum performance score 0.70; score = precision + correlation + delay (paper simplifies to precision); mileage ratio 3 used to unify prices.
- Price-taker; RegD signal assumed energy-zero-mean and stationary.
- Battery (case study): 10 MW / 3 MWh, η = 95% each way, SoC 10–95%, NMC cells; cycle stress Φ(u)=1.57e-3·u^2.03; 1,000 cycles at 80% DoD; replacement $300/kWh; 10-y shelf life.

## 3. Constraints that drove the model choice
Rainflow cycle-ageing cost is non-Markovian; signal is stochastic with fast (2-s) dispatch. Authors derive a threshold policy with a time-independent regret bound instead of solving a large stochastic program.

## 4. Model
- Π(C,λ,r,b) = P(Cr,b)·λC − A(b); P = 1 − scaled mean |response error|; A = rainflow ageing cost.
- Constraints: −B ≤ b_t ≤ B; SoC bounds; e_t − e_{t−1} = Mη[b_t]⁺ − M[−b_t]⁺/η; P ≥ ρ_min (chance constraint with confidence ξ).
- Control: Algorithm 1 — track running max/min SoC and cap the cycle depth at û = φ⁻¹((η²+1)π/(ηR)) (marginal ageing = marginal performance revenue). Theorem 1: regret bound independent of horizon T. Theorem 2: without performance constraint, optimal capacity = power rating.
- Bidding: Algorithm 2, inverse of C*(μ_λ) using empirical performance function of energy/capacity ratio γ.

## 5. Data & processing
PJM RegD signals 06/2013–05/2014 (policy calibration) and 03/2016–02/2017 (case study); PJM capability/performance clearing prices 03/2016–02/2017.

## 6. Justification
Regret bounds; simulation regret ≈ $0 vs $47.9–408.8 for a benchmark; one-year back-test.

## 7. Key results (03/2016–02/2017)
- Benchmark: income $1,472.9k, ageing $494.8k, profit $823.2k, life 26 months, score 0.96.
- Proposed ξ=50%: income $1,266.8k, ageing $326.3k, profit $940.5k (+14%), life 42 months, score 0.84.
- Proposed ξ=95%: profit $654.8k, life 69 months, score 0.99.
→ Explicit trade-off between performance score (a product rule) and ageing.

## 8. Limitations (stated + your critical reading)
Zero-mean, stationary signal (PJM's 2017 RegD redesign changed energy neutrality); performance metric simplified; price-taker, single battery; convex stress function required. Note the case-study energy/power ratio (0.3 h) reflects the short-duration batteries PJM RegD attracted.

## 9. Relevance to my study
Shows how a performance-score/mileage remuneration rule translates into an optimal cycle-depth threshold — the cleanest analytic link between US pay-for-performance rules and battery wear. Reusable as a rule-aware benchmark policy for an RL agent in a regulation product.

## 10. Lineage links
- Builds on: shi2019_cycleagingpfp; xu2018_cycleagingcost; FERC Order 755.
- Built upon by (notable): Kirschen/Xu group follow-ups on storage bidding (S3/S4 streams).

## 11. Verification log
- OpenAlex works/doi:10.1109/TPWRS.2018.2846774: title, 33(6):6715-6725, all authors UW EE.
- SJR sid 28825: IEEE TPWRS Q1 2018.
- Full text read via arXiv v2 (journal accepted version). Battery 10 MW/3 MWh as reported in arXiv case study.
