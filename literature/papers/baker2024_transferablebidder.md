---
id: baker2024_transferablebidder
title: "Transferable Energy Storage Bidder"
authors: ["Baker, Y.", "Zheng, N.", "Xu, B."]
year: 2024
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "39(2):4117-4126 (online 2023-05-29)"
doi: "10.1109/TPWRS.2023.3280841"
quartile: "Q1 (SJR 2019-2025, Electrical & Electronic Eng. and Energy Eng. & Power Technology; SJR 2024 = 3.629)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Bolun Xu (Columbia University, Earth & Environmental Engineering)"
lineage: "Columbia Xu group (Xu = UW PhD 2018, Kirschen group). Baker = current PhD student and Ningkun (Nik) Zheng = PhD graduate 2024, both listed on bolunxu.github.io/group (verified)."
streams: [S5_rl_learning]
market_context: "Real-time wholesale arbitrage: NYISO 5-min RT prices (NYC, LONGIL, NORTH, WEST) with DA prices as features; transfer to AEMO Queensland; price-taker"
method_class: "SDP/DP"
evidence_read: "full text (arXiv 2301.01233v2, accepted version)"
oa_link: "https://arxiv.org/abs/2301.01233"
---

## 1. Research question
Can a storage bidder that combines dynamic programming with a neural network that predicts the opportunity value (marginal value of stored energy) bid near-optimally in real-time markets, train in minutes, and transfer across price zones with little data - addressing the poor transferability of RL?

## 2. Setting & assumptions
- Price-taker; historical prices (market clearing evaluated against realised RT prices; no clearing simulator).
- 5-min RT; hour-ahead bidding (HA) and price-response (PR) modes; single- and 10-segment SoC-dependent bids.
- Storage durations 2, 4, 12 h; round-trip efficiency 90% (100% in the RL comparison); marginal discharge cost 10 USD/MWh.

## 3. Constraints that drove the model choice
"A common disadvantage of RL-based approaches is transferability, as the model must undergo time-consuming training to be adapted to a new price zone or market environment." Authors keep the model-based structure (DP-derived value function = interpretable bid curve) and learn only the value-function mapping.

## 4. Model
- Training targets: derivatives q_t(e) of the value function obtained by deterministic DP on historical price paths (hindsight-optimal opportunity values).
- Predictor: ConvLSTM (3 time-distributed Conv+MaxPool, 2 BiLSTM+dropout, Dense) mapping lagged RT (36 x 5-min) and DA (24 h) prices to q_t; MSE loss; lr 1e-3; 100 epochs (25 for transfer); early stopping.
- Bids: discharge bid = c + q/eta; charge bid = eta q (averaged across SoC segments).
- Transfer learning: pre-train on NYC, freeze all but the output layer, re-train on the target zone.

## 5. Data & processing
- NYISO 2017-2018 training, **2019 test (chronological)**; Queensland: 2019 train, H1-2021 test (2020 skipped for COVID).
- "Multiple networks were trained for each case"; the model with most consistent low validation error retained, then **"the best model was chosen by the highest arbitrage profit"** (selection procedure could leak test performance - unclear from text).
- Training < 6 min including DP target generation.

## 6. Justification (why the authors argue the approach is valid)
Benchmarks: perfect foresight (upper bound), the Wang & Zhang (2018) tabular RL arbitrage method (11 actions, 1000 price states, 121 SoC states; needs eta = 100%; >1 h training), SDP with DA updates (Zheng et al. TPWRS 2022), and DP-MLP.

## 7. Key results
- PR-10, 2019 NYISO: **75.7-88.0% of perfect-foresight profit** (e.g. WEST 2 h 87.97%, NYC 12 h 75.67%); HA-10: 73.2-84.6%.
- Outperforms the RL benchmark particularly in capturing low-frequency price spikes (qualitative/figure).
- Queensland transfer (HA-1, 2 h): with 3 days of target data 82.8% (transfer) vs 48.2% (scratch); with 1 year 85.4% vs 83.9%. ~80% vs a commercial MPC reference of 68.2%.

## 8. Limitations (stated + your critical reading)
- Stated: prediction saturates on anomalous (spike) data; for 12-h storage opportunity value prediction may be ineffective; ConvLSTM training "volatile and initialization-sensitive".
- No multi-seed statistics; model selection by profit.
- Price-taker; RT only; no ancillary services.

## 9. Relevance to my study
Strong example of a learning method that keeps the optimisation structure (value function -> bid curve) - the output is a market bid that could be re-cleared under alternative rules. Its % of PF numbers (75-88%) give a realistic non-anticipative benchmark for RT arbitrage; and its explicit argument against RL transferability supports the methodological choice.

## 10. Lineage links
- Builds on: zheng2022_asdp (Zheng, Jaworski & Xu, analytical SDP, TPWRS 2022); jiang2015_hourahead (ADP hour-ahead bidding); Wang & Zhang 2018 RL arbitrage (PESGM, conference).
- Built upon by (notable): Xu group's decision-focused predict-then-bid and transformer two-settlement works (Alghumayjan et al. EPSR 2024; Yi et al. TSG 2025).

## 11. Verification log
- OpenAlex autocomplete -> W4378697249; OpenAlex (doi:10.1109/TPWRS.2023.3280841): 39(2):4117-4126, online 2023-05-29, Columbia affiliations.
- Full text: arXiv 2301.01233v2.
- Group membership: bolunxu.github.io/group (Baker current PhD; Zheng PhD 2024).
- SJR: scimagojr sid 28825 - Q1 2019-2025.
