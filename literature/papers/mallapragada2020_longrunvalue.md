---
id: mallapragada2020_longrunvalue
title: "Long-run system value of battery energy storage in future grids with increasing wind and solar generation"
authors: ["Mallapragada, D. S.", "Sepulveda, N. A.", "Jenkins, J. D."]
year: 2020
journal: "Applied Energy"
volume_issue_pages: "275:115390"
doi: "10.1016/j.apenergy.2020.115390"
quartile: "Q1 (SJR 2020 and 2024/2025, Energy (misc.) and others)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "MIT Energy Initiative (Mallapragada, Sepulveda) with Jesse Jenkins (Princeton, Andlinger Center / ZERO lab)"
lineage: "GenX modelling team (Jenkins & Sepulveda created GenX at MIT); continues desisternes2016_decarbvalue; companion theory in junge2022_efficientstorage (Mallapragada co-author)."
streams: [S1_foundations_value]
market_context: "stylised U.S. Northeast and Texas systems, long-run capacity expansion, 40-60% VRE, Li-ion 2-8 h"
method_class: "LP (GenX capacity expansion, hourly, perfect foresight)"
evidence_read: "abstract (RePEc) + MIT News summary (https://news.mit.edu/2020/assessing-value-battery-energy-storage-future-power-grids-increasing-integration-wind-and-solar-0812); full text paywalled"
oa_link: ""
---

## 1. Research question
What is the long-run (investment-inclusive) system value of Li-ion battery storage as wind and solar shares rise, which value streams dominate, and how much battery capacity is cost-effective at current and projected costs?

## 2. Setting & assumptions
(from abstract/news) GenX least-cost capacity expansion at high temporal resolution; two stylised systems (U.S. Northeast-like and Texas-like); VRE 40–60 %; battery durations 2–8 h; current and future ($150/kWh for 4-h) battery costs. Planner perspective (perfect foresight, perfect competition implied). Exact resolution/representative periods not verified.

## 3. Constraints that drove the model choice
(from abstract) Need to capture capacity-deferral and operational value jointly → capacity expansion with chronological hourly operation rather than price-taker arbitrage.

## 4. Model
(from abstract/news) GenX: minimise investment + operating cost subject to hourly balance, operating constraints, storage dynamics, possibly transmission between zones. System value of storage computed as reduction in total system cost per unit of storage. Formulation not read.

## 5. Data & processing
Not verified (likely NREL/EIA cost data and historical load/VRE profiles).

## 6. Justification (why the authors argue the approach is valid)
Not assessable beyond abstract; marginal system value approach consistent with long-run equilibrium theory (cf. junge2022_efficientstorage).

## 7. Key results
(from abstract/news)
- Storage value comes primarily from **deferring generation (and transmission) capacity investment**, not energy arbitrage.
- Marginal value declines with storage penetration; 1 MW of storage displaces < 1 MW of gas capacity, ratio falling with penetration.
- Raising VRE share from 40 % to 60 % increases storage value only modestly.
- At (2020) Li-ion costs only up to ~4 % of peak demand in storage is cost-effective; at $150/kWh (4-h), 4–16 % of peak demand.
- 8-h storage displaces more gas capacity than 2-h but extra value does not justify extra energy-capacity cost.

## 8. Limitations (stated + your critical reading)
Critical: planner value ≠ merchant revenue — capacity-deferral value reaches a merchant battery only through scarcity pricing or capacity payments (market-rule dependent); ancillary services and uncertainty likely simplified.

## 9. Relevance to my study
Key motivation: if storage value is mainly capacity value, then **capacity-market / scarcity-pricing rules** (de-rating factors, price caps) determine whether batteries can monetise it — a central hypothesis for a market-rules profitability study.

## 10. Lineage links
- Builds on: desisternes2016_decarbvalue; GenX (Jenkins & Sepulveda 2017 working paper).
- Built upon by (notable): junge2022_efficientstorage; Sepulveda et al. 2021 Nature Energy (LDES design space).

## 11. Verification log
- Crossref (10.1016/j.apenergy.2020.115390): authors, Applied Energy 275, article 115390, Oct 2020 ✔.
- IDEAS record: same fields + abstract ✔.
- SJR Applied Energy Q1 2020 ✔.
- Full text NOT read (ScienceDirect robots-blocked; no OA copy found). Deep fields from abstract + MIT News only.
