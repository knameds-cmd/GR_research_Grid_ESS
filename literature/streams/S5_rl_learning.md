# S5 — Reinforcement learning and learning-based bidding and operation of storage

## (a) Overview
This stream maps how **learning**, rather than explicit optimisation, has been used to bid and operate storage and flexible units in electricity markets. It also records what the papers themselves say about benchmarking and reproducibility. The papers fall into four strands.

1. **Model-free DRL arbitrage on historical prices, as a price-taker**: cao2020_drlarbitragedegradation, harrold2022_rainbowarbitrage, kwon2022_rlcycledegradation, li2024_temporalawaredrl, karimimadahi2024_distrlimbalance, jeong2023_deepbid and sage2025_drlbatterybenchmark. The environment is a replay of exogenous price series (GB DA, ERCOT/PJM, NEM spot + FCAS, Elia imbalance). Market clearing is never simulated. The agent's actions cannot change prices.
2. **RL against a replayed market mechanism**: bertrand2020_intradaystorage and boukas2021_intradaydrl. The environment is a historical EPEX continuous-intraday order book that is replayed event by event. This captures the pay-as-bid matching rule, but other traders do not react to the agent.
3. **RL against a market-clearing simulator** (price-maker or multi-agent): ye2020_drlstrategicbidding and ye2023_marllocalmarket. The environment is a unit-commitment or local-market clearing model, so prices are endogenous. These are the only papers in the stream where a market rule is part of the environment rather than of the data.
4. **Learning that keeps an optimisation model in the loop**: sang2022_dfpricearbitrage, baker2024_transferablebidder, bian2024_predictstoragebehavior and yi2025_perturbeddfl. This strand covers decision-focused / predict-then-optimise methods, learned value functions inside DP, and inverse optimisation through differentiable layers. Learning targets a forecast, a value function or a behaviour model. The decision itself still comes from an explicit, constraint-respecting optimisation.

Three patterns hold across the stream:
- Headline "RL beats optimisation" results almost always compare against a **weak or mis-specified optimisation baseline**. Typical baselines are a deterministic MILP on point forecasts, or a "perfect-foresight" LP with a simpler plant model than the one the RL agent is scored on.
- Where an exact optimum exists, RL at best matches it: DDPG reaches MPEC within 0.04% in ye2020.
- **Multi-seed reporting is the exception.**

The decision-focused and value-function papers come from the Xu (Columbia) / Shi (UCSD) and Tsinghua groups. They argue explicitly that RL is ill-suited to storage problems whose objectives are well defined (yi2025) and that it transfers poorly across zones (baker2024).

