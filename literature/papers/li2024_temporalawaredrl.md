---
id: li2024_temporalawaredrl
title: "Temporal-Aware Deep Reinforcement Learning for Energy Storage Bidding in Energy and Contingency Reserve Markets"
authors: ["Li, J.", "Wang, C.", "Zhang, Y.", "Wang, H."]
year: 2024
journal: "IEEE Transactions on Energy Markets, Policy and Regulation"
volume_issue_pages: "2(3):392-406"
doi: "10.1109/TEMPR.2024.3372656"
quartile: "Q1 (SJR 2025: Economics & Econometrics; Energy (misc.); Management, Monitoring, Policy & Law; SJR 1.449). Journal indexed 2023-; earlier-year quartile not published by SJR."
group: "Hao Wang (Monash University, Dept. of Data Science & AI; ARC DECRA DE230100046)"
lineage: "Monash energy-AI group of Hao Wang; first author Jinhao Li (Monash DSAI) co-authors repeatedly with Wang (advisor-student relation plausible but not independently verified). Changlong Wang = Monash Civil Eng. (energy systems)."
streams: [S5_rl_learning]
market_context: "Australian NEM, 5-min spot + 6 contingency FCAS (fast/slow/delayed raise & lower), 5 regions, price-taker"
method_class: "RL/DRL"
evidence_read: "full text (arXiv 2402.19110v1, preprint version of the published paper)"
oa_link: "https://arxiv.org/abs/2402.19110"
---

## 1. Research question
Can a DRL agent with a transformer-based temporal feature extractor jointly bid a BESS into the NEM spot market and the contingency FCAS markets, and outperform predict-then-optimise baselines?

## 2. Setting & assumptions
- Price-taker; **exogenous historical NEM clearing prices** (spot + 6 contingency FCAS); no clearing simulation, no bid-stack.
- Contingency FCAS energy is only drawn when an (exogenous, data-derived) contingency indicator fires; deployment durations 6 s / 55 s / 4 min.
- 5-min dispatch intervals; daily episodes of 288 steps.
- BESS 2 MW / 10 MWh, eta_ch = eta_dch = 0.95, SoC 5-95%, FCAS max 1 MW, degradation 1 AUD/MWh discharged (subtracted ex post, not in step reward).

## 3. Constraints that drove the model choice
Authors argue that joint spot+FCAS bidding is a sequential decision under high-dimensional, volatile multi-market prices; P&O methods depend on forecast accuracy, while an MLP-only DRL cannot capture temporal patterns -> transformer encoder + SAC.

## 4. Model
- MDP: s_t = [SoC_{t-1}, rho_{t-1} (7 prices), f_{t-1} (64-d transformer feature over last L=32 intervals)].
- Action: binary charge/discharge flags + continuous shares for spot, fast, slow, delayed FCAS with sum <= 1 (enforced by an ancillary loss, weight 10).
- Reward: spot revenue + arbitrage "bonus" beta_S=10 times |rho - EMA(rho)| (reward shaping) + FCAS enablement revenues - penalty 50 on SoC violation (bids also clipped).
- Algorithm: SAC (policy/Q/V nets 2x512 ReLU, lr 3e-4 Adam, gamma 0.99, tau 0.01, learned temperature). Transformer: embed 64, 2 MHA layers x 8 heads, FFN 2048, global average pooling.

## 5. Data & processing
- NEM 2016, 5 regions (VIC, NSW, QLD, SA, TAS), 5-min resolution.
- **Chronological split**: first 10 months (300 days) train, last 2 months (60 days) test. Separate agent per region.
- Training 80.7 min on TITAN RTX.

## 6. Justification (why the authors argue the approach is valid)
Benchmarks: LP&O (LSTM forecast + MILP in Gurobi), TP&O (transformer forecast + MILP), MLP-DRL (SAC without encoder), and PIO (perfect-information optimisation). Data-size sensitivity (1 vs 10 months training).

## 7. Key results
- Joint-market test revenue (AUD, 60 days): VIC 35,686 vs TP&O 30,320 (+18%); NSW 25,948 vs 19,682 (+32%); QLD 46,703 vs 39,640 (+18%); SA 49,146 vs 41,165 (+19%); TAS 52,478 vs 44,558 (+18%).
- Transformer vs MLP-DRL in spot-only: +42-57%.
- **Gap to perfect-information bound (read from Fig. 6, approximate): about 30-37% below PIO jointly; 16-31% below in contingency FCAS; 32-37% in spot.**

## 8. Limitations (stated + your critical reading)
- Stated: price-taker; degradation approximated by discharge throughput; future work on emissions, degradation, new NEM products.
- **No seeds, no confidence bands, single run per region** - RL-vs-P&O margins of ~18% are not shown to exceed seed variance.
- Reward shaping (arbitrage bonus beta_S=10) means the learned objective is not the revenue objective; results depend on that tuning.
- 2016 data only; the 2023 FCAS changes (very-fast FCAS, end of regulation-energy causer-pays) are absent.
- P&O baselines are deterministic point-forecast MILPs, not stochastic/rolling MPC.

## 9. Relevance to my study
Direct template for a NEM energy+contingency FCAS RL environment and for how FCAS enablement revenue is modelled from historical prices. The ~30% gap to PIO and the lack of seed statistics are evidence for choosing optimisation-based counterfactuals for market-rule attribution.

## 10. Lineage links
- Builds on: Haarnoja et al. SAC (2018); Monash group's earlier NEM DRL work (Anwar et al., Li et al. Energy & AI 2023 - not archived).
- Built upon by (notable): Monash follow-ups on multi-market BESS bidding (not verified here).

## 11. Verification log
- OpenAlex (doi:10.1109/TEMPR.2024.3372656): title, authors order, 2(3):392-406, online 2024-03-05.
- Monash research portal: same bibliographic data, issue Sept 2024.
- SJR: scimagojr.com sid 21101343415 - Q1 2025 in 3 categories (SJR 1.449); coverage 2023-2026.
- Full text read: arXiv 2402.19110v1 (pre-publication version; published numbers may differ slightly).
