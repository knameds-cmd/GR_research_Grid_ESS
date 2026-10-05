---
id: desisternes2016_decarbvalue
title: "The value of energy storage in decarbonizing the electricity sector"
authors: ["de Sisternes, F. J.", "Jenkins, J. D.", "Botterud, A."]
year: 2016
journal: "Applied Energy"
volume_issue_pages: "175:368-379"
doi: "10.1016/j.apenergy.2016.05.014"
quartile: "Q1 (SJR 2016 and 2024/2025, Energy (misc.) and others)"
group: "MIT (de Sisternes, Jenkins — MIT at the time) with Audun Botterud (Argonne National Laboratory; later MIT LIDS)"
lineage: "MIT–Argonne line; Jenkins later leads Princeton ZERO lab (GenX), continuing in mallapragada2020_longrunvalue. Funded under DOE contract AC02-06CH11357 (Argonne) per OSTI record. Advisor-student ties not verified."
streams: [S1_foundations_value]
market_context: "ERCOT-like (Texas) system, long-run capacity expansion under CO2-intensity limits; generic 2-h and 10-h storage"
method_class: "MILP (capacity expansion with clustered unit commitment)"
evidence_read: "abstract (RePEc/EconPapers) + model description from companion working paper (IMRES, CEEPR WP 2013-016r, https://ceepr.mit.edu/wp-content/uploads/2022/07/2013-016r.pdf); journal full text not accessible"
oa_link: ""
---

## 1. Research question
What is the long-run system value of storage (2-h and 10-h) for meeting progressively stricter CO2 limits, and does it depend on the availability of other flexible low-carbon resources (e.g., nuclear)?

## 2. Setting & assumptions
- (from abstract) Generation capacity expansion model with Texas (ERCOT) data; carbon-intensity constraints of increasing stringency; storage durations of 2 h and 10 h.
- (from IMRES WP — model used by first author, not verified as identical configuration) single-year horizon at hourly resolution approximated by four representative weeks selected by least-squares fit to net-load duration curves; perfect foresight; system cost minimisation incl. VOLL.

## 3. Constraints that drove the model choice
(from IMRES WP) Operational flexibility constraints (ramping, start-up costs, minimum stable output, reserves) materially change least-cost portfolios at high VRE shares → capacity expansion must embed unit commitment; representative weeks keep MILP tractable.

## 4. Model
(from IMRES WP)
- Objective: min annualised fixed cost + variable cost + start-up cost + VOLL × unserved energy.
- Variables: thermal build (binary/integer), renewable capacity (continuous), hourly commitment/start/shut/output, storage charge/discharge/SoC, DSM.
- Constraints: demand balance, UC coupling to built units, ramping, min up/down, min stable output, primary/secondary/tertiary reserves, CO2 cap, storage energy balance with efficiencies.
- Solver: commercial MILP (not verified).

## 5. Data & processing
(from abstract) Texas load and wind/solar profiles; technology costs; representative-week selection (IMRES).

## 6. Justification (why the authors argue the approach is valid)
UC-constrained expansion captures flexibility value that energy-only screening curves miss (IMRES rationale).

## 7. Key results
(from abstract)
- 2-h storage justifies deployment only under strict emission constraints; 10-h storage is economic at roughly current pumped-hydro costs under deep decarbonisation.
- Storage is essential in scenarios relying on wind and solar, but becomes optional when diverse flexible low-carbon generation (e.g., nuclear) is available.

## 8. Limitations (stated + your critical reading)
Critical: single-node, perfect foresight, representative weeks (can understate multi-day storage needs); value is system (planner) value, not merchant revenue under real market rules.

## 9. Relevance to my study
Establishes "system value ≠ market revenue": system value of storage is highest under strict decarbonisation and VRE-heavy mixes; useful to motivate why market-rule design must transmit this value to merchant batteries.

## 10. Lineage links
- Builds on: IMRES (de Sisternes & Webster, CEEPR WP 2013-016r); sioshansi2009_pjmvalue.
- Built upon by (notable): mallapragada2020_longrunvalue; junge2022_efficientstorage; Sepulveda et al. 2021 (Nature Energy, LDES design space).

## 11. Verification log
- Crossref (10.1016/j.apenergy.2016.05.014): title, authors, Applied Energy 175(C):368–379, Aug 2016 ✔.
- OSTI record 1425501: DOE contract AC02-06CH11357 ✔ (OSTI PDF blocked by robots).
- SJR Applied Energy Q1 2016 ✔.
- Journal full text NOT read; deep fields from abstract + companion IMRES WP, clearly marked.