## (b) Chronological lineage of ideas
- **2015** jiang2015_hourahead (Jiang & Powell; archived by another stream): ADP for hour-ahead storage bidding. This is the approximate-DP ancestor of learned value functions.
- **2018** Wang & Zhang (Baosen Zhang, UW), "Energy storage arbitrage in real-time markets via reinforcement learning" (IEEE PESGM; *conference, excluded*). This tabular Q-learning arbitrage is the reference RL baseline later used by baker2024.
- **2020** ye2020_drlstrategicbidding (Imperial, Strbac/Papadaskalopoulos): DDPG+PER against a UC market-clearing simulator. Validated against MPEC on a convex instance and run on 10 seeds. This is the methodological high point of the stream.
- **2020** cao2020_drlarbitragedegradation (Keele/Oxford/Leeds, Fan & Morstyn): NoisyNet-D3QN with rainflow-based degradation in the reward and GB prices. Claims +58.5% over a point-forecast MILP.
- **2020** bertrand2020_intradaystorage (UCLouvain, Papavasiliou): REINFORCE-trained threshold policy on a replayed German CIM order book. Beats rolling intrinsic by 17.8% out of sample and reports 6 seeds.
- **2021** boukas2021_intradaydrl (Liège, Ernst/Cornélusse + ENGIE): fitted-Q with an LSTM on the CIM order book; the policy chooses between Trade and Idle on top of an optimisation step. Reports averages over 10 policies.
- **2022** sang2022_dfpricearbitrage (Tsinghua SIGS, Y. Xu/H. Sun): decision-focused price prediction with a surrogate regret. Reaches 97.3% of perfect-foresight profit in PJM DA.
- **2022** harrold2022_rainbowarbitrage (Keele): Rainbow DQN, run on a single seed, "beats" a perfect-foresight LP that uses a mis-specified plant model.
- **2022** kwon2022_rlcycledegradation (UT Austin, H. Zhu): state augmentation makes rainflow degradation Markov for DQN (ERCOT + PJM regulation signal).
- **2023** ye2023_marllocalmarket (Southeast Univ./Imperial): multi-agent DRL (MAAC+PER) for a local market with flexibility services, benchmarked against a system-centric optimum.
- **2023** jeong2023_deepbid (Sogang H. Kim, with **Seung Wan Kim**): DRL joint renewable bidding and battery control under deviation penalties. Code is public.
- **2024** baker2024_transferablebidder (Columbia, B. Xu): ConvLSTM predicts DP value-function derivatives, which are turned into bids. Reaches 75–88% of perfect foresight in NYISO RT and transfers to Queensland. Explicitly positioned against RL.
- **2024** bian2024_predictstoragebehavior (UCSD Shi + Columbia Xu): differentiable-optimisation inverse model of storage behaviour, intended for market monitoring and tariff design.
- **2024** li2024_temporalawaredrl (Monash, Hao Wang): SAC with a transformer encoder for NEM spot + contingency FCAS. Roughly 30–37% below perfect information; no seeds reported.
- **2024** karimimadahi2024_distrlimbalance (Ghent, Develder): distributional/risk-aware DRL for Belgian implicit balancing. No bound, interleaved split, single runs.
- **2025** sage2025_drlbatterybenchmark (McGill): design-choice benchmark. Action space, time encoding and stacking change rewards by 20–51%.
- **2025** yi2025_perturbeddfl (Columbia, B. Xu): perturbed decision-focused learning. Beats a tabular RL baseline by 50–72% and models strategic storage behaviour.

## (c) Research groups
| Group / PI | Institution | Papers in stream | Verified ties |
|---|---|---|---|
| Goran Strbac, Dimitrios Papadaskalopoulos | Imperial College London (Control & Power) | ye2020_drlstrategicbidding, ye2023_marllocalmarket | Ye: Imperial → Southeast Univ. (affiliations, OpenAlex). Advisor tie not independently verified |
| Anthony Papavasiliou | UCLouvain CORE | bertrand2020_intradaystorage | Bertrand at CORE as IEEE Student Member; supervision not verified |
| Damien Ernst, Bertrand Cornélusse | Univ. of Liège (Montefiore) + ENGIE | boukas2021_intradaydrl | Ernst = originator of fitted-Q iteration |
| Zhong Fan (with Thomas Morstyn, Kang Li) | Keele; Oxford (Morstyn); Leeds | cao2020_drlarbitragedegradation, harrold2022_rainbowarbitrage | Same Keele group across both papers |
| Hao Zhu | UT Austin ECE | kwon2022_rlcycledegradation | Kwon as Student Member; not verified |
| Hao Wang | Monash Data Science & AI (ARC DECRA) | li2024_temporalawaredrl | Not verified |
| Hongseok Kim; Seung Wan Kim | Sogang Univ.; Chungnam National Univ. (now KENTECH SEND Lab) | jeong2023_deepbid | Affiliations per OpenAlex; **direct lineage to the researcher's own lab** |
| Yinliang Xu, Hongbin Sun | Tsinghua SIGS / Tsinghua EE | sang2022_dfpricearbitrage | Not verified |
| Bolun Xu | Columbia EEE / Data Science Institute | baker2024_transferablebidder, yi2025_perturbeddfl, bian2024_predictstoragebehavior | **Verified** on bolunxu.github.io/group: Baker and Alghumayjan are PhD students, N. Zheng PhD 2024, M. Yi postdoc |
| Yuanyuan Shi | UC San Diego ECE | bian2024_predictstoragebehavior | Bian as Student Member at UCSD; not verified |
| Chris Develder (with Bert Claessens) | Ghent University – imec IDLab; BEEBOP | karimimadahi2024_distrlimbalance | Not verified |
| Yaoyao Fiona Zhao | McGill Mechanical Eng. | sage2025_drlbatterybenchmark | Not a core power-systems group; included as the only Q1 design-choice benchmark found |

