---
id: schmidt2019_lcos
title: "Projecting the Future Levelized Cost of Electricity Storage Technologies"
authors: ["Schmidt, O.", "Melchior, S.", "Hawkes, A.", "Staffell, I."]
year: 2019
journal: "Joule"
volume_issue_pages: "3(1):81-100"
doi: "10.1016/j.joule.2018.12.008"
quartile: "Q1 (SJR 2019 and 2024/2025, Energy (misc.))"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Imperial College London — Grantham Institute, Centre for Environmental Policy, Energy Futures Lab, Chemical Engineering (Hawkes, Staffell)"
lineage: "Direct continuation of schmidt2017_experiencerates (same core team); interactive tool EnergyStorage.ninja."
streams: [S1_foundations_value]
market_context: "generic application archetypes (12 applications: arbitrage, primary/secondary/tertiary response, peaker replacement, black start, seasonal, T&D deferral, congestion, bill mgmt, power quality, reliability)"
method_class: "techno-economic LCOS + Monte Carlo"
evidence_read: "full text (accepted manuscript, Spiral: https://spiral.imperial.ac.uk/server/api/core/bitstreams/2eb0342c-190d-4dd0-b165-c6635293a333/content)"
oa_link: "https://spiral.imperial.ac.uk/server/api/core/bitstreams/2eb0342c-190d-4dd0-b165-c6635293a333/content"
---

## 1. Research question
Which storage technology will offer the lowest lifetime cost (LCOS) for each power-system application between 2015 and 2050, accounting for application-specific cycling and duration and projected investment-cost declines?

## 2. Setting & assumptions
- 9 technologies (PHES, CAES, flywheel, Li-ion, NaS, lead-acid, VRFB, hydrogen, supercapacitor) × 12 applications defined by discharge duration and annual cycles (e.g., arbitrage ~1,000 cycles/yr; primary response ~5,000 cycles/yr; seasonal < 10 cycles/yr, 700+ h).
- Discount rate 8 %; charging electricity price US$50/MWh (system) and US$100/MWh (behind-meter); degradation (cycle + temporal) to 80 % end-of-life capacity; investment cost projections from experience curves (schmidt2017_experiencerates).

## 3. Constraints that drove the model choice
Investment cost alone ($/kWh) misleads across applications with different cycling/duration → need application-specific lifetime cost; parameter uncertainty large → Monte Carlo.

## 4. Model
LCOS = [Investment + Σ_n O&M_n/(1+r)^n + Σ_n Charging_n/(1+r)^n + EoL/(1+r)^(N+1)] / Σ_n Discharged_n/(1+r)^n,
with charging cost = electricity price / round-trip efficiency, construction time and degradation reflected in discounting and throughput. 500 Monte Carlo draws per technology–application–year; probability of being cheapest reported.

## 5. Data & processing
17 cost/performance parameters per technology from 21 sources, cross-checked with 6 industry experts; 2015 base = median of ranges; projections via experience rates and market growth to 2050; data on Figshare.

## 6. Justification (why the authors argue the approach is valid)
Transparent, application-resolved metric comparable to LCOE; uncertainty propagated; sensitivity on discount rate, electricity price, cycles, duration.

## 7. Key results
- LCOS falls by about one third by 2030 and one half by 2050 (application-averaged).
- Lithium-ion likely becomes the most cost-efficient option for nearly all stationary applications from ~2030; hydrogen competitive only for seasonal/very long discharge; PHES/CAES remain competitive for long-duration, low-cycle uses.
- Annual cycles and discharge duration are the dominant LCOS drivers; investment cost share falls over time.
- High-cycle applications reach ~US$130–200/MWh LCOS long-run (as extracted; check the paper's figures before citing exact values).

## 8. Limitations (stated + your critical reading)
- Stated: LCOS disregards revenue/value; flat electricity prices; simplified degradation (no SoC/C-rate/temperature); cost projections uncertain; each technology assumed to capture the whole market for experience.
- Critical: LCOS is a cost metric only — must be paired with market-specific value (e.g., spread capture, ancillary prices) to judge profitability.

## 9. Relevance to my study
Provides the **cost denominator** (per-application LCOS) against which market-rule-specific revenues (per MWh discharged) can be compared; shows why high-cycle frequency/arbitrage products favour Li-ion.

## 10. Lineage links
- Builds on: schmidt2017_experiencerates; staffell2016_maxvalue.
- Built upon by (notable): Schmidt et al. 2020 Joule (competition between storage technologies); widespread LCOS use in policy reports.

## 11. Verification log
- Crossref (10.1016/j.joule.2018.12.008): authors, Joule 3(1):81–100, Jan 2019 ✔.
- SJR (id 21100834904) Q1 2019, 2024, 2025 ✔.
- Full text: accepted manuscript on Spiral; cell.com page returned 403. Some detailed numeric ranges flagged "as extracted".
