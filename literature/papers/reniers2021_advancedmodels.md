---
id: reniers2021_advancedmodels
title: "Unlocking extra value from grid batteries using advanced models"
authors: ["Reniers, J. M.", "Mulder, G.", "Howey, D. A."]
year: 2021
journal: "Journal of Power Sources"
volume_issue_pages: "487:229355"
doi: "10.1016/j.jpowsour.2020.229355"
quartile: "Q1 (SJR 2025, J. Power Sources, SJR 1.598; Q1 EEE, Energy Eng. & Power Tech., Phys. & Theor. Chem., Renewable Energy)"
quartile_basis: "latest-only; rule=unchecked; SJR 2021 (publication year) not checked — only later years"
group: "David Howey (Univ. of Oxford, Battery Intelligence Lab; Faraday Institution) with VITO/EnergyVille (Mulder)"
lineage: "Reniers = Oxford DPhil 2019 (thesis cited as ref. [27] in the paper) supervised by Howey; co-funded by VITO/EIT InnoEnergy. Precursor: Reniers, Mulder, Ober-Blöbaum, Howey 2018 J. Power Sources 379 (optimal control with physics-based degradation, simulation only)."
streams: [S4_degradation_operation]
market_context: "Belgian day-ahead market 2014, hourly; energy arbitrage; price-taker"
method_class: "NLP (physics-based SPM + SEI model as constraints) vs. LP (linear throughput model); validated by 1-year cell experiment"
evidence_read: "full text (arXiv 2009.11615, https://arxiv.org/pdf/2009.11615)"
oa_link: "https://arxiv.org/abs/2009.11615 ; data: Oxford Research Archive doi:10.5287/bodleian:gJPdDzvP4"
---

## 1. Research question
Does replacing the linear (throughput-based) battery/degradation model in an arbitrage optimiser with a physics-based electrochemical + degradation model increase real (experimentally measured) revenue and reduce degradation?

## 2. Setting & assumptions
- Price-taker, perfect foresight of 2014 Belgian DA prices; one-year operation.
- Single NMC/graphite pouch cell (Kokam SLPB78205130H, 16 Ah) scaled to "10 Wh" unit; 25 ± 0.5 °C ambient.
- Degradation cost λ_deg = €330/kWh of capacity lost.
- Calendar aging not explicitly in the physics model.

## 3. Constraints that drove the model choice
Linear models ignore SoC, current and temperature dependence of degradation and voltage/efficiency; the authors argue that the resulting schedules are both suboptimal and mis-predict profit. Physics model is non-linear → NLP solved with linear solution as initial guess.

## 4. Model
- Objective: π = ∫ [θ P(t) λ_DA(t) − (1−θ) (dC/dt) λ_deg] dt; θ = 1 revenue max, θ = 0.5 profit max.
- Linear model: dC/dt = β_t |P(t)| + β_p P_max with β_t = 1.26e-5 h/s (8000 cycles to 80 %), β_p = 2.12e-4 h; SoC window 10–90 % in profit-max case.
- Physics model: single particle model (Fick diffusion, Butler–Volmer kinetics), Arrhenius temperature dependence, lumped thermal model, SEI growth (Christensen-type) with capacity loss dC/dt ∝ j_SEI (Eq. A12).
- Parameters: SPM fitted to Mat4Bat (EU FP7) dataset; degradation parameters from Reniers' thesis/earlier work.

## 5. Data & processing
- Belgian DA prices 2014 (hourly).
- Experiment: PEC SBT8050 tester, 6 cells (3 profiles × 2 cells): (1) linear revenue-max, (2) linear profit-max, (3) physics profit-max; monthly capacity checks; 347 days of operation.

## 6. Justification
Experimental closed loop: schedules computed by each model are applied to real cells and measured capacity fade and revenue compared; also compares predicted vs. realised profit.

## 7. Key results
| | Linear revenue-max | Linear profit-max | Physics profit-max |
|---|---|---|---|
| Capacity loss (1 yr) | 14.44 % | 2.46 % | 1.71 % |
| Extrapolated life | 1.4 yr | 8.1 yr | 12 yr |
- Physics vs. linear profit-max: +17 % revenue, −30 % degradation; degradation per full-equivalent cycle −75 %; lifetime revenue +70 %.
- Profit prediction error: linear model 170 %, physics model 13 %.

## 8. Limitations (stated + your critical reading)
- Stated: single-cell scale (no cell-to-cell variation, thermal management, converter losses); computational cost; needs BMS–EMS coupling; calendar aging not modelled; lab parameterisation extrapolated.
- Critical: one market/year, perfect foresight, 2 cells per profile (small sample); revenue gain partly comes from better voltage/efficiency modelling, not only degradation.

## 9. Relevance to my study
Strongest experimental evidence that the degradation representation is first-order for profit (± 70 % lifetime revenue) — supports including at least a SoC-dependent aging model in a market-rule study, and reporting realised (not model-predicted) degradation.

## 10. Lineage links
- Builds on: Reniers et al. 2018 JPS 379 (simulation-only precursor); Reniers et al. 2019 J. Electrochem. Soc. degradation model review.
- Related: Kumtepeli/Hesse/Howey ageing-aware MILP work (IEEE Access 2020 — excluded, see stream file); collath2023_lifetimeprofit.

## 11. Verification log
- Crossref (api.crossref.org/works/10.1016/j.jpowsour.2020.229355): title, 3 authors, J. Power Sources vol 487, art. 229355, March 2021.
- arXiv 2009.11615 full text read (equations, experimental design, Table of results, funding VITO + EIT InnoEnergy).
- SJR: scimagojr.com sourceid 18063 → Q1 (2025, SJR 1.598).
