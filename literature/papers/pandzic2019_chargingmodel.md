---
id: pandzic2019_chargingmodel
title: "An Accurate Charging Model of Battery Energy Storage"
authors: ["Pandžić, H.", "Bobanac, V."]
year: 2019
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "34(2):1416-1426"
doi: "10.1109/TPWRS.2018.2876466"
quartile: "Q1 (SJR 2025, IEEE Trans. Power Systems, SJR 4.217)"
quartile_basis: "pub-year; rule=pass; SJR 2019 Q1 for this journal recorded in baker2024_transferablebidder"
group: "Hrvoje Pandžić (Univ. of Zagreb FER, Innovation Centre Nikola Tesla / LARES lab)"
lineage: "Pandžić was a postdoc with D. Kirschen at UW (co-authored UW storage siting/sizing papers with Kirschen c. 2014-2015; citation not re-verified here) — tie per co-authorship; Bobanac = Zagreb researcher. Funded by Croatian Science Foundation EVBASS (IP-2014-09-3517) and SIREN (with Croatian TSO HOPS)."
streams: [S4_degradation_operation]
market_context: "EPEX spot day-ahead (15 Jan 2018 prices), 10 MWh price-taker arbitrage with imbalance-style penalties for undelivered energy"
method_class: "LP (piecewise-linear SoE-dependent charging limit, no binaries if concave) / MILP with SOS2 otherwise; lab-validated"
evidence_read: "full text (author PDF, https://evbass.fer.hr/images/site_4351/An%20Accurate%20Charging%20Model%20of%20Battery%20Energy%20Storage.pdf)"
oa_link: "https://evbass.fer.hr/images/site_4351/An%20Accurate%20Charging%20Model%20of%20Battery%20Energy%20Storage.pdf"
---

## 1. Research question
Standard storage models in market optimisation assume a constant power limit regardless of state of energy (SoE). Li-ion cells charge under CC-CV, so achievable charging power collapses at high SoE. How large is the resulting scheduling error and profit loss, and can a linear model fix it?

## 2. Setting & assumptions
- Price-taker DA arbitrage, perfect price knowledge, hourly steps, 24-h horizon, SoE_0 = 50 % and SoE_T ≥ 50 %.
- Shortfall settlement rule used in the case study: undelivered charging energy sold back at 70 % of price; undelivered discharge bought at 140 % of price.
- No degradation modelled (pure SoC/efficiency physics).

## 3. Constraints that drove the model choice
Must remain LP/MILP for market tools; CC-CV behaviour is non-linear in SoE; the authors want a model parameterisable from a simple lab charge test.

## 4. Model
- SoE dynamics: soe_t = soe_{t−1} + η_E Δt ch_t − Δt dis_t (round-trip energy efficiency η_E on charge side).
- Baseline: ch_t ≤ P^ch (constant).
- Linear CC-CV: ch_t ≤ P^ch (C^E − soe_t)/(C^E − SOE^{cc,cv}) above the CC→CV switch point.
- Proposed energy-charging model: SoE split into segments soe_t = Σ_i soe_{t,i}, soe_{t,i} ≤ R_{i+1} − R_i; chargeable energy Δsoe_t = F_1 + Σ_i (F_{i+1} − F_i)/(R_{i+1} − R_i) · soe_{t−1,i}; ch_t ≤ Δsoe_t / (Δt η_E). LP if slopes decrease monotonically, otherwise SOS2.
- Parameters from lab: 1C → η_E = 0.81, SOE^{cc,cv} = 55.5 %, 3 segments; 0.2C → η_E = 0.866, SOE^{cc,cv} = 89.7 %, 4 segments.

## 5. Data & processing
- Panasonic 18650 (2.8 Ah, ~10 Wh) cell tested on a 1 kW bidirectional converter testbed (NI cRIO/LabVIEW); scaled to 10 MWh.
- Procedure: record CC-CV curves at given C-rate → integrate energy → time–SoE curve → SoE–ΔSoE curve → piecewise linearise.
- Validation: schedules from each model executed on the real cell; delivered energy and settled profit measured.

## 6. Justification
Hardware-in-the-loop experiment comparing scheduled vs. delivered energy; realised profit after shortfall settlement.

## 7. Key results
| 1C | Baseline | Linear CC-CV | Proposed |
|---|---|---|---|
| Delivered energy error | −14.6 % | 0 % | −0.4 % |
| Scheduled profit (€) | 272.04 | 249.51 | 264.71 |
| Realised profit after settlement (€) | 91.02 | 249.51 | 259.64 |
- At 1C the constant-power model's realised profit is ~65 % below the proposed model's (failed in 4 hours); at 0.2C the baseline and linear CC-CV models realise ~16–19 % less than the proposed model (end-SoE violated).

## 8. Limitations (stated + your critical reading)
- Stated: single cell scaled to MWh (pack/converter losses ignored); efficiency fixed per C-rate; hourly resolution; no price uncertainty; Li-ion only.
- Critical: penalty rule (70 %/140 %) is assumed, so the size of the realised loss depends on the settlement design — this is itself a market-rule lever.

## 9. Relevance to my study
Shows that SoC-dependent power capability (not degradation) can dominate profit errors when products demand full-power delivery near SoC limits (e.g., FCR/aFRR energy-reservoir rules). A market-rule study should at least include an SoE-dependent charge limit for high-C-rate products.

## 10. Lineage links
- Builds on: conventional bucket storage models; CC-CV charging physics.
- Related: Gonzalez-Castellanos, Pozo & Bischi 2020 TPWRS 35(1):672–682 (convex-hull LP for SoC-dependent power limits and variable efficiency; dispatch, not market; cross-ref).

## 11. Verification log
- Crossref (api.crossref.org/works/10.1109/TPWRS.2018.2876466): title, authors, TPWRS 34(2):1416–1426, March 2019.
- Author PDF read (evbass.fer.hr) — includes funding statement and lab setup.
- SJR: scimagojr.com sourceid 28825 → Q1.
- Pandžić–Kirschen postdoc tie: from co-authorship history, not checked against a CV here.
