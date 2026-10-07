---
id: maheshwari2020_nonlineardeg
title: "Optimizing the operation of energy storage using a non-linear lithium-ion battery degradation model"
authors: ["Maheshwari, A.", "Paterakis, N. G.", "Santarelli, M.", "Gibescu, M."]
year: 2020
journal: "Applied Energy"
volume_issue_pages: "261:114360"
doi: "10.1016/j.apenergy.2019.114360"
quartile: "Q1 (SJR 2025, Applied Energy, SJR 2.864)"
quartile_basis: "pub-year; rule=pass; SJR 2020 Q1 for this journal recorded in mallapragada2020_longrunvalue"
group: "Nikolaos Paterakis & Madeleine Gibescu (TU Eindhoven, Electrical Energy Systems) with Massimo Santarelli (Politecnico di Torino)"
lineage: "Paterakis = corresponding author (TU/e research portal). Maheshwari's student status/advisor not verified (likely TU/e–PoliTo joint thesis work; unverified)."
streams: [S4_degradation_operation]
market_context: "Wholesale market scheduling (market time constraints); specific market not verified"
method_class: "MILP with linearised non-linear degradation model + decomposition for long horizons (details not read)"
evidence_read: "abstract only (IDEAS/RePEc, TU/e research portal) — (from abstract)"
oa_link: "none (TU/e portal lists no OA file)"
---

## 1. Research question
How can experimentally observed non-linear dependence of Li-ion degradation on operating conditions be embedded in a storage scheduling model fast enough for market time constraints? (from abstract)

## 2. Setting & assumptions
Grid-connected Li-ion BESS providing market services; aging data from a commercial cell. (from abstract)

## 3. Constraints that drove the model choice
"Lack of data on degradation processes combined with requirement of fast computation have led to over-simplified models of battery degradation" — need a model both faithful (non-linear) and solvable within market timeframes. (from abstract)

## 4. Model
Non-linear degradation model fitted to commercial-cell aging data, incorporated into a scheduling optimisation; a decomposition technique gives near-optimal results for longer horizons. Exact functional form, stress factors and linearisation NOT read — do not cite specifics.

## 5. Data & processing
Experimental aging data of a commercial Li-ion battery (source not verified). (from abstract)

## 6. Justification
Decomposition validated as "near-optimal" against the monolithic model for longer horizons. (from abstract)

## 7. Key results
Not available from abstract.

## 8. Limitations
Full text not accessed; this entry is a placeholder for the TU/e line of work and should be upgraded before quantitative use.

## 9. Relevance to my study
Represents the "linearise a multi-stress-factor empirical model inside MILP" family (contrast with segment cost of xu2018_cycleagingcost and physics NLP of reniers2021_advancedmodels); the decomposition idea is relevant for lifetime-horizon market-rule simulations.

## 10. Lineage links
- Related: collath2023_lifetimeprofit (linearised calendar + cyclic model in MILP-MPC), Hesse/Kumtepeli MILP aging work.

## 11. Verification log
- TU/e research portal + IDEAS/RePEc: authors, Applied Energy 261, art. 114360, 1 March 2020, DOI; abstract verbatim on IDEAS.
- OpenAlex call was rate-limited (HTTP 429); ScienceDirect robots-blocked; ResearchGate 429.
- SJR: scimagojr.com sourceid 28801 → Q1.
