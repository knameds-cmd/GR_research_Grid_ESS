---
id: ye2020_drlstrategicbidding
title: "Deep Reinforcement Learning for Strategic Bidding in Electricity Markets"
authors: ["Ye, Y.", "Qiu, D.", "Sun, M.", "Papadaskalopoulos, D.", "Strbac, G."]
year: 2020
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "11(2):1343-1355"
doi: "10.1109/TSG.2019.2936142"
quartile: "Q1 (SJR 2020 and 2024/2025, Computer Science (miscellaneous); SJR 2024 = 4.608)"
group: "Goran Strbac and Dimitrios Papadaskalopoulos (Control & Power Group, Imperial College London)"
lineage: "Imperial Strbac/Papadaskalopoulos line on strategic bidding (bi-level/MPEC -> DRL). Ye and Qiu: Imperial-affiliated first/second authors who continue this line (e.g. Ye et al. multi-agent DRL local markets, TSG 2023; Qiu et al. MARL papers) - advisor relation consistent with co-authorship but not independently verified. Mingyang Sun: Imperial (later Zhejiang/Peking)."
streams: [S5_rl_learning]
market_context: "Stylised single-bus pool-based day-ahead energy market, 7 producers (1 strategic), UK-style GBP case values"
method_class: "RL/DRL"
evidence_read: "full text (Imperial Spiral accepted version: https://spiral.imperial.ac.uk/bitstreams/ae1b6575-53ad-49a0-90d7-c1de06a47884/download)"
oa_link: "http://hdl.handle.net/10044/1/82270"
---

## 1. Research question
Can DRL with continuous state/action spaces (DDPG + prioritised experience replay) model a strategic producer's bidding when market clearing is non-convex (unit commitment), where bi-level/MPEC methods cannot be applied directly and tabular RL suffers from discretisation?

## 2. Setting & assumptions
- Price-maker: the agent's bids change the clearing outcome. **Market clearing is explicitly simulated** (endogenous prices): lower level = MIP unit commitment with no-load, start-up/shut-down costs, minimum stable generation, min up/down, ramping; prices from the continuous re-solve with UC fixed.
- One strategic producer; six competitive producers bid true costs (stationary opponents); price-elastic stepwise demand bids; no network.
- Day-ahead, hourly, 24-h horizon; episode = 20 days.
- Not a storage paper: it is the reference "market-simulator-as-environment" DRL design in this stream.

## 3. Constraints that drove the model choice
Bi-level/MPEC requires a convex lower level (KKT); non-convex UC clearing breaks this. Tabular Q-learning/DQN need discretised actions (curse of dimensionality). DDPG handles continuous 24-dimensional bid multipliers and treats clearing as a black-box environment.

## 4. Model
- State: [u_{1:24}, g_{1:24}, lambda_{1:24}] (commitment, dispatch, prices of previous day; 72-d).
- Action: 24 bid multipliers k_h in [1, 2] applied to marginal cost blocks.
- Reward: asymmetric profit difference vs competitive profit: l_p=1.45 if above, l_n=1.05 if below (reward shaping).
- Algorithm: DDPG + rank-based PER (buffer 1e4, beta1 0.6, beta2 0.4); actor/critic 400-300-100 ReLU; softsign output; tau 0.001; lr actor 1e-4, critic 1e-3; batch 128; gamma 0.7; Gaussian exploration decaying exp(-0.001 t); 1000 episodes (converges ~250).

## 5. Data & processing
- Test system adapted from a literature case (7 generators, quadratic costs linearised to 5 blocks); stylised, no historical price data.
- **10 random seeds; mean and standard deviation reported.** No train/test split (environment is a deterministic simulator with fixed opponents).

## 6. Justification (why the authors argue the approach is valid)
In the convex case DDPG+PER matches MPEC (the exact bi-level optimum) to within 0.04%: a built-in optimality check. In the non-convex case it is compared with MPEC applied to the convexified problem, Q-learning, DQN and plain DDPG.

## 7. Key results
- Convex clearing: MPEC 847,367 GBP; DDPG+PER 847,048 (-0.04%); DQN 769,398 (-9.2%); Q-learning 710,458 (-16.2%).
- Non-convex clearing: MPEC (indirect) 418,736; DDPG+PER 588,572 (+40.6%); DQN 530,358; Q-learning 492,017.
- Seed dispersion at convergence (10 seeds): sigma = 6,526 (DDPG+PER), 9,901 (DQN), 14,299 (Q-learning) GBP.
- PER reaches DQN profit in ~150 vs ~300 episodes.

## 8. Limitations (stated + your critical reading)
- Stated: single strategic agent; opponents stationary; exogenous conditions fixed; no network; hyperparameter selection "challenging"; no optimality guarantees in non-convex case.
- "MPEC indirect" in the non-convex case is not an optimal benchmark, so +40.6% measures the failure of the convexified bi-level, not the gap to the true optimum.
- Reward shaping (l_p, l_n) and gamma = 0.7 are tuned choices that affect the learned strategy.

## 9. Relevance to my study
Gold-standard design pattern if RL is ever coupled to a market-clearing simulator: (a) validate against the exact bi-level optimum in a convex instance, (b) report multi-seed mean/sd. Its convex-case result also shows that where an exact optimisation exists, RL at best matches it - supporting optimisation-based attribution.

## 10. Lineage links
- Builds on: Ruiz & Conejo MPEC strategic bidding (bi-level); Lillicrap et al. DDPG; Schaul et al. PER.
- Built upon by (notable): Ye et al. 2023 TSG multi-agent DRL in local markets; Qiu et al. MARL works (Imperial); many strategic-bidding DRL papers (299 citations per OpenAlex, Oct 2026).

## 11. Verification log
- OpenAlex (doi:10.1109/TSG.2019.2936142): title, authors (Imperial; Ye also Fetch.AI), 11(2):1343-1355.
- Spiral record: issue date 2020-03-01, accepted version PDF read in full.
- SJR: scimagojr sid 19700170610 - Q1 2019-2025.
