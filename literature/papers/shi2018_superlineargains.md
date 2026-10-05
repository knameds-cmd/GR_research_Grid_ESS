---
id: shi2018_superlineargains
title: "Using Battery Storage for Peak Shaving and Frequency Regulation: Joint Optimization for Superlinear Gains"
authors: ["Shi, Y.", "Xu, B.", "Wang, D.", "Zhang, B."]
year: 2018
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "33(3):2882-2894"
doi: "10.1109/TPWRS.2017.2749512"
quartile: "Q1 (SJR 2025, Energy Engineering and Power Technology; Electrical and Electronic Engineering)"
group: "Baosen Zhang (Univ. of Washington, EE) with Microsoft Research (Di Wang)"
lineage: "UW EE power/energy group. Shi = B. Zhang PhD student; Bolun Xu = D. Kirschen PhD student at UW (later Columbia). Companion to xu2018 'Optimal battery participation in frequency regulation markets' (TPWRS 2018) from the same UW group."
streams: [S2_stacking_cooptimization, S4_degradation_operation]
market_context: "PJM RegD capacity payment + US C&I tariff (energy + monthly demand charge); behind-the-meter"
method_class: "SP"
evidence_read: "full text (arXiv:1702.08065, https://arxiv.org/pdf/1702.08065)"
oa_link: "https://arxiv.org/abs/1702.08065"
---

## 1. Research question
Can one battery serve demand-charge peak shaving and fast frequency regulation (RegD) at the same time, and is the jointly optimised saving larger than the sum of the savings from each service on its own?

## 2. Setting & assumptions
- Price-taker. Energy, demand-charge and regulation prices known and fixed ($47/MWh, $12/kW-month, $50/MW-h regulation capacity). The only uncertainty is in load s(t) and the regulation signal r(t).
- Two time scales: the demand charge uses 15–30 min averaged load, settled monthly; the regulation signal arrives every 4 s (T = 4320 steps per 8 h).
- Asset: 1 MW behind-the-meter backup battery (LMO). Only 3 min of energy (out of 15 min) is used for grid services; the rest is kept as backup. SoC window [0.2, 0.8], N = 10,000 cycles.
- Market: regulation capacity C is paid per hour, with a mismatch penalty set so that the performance score stays at or above 80%.

## 3. Constraints that drove the model choice
Fast, nearly zero-mean RegD cycling makes cycle-count degradation awkward to model. The authors argue that for this chemistry and depth-of-discharge range, wear can be written as a linear cost on throughput, which keeps the problem convex. The real-time controller has to run with nothing more than an SoC measurement.

## 4. Model
- Objective: minimise $J = \lambda_{elec}\sum_t s(t) + \lambda_{peak}\max_t \bar s(t) + f(b) - R(C)$, where $f(b)\propto\lambda_b|b(t)|$ is linear wear ($\lambda_b \approx \$83$/MWh) and R is regulation revenue minus the mismatch penalty.
- Decisions: regulation capacity C and peak threshold U (both day-ahead, first stage), plus charge/discharge $b^{ch}(t), b^{dc}(t)$ and baseline y(t).
- Key constraint: $SoC_{min}\le [SoC_{ini}+\sum(b^{ch}\eta_c-b^{dc}/\eta_d)t_s]/E\le SoC_{max}$. The battery follows $y(t)+C\,r(t)$ while shaving net load above U.
- **Capacity split: fixed** day-ahead. C* and U* are held constant over the horizon. **Frequency-signal energy: scenario replay.** 365 historical daily PJM RegD signals are reduced to 10 scenarios by forward scenario reduction, inside a two-stage stochastic convex programme (CVX, about 10 min for an 8 h horizon).
- Real-time: a threshold policy (Algorithm 1) that uses only the current SoC.

## 5. Data & processing
- One year of PJM RegD signal at 2 s resolution.
- Load: Microsoft data centre (183 days, about 1 MW) and the UW EE/CSE building (365 days).
- Load forecasts by multiple linear regression (MAPE 3.7% and 2.3%).
- Daily out-of-sample evaluation over the data period.

## 6. Justification (why the authors argue the approach is valid)
The paper proves analytically that the joint problem can be superlinear: the regulation signal is roughly zero-mean, so the same headroom can absorb load peaks. The superlinear gain is then shown empirically on most days. Benchmarks are each service optimised alone and the arithmetic sum of the two.

## 7. Key results
- Data centre: joint optimisation saves 10.72% of the annual bill ($52.3k). The superlinear gain is 2.71% ($13.2k) beyond the sum of the single-service savings, on 151 of 183 days.
- UW building: 12.35% saving ($44.4k), superlinear gain 3.91%, on 362 of 365 days.
- Single example day: regulation alone gives 6.77%, peak shaving alone 1.76%, joint 11.24% (versus a sum of 8.53%).

## 8. Limitations (stated + your critical reading)
- Stated: the linear throughput wear model is valid only for some chemistries and DoD ranges.
- Prices are deterministic, and the split (C, U) is static within the day.
- The performance-score penalty is simplified.
- Critical reading: superlinearity depends on a zero-mean, energy-neutral signal (RegD with conditional neutrality). It may not carry over to droop-based FCR/DC products with sustained one-directional deviations, or to rules that require explicit energy reservation (for example the GB DC/DR/DM SoE requirements).

## 9. Relevance to my study
This is the cleanest analytic statement of why stacking can be more than additive. The formulation (first-stage capacity plus a scenario-replayed signal) can be reused as a baseline. It is also a direct counterpoint for testing whether SoE-management rules erase the superlinear gain.

## 10. Lineage links
- Builds on (reference list not itemised): PJM performance-based regulation literature and UW degradation work. Related archive ids: walawalkar2007_nyisoarbitrage (S1), xu2018_degradationmodel (S4).
- Built upon by (notable): not checked. Related: engels2020_fcrpeakshaving (the same service pair with FCR and chance constraints).

## 11. Verification log
- Crossref API (api.crossref.org/works/10.1109/TPWRS.2017.2749512): title, authors, vol 33, issue 3, pp. 2882–2894, May 2018. Confirmed.
- arXiv 1702.08065 full text read: affiliations, model, data and results.
- SJR (scimagojr.com, source id 28825): Q1 in 2025 in both categories.
- The lineage (Shi–Zhang, Xu–Kirschen) is from known UW advising relations and was not re-verified on a thesis page in this session.
