---
id: collath2022_agingreview
title: "Aging aware operation of lithium-ion battery energy storage systems: A review"
authors: ["Collath, N.", "Tepe, B.", "Englberger, S.", "Jossen, A.", "Hesse, H."]
year: 2022
journal: "Journal of Energy Storage"
volume_issue_pages: "55:105634"
doi: "10.1016/j.est.2022.105634"
quartile: "Q1 (SJR 2025, J. Energy Storage, SJR 1.795)"
group: "Andreas Jossen (TUM Chair of Electrical Energy Storage Technology) & Holger Hesse (Kempten UAS / TUM)"
lineage: "Collath, Tepe, Englberger = TUM EES doctoral researchers (Collath listed as EES alumnus on epe.ed.tum.de); same group as schimpe2018_efficiency and SimSES. Continued by collath2023_lifetimeprofit."
streams: [S4_degradation_operation]
market_context: "Review; case studies on FCR, self-consumption increase (SCI), peak shaving; also arbitrage, V2G, microgrids"
method_class: "review"
evidence_read: "full text (mediaTUM, https://mediatum.ub.tum.de/doc/1768077/1768077.pdf; CC-BY)"
oa_link: "https://mediatum.ub.tum.de/doc/1768077/1768077.pdf"
---

## 1. Research question
How is battery aging represented and controlled in BESS operation (scheduling/EMS) literature, which stress factors matter per application, and what are the open problems?

## 2. Setting & assumptions
Review of aging-aware operation literature (~2005–2022, concentrated 2015–2022; 30+ scheduling studies tabulated in Tables 4–7) plus own simulation of stress-factor distributions for FCR, SCI and peak shaving.

## 3. Constraints that drove the model choice
N/A (review). Notes the tension between model fidelity and the MILP-dominated solution methods.

## 4. Model (taxonomy)
- Aging models: empirical (FEC or multi-stress fits), semi-empirical (calendar + cycle superposition, √t SEI growth), physicochemical (SPM, P2D), filtering/ML (absent from scheduling literature).
- Cycle detection: throughput/FEC, half-cycle counting, rainflow; "virtual time" method for changing stress.
- Aging-awareness methods: objective-function cost (based on battery cost, EOL capacity, SOH change; or FEC budget), revenue-based (link future profit to life), multi-objective technical weighting; constraints (SoC window, C-rate limits, throughput limits).
- Solvers: MILP most common; NLP, DP; metaheuristics (DE, PSO, NSGA-II); RL, fuzzy.

## 5. Data & processing
Literature tables; own simulations (TUM SimSES) of DOC, SoC, C-rate distributions for FCR, SCI, PS.

## 6. Justification
Systematic tabulation; application-specific stress-factor analysis.

## 7. Key results
- "Empirical or semi-empirical degradation models as well as the exact solution approach of mixed integer linear programming are particularly common."
- Aging cost usually set from replacement cost (€250–500/kWh, EOL 70–80 %); one reviewed study finds optimal profit at a much lower €100/kWh penalty → replacement cost is not the right aging price.
- Reported impacts in reviewed studies: multi-use life 2.4 → 8.6 yr (profitability index 0.06 → 1.24, Englberger et al.); arbitrage "He et al." life 6.3 → 10 yr at −19.2 % daily revenue; Perez et al. 2× lifespan at −18 % annual gross revenue.
- Application stress: FCR → small DOC (~1–2 %) around 50 % SoC, calendar aging dominant; SCI → large DOC and SoC swings, cyclic aging dominant; PS → high static SoC, calendar aging dominant.
(Numbers as extracted from the full text; re-check tables before citing.)

## 8. Limitations (stated + your critical reading)
- Gaps named: path dependence under varying stress; unquantified error of linearising non-linear aging models; ML models lack algebraic link to stress factors; gap between simulated and real operation.
- Critical: little on how market product rules (energy reservoir requirements, SoC management rules, delivery duration) shape stress factors — the review is application- not rule-oriented.

## 9. Relevance to my study
Best single map of the design space; application-specific stress analysis justifies that for FCR-type products calendar aging (SoC/T) matters more than cycle depth — so a rainflow-only cost (Kirschen/Xu lineage) is mis-specified for reserve-dominated portfolios.

## 10. Lineage links
- Builds on: Weitzel & Glock 2018 review (EJOR), TUM SimSES work, schimpe2018_efficiency.
- Built upon by: collath2023_lifetimeprofit.

## 11. Verification log
- OpenAlex (doi:10.1016/j.est.2022.105634): title, authors (TUM; Kempten UAS), JES 55, art. 105634, CC-BY, mediaTUM 1768077.
- Crossref: Nov 2022 issue, CC-BY 4.0 licence.
- mediaTUM PDF read.
- SJR: scimagojr.com sourceid 21100400826 → Q1.
