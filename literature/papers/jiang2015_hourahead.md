---
id: jiang2015_hourahead
title: "Optimal Hour-Ahead Bidding in the Real-Time Electricity Market with Battery Storage Using Approximate Dynamic Programming"
authors: ["Jiang, D. R.", "Powell, W. B."]
year: 2015
journal: "INFORMS Journal on Computing"
volume_issue_pages: "27(3):525-543"
doi: "10.1287/ijoc.2015.0640"
quartile: "Q1 (SJR 2024, INFORMS J. on Computing, SJR 1.439; Q1 in CS Applications, Information Systems, Mgmt Science & OR, Software)"
quartile_basis: "latest-only; rule=unchecked; SJR 2015 (publication year) not checked — only later years"
group: "Powell (CASTLE Lab, ORFE, Princeton)"
lineage: "Both Princeton ORFE (OpenAlex). Jiang = Powell PhD student (Princeton); Monotone-ADP developed in Jiang & Powell (2015) Operations Research 'An approximate dynamic programming algorithm for monotone value functions'."
streams: [S3_bidding_uncertainty]
market_context: "NYISO real-time market (NYC zone), 5-min settlement, hourly bid submitted one hour ahead; price-taker 1 MW / 6 MWh battery"
method_class: "SDP/DP (Monotone-ADP)"
evidence_read: "full text (arXiv 1402.3575, https://arxiv.org/pdf/1402.3575)"
oa_link: "https://arxiv.org/abs/1402.3575"
---

## 1. Research question
How should a battery owner choose hour-ahead buy/sell price thresholds for real-time energy arbitrage when the battery's energy level at the start of the hour and the 5-min prices inside the hour are unknown at bid time?

## 2. Setting & assumptions
- Price-taker ("no price impact").
- Bid: a pair (b⁻, b⁺) placed at hour t governs interval (t, t+1]; within each of M = 12 five-minute settlements, discharge 1 MW if price > b⁺ … charge if price < b⁻ (sell bids below spot are dispatched; buy bids above spot charge). Bid = two-point step bid curve (implicit b⁻ ≤ b⁺).
- Information structure: bid made without knowing resource level at start of the hour (because previous hour's bid is still executing) and before the 12 intra-hour prices are revealed; previous bid b_{t-1} is part of state.
- State: resource level R_t, remaining cycle-life L_t, previous bid, price state.
- Battery: 1 MW, 6 MWh (case study); cycle-life counter with degradation factor β(l) (constant, step, linear, power forms).

## 3. Constraints that drove the model choice
- Exact backward DP intractable (case study 3.6 M post-decision states); distribution of prices unknown → distribution-free post-decision ADP trained on historical data.
- Proven monotonicity of transition in (r, b⁻, b⁺) and of value function → exploited by Monotone-ADP projection to accelerate learning.

## 4. Model
- MDP with hourly decision epochs, revenue maximisation; transition simulated through 12 settlements.
- Propositions 1–2: resource and lifetime transitions nondecreasing in r, l, b⁻, b⁺ → value function monotone.
- Algorithm: Monotone-ADP (lookup table with monotonicity-preserving projection) on post-decision state; convergent.
- Bid grid: benchmarks 30 values/dimension ($15–$85); NYISO case 15 grid points/dimension ($0–$150).

## 5. Data & processing
- Benchmarks: synthetic prices — sinusoidal seasonal + discrete pseudonormal noise (σ = 7); regime-switching variant (spike regime σ = 20, mean 15); 12–36 h horizons; 22,320–150,660 states.
- Case study: NYISO RT 5-min prices, NYC zone, 2011–2012; training on same month of prior year vs previous month; test on 2012.

## 6. Justification
Compared against exact backward DP on benchmark instances (optimality %) and against rule-based policies (two from arbitrage literature, one industry rule) on real data.

## 7. Key results
- Monotone-ADP 97.0 % vs 86.4 % (approx. value iteration) of optimal on problem A₁ after 25k iterations; 94.8 % vs 76.0 % on largest F₁; 98.2 % vs 60.8 % on F₂.
- 90–95 % optimality using 4–7 % of exact-DP compute time.
- NYISO 2012 annual revenue: ADP policy 1 $76,512.68; policy 2 $69,247.02; best rule-based $52,443.88 (ADP +46–68 %).

## 8. Limitations (stated + critical reading)
- Stated: arbitrage alone unlikely to be sustainable; model is hourly, impractical for multi-year horizons; price-taker.
- Critical: action space limited to ±1 MW/0 per 5-min; two-threshold bid is far simpler than multi-segment SoC-dependent bids (cf. zheng2022_asdp, CAISO multi-segment); no DA market.

## 9. Relevance to my study
Cleanest formalisation of the "bid submitted before SoC is known" information structure — directly relevant to GB/Nordic gate-closure lead times. Reusable as a structured-ADP benchmark against DRL bidders.

## 10. Lineage links
- Builds on: Powell (2011) ADP book; Jiang & Powell (2015, OR) Monotone-ADP.
- Built upon by: zheng2022_asdp (analytical SDP), RL bidding literature (other stream).

## 11. Verification log
- OpenAlex works/doi:10.1287/ijoc.2015.0640 → 27(3):525-543, 2015, Jiang & Powell (Princeton ORFE).
- Full text: arXiv 1402.3575 (preprint; numbers taken from arXiv PDF).
- SJR: INFORMS J. Computing id 25040, Q1 2015, 2023, 2024.
