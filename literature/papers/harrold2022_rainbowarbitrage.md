---
id: harrold2022_rainbowarbitrage
title: "Data-driven battery operation for energy arbitrage using rainbow deep reinforcement learning"
authors: ["Harrold, D. J. B.", "Cao, J.", "Fan, Z."]
year: 2022
journal: "Energy"
volume_issue_pages: "238:121958 (online 2021-09-08; volume dated Jan 2022)"
doi: "10.1016/j.energy.2021.121958"
quartile: "Q1 (SJR 2021/2022/2024/2025, incl. Energy Engineering & Power Technology and Electrical & Electronic Eng.; SJR 2022 = 1.989)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Zhong Fan (Keele University, School of Computing & Mathematics)"
lineage: "Keele group of Zhong Fan; Harrold first author (Keele) - follows cao2020_drlarbitragedegradation (same group; Cao later at Luxembourg Institute of Science and Technology). Supervision not independently verified."
streams: [S5_rl_learning]
market_context: "GB day-ahead wholesale prices as tariff for a campus microgrid (load + PV + wind) with 5 MWh battery; price-taker"
method_class: "RL/DRL"
evidence_read: "full text (arXiv 2106.06061v1, also Keele eprint 10153)"
oa_link: "https://eprints.keele.ac.uk/id/eprint/10153/1/2106.06061v1.pdf"
---

## 1. Research question
Does the full Rainbow DQN (all six DQN extensions) outperform simpler DQN variants, DDPG and an LP benchmark for battery energy arbitrage in a microgrid with renewables, when trained on limited real data?

## 2. Setting & assumptions
- Price-taker; exogenous historical GB day-ahead prices (cap 250 GBP/MWh), import = export price; Keele campus demand, PV (5 MW) and wind (2 MW) data.
- Hourly steps, weekly episodes (168 h).
- Battery 5 MWh (50 x 100 kWh Li-ion), +/-2 MW, nonlinear charge/discharge efficiency (after Morstyn et al.), self-discharge 0.1%/h; nonlinear transformer/inverter losses.
- Partial observability acknowledged.

## 3. Constraints that drove the model choice
Nonlinear efficiency and losses make an exact LP inaccurate; limited data (4 years) rules out the "infinite simulation" regime of typical RL benchmarks, motivating sample-efficient Rainbow.

## 4. Model
- State: 8 features (SoC, demand, price, PV, wind, hour, weekday, workday) or 12 with one-hour-ahead ANN forecasts of demand, PV, wind, price.
- Action: 5 or 9 discrete power levels in [-2, 2] MW.
- Reward: normalised energy-cost saving vs no-battery baseline minus penalty for SoC violations.
- Algorithm: Rainbow (Double, Dueling, PER alpha 0.7 beta 0.5, 2-step returns, Noisy nets sigma0 0.5, C51 with 51 atoms on [-10,10]); lr 1e-3, gamma 0.99, batch 64.

## 5. Data & processing
- 2014-2017 Keele data; 200 weekly episodes; **chronological split: weeks 1-100 train (also used to train forecast ANNs), weeks 101-200 evaluation.**
- Forecast MAPE: demand 5.01%, price 11.62%.
- **Single run per algorithm with a fixed TensorFlow/NumPy seed** ("for fairness and repeatability"); no variance reported.

## 6. Justification (why the authors argue the approach is valid)
Ablation across DQN, DDQN, D3QN, PER, multistep, NoisyNet, C51, Rainbow and DDPG under four configurations (5/9 actions x with/without forecasts), plus an LP with perfect price foresight but constant efficiencies (eta_ESS 0.95, eta_grid 0.92).

## 7. Key results
- Forecast + 9 actions: savings (kGBP over test) DQN 76.10, C51 83.30, DDPG 82.93, LP 79.54, **Rainbow 91.49 (+20.2% vs DQN)**.
- Basic config (5 actions, no forecasts): Rainbow 79.46 vs LP 79.54 (on par).
- **Rainbow exceeds the "perfect-foresight" LP by ~15%**: this is only possible because the LP's constant-efficiency model mis-specifies the evaluated nonlinear plant - the LP is not a true upper bound.

## 8. Limitations (stated + your critical reading)
- Stated: data scarcity; forecast accuracy; simplified LP benchmark; partial observability; future multi-agent extension.
- Single seed -> differences of a few % among DQN variants are within plausible seed noise (cf. ye2020_drlstrategicbidding reporting sd of 1-3% of mean).
- The perfect-foresight benchmark is not evaluated on the same plant model, so the "gap to PF" is undefined; a PF NLP/MINLP with the true efficiency curves would be the right bound.
- Behind-the-meter savings with import=export price is not wholesale market participation.

## 9. Relevance to my study
Cautionary example: an RL agent "beating perfect foresight" signals benchmark mis-specification, not superior intelligence. When I compare rules, the optimisation bound must be evaluated on the same asset model as the policy.

## 10. Lineage links
- Builds on: cao2020_drlarbitragedegradation; Hessel et al. Rainbow (AAAI 2018); Morstyn et al. battery efficiency modelling.
- Built upon by (notable): Keele multi-agent ESS follow-ups (not archived).

## 11. Verification log
- OpenAlex (doi:10.1016/j.energy.2021.121958): title, authors (Harrold, Cao, Fan), Energy 238, art. 121958, online 2021-09-08; OA copy Keele eprint 10153.
- Full text: arXiv 2106.06061v1.
- SJR: scimagojr sid 29348 (Energy, Elsevier) - Q1 in all categories 2021-2025.
- Note: arXiv lists Cao at Keele; OpenAlex lists Cao at LIST Luxembourg (published version affiliation).
