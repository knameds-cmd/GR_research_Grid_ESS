---
id: zheng2022_asdp
title: "Arbitraging Variable Efficiency Energy Storage Using Analytical Stochastic Dynamic Programming"
authors: ["Zheng, N.", "Jaworski, J.", "Xu, B."]
year: 2022
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "37(6):4785-4795"
doi: "10.1109/TPWRS.2022.3154353"
quartile: "Q1 (SJR 2024, IEEE Trans. Power Systems, SJR 3.629; Q1 Electrical & Electronic Eng. and Energy Eng. & Power Tech.)"
quartile_basis: "pub-year; rule=pass; SJR 2022 Q1 for this journal recorded in baker2024_transferablebidder"
group: "Bolun Xu (Columbia University)"
lineage: "All Columbia (OpenAlex). Xu = Kirschen PhD (UW 2018) → Columbia; Zheng = Xu PhD student (Zheng's site lists joint papers). Successor work: baker2024_transferablebidder (filed by S5 stream)."
streams: [S3_bidding_uncertainty]
market_context: "NYISO real-time 5-min energy, zones NYC, LONGIL, NORTH, WEST; price-taker; price-response (observe price then act)"
method_class: "SDP/DP (analytical SDP with piecewise-linear value function, Markov price model)"
evidence_read: "full text (arXiv 2108.06000, https://arxiv.org/pdf/2108.06000 and ar5iv HTML)"
oa_link: "https://arxiv.org/abs/2108.06000"
---

## 1. Research question
Can real-time storage arbitrage with SoC-dependent (variable) efficiency and degradation cost be solved by stochastic dynamic programming fast enough for edge deployment, and how much of perfect-foresight profit does it capture?

## 2. Setting & assumptions
- Price-taker; information structure: storage updates control for period t after observing RT price λ_t (announced before dispatch) — i.e., price-response, not ex-ante bidding.
- 5-min resolution, 288 stages/day; energy normalised 1 MWh; power-to-energy 1.0, 0.5, 0.25.
- Efficiency: constant 90 % one-way, or SoC-dependent (70/80/90 % segments), modelled as affine in starting SoC; marginal discharge (degradation) cost c ∈ {0, 10, 30, 50} $/MWh.

## 3. Constraints that drove the model choice
- Need for sub-second computation (edge controllers) ⇒ avoid state/control discretisation of standard SDP.
- Variable efficiency breaks LP convexity ⇒ fix efficiency per stage based on starting SoC to keep each stage problem convex and analytically solvable.
- RT price serial dependence ⇒ first-order Markov price model rather than i.i.d. scenarios.

## 4. Model
- Recursion: Q_{t−1,i}(e_{t−1}) = max_{p,b} π_{t,i}(p_t − b_t) − c p_t + V_{t,i}(e_t), with V_t = Σ_j ρ_{ij,t} Q_{t,j}.
- Value function piecewise-linear in SoC; KKT of single-stage problem gives closed-form derivative update with five cases (full charge, partial charge, idle, partial discharge, full discharge).
- Policy: on observing λ_t, locate price node, compare λ_t with marginal value q_t(e) scaled by efficiency → charge/discharge thresholds (implicitly an SoC-dependent bid curve).

## 5. Data & processing
- Price nodes: 22 per stage for RTP model (clustered ranges, explicit spike/negative handling); 12 for DA-RT bias model.
- Transition probabilities ρ_{ij,h} by counting hourly transitions in historical data (hourly transition matrices).
- Training: data before 2019 (sensitivity with 2016–2018, 2017–2018, 2018); test: full year 2019.

## 6. Justification
Benchmarks: BEN-PF (perfect foresight) and BEN-DA (MPC with DA price predictions); variants of SDP (stage-dependent, seasonal, weekly).

## 7. Key results
- Profit ratio vs perfect foresight: NYC 59.9–90.8 %, LONGIL 56.0–72.7 %, NORTH 58.4–90.2 %, WEST 67.1–86.7 %; > 80 % in 3 of 4 zones for ≥ 2-h batteries with realistic degradation cost.
- One operating day solved in < 1 s on a PC.
- Stage-wise Markov dependence improves performance significantly vs naive models.

## 8. Limitations (stated + critical reading)
- Stated: rare price regimes poorly estimated; hourly transition matrices smooth intra-hour dynamics; Markov assumption.
- Critical: price-response (act after price) is an optimistic information structure — not valid for markets with ex-ante bid submission (DA auctions, GB BM bids at gate closure); baker2024_transferablebidder reports 3–7 % lower profit ratio under hour-ahead bidding vs price response (arXiv 2301.01233).

## 9. Relevance to my study
Strong non-RL baseline for battery arbitrage; value-function derivative q_t(e) is the natural object to map into multi-segment price-quantity bids, and a principled comparator for DRL bidders in my CIRED/market-design work.

## 10. Lineage links
- Builds on: jiang2015_hourahead (ADP), wang2017_lookahead (Xu co-author; terminal SoC value), Xu's cycle-aging cost work (xu2018_cycleagingcost).
- Built upon by: baker2024_transferablebidder; Xu-group two-settlement and market-power-bound papers. Related: xu2022_dynamicvaluation (same piecewise-linear SDP machinery over state of health).

## 11. Verification log
- OpenAlex works/doi:10.1109/TPWRS.2022.3154353 → 37(6):4785-4795, 2022, Columbia ×3; confirmed by Zheng's publication page and citation in arXiv 2404.17683.
- Full text: arXiv 2108.06000 (v6).
- SJR: IEEE TPWRS Q1 2023/2024.
