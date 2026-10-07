---
id: celicortes2025_deterministicfreq
title: "Deterministic grid frequency deviations and the provision of frequency containment reserve with battery storage systems"
authors: ["Celi Cortés, M.", "Koltermann, L.", "Dang, T.D.", "Figgener, J.", "Zurmühlen, S.", "Sauer, D.U."]
year: 2025
journal: "Energy Reports"
volume_issue_pages: "13:1029-1040"
doi: "10.1016/j.egyr.2024.12.057"
quartile: "Q1 (SJR 2024, Energy (misc.); 2025 Q1 in EEE and Energy Eng.) — note Q2 in 2023"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Dirk Uwe Sauer, ISEA RWTH Aachen / JARA-Energy"
lineage: "RWTH ISEA Sauer group; Koltermann, Figgener, Zurmühlen shared with koltermann2022_fcrbalancinggroup."
streams: [S6_ancillary_products]
market_context: "Continental Europe FCR (Germany); frequency data 2014-2023"
method_class: "time-series decomposition (statistical) + rule-based BESS management"
evidence_read: "abstract only (OpenAlex); gold OA (CC BY) but publisher PDF not fetchable"
oa_link: "https://doi.org/10.1016/j.egyr.2024.12.057"
---

## 1. Research question
How large and how regular are deterministic frequency deviations (DFDs, e.g., around hourly schedule changes) in Continental Europe 2014–2023, and how should a battery providing FCR manage SoC given them?

## 2. Setting & assumptions
Continental European synchronous area; FCR from BESS; DFDs caused by market-schedule steps.

## 3. Constraints that drove the model choice
Systematic (predictable) components of frequency create biased energy drift for proportional FCR; separating deterministic from stochastic components requires decomposition.

## 4. Model
Time-series decomposition of frequency deviations (seasonal/daily); rule-based BESS energy management exploiting DFD patterns (from abstract).

## 5. Data & processing
Continental Europe grid frequency 2014–2023 (source/resolution not verified).

## 6. Justification
Ten-year statistical analysis; correlation tests with renewable output and reserve demand.

## 7. Key results
- High-magnitude deviations increased 37% by 2023; occurrence shifted ~10 mHz.
- Median deviations vary up to 100% between years; deviations ~65% more frequent in March than July.
- Weak correlation of frequency behaviour with RES production or reserve demand.
- Rule-based BESS management proposed to address DFD patterns (numbers not verified).

## 8. Limitations (stated + your critical reading)
Abstract-level only; journal Q1 status is recent (Q2 in 2023).

## 9. Relevance to my study
Frequency traces used as model input are non-stationary (seasonal, yearly drift) — any back-test of FCR battery economics on one year is biased. Supports using multi-year frequency data and modelling deterministic hour-boundary drift as part of the "energy requirement" a product implicitly imposes.

## 10. Lineage links
- Builds on: thien2017_fcrgermanystrategy; koltermann2022_fcrbalancinggroup; ENTSO-E reports on DFDs.
- Built upon by: —

## 11. Verification log
- Crossref + OpenAlex works/doi:10.1016/j.egyr.2024.12.057: title, 13:1029-1040 (June 2025 issue; online Dec 2024), six authors all RWTH/JARA, CC BY 4.0, abstract.
- SJR sid 21100389511: Energy Reports Q1 2024 (Energy misc.), Q1 2025 (multiple), Q2 2023.
- Full text NOT read.
