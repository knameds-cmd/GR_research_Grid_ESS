---
id: kwon2022_rlcycledegradation
title: "Reinforcement Learning-Based Optimal Battery Control Under Cycle-Based Degradation Cost"
authors: ["Kwon, K.-b.", "Zhu, H."]
year: 2022
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "13(6):4909-4917"
doi: "10.1109/TSG.2022.3180674"
quartile: "Q1 (SJR 2022 and 2024/2025, Computer Science (miscellaneous); SJR 2024 = 4.608)"
group: "Hao Zhu (Dept. of ECE, The University of Texas at Austin)"
lineage: "UT Austin Hao Zhu group (Zhu = UIUC/Minnesota lineage, G. Giannakis postdoc/PhD line - not checked here). Kwon listed as IEEE Student Member at UT Austin and sole co-author with Zhu (PhD-student relation consistent, not independently verified)."
streams: [S5_rl_learning]
market_context: "ERCOT 5-min energy prices + PJM regulation signal (RegD-type); price-taker; joint arbitrage + frequency regulation"
method_class: "RL/DRL"
evidence_read: "full text (arXiv 2108.02374)"
oa_link: "https://arxiv.org/abs/2108.02374"
---

## 1. Research question
How can rainflow cycle-based degradation - which depends on the whole SoC trajectory and is non-Markovian - be represented exactly as an instantaneous cost inside an MDP so that DQN can learn battery policies without the usual linearised throughput approximation?

## 2. Setting & assumptions
- Price-taker; exogenous historical ERCOT prices and PJM regulation signals (no market clearing, no capacity payment modelled - regulation enters as a tracking penalty delta|f_t - b_t|).
- 5-min steps for prices; regulation signal downsampled from 2 s to 10 s for training.
- Battery 200 kWh, 120 kW, min SoC 10%; DoD stress Phi(d) = alpha_d exp(beta d), alpha_d 4.5e-3, beta 1.3.
- Price and regulation processes treated as Markov (short memory).

## 3. Constraints that drove the model choice
Rainflow counting needs the full trajectory; existing RL work linearises it (cost proportional to |b_t|, cf. cao2020_drlarbitragedegradation). Authors augment the state with the last three switching points so that the incremental cycle cost becomes Markov; Proposition 1 shows equivalence with the original rainflow cost.

## 4. Model
- State s_t = [p_t, f_t, c_t, c_t^(0), c_t^(1), c_t^(2)].
- Action: 11 discrete normalised power levels {-1, -0.8, ..., 1}.
- Cost: h = p_t b_t + delta |f_t - b_t| + [alpha_d exp(beta|c_t + b_t - c^(2)|) - alpha_d exp(beta|c_t - c^(2)|)]; reward = -h; gamma = 1 (finite horizon).
- Switching-point updates follow rainflow cases (NR_a, NR_b, RA).
- DQN with replay and target network; 2 hidden layers [128, 32] ReLU; Adam lr 1e-3; batch 256; epsilon-greedy with decay; 2,000 episodes.

## 5. Data & processing
- Training on 7 daily profiles; testing on 60 days (43,200 steps). Chronology of train vs test not explicit.
- **Single training run; no seeds or confidence bands**; test variability shown only across test days.

## 6. Justification (why the authors argue the approach is valid)
Proposition 1 (exact equivalence of the augmented-state instantaneous cost to rainflow); comparison of cycle-based (CD) vs linearised (LD) DQN policies at two degradation weights.

## 7. Key results
- CD beats LD on 73.33% (alpha_d) and 81.67% (2 alpha_d) of test days; mean reward gain +84.45 and +176.51 (units as reported), with min differences of -97 and -199 (CD worse on some days).
- Lower secondary aging stresses: high C-rate stress -39% / -20%; SoC stress -23% / -41%.
- **No comparison with an optimisation bound (e.g. MILP with rainflow linearisation or perfect-foresight DP).**

## 8. Limitations (stated + your critical reading)
- Stated: Markov price assumption, FR downsampling, DoD-only aging, no network, single battery; future: peak shaving, network constraints, continuous actions.
- Only RL-vs-RL comparison; absolute optimality unknown. Seven training days is a very small sample for 5-min price dynamics.
- Regulation modelled as tracking penalty without capacity revenue, so the market-product economics are not represented.

## 9. Relevance to my study
Clean statement of how to make path-dependent degradation Markov (state augmentation) - the same trick is relevant to DP/SDP formulations. Illustrates the stream's typical evaluation gap (no PF bound, single seed).

## 10. Lineage links
- Builds on: xu2018_cycleagingcost (rainflow cycle-aging cost in market operation); cao2020_drlarbitragedegradation (linearised degradation in DRL).
- Built upon by (notable): later RL-with-degradation papers (not archived).

## 11. Verification log
- OpenAlex (doi:10.1109/TSG.2022.3180674): authors Kwon & Zhu (UT Austin), 13(6):4909-4917, online 2022-06-07; 37 citations.
- OpenAlex autocomplete links arXiv version 2108.02374 (read in full).
- SJR: scimagojr sid 19700170610 - Q1 2019-2025.