## (d) Summary table
"PF" means perfect foresight / perfect information. "Seeds" means independent training runs reported with dispersion.

| id | year | algorithm | env / price model | baseline(s) | gap to PF bound | seeds reported? |
|---|---|---|---|---|---|---|
| ye2020_drlstrategicbidding | 2020 | DDPG + PER (vs Q-learning, DQN) | **Market-clearing simulator** (UC + continuous re-solve); 1 strategic + 6 truthful producers | MPEC (exact in convex case), Q-learning, DQN, DDPG | Convex case: −0.04% vs exact MPEC optimum. Non-convex: no exact bound | **Yes: 10 seeds, mean ± sd** |
| cao2020_drlarbitragedegradation | 2020 | NoisyNet Double Dueling DQN | Historical GB hourly prices; CNN-LSTM forecast in state | MILP on forecasts; DQN variants; RL with oracle forecasts | Not reported vs true PF LP. Oracle-forecast RL only +4.63% | No (single run) |
| bertrand2020_intradaystorage | 2020 | REINFORCE on threshold policy | **Replayed EPEX CIM order book** (liquidity taker, no reaction) | Rolling intrinsic; earlier threshold policy | Not reported. +17.8% vs RI | Partly: 6 runs "very similar" (supplement) |
| boukas2021_intradaydrl | 2021 | Fitted-Q iteration + LSTM, asynchronous actors | Replayed EPEX CIM order book | Rolling intrinsic | Not reported | Average of 10 policies (dispersion not retrieved) |
| sang2022_dfpricearbitrage | 2022 | Decision-focused predictor (surrogate regret + MSE), MILP downstream | Historical PJM DA hourly | MSE predictor, MLP, RF, oracle | **97.3% of PF** (29.86 vs 30.71 USD/day) | Linear model 100 runs; ResNet single run |
| harrold2022_rainbowarbitrage | 2022 | Rainbow DQN (vs DQN family, DDPG) | Historical GB DA prices + campus load/PV/wind | DQN variants, DDPG, PF LP with constant efficiencies | Undefined: Rainbow is **+15% above the "PF" LP** (LP plant model mis-specified) | No (single fixed seed) |
| kwon2022_rlcycledegradation | 2022 | DQN with switching-point state augmentation | Historical ERCOT prices + PJM regulation signal | Same DQN with linearised degradation | Not reported | No |
| jeong2023_deepbid | 2023 | DRL (details unverified) | Real solar/wind data, RT market with deviation penalties | Forecast-bidding, compensation strategies | Not reported (abstract) | Unknown (abstract only) |
| ye2023_marllocalmarket | 2023 | Multi-agent MAAC + PER | **LEM clearing, multi-agent** | System-centric optimum; prior MARL | Benchmark exists; gap unverified (abstract only) | Unknown |
| baker2024_transferablebidder | 2024 | DP + ConvLSTM value-function prediction (supervised) | Historical NYISO 5-min RT; AEMO QLD transfer | PF, tabular RL (Wang & Zhang), SDP, DP-MLP, commercial MPC (68.2%) | **75.7–88.0% of PF** (PR-10); 73–85% (HA-10) | No (multiple nets trained, best kept) |
| bian2024_predictstoragebehavior | 2024 | Differentiable optimisation (KKT / SCP + ICNN) | NYISO-driven synthetic agents; real UQ Powerpack | MLP, LSTM, threshold, Gurobi inverse optimisation | n/a (prediction task) | Yes for synthetic (10 runs, quantile bands) |
| li2024_temporalawaredrl | 2024 | SAC + transformer encoder | Historical NEM 5-min spot + 6 contingency FCAS (2016) | LSTM/transformer predict-and-optimise MILP, MLP-SAC, PF | **~30–37% below PF** (joint; from figure) | No |
| karimimadahi2024_distrlimbalance | 2024 | DQN, C51-DQN, SAC, distributional SAC (+VaR) | Historical Elia 1-min imbalance prices | Other DRL variants only | Not reported | No |
| sage2025_drlbatterybenchmark | 2025 | 4 DRL models incl. DQN (best) | Canada + Germany case studies | Oracle (definition unverified) | "RL can outperform oracles" (abstract): oracle not a true bound | Unknown (abstract only) |
| yi2025_perturbeddfl | 2025 | Perturbed decision-focused learning (Fenchel-Young) | Historical NYISO; real UQ Powerpack | LSTM-/MLP-MPC, tabular RL | Not reported. +50–72% vs RL | No |

