---
id: lohndorf2013_addp
title: "Optimizing Trading Decisions for Hydro Storage Systems Using Approximate Dual Dynamic Programming"
authors: ["Löhndorf, N.", "Wozabal, D.", "Minner, S."]
year: 2013
journal: "Operations Research"
volume_issue_pages: "61(4):810-823"
doi: "10.1287/opre.2013.1182"
quartile: "Q1 (SJR 2024, Operations Research, SJR 2.557; Q1 Computer Science Applications and Management Science & OR)"
group: "Löhndorf (WU Vienna) / Wozabal & Minner (TU Munich)"
lineage: "OR/stochastic-programming school (Vienna/Munich); same pair later writes lohndorf2023_coordination. Methodologically descends from SDDP (Pereira & Pinto 1991) and Powell-style ADP."
streams: [S3_bidding_uncertainty]
market_context: "EEX (German) day-ahead hourly auction with intraday as secondary market; Austrian Alpine pumped-hydro (2 reservoirs + downstream cascade); price-taker DA, price-setter intraday"
method_class: "SDP/DP (ADDP = SDDP cuts in reservoir state × ADP over exogenous Markov price state) + SP (intraday MIQP with bid curves)"
evidence_read: "full text (Optimization Online preprint 2011/12/3269, https://optimization-online.org/wp-content/uploads/2011/12/3269.pdf)"
oa_link: "https://optimization-online.org/2011/12/3269/"
---

## 1. Research question
How can a hydro storage operator with connected reservoirs make day-ahead bidding (bid-curve) decisions that are consistent with long-term (inter-day, yearly) storage value under price and inflow uncertainty?

## 2. Setting & assumptions
- Price-taker in DA; price-setter in intraday (intraday price response β); expected DA price assumed = expected intraday price.
- Information structure: bid curves for all 24 h submitted one day ahead knowing reservoir levels R_{t-1} and exogenous state S_t (weekday, temperature, wind, solar, inflow, gas price); 24 DA prices realise simultaneously; intraday resolves up to 45 min before delivery.
- Horizon T = 365 days × H = 24 h; two-level decomposition: intraday (within-day) stochastic MIQP with K price scenarios; interday MDP with post-decision value function over reservoir states.
- Asset: upper reservoir 84,941 (1000 m³), lower 83,000; turbine 592 MW (1,072 MW large variant), pump 600 MW (120/1,080 MW variants); head effects ignored; no flow delays.

## 3. Constraints that drove the model choice
- Full SDP infeasible: |S| = 282,211 exogenous states, 44.8 M transition probabilities, continuous multi-reservoir state.
- Binary pump/turbine and intraday quadratic price impact make intra-stage problem nonconvex → cannot apply SDDP directly; relax (β = 0, LP) to get valid cuts (upper bound), then use cuts inside the original MIQP.
- Bid curves must be non-anticipative: one curve per hour, fixed before prices.

## 4. Model
- Bid format: I price-volume pairs (ρ_{hi}, X_{hi}) with linear interpolation → monotone non-decreasing piecewise-linear bid curve per hour; default I = 3 breakpoints, price points chosen so each segment holds ≈ equal number of price scenarios.
- Intra-stage: stochastic MIQP over 24 h × K scenarios; dispatch = bid curve evaluated at realised price; intraday deviations with price impact.
- Inter-stage: post-decision value function \bar V_t(S_t, R_t) approximated by hyperplanes (SDDP cuts) per Markov state; slopes from duals of reservoir balance.
- ADDP: forward simulation of Markov states + backward cut generation on LP relaxation; cut pruning if improvement < ε (ε = 10⁴ saves ~12 % runtime).
- Convergence: Prop. 3 — for ε = 0 converges to optimal policy of the relaxed problem in finite steps; ε > 0 gives ≤ ε(T−1) loss.

## 5. Data & processing
- EEX spot prices 2009–2011; 18 years of inflow data (Austrian utility).
- Exogenous state: trend + stationary residual Markov chain via k-means (M = 30 clusters); gas price as GBM discretised by Kantorovich-distance minimisation (≤30 states/day).
- DA prices: 48 linear models (workday/weekend × 24 h), stepwise BIC; in-sample R² 65.81 % (intraday 45.07 %).
- Scenarios: Latin Hypercube Sampling, K = 20 price scenarios per state.
- Evaluation: out-of-sample simulation of the policy (lower bound) vs ADDP value (upper bound).

## 6. Justification
Upper bound (relaxation) vs simulated lower bound gap; comparison against deterministic rolling-horizon benchmark.

## 7. Key results
- Default system: expected profit €164.3 M (UB) vs simulated €162.4 M ± 2.1 M → gap 1.2 %; large-capacity variant 0.0 %; worst case 0.8 %.
- Runtime: 6.9 h (13 iterations) default; 38.8 h for 7-plant reservoir chain; ~2.0–2.2 M hyperplanes.
- Stochastic policy beats deterministic rolling horizon by +0.7 % to +8.5 % (larger gain for large power-to-energy capacity).

## 8. Limitations (stated + critical reading)
- Stated: relaxation ignores intraday price response and binaries (bound only); first-order Markov only; head effects ignored; price model fit moderate; no reserve/futures markets.
- Critical: DA bid curves restricted to 3 breakpoints; battery-scale storage (short duration, many cycles) would make the intra-day problem dominant and the inter-day value function nearly flat.

## 9. Relevance to my study
Best-documented template for "bid curve = stochastic intra-day problem + end-of-day value function". The equal-scenario-mass rule for bid price points and the UB/LB validation design are directly reusable for a battery DA bidding benchmark.

## 10. Lineage links
- Builds on: Pereira & Pinto (1991) SDDP; Powell ADP; Fleten & Kristoffersen (2007) hydro bidding (not in archive).
- Built upon by: lohndorf2023_coordination; finnah2022_dpid (ADP for DA+ID storage); Löhndorf & Shapiro (2019) MSPPy-type SDDP extensions (not in archive).

## 11. Verification log
- OpenAlex works/doi:10.1287/opre.2013.1182 → title, authors (WU Vienna; TU Munich ×2), 61(4):810-823, 2013; OA via mediaTUM node 1246396.
- Full text: Optimization Online 2011 preprint (pre-publication version; numbers may differ slightly from published version — flag).
- SJR: Operations Research id 22238, Q1 2023/2024.
