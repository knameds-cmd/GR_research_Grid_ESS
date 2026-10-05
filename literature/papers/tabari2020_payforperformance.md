---
id: tabari2020_payforperformance
title: "Paying for performance: The role of policy in energy storage deployment"
authors: ["Tabari, M.", "Shaffer, B."]
year: 2020
journal: "Energy Economics"
volume_issue_pages: "92:104949"
doi: "10.1016/j.eneco.2020.104949"
quartile: "Q1 (SJR 2025, Economics and Econometrics; Energy (misc.))"
group: "Shaffer (Univ. of Calgary, Economics & School of Public Policy); Tabari (UBC Sauder)"
lineage: "Not verified."
streams: [S8_empirical_econ]
market_context: "US ISOs/RTOs; FERC Order 755 (2011) pay-for-performance frequency regulation; storage project deployment"
method_class: "econometric (difference-in-differences on project counts)"
evidence_read: "(from abstract) — RePEc/author page abstracts; full text not accessible in session"
oa_link: ""
---

## 1. Research question
Did a market-rule change that pays frequency regulation for speed and accuracy (FERC Order 755) increase energy-storage deployment?

## 2. Setting & assumptions
- Natural experiment: Order 755 required FERC-jurisdictional ISOs/RTOs to adopt two-part (capacity + performance/mileage) regulation compensation; regions not covered serve as controls (abstract).
- Outcome: number / likelihood of storage projects built to provide frequency regulation.

## 3. Constraints that drove the model choice
Policy applies to a subset of regions at a common date -> DiD across affected vs unaffected regions (abstract).

## 4. Model
DiD: storage projects (for regulation) in covered vs non-covered regions, pre vs post Order 755 (exact specification, FE, controls not verified).

## 5. Data & processing
Storage project records by region and year (likely DOE Global Energy Storage Database — NOT verified).

## 6. Justification
Not verified beyond abstract.

## 7. Key results
- Order 755 increases the likelihood that projects are built to provide frequency regulation by ~37% (RePEc abstract); author page: ">30% increase in the number of storage projects in the covered regions".
- Message: correct valuation of fast response through market rules can overcome barriers even when costs are high.

## 8. Limitations (critical reading)
- Covered vs uncovered regions differ (ERCOT and non-ISO areas as controls) in many ways; parallel trends credibility unknown.
- Compliance/implementation dates differed across ISOs (roughly 2012-2013; dates from general knowledge, not verified here), suggesting staggered treatment; a single post dummy may mis-time effects.
- Project counts, not MW or revenues; PJM RegD saturation and its 2017 redesign show the subsequent reversal.

## 9. Relevance to my study
The cleanest published example of "market product design -> storage investment" via DiD — the same causal question as "GB DC launch / EAC co-optimisation -> battery entry and bidding". In GB, product-launch dates (approx.: DC 2020; DM/DR 2022; EAC Nov 2023; Balancing Reserve 2024 — check exact dates in NESO notices) provide staggered events across services, and NESO EAC unit-level results allow outcomes at unit x service x EFA level rather than project counts.

## 10. Lineage links
- Builds on: PJM RegD/performance-payment engineering literature (cross-ref frequency stream).
- Built upon by: not checked.

## 11. Verification log
- OpenAlex: Energy Economics vol 92, art. 104949, pub. 16 Sep 2020; affiliations UBC Sauder (corresponding) and U Calgary.
- RePEc IDEAS record and Shaffer homepage (Energy Economics vol 92, Oct 2020).
- SJR Energy Economics Q1 2025.
- Full text NOT read; all method details beyond abstract unverified.
