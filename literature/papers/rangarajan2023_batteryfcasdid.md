---
id: rangarajan2023_batteryfcasdid
title: "Assessing the impact of battery storage on Australian electricity markets"
authors: ["Rangarajan, A.", "Foley, S.", "Trück, S."]
year: 2023
journal: "Energy Economics"
volume_issue_pages: "120:106601"
doi: "10.1016/j.eneco.2023.106601"
quartile: "Q1 (SJR 2025, Economics and Econometrics; Energy (misc.))"
quartile_basis: "pub-year; rule=pass; SJR 2023 Q1 for this journal recorded in mercier2023_eudaarbitrage"
group: "Macquarie Business School (Trück: energy finance/risk; Foley: market microstructure)"
lineage: "All three authors Macquarie University (OpenAlex). Advisor-student ties not verified."
streams: [S8_empirical_econ]
market_context: "Australia NEM, FCAS (regulation + contingency raise/lower, incl. 6-second) across two states"
method_class: "econometric (staggered difference-in-differences)"
evidence_read: "(from abstract) + SSRN abstract page; full text (OA CC BY-NC-ND) could not be retrieved in this session (429/403/robots)"
oa_link: "https://doi.org/10.1016/j.eneco.2023.106601"
---

## 1. Research question
Did the staggered entry of grid-scale batteries reduce the cost of frequency control ancillary services (FCAS) in the NEM, and in which FCAS markets?

## 2. Setting & assumptions
- Reduced-form; treatment = battery deployments in two Australian states with staggered timing (abstract). Outcome = FCAS costs by market.
- Details of resolution, period, control regions, clustering not read (from abstract).

## 3. Constraints that drove the model choice
Battery entry is regional and staggered while FCAS is co-optimised NEM-wide with regional requirements -> region-level DiD with staggered timing is the natural design (abstract-level inference).

## 4. Model
Staggered difference-in-differences across states/markets; effect scales with battery capacity (abstract). Exact specification not verified.

## 5. Data & processing
AEMO NEM FCAS market data (abstract). Period/resolution: not verified.

## 6. Justification
Quasi-experimental variation from staggered regional battery commissioning. Robustness checks not verified.

## 7. Key results
- Grid-scale batteries significantly lower overall FCAS costs.
- Reductions increase with battery capacity.
- Largest effects in short-duration markets (regulation, 6-second contingency) historically supplied by more expensive fossil units.

## 8. Limitations (stated + critical reading)
- (Critical) Staggered DiD with heterogeneous timing is vulnerable to negative weighting (Goodman-Bacon 2021); whether a heterogeneity-robust estimator is used is unverified.
- NEM FCAS regions are linked; spillovers via global requirements contaminate "control" regions (SUTVA) unless regional/islanding events are handled.
- Concurrent rule changes (e.g., the 2020 mandatory primary frequency response rule; later very-fast FCAS markets — dates from general knowledge) are potential confounders depending on the sample window.

## 9. Relevance to my study
Closest published analogue to a GB question: "did battery entry collapse DC/DM/DR prices?". In GB the cleaner design is unit- or service-level: treat battery MW procured per EFA block as dose, use non-battery providers or services with different entry timing as controls, and exploit discrete product launches (DC Oct 2020, DM/DR 2022, EAC Nov 2023) as events.

## 10. Lineage links
- Builds on: NEM FCAS cost literature (e.g., Gilmore, Nolan & Simshauser 2024 Energy Journal on levelised FCAS costs - cross-ref frequency stream).
- Built upon by: not checked.

## 11. Verification log
- Bibliographic: Macquarie research portal (vol 120, art. 106601, April 2023, pp. 1-16, CC BY-NC-ND), RePEc IDEAS, OpenAlex (authors all Macquarie; corresponding Foley).
- SJR Energy Economics: Q1 2025.
- Full text NOT read: SSRN Delivery (429), MQ PDF (403/404), ScienceDirect (robots). All deep fields beyond the abstract are marked unverified. PRIORITY to re-read.