## (e) Why RL is risky for causal / market-rule attribution
The study question is whether a change in market product rules causes a change in battery revenue or bidding. For that, the policy-generation method must hold everything fixed except the rule. The archived papers themselves show five ways RL breaks that requirement.

1. **Seed variance is of the same order as the effects we want to measure, and it is rarely reported.** Only ye2020 (10 seeds), bertrand2020 (6 runs, in the supplement), boukas2021 (10 policies averaged) and bian2024 (10 synthetic runs) report repeated training. In ye2020 the seed standard deviation is about 1.1% of mean profit for DDPG+PER, 1.9% for DQN and 2.9% for Q-learning. That is in a deterministic simulator with stationary opponents. The other papers compare single runs whose differences are often a few percent: DQN variants in harrold2022, SAC vs DSAC at 1,147.6 vs 1,148.5 EUR/day in karimimadahi2024, and the regional margins in li2024. Any "rule effect" estimated from one RL run per rule would mix the rule with seed noise.
2. **Implementation choices move results by 20–50%.** sage2025 reports that action discretisation, time encoding, observation stacking and the choice of algorithm change rewards by +20% to +51% on the same task. Many papers also shape the reward with hand-tuned terms: an arbitrage bonus β_S = 10 in li2024, asymmetric profit weights in ye2020, SoC-violation penalties in harrold2022 and li2024. Changing a market rule changes the reward landscape, so each rule would need re-tuning. The design then becomes a confounder that moves together with the treatment.
3. **No common, valid upper bound.** Without a perfect-foresight bound evaluated on the same plant and market model, a policy's sub-optimality cannot be separated from the rule's effect. harrold2022 and sage2025 report RL "beating" an oracle, which shows the benchmark was mis-specified. cao2020 reports +58.5% over a point-forecast MILP. li2024 is ~30–37% below perfect information. If RL sub-optimality varies across rule regimes, the RL gap itself becomes a rule-dependent bias. Optimisation-based counterfactuals have a known, rule-consistent bound by construction. Bounds are reported only by sang2022 (97%), baker2024 (75–88%) and ye2020's convex check.
4. **Environments that cannot represent the counterfactual.** Ten of the fifteen papers replay historical (or historical-data-driven) prices as a price-taker. Their environments cannot express how a rule change alters prices. The two order-book papers replay others' orders without reaction (bertrand2020 Simplification 6; boukas2021 Assumption 8). Only ye2020 and ye2023 simulate clearing, and those rely on stationary or co-learning opponents, which raises equilibrium-selection and non-stationarity issues (ye2020's stated future work).
5. **Split and selection practices that leak information.** boukas2021 samples test days at random, and karimimadahi2024 interleaves days within months, so neither is walk-forward. baker2024 chooses its final model by "highest arbitrage profit". cao2020 clips prices at the 15th and 85th percentiles. Each of these can inflate apparent performance by different amounts under different rule regimes.

**What the stream offers instead.** The strongest papers keep an explicit optimisation model (sang2022, baker2024, yi2025, bian2024) or validate RL against an exact optimum (ye2020). For attribution, this supports:
- (i) deterministic or stochastic optimisation with a perfect-foresight bound and rolling non-anticipative variants under each rule;
- (ii) learning used only for inputs (decision-focused forecasts, value-function approximations) and held fixed across rules;
- (iii) where behaviour must be learned from data, inverse/differentiable optimisation (bian2024, yi2025) rather than model-free RL.

