---
id: <firstauthor><year>_<keyword>          # e.g. xu2018_cycleaging (lowercase, ascii)
title: "<exact title>"
authors: ["Last, F.", "Last, F."]
year: <year of issue>
journal: "<full journal name>"
volume_issue_pages: "<vol(issue):pages or article no.>"
doi: "<10.xxxx/...>"
quartile: "<Q1 + source, e.g. 'Q1 (SJR 2023, Energy Engineering)' or 'Q1 (JCR 2023, EEE)'>"
group: "<PI / lab / institution of senior author>"
lineage: "<advisor→student or group ties if verifiable, e.g. 'Kirschen (UW) group; Xu = Kirschen PhD 2018'>"
streams: [<stream tags>]
market_context: "<market/country/product, e.g. 'PJM RegD + energy', 'GB DC', 'generic price-taker'>"
method_class: "<LP | MILP | NLP | SP | RO | DRO | SDP/DP | MPC | RL/DRL | econometric | agent-based | review>"
evidence_read: "<full text (URL) | abstract + intro only | metadata only>"
oa_link: "<open-access URL if any>"
---

## 1. Research question
One or two sentences.

## 2. Setting & assumptions
- Price-taker / price-maker? Perfect foresight / forecasts / scenarios?
- Time resolution, horizon, rolling or one-shot
- Asset assumptions (power, energy, efficiency, SoC limits, degradation)
- Market assumptions (products, settlement, penalties, gate closure)

## 3. Constraints that drove the model choice
What the authors say forced their modelling choice (tractability, non-anticipativity, integer decisions, nonconvex aging, data availability...).

## 4. Model
- Objective
- Decision variables
- Key constraints (write the important ones compactly; LaTeX allowed)
- Solution method / algorithm / solver

## 5. Data & processing
- Sources, period, resolution
- Cleaning / scenario generation / forecasting / feature engineering
- Train/test split or back-test design

## 6. Justification (why the authors argue the approach is valid)
Their argument + validation (benchmarks, bounds, sensitivity, out-of-sample).

## 7. Key results
Numbers with units where available.

## 8. Limitations (stated + your critical reading)

## 9. Relevance to my study
How it can be reused: formulation, data pipeline, benchmark, counter-argument.

## 10. Lineage links
- Builds on: <ids or citations>
- Built upon by (notable): <citations>

## 11. Verification log
What was checked where (DOI resolver, publisher page, arXiv version, SJR page). Mark anything unverified.
