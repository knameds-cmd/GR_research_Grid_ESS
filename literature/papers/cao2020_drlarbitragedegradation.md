---
id: cao2020_drlarbitragedegradation
title: "Deep Reinforcement Learning-Based Energy Storage Arbitrage With Accurate Lithium-Ion Battery Degradation Model"
authors: ["Cao, J.", "Harrold, D.", "Fan, Z.", "Morstyn, T.", "Healey, D.", "Li, K."]
year: 2020
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "11(5):4513-4521"
doi: "10.1109/TSG.2020.2986333"
quartile: "Q1 (SJR 2020 and 2024/2025, Computer Science (miscellaneous); SJR 2024 = 4.608)"
group: "Keele University (Zhong Fan, School of Computing & Mathematics) with Thomas Morstyn (Oxford Eng. Science, now Oxford/Edinburgh) and Kang Li (Leeds)"
lineage: "Keele smart-energy group (Fan); Harrold is a Keele co-author who later first-authored harrold2022_rainbowarbitrage with Cao & Fan (supervision relation not independently verified). Morstyn = Oxford Energy & Power Group, later leading the Edinburgh/Oxford power-systems-economics line."
streams: [S5_rl_learning]
market_context: "GB wholesale (hourly) energy arbitrage, price-taker"
method_class: "RL/DRL"
evidence_read: "full text (Oxford ORA author accepted manuscript: https://ora.ox.ac.uk/objects/uuid:016dcecb-94ab-49a3-ad72-7d8bcbe336ca)"
oa_link: "https://ora.ox.ac.uk/objects/uuid:016dcecb-94ab-49a3-ad72-7d8bcbe336ca"
---

## 1. Research question
Can a model-free DRL agent fed with a 24-h price forecast learn a profitable price-taker arbitrage policy for a Li-ion battery while internalising a nonlinear efficiency model and an accurate (rainflow-based, calendar + cycling) degradation model that MILP formulations usually linearise or omit?

## 2. Setting & assumptions
- Price-taker; prices are **exogenous historical GB wholesale prices** (no market simulator, no price impact).
- Forecasts, not perfect foresight: a hybrid CNN-LSTM predicts the next 24 h from the last 168 h; the forecast vector is part of the state.
- Hourly steps; daily episodes; one-year test.
- Asset: five Li-ion units of 200 kWh; power discretised to {-100,-50,0,50,100} kW; SoC-dependent efficiency from an equivalent-circuit model (Voc, Rs, Rts, Rtl as functions of SoC).
- Degradation: semi-empirical calendar + cycling model with rainflow counting; mapped into the reward as a per-episode updated linear coefficient alpha_d.

## 3. Constraints that drove the model choice
Authors argue that (i) perfect-foresight price assumptions, (ii) constant efficiency and (iii) simple degradation models in MILP arbitrage are unrealistic; the nonlinear efficiency and the non-additive rainflow degradation are hard to embed in a MILP, which motivates a model-free learner.

## 4. Model
- MDP: state s_t = (c_t ... c_{t+23} forecast, SoC_t); action a in 5 discrete power levels; reward R_t = c_t P_t/P_max - alpha_d |P_t|/P_max; transition = SoC update with SoC-dependent efficiency.
- alpha_d,j = (E_s,j - E_c,j)/(sum |P|) * C_B, i.e. capacity fade from the rainflow model over the previous episode, monetised by battery cost per kWh; recomputed every episode.
- Algorithm: NoisyNet Double Dueling DQN ("NN-DDQN"); 3 hidden layers x 16 ReLU units; Adam, lr 2.5e-4, batch 32, target update every 10,000 steps, 12,000 training episodes, experience replay.
- Forecaster: Conv1D (kernel/stride 24, 128 filters) -> LSTM(32) -> Dense(24).

## 5. Data & processing
- GB wholesale hourly prices, 2015 (training) and 2016 (testing); a clean **chronological year split**, no validation year reported.
- Prices clipped at 15th/85th percentiles, scaled to [0,1] (note: clipping removes exactly the spikes that drive arbitrage value).
- Forecast MAE 4.686 (units as in paper).

## 6. Justification (why the authors argue the approach is valid)
Ablations vs vanilla DQN and Double Dueling DQN, vs a MILP using the same predicted prices, vs the same agent with perfect price forecasts, and vs ignoring degradation. Learning curves shown.

## 7. Key results
- NN-DDQN cumulative 2016 profit approx. 800k vs approx. 500k for MILP on forecast prices: **+58.51% vs MILP**.
- Giving the agent perfect price forecasts improves profit by only **4.63%** over NN-DDQN (this is NOT a perfect-foresight LP bound on true prices; it is the same RL agent with oracle forecasts).
- Omitting degradation in the reward lowers net profit by 5.13%.

## 8. Limitations (stated + your critical reading)
- Stated: none in a dedicated section; future work not discussed.
- **Single run, no seeds, no confidence bands**; the authors note episode rewards keep fluctuating because of residual exploration.
- The +58.5% over MILP compares against a deterministic MILP on point forecasts with (apparently) simplified efficiency/degradation; it does not show RL beating a well-tuned stochastic/rolling MPC, and the gap to a true perfect-foresight bound is not reported.
- 5-level discrete action, one market, one test year; percentile clipping distorts price distribution.

## 9. Relevance to my study
Canonical "RL beats MILP" claim that should be cited with care: the comparison baseline is weak (point-forecast MILP), no seed variance is reported. Useful as an example of how degradation-inclusive rewards are built and of why attribution to market rules would be confounded by run-to-run noise.

## 10. Lineage links
- Builds on: xu2018_cycleagingcost / xu2018_degradationmodel (rainflow degradation); Wang & Zhang 2018 (PESGM, conference).
- Built upon by (notable): harrold2022_rainbowarbitrage; kwon2022_rlcycledegradation (cycle-based degradation in RL).

## 11. Verification log
- OpenAlex (api.openalex.org/works/doi:10.1109/TSG.2020.2986333): title, author order, affiliations, 11(5):4513-4521, published 2020-04-08 online. Green OA (Keele, White Rose, ORA).
- Full text read: Oxford ORA AAM.
- SJR: scimagojr.com sid 19700170610 - Q1 every year 2019-2025 (Computer Science misc.), SJR 2024 4.608.
- Unverified: exact currency units of profit figures (read off figure).