## (f) Open gaps
- **No Q1 paper reports RL-vs-optimisation results across market-rule variants** (for example, the same BESS under different FCAS product definitions, settlement intervals or imbalance pricing) with multi-seed confidence intervals and a common perfect-foresight bound. This is the gap the current study fills with optimisation.
- Joint energy + multiple ancillary products with SoC-reservation rules (GB DC/DM/DR, Nordic FCR-D/FFR, NEM very-fast FCAS after 2023) are absent from the RL literature here. li2024 uses NEM 2016 contingency FCAS only.
- No standardised open environment with fixed data splits for storage bidding RL. jeong2023 releases code; most papers do not.
- Price-maker and multi-agent RL for storage fleets, with equilibrium checks, remains thin. ye2020 and ye2023 concern producers or prosumers, not utility-scale BESS fleets.
- Decision-focused learning under multi-product co-optimisation (energy + reserves with deliverability constraints) is unexplored. sang2022 and yi2025 cover energy arbitrage only.
- Inverse modelling of real BESS bidding from public bid data (e.g. NEM bid stacks, CAISO storage bids) for counterfactual re-clearing is only demonstrated on single batteries (bian2024, yi2025).

## (g) Dropped / not archived candidates
- **Wang & Zhang 2018** ("Energy storage arbitrage in real-time markets via reinforcement learning", IEEE PESGM): conference paper, excluded by rule. Cited as lineage only.
- **Anwar et al. (Monash) PPO joint energy + FCAS bidding**: no Q1 journal version verified; arXiv 2212.06551 (a NEM spot + FCAS BESS DRL preprint, authorship not verified) appears to be preprint-only.
- **Cardo-Miota, Beltrán, Pérez, Khadem & Bahloul 2025, Applied Energy 388:125561** (TD3 for PV+BESS in the Irish DAM + DS3; DOI 10.1016/j.apenergy.2025.125561 verified on OpenAlex): dropped. The groups (UJI / UCC-IERC-Tyndall) are not among the established groups in the selection criteria, and the full text was not accessible (ScienceDirect blocked). It is a candidate for later inclusion if the group criterion is relaxed.
- **Bolun Xu group "Energy Storage Price Arbitrage via Opportunity Value Function Prediction"** (arXiv 2211.07797) and **"A Decision-Focused Predict-then-Bid Framework for Strategic Energy Storage"** (arXiv 2505.01551): no Q1 journal version found (preprint / conference). Excluded.
- **Alghumayjan et al. 2024, "Energy storage arbitrage in two-settlement markets: a transformer-based approach", Electric Power Systems Research 235** (listed on Bolun Xu's CV): not archived because the DOI and SJR quartile were not verified within the session's API limits.
- **Qiu/Strbac MARL papers** (Imperial): not archived because they concern P2P/EV coordination rather than storage bidding, and no DOI was verified in-session.
- **"Comparison of machine learning and MPC methods for control of home battery storage systems in distribution grids"** (Applied Energy 2025, S030626192501195X): behind-the-meter home batteries, not market bidding; authors and group not verified. Not archived.
- **Comparative MILP/MPC/RL commercial battery dispatch** (arXiv 2609.14776): preprint only.
- **MDPI paper "Comparative Analysis of Optimal Control and RL Methods for Energy Storage Management Under Uncertainty"** (10.3390/esa2040014): MDPI, excluded.

## (h) Verification notes
- Bibliographic fields come from OpenAlex single-work DOI lookups and autocomplete (W-ids recorded in each file), plus publisher or repository pages (Spiral, ORA, Monash portal, Springer).
- Quartiles were checked on scimagojr.com for: IEEE TSG (sid 19700170610), IEEE TPWRS (28825), IEEE TEMPR (21101343415; ranked from 2025), Energy (29348), J. Energy Storage (21100400826) and Machine Learning (24775).
- Three files are abstract-only: jeong2023_deepbid, ye2023_marllocalmarket and sage2025_drlbatterybenchmark. boukas2021_intradaydrl lacks its quantitative results section.
- WebSearch quota and Crossref/Semantic Scholar rate limits were hit during this session. Advisor–student ties are therefore asserted only where a group page confirmed them (Bolun Xu group).
