---
id: engels2020_fcrpeakshaving
title: "Optimal Combination of Frequency Control and Peak Shaving With Battery Storage Systems"
authors: ["Engels, J.", "Claessens, B.", "Deconinck, G."]
year: 2020
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "11(4):3270-3279"
doi: "10.1109/TSG.2019.2963098"
quartile: "Q1 (SJR 2025, Computer Science (misc.))"
quartile_basis: "pub-year; rule=pass; SJR 2020 Q1 for this journal recorded in cao2020_drlarbitragedegradation"
group: "Geert Deconinck, KU Leuven ELECTA / EnergyVille, with Centrica Business Solutions (B. Claessens)"
lineage: "KU Leuven/EnergyVille. Engels has a dual Centrica + KU Leuven/EnergyVille affiliation with Deconinck as senior academic author, which suggests an industrial PhD under Deconinck (not verified). Claessens is affiliated with Centrica."
streams: [S2_stacking_cooptimization, S6_ancillary_products]
market_context: "Continental Europe FCR (symmetric, ±200 mHz, daily auction) + industrial peak (capacity/demand) charge; German FCR price used"
method_class: "SDP/DP"
evidence_read: "full text (arXiv:1906.06907, https://arxiv.org/pdf/1906.06907)"
oa_link: "https://arxiv.org/abs/1906.06907"
---

## 1. Research question
How should a behind-the-meter battery at an industrial site split itself between daily FCR provision and monthly peak shaving? The frequency-driven SoC must stay safe, and the uncertain monthly peak must be handled optimally.

## 2. Setting & assumptions
- Price-taker with known FCR price (12 €/MW/h), peak charge (13,000 €/MW/month) and energy price (45 €/MWh).
- Uncertainties: frequency deviations (four years of CE data) and site consumption (scenarios).
- Daily FCR decision $r_d$ (daily auction, symmetric, must be available for the whole contracted period). The peak charge is on the monthly maximum 15-min average.
- Asset: 1 MW / 1 MWh batteries (two sites) with constant η.
- SoC recovery through a linear recharge controller that feeds back on past frequency deviations. This mirrors the "recharge set-point" allowance in FCR rules.

## 3. Constraints that drove the model choice
- The monthly demand charge couples days, so dynamic programming over days is needed with the observed peak as the state.
- FCR availability must hold with very high probability, so chance constraints are needed. The authors reformulate these robustly as SOCP using forward/backward deviation measures of the frequency signal.

## 4. Model
- Daily subproblem: choose $r_d$, recharge-policy matrix D and "virtual battery" limits for peak shaving. Chance constraints on energy and recharge power ($\epsilon = 5\times10^{-3}$) are made tractable by a robust SOC reformulation using $\sigma_f,\sigma_b$ estimated from frequency data.
- **Capacity split: dynamic at daily granularity.** FCR capacity varies by day. Peak shaving is confined to a separated "virtual battery" (residual power/energy) so it cannot undermine FCR delivery.
- **Frequency-signal energy: chance-constrained / distribution-robust envelope** derived from historical frequency statistics. Not an expected value and not scenario replay in the optimisation; replay is used for validation.
- Outer layer: DP over the month with a piecewise-linear convex value-function approximation in the current peak. SAA with a scenario-reduction cost tailored to peak statistics.
- Real-time: a rule-based peak-shaving controller (Algorithm 1).

## 5. Data & processing
- Four years of CE frequency data.
- Real consumption from a pumping station and a cold store.
- German FCR price level.
- Scenario reduction with a custom distance on scenario maxima, which cuts the SAA gap by about 50% for a given number of scenarios.

## 6. Justification (why the authors argue the approach is valid)
- Probabilistic feasibility guarantee from the robust reformulation of the chance constraints.
- Simulation over months, compared with single-service operation.
- Multi-site aggregation exploits non-coincident peaks.

## 7. Key results
Per month, for two 1 MW/1 MWh batteries:
- peak shaving only: 7.2 k€;
- FCR only: 13.1 k€, but the peak rises to 2.09 MW;
- combined: 14.4 k€ (about +10% over FCR only), keeping the peak at 1.96 MW with average FCR of 1.76 MW.

## 8. Limitations (stated + your critical reading)
- Stated: the rule-based peak controller is suboptimal; DP state grows with the number of sites; efficiency is handled approximately.
- Critical reading: the FCR price is fixed, so there is no market-price uncertainty. Daily FCR products (now 4-hour blocks in the CE FCR cooperation) would change the granularity. The 15/30-min LER rules are not modelled explicitly; feasibility is purely probabilistic.

## 9. Relevance to my study
- A rigorous template for translating frequency-signal statistics into SoE constraints (the chance-constraint route), as opposed to deterministic rule-based reservation. It allows comparing "TSO rule" with "statistically sufficient" reservation.
- Shows a DP layer handling inter-temporal coupling from monthly charges, analogous to monthly or weekly product commitments.

## 10. Lineage links
- Related: shi2018_superlineargains (the same service pair, US regulation; citation not verified). Builds on: the authors' earlier FCR chance-constraint work (cited in the paper; not separately verified); robust optimisation with forward/backward deviation measures.
- Built upon by (notable): not checked.

## 11. Verification log
- Crossref (api.crossref.org/works/10.1109/TSG.2019.2963098): title, authors, vol 11, issue 4, pp. 3270–3279, July 2020. Confirmed. The arXiv-listed date is earlier; the issue year 2020 is used.
- arXiv 1906.06907 full text read.
- SJR (id 19700170610): Q1 2025.
- Advisor tie inferred from affiliations; thesis not checked.
