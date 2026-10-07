---
id: karimimadahi2024_distrlimbalance
title: "Distributional reinforcement learning-based energy arbitrage strategies in imbalance settlement mechanism"
authors: ["Karimi Madahi, S. S.", "Claessens, B.", "Develder, C."]
year: 2024
journal: "Journal of Energy Storage"
volume_issue_pages: "104:114377"
doi: "10.1016/j.est.2024.114377"
quartile: "Q1 (SJR 2024: Electrical & Electronic Eng.; Energy Eng. & Power Technology; Renewable Energy, Sustainability & Env.; SJR 2024 = 1.760)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Chris Develder (IDLab, Ghent University - imec) with Bert Claessens (BEEBOP; IDLab)"
lineage: "Ghent IDLab Develder group (AI for energy / demand response RL); Claessens = long-standing industrial RL-for-flexibility researcher (VITO/REstore lineage, not checked). Karimi Madahi = Ghent IDLab doctoral researcher (co-authorship; supervision not independently verified)."
streams: [S5_rl_learning]
market_context: "Belgian (Elia) single-price imbalance settlement, 15-min ISP, real-time 1-min published prices; BESS reacting passively to imbalance price; price-taker"
method_class: "RL/DRL"
evidence_read: "full text (arXiv 2401.00015)"
oa_link: "https://arxiv.org/abs/2401.00015"
---

## 1. Research question
Can distributional (risk-aware) DRL learn profitable and risk-controllable battery strategies for implicit balancing - reacting to minute-by-minute imbalance-price information under Belgium's single-price settlement?

## 2. Setting & assumptions
- Price-taker; own imbalance does not affect the imbalance price (stated limitation); day-ahead schedule set to zero.
- **Exogenous historical Elia data (2022)**: non-validated 1-min imbalance prices used as the price forecast for the 15-min settlement.
- Agent acts every minute; 15-min settlement.
- BESS 1 MW / 2 MWh, eta 0.9 each way, limits 400 cycles/yr and 1.1 cycles/day (in constrained case).

## 3. Constraints that drove the model choice
Imbalance price is unknown until the end of the ISP and is heavy-tailed; risk-neutral expected-value RL ignores tail risk -> learn the return distribution and penalise VaR.

## 4. Model
- State: minute within ISP, ISP index, month, SoC, forecast imbalance price, daily cycles used.
- Action: {-P_max, 0, +P_max} (3 discrete actions) for DQN variants; SAC variants likewise in discrete form.
- Reward: r_t = -a_t * pi_imb_t.
- Algorithms: DQN, distributional DQN (categorical), SAC, distributional SAC; risk-sensitive DSAC with objective expected return + beta * VaR_0.1. gamma 0.9995; critic lr 1e-4, actor lr 2e-5; tau 0.1; buffer 1e6; batch 16,384; [256,128]; V in [-5000, 5000]; 50,000 episodes.

## 5. Data & processing
- Elia 2022. Split **within each month: days 1-20 train, 21-25 validation, 26-end test** (interleaved, not walk-forward - seasonal information leaks between sets).
- **Single run per configuration; no seeds or error bars.**

## 6. Justification (why the authors argue the approach is valid)
Comparison among the four DRL variants, with and without cycle constraint, and across risk-aversion levels beta.

## 7. Key results
- Risk-neutral, no cycle cap (EUR/day on test days): DQN 749.9, DDQN 877.5, SAC 1,147.6, DSAC 1,148.5 (+53% vs DQN), ~3.2-3.7 cycles/day.
- With 1.1 cycles/day cap: DQN 338.0, DDQN 397.2, SAC 504.9, DSAC 486.4.
- Risk aversion (DSAC, beta = 3): 518.9 EUR/day (-55%) with VaR improved from -71 to -24.7 EUR and ~1 cycle/day.
- **No perfect-foresight or MPC benchmark** -> gap to bound unknown.

## 8. Limitations (stated + your critical reading)
- Stated: zero DA schedule; no price impact; discrete actions; future: joint DA + imbalance, continuous actions.
- Single-seed comparisons of SAC vs DSAC (1,147.6 vs 1,148.5) are indistinguishable without variance estimates.
- Price-taker on imbalance price is particularly questionable for BESS fleets in Belgium (implicit balancing feeds back on the system imbalance).

## 9. Relevance to my study
Relevant for my Belgian imbalance-market DRO sizing work: shows the RL design used for implicit balancing and its blind spots (no bound, interleaved split, no seeds, no price feedback). A good foil for an optimisation/DRO-based approach whose outputs are attributable to settlement-rule parameters.

## 10. Lineage links
- Builds on: Bellemare et al. distributional RL (C51); Haarnoja SAC; Ghent IDLab RL-for-flexibility works.
- Built upon by (notable): Karimi Madahi, Claessens & Develder control-policy correction for RL arbitrage (conference, not archived).

## 11. Verification log
- OpenAlex autocomplete -> W4404096392; OpenAlex (doi:10.1016/j.est.2024.114377): J. Energy Storage 104, art. 114377, online 2024-11-06; affiliations IDLab Ghent-imec, BEEBOP.
- Full text: arXiv 2401.00015.
- SJR: scimagojr sid 21100400826 - Q1 2024 and 2025 in three categories.
