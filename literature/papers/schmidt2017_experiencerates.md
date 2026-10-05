---
id: schmidt2017_experiencerates
title: "The future cost of electrical energy storage based on experience rates"
authors: ["Schmidt, O.", "Hawkes, A.", "Gambhir, A.", "Staffell, I."]
year: 2017
journal: "Nature Energy"
volume_issue_pages: "2(8):17110"
doi: "10.1038/nenergy.2017.110"
quartile: "Q1 (SJR 2017 and 2024/2025, Energy Eng. & Power Tech.; Renewable Energy, Sustainability & Environment; Fuel Tech.)"
group: "Imperial College London — Grantham Institute / Centre for Environmental Policy / Chemical Engineering (Adam Hawkes, Iain Staffell, Ajay Gambhir)"
lineage: "Imperial storage-economics line (Staffell/Hawkes); Schmidt first author (Imperial PhD-era; supervision not verified). Precursor of schmidt2019_lcos."
streams: [S1_foundations_value]
market_context: "global technology cost data (no market); 11 storage technologies across portable, transport, stationary (residential/utility)"
method_class: "econometric (experience-curve regression) + logistic diffusion projection"
evidence_read: "full text (accepted manuscript, Spiral: https://spiral.imperial.ac.uk/server/api/core/bitstreams/1a800592-7f7f-4bda-9deb-2939897d2e67/content)"
oa_link: "https://spiral.imperial.ac.uk/server/api/core/bitstreams/1a800592-7f7f-4bda-9deb-2939897d2e67/content"
---

## 1. Research question
How fast will the capital cost of electrical energy storage technologies fall, based on empirically derived experience rates and plausible market growth, and when could they reach cost levels that enable stationary applications?

## 2. Setting & assumptions
- Wright's-law experience curves on product prices (not production costs) vs cumulative installed capacity.
- Multiple scopes (cell, module, pack, installed system) and applications (portable, HEV/EV, residential, utility).
- Future deployment from logistic S-curves fitted to literature market forecasts.

## 3. Constraints that drove the model choice
Lack of open cost data forced prior studies to use wide cost ranges or expert elicitation → compile price/deployment data and fit experience curves consistently across technologies.

## 4. Model
- P(X) = A·X^(−b); experience rate ER = 1 − 2^(−b) (price reduction per doubling of cumulative capacity X).
- Annual market A_n = A_sat / [1 + ((A_sat − A_base)/A_base)·e^(−r n)], r fitted by non-linear regression.
- Uncertainty: 95 % confidence intervals on ER; max/min growth rates; raw-material cost floors as feasibility check.

## 5. Data & processing
Product prices from peer-reviewed literature, industry reports, news, databases and manufacturer interviews; converted to US$/kWh (and US$/kW via C-rates); dataset released on Figshare (doi:10.6084/m9.figshare.5048062).

## 6. Justification (why the authors argue the approach is valid)
Cumulative capacity reported as the best-performing single predictor; consistent multi-technology method; cost-floor (raw materials < ~US$110/kWh) shows projections are physically feasible; raw-material reserves suffice beyond 10 TWh.

## 7. Key results
- Regardless of technology, capital costs head to ≈ US$340 ± 60/kWh for installed stationary systems and US$175 ± 25/kWh for battery packs once 1 TWh cumulative capacity is installed.
- 1 TWh could be reached within 10–23 years for most technologies.
- Li-ion's multi-application modularity (EV + stationary + portable) accelerates cumulative deployment → likely cost leader.
- ER uncertainty plus growth uncertainty can shift competitiveness timelines by up to ~12 years (EV case).
- Per-technology ER values exist in the paper but are not transcribed here (extraction was ambiguous).

## 8. Limitations (stated + your critical reading)
- Stated: prices ≠ costs; aggregate ERs hide component dynamics; extrapolation risk; ERs for mature technologies not significantly different from zero; application-specific LCOS needed for competitiveness.
- Critical: actual 2020–2024 Li-ion pack prices fell faster than many central projections; system-level BoS/EPC costs for grid batteries learn differently from packs.

## 9. Relevance to my study
Cost side of the cost-vs-value comparison: use ER-based capex trajectories to translate market-rule-driven revenue into break-even years / investment thresholds.

## 10. Lineage links
- Builds on: staffell2016_maxvalue (cost/revenue gap); experience-curve literature (Wright 1936; Rubin et al.).
- Built upon by (notable): schmidt2019_lcos; Schmidt et al. 2020 Joule (competition between storage technologies — not archived).

## 11. Verification log
- Crossref (10.1038/nenergy.2017.110): authors, Nature Energy 2(8), article 17110, issued 10 Jul 2017 ✔.
- SJR (id 21100812579) Q1 2017, 2024, 2025 ✔.
- Full text: accepted manuscript on Spiral; key headline numbers quoted; per-technology ER table deliberately not transcribed due to extraction ambiguity.
