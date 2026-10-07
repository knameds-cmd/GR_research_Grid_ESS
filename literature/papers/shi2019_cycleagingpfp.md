---
id: shi2019_cycleagingpfp
title: "Optimal Battery Control Under Cycle Aging Mechanisms in Pay for Performance Settings"
authors: ["Shi, Y.", "Xu, B.", "Tan, Y.", "Kirschen, D. S.", "Zhang, B."]
year: 2019
journal: "IEEE Transactions on Automatic Control"
volume_issue_pages: "64(6):2324-2339"
doi: "10.1109/TAC.2018.2867507"
quartile: "Q1 (SJR 2025, IEEE Trans. Automatic Control, SJR 3.929; Q1 Control & Systems Eng., EEE, CS Applications)"
quartile_basis: "latest-only; rule=unchecked; SJR 2019 (publication year) not checked — only later years"
group: "Baosen Zhang & Daniel Kirschen (Univ. of Washington, EE)"
lineage: "Shi, Xu, Tan = UW EE students (OpenAlex affiliations); Shi supervised by B. Zhang, Xu by Kirschen (advisor relations per UW groups; not separately verified here). Code: github.com/Yuanyuan-Shi/Cycle-based-Battery-Controller"
streams: [S4_degradation_operation, S6_ancillary_products]
market_context: "PJM pay-for-performance frequency regulation (RegD signal, 2-4 s); penalty prices for under/over-response"
method_class: "convex optimisation (subgradient, offline) + online threshold policy with worst-case gap bound"
evidence_read: "full text (arXiv 1709.05715, https://arxiv.org/pdf/1709.05715)"
oa_link: "https://arxiv.org/abs/1709.05715"
---

## 1. Research question
Is rainflow-based cycle aging cost tractable in an optimal control problem, and what is the optimal (offline and online) control of a battery following a pay-for-performance regulation signal when mismatch penalties are traded against cycle aging?

## 2. Setting & assumptions
- Battery follows regulation signal r_t; mismatch penalised at θ (under-response) and π (over-response) $/MWh; penalty prices fixed in advance.
- 1 MW / 0.25 MWh Li-ion, 95 % efficiencies, 3000 cycles at 80 % DoD, cell cost $300/kWh.
- Only cycle-depth aging; temperature assumed controlled; C-rate ignored.
- Offline (signal known) and online (causal) variants.

## 3. Constraints that drove the model choice
Rainflow maps a sequence in ℝ^T to an indeterminate-length set of cycle depths: no closed form, appears non-convex. Prior numerical approaches failed beyond ~4 h horizons. The authors need (i) a convexity result to justify optimisation and (ii) a cheap online policy since regulation signals arrive every 2–4 s.

## 4. Model
- Stress function Φ(u) = 5.24e-4 u^2.03 (Laresgoiti et al. 2015 lab data); cost = B·E·Σ Φ(cycle depths)/2 per half-cycle.
- SoC: x_t = x_{t−1} + (τη_c/E)c_t − (τ/(η_d E))d_t, x ≤ x_t ≤ x̄, 0 ≤ c_t, d_t ≤ P.
- Objective (offline): min τΣ[θ |η_c c_t − d_t/η_d − r_t|^+ + π |r_t − η_c c_t + d_t/η_d|^+] + rainflow cycle cost.
- Theorem 1: if Φ is convex, the rainflow cycle cost is convex in the control sequence → whole problem convex.
- Offline solver: subgradient method with analytical subgradients.
- Online policy (Alg. 1): follow r_t until tracked SoC band width reaches û = Φ'^{-1}[(πη_d + θ/η_c)/B]; then restrict response. Theorem 2–3: constant worst-case optimality gap independent of T; gap = 0 when πη_d = θ/η_c.

## 5. Data & processing
- Real PJM RegD signals (2/4-s resolution); simulation horizons of 100–200 steps for gap validation (100 random runs), 24-h for offline benchmarks.

## 6. Justification
Formal convexity proof; online gap bounds validated empirically (observed max gap matches theoretical ε in all 9 test cases); comparison to linear throughput cost model, greedy and MPC controllers.

## 7. Key results
- Rainflow-aware vs. linear throughput model at θ = π = 50 $/MWh: rainflow strategy earns ~$14.1/h whereas the linear model's optimal action is not to participate (zero) — linear cost over-penalises shallow cycles.
- Subgradient solver solves 24-h problems (~42 min) where generic numerical solvers time out beyond a few hours.
- Online policy vs. greedy/MPC under realistic PJM prices (≤ 50 $/MWh): > 30 % cost saving and 3–4× longer battery life.

## 8. Limitations (stated + your critical reading)
- Stated: cycle-depth only; penalty prices fixed; no online learning of degradation parameters.
- Critical: regulation capacity offer (how much MW to bid) is taken as given — it is a control, not a bidding, paper; PJM performance-score rules are abstracted to linear penalties.

## 9. Relevance to my study
Theoretical anchor for using rainflow cost directly (no linearisation) in convex/RL settings, and shows the market-rule dependence: the optimal cycle-depth threshold û depends explicitly on penalty prices — i.e., product penalty rules shape degradation-optimal behaviour.

## 10. Lineage links
- Builds on: xu2018_degradationmodel; Shi et al. 2017 "Optimal regulation response of batteries under cycle aging mechanisms" (CDC, conference — not archived).
- Built upon by: xu2022_dynamicvaluation; RL papers adopting rainflow cost (cross-ref S5).

## 11. Verification log
- OpenAlex (doi:10.1109/TAC.2018.2867507): title, authors (all UW EE), vol 64(6) pp. 2324–2339; online 2018, issue 2019.
- arXiv 1709.05715 full text read; funding: UW Clean Energy Institute.
- SJR: scimagojr.com sourceid 17339 → Q1 (2025, SJR 3.929).
