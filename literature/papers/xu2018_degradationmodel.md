---
id: xu2018_degradationmodel
title: "Modeling of Lithium-Ion Battery Degradation for Cell Life Assessment"
authors: ["Xu, B.", "Oudalov, A.", "Ulbig, A.", "Andersson, G.", "Kirschen, D. S."]
year: 2018
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "9(2):1131-1140"
doi: "10.1109/TSG.2016.2578950"
quartile: "Q1 (SJR 2025, IEEE Trans. Smart Grid, SJR 4.363; Q1 in all years 2011-2025 per scimagojr.com)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Kirschen (Univ. of Washington, REAL lab) with ABB Corporate Research (Oudalov) and ETH Zurich Power Systems Lab (Andersson, Ulbig)"
lineage: "Xu = UW EE PhD 2014-2018 (Xu CV); Kirschen senior author/supervisor (advisor relation inferred from co-authorship + UW group; CV does not name advisor). Oudalov (ABB) is a long-time BESS-economics author (Oudalov et al. 2007 sizing/PFC work)."
streams: [S4_degradation_operation]
market_context: "PJM frequency regulation (RegA/RegD-type signal) case study for life assessment; not a bidding model"
method_class: "semi-empirical aging model + rainflow cycle counting (simulation / assessment, no optimisation)"
evidence_read: "partial full text (equations + parameter table) via ResearchGate page extraction https://www.researchgate.net/publication/303890624 ; abstract via OpenAlex. Model equations below cross-checked against their re-use in xu2018_cycleagingcost (arXiv 1707.04567)."
oa_link: "none found (closed); ResearchGate copy"
---

## 1. Research question
How to build a cell-level Li-ion degradation model that (i) is grounded in degradation physics (SEI formation) and experimental stress-factor data and (ii) can assess life loss from irregular grid operating profiles (e.g., frequency regulation) where cycles are not uniform.

## 2. Setting & assumptions
- Assessment (forward simulation) of a given SoC/temperature/time profile; no decision-making.
- Cycles extracted by rainflow counting (full and half cycles), each with depth δ, mean SoC σ, temperature T.
- Cell temperature, SoC, DoD, time are the stress factors; C-rate is not in the LMO parameterisation shown.
- Case study: battery following PJM regulation signal.

## 3. Constraints that drove the model choice
Grid profiles are irregular; empirical cycle-life curves (cycles-to-failure at fixed DoD) cannot be applied directly. Need a model that (a) superposes calendar and cycle aging, (b) handles arbitrary cycles via rainflow, (c) reproduces the non-linear early-life capacity drop due to SEI formation.

## 4. Model
- Linearised degradation rate f_d = f_t(t, σ̄, T_c) + Σ_i n_i f_c(δ_i, σ_i, T_c,i)  (calendar + cycle, stress-factor products; cycle part summed over rainflow cycles, n_i = 0.5 for half cycles). [Composition structure NOT in the extracted text — written from the known structure of this model; confirm against the PDF.]
- Non-linear SEI-aware life loss: L = 1 − α_sei e^{−β_sei f_d} − (1 − α_sei) e^{−f_d}.
- Stress factors (LMO parameterisation):
  - DoD: S_δ(δ) = (k_δ1 δ^{k_δ2} + k_δ3)^{−1}  (fit R² = 0.993)
  - SoC: S_σ(σ) = exp(k_σ(σ − σ_ref))
  - Temperature: S_T(T) = exp(k_T (T − T_ref) T_ref / T)
  - Time: S_t(t) = k_t t
- Parameters (LMO cell): α_sei = 5.75e-2, β_sei = 121, k_δ1 = 1.40e5, k_δ2 = −5.01e-1, k_δ3 = −1.23e5, k_σ = 1.04, σ_ref = 0.5, k_T = 6.93e-2, T_ref = 25 °C, k_t = 4.14e-10 s⁻¹.
- No solver: rainflow + closed-form evaluation.

## 5. Data & processing
- Parameters fitted to published LMO cell aging data: calendar tests at 15–55 °C and 60–100 % SoC (1–5 yr), cycle-life tests at varying DoD (to > 9000 cycles), DST profiles (as reported on the extracted page).
- PJM regulation signal for case study (details not extracted).

## 6. Justification
Physics-motivated SEI two-exponential form reproduces fast initial fade then linear regime; stress-factor fits reported with high R²; rainflow is the standard fatigue tool for irregular cycles.

## 7. Key results
- Provides the canonical modular calendar+cycle+SEI model reused by the Kirschen/Xu lineage. Quantitative regulation-case life numbers not extracted (not verified here).

## 8. Limitations (stated + your critical reading)
- Parameterised for one LMO chemistry; NMC/LFP need refits (later papers swap in Φ(δ) = 5.24e-4 δ^2.03 for NMC).
- Rainflow is non-analytical → not directly usable inside an optimiser (motivates xu2018_cycleagingcost, shi2019_cycleagingpfp).
- Superposition of calendar and cycle aging and path independence are assumptions.
- Critical: C-rate stress absent in the shown parameter set; regulation signals are high-power/low-energy so this matters for short-duration BESS.

## 9. Relevance to my study
Reference "plant" model for ex-post life assessment of any RL/MILP bidding policy: run the dispatched SoC profile through rainflow + this model to report life loss consistently across market-rule scenarios, independent of the (simpler) cost proxy used inside the optimiser.

## 10. Lineage links
- Builds on: SEI growth theory; fatigue/rainflow (Matsuishi–Endo); Laresgoiti et al. 2015 JPS stress functions.
- Built upon by: xu2018_cycleagingcost, shi2019_cycleagingpfp, xu2022_dynamicvaluation; widely used in RL bidding papers with rainflow cost (cross-ref S5 RL stream).

## 11. Verification log
- OpenAlex (api.openalex.org/works/doi:10.1109/TSG.2016.2578950): title, authors, affiliations (UW, ABB Switzerland, ETH PSL), vol 9 issue 2 pp. 1131–1140, closed access. Online 2016, issue 2018.
- Xu CV (bolunxu.github.io/assets/files/Xu_CV.pdf): same citation listed; PhD UW 2014–2018.
- SJR: scimagojr.com sourceid 19700170610 → Q1 (2025, SJR 4.363).
- Equations/parameters: single source (ResearchGate extraction); not checked against publisher PDF — treat numerical parameters as "to re-check before reuse".
