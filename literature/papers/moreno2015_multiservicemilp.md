---
id: moreno2015_multiservicemilp
title: "A MILP model for optimising multi-service portfolios of distributed energy storage"
authors: ["Moreno, R.", "Moreira, R.", "Strbac, G."]
year: 2015
journal: "Applied Energy"
volume_issue_pages: "137:554-566"
doi: "10.1016/j.apenergy.2014.08.080"
quartile: "Q1 (SJR 2025, Energy (misc.); Renewable Energy, Sustainability and the Environment)"
quartile_basis: "latest-only; rule=unchecked; SJR 2015 (publication year) not checked — only later years"
group: "Goran Strbac, Control & Power group, Imperial College London (R. Moreno also Univ. of Chile)"
lineage: "Imperial (Strbac) group. Moreno and Moreira at Imperial; Moreno later at Universidad de Chile (repository record, funding by Conicyt). Direct predecessor of perez2016 (Pérez, Moreno, Moreira, Orchard, Strbac, IEEE TSTE 2016) on degradation in multi-service portfolios."
streams: [S2_stacking_cooptimization]
market_context: "Great Britain: distribution-network congestion management (DNO contract), energy arbitrage, 'various reserve and frequency regulation services' (abstract wording); distributed storage with active + reactive power"
method_class: "MILP"
evidence_read: "abstract only (IDEAS/RePEc; university repository PDF blocked by anti-bot page)"
oa_link: "https://repositorio.uchile.cl/handle/2250/132677"
---

## 1. Research question
How should a distributed storage operator choose and schedule a portfolio of network, energy and balancing services to maximise profit, given that the services compete for the same capacity? What does this imply for pricing DNO congestion-management contracts and for network investment? (from abstract)

## 2. Setting & assumptions
(from abstract) Distributed storage in a distribution network. Coordinated provision of:
- DNO congestion management;
- energy price arbitrage;
- several reserve and frequency-regulation services;
- active and reactive power control.

GB market case studies. Price, foresight and resolution assumptions were not read.

## 3. Constraints that drove the model choice
(from abstract) Services interact and conflict, so they need a joint optimisation, written as a MILP. Integer variables are likely for service-commitment/exclusivity, but this was not confirmed from the full text.

## 4. Model
- Objective: maximise the storage operator's profit from the service portfolio (from abstract).
- Capacity split, reserve-energy modelling, SoC management: **not read; not recorded**.

## 5. Data & processing
GB market and network case studies (from abstract); details not read.

## 6. Justification (why the authors argue the approach is valid)
Case studies on GB data (from abstract).

## 7. Key results
- (from abstract) Frequency-control services are "significantly more profitable" than other services in the GB case.
- Reactive power control improves both distribution management and energy/balancing trading.
- The model is used to price congestion-management services and to propose network-reinforcement investment policies when storage is present.

## 8. Limitations (stated + your critical reading)
- Not read.
- Critical reading: it predates the GB Dynamic Containment/Moderation/Regulation suite, so its frequency-response representation reflects the old regime (FFR/mandatory response).

## 9. Relevance to my study
- The canonical "multi-service portfolio MILP" in the Imperial lineage.
- The source of the GB finding that frequency services dominate stacked value; a historical baseline for GB.
- Worth obtaining the full text for its service-priority/conflict constraints.

## 10. Lineage links
- Builds on: he2011_aggregatingvalues (aggregation of storage values); Imperial whole-system storage value work (S1).
- Built upon by (notable): Pérez, Moreno, Moreira, Orchard, Strbac, "Effect of battery degradation on multi-service portfolios of energy storage", IEEE TSTE 7(4):1718–1729, 2016, DOI 10.1109/TSTE.2016.2589943 (metadata verified through OpenAlex; cross-ref to the degradation stream).

## 11. Verification log
- Crossref (api.crossref.org/works/10.1016/j.apenergy.2014.08.080): title, authors, Applied Energy 137, pp. 554–566, January 2015. Confirmed.
- IDEAS/RePEc abstract read.
- Univ. of Chile repository record confirms metadata; the PDF was blocked by an anti-bot page.
- SJR (id 28801): Q1 2025.
- All deep fields marked as from the abstract or not read.
