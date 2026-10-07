---
id: schimpe2018_efficiency
title: "Energy efficiency evaluation of a stationary lithium-ion battery container storage system via electro-thermal modeling and detailed component analysis"
authors: ["Schimpe, M.", "Naumann, M.", "Truong, N.", "Hesse, H. C.", "Santhanagopalan, S.", "Saxon, A.", "Jossen, A."]
year: 2018
journal: "Applied Energy"
volume_issue_pages: "210:211-229"
doi: "10.1016/j.apenergy.2017.10.129"
quartile: "Q1 (SJR 2025, Applied Energy, SJR 2.864; Q1 Energy (misc.), Mech. Eng., Building & Construction, Mgmt/Policy)"
quartile_basis: "bracketed; rule=pass; Applied Energy Q1 in SJR 2017 (greenwood2017_efrservicedesign) and 2019 (engels2019_fcrgermanytechnoeco); 2018 itself not checked"
group: "Andreas Jossen & Holger Hesse (TUM Chair of Electrical Energy Storage Technology, EES) with NREL (Santhanagopalan, Saxon)"
lineage: "Schimpe, Naumann, Truong = TUM EES doctoral researchers under Jossen (Schimpe listed as EES alumnus on epe.ed.tum.de); Hesse = EES group leader (later Kempten UAS). NREL report no. NREL/JA-5400-70546."
streams: [S4_degradation_operation]
market_context: "German Primary Control Reserve (FCR), Secondary Control Reserve (aFRR) and PV self-consumption profiles (technical evaluation, no bidding)"
method_class: "electro-thermal system simulation (component loss models), no optimisation"
evidence_read: "abstract only (IDEAS/RePEc and NREL research hub) — (from abstract)"
oa_link: "NREL accepted manuscript via OSTI record 1409737 (not accessed)"
---

## 1. Research question
What is the real round-trip and overall energy efficiency of a containerised stationary Li-ion BESS once power electronics, thermal management and auxiliary consumption are included, and how does it vary across grid applications?

## 2. Setting & assumptions
- 192 kWh LFP prototype system connected to LV grid; holistic sub-models for battery rack, power electronics, thermal management (HVAC), control/monitoring.
- Generic profiles + application profiles: Primary Control Reserve, Secondary Control Reserve, PV surplus storage. (from abstract)

## 3. Constraints that drove the model choice
Constant round-trip efficiency assumptions in techno-economic studies ignore part-load converter losses and standby auxiliary load, which dominate at low utilisation. (from abstract)

## 4. Model
Coupled electro-thermal model: cell/rack electrical losses, converter efficiency curves vs. load, thermal model driving HVAC power, constant control/monitoring consumption. Equations not read (abstract only).

## 5. Data & processing
Parameterised on the prototype system (component measurements). (from abstract)

## 6. Justification
Model parameterised and built for a real prototype; loss mechanisms "identified, thoroughly analyzed and modeled". (from abstract)

## 7. Key results
- Conversion round-trip efficiency 70–80 %.
- Overall system efficiency (incl. auxiliary consumption) 8–13 percentage points lower for Primary Control Reserve and PV-battery applications.
- Secondary Control Reserve: total round-trip efficiency only 23 % due to low energy throughput.
- At low power, power-electronics losses outweigh battery losses; auxiliary consumption dominates at low utilisation. (all from abstract)

## 8. Limitations (stated + your critical reading)
- Single prototype / LFP / German profiles; aging not studied.
- Critical: results are product-dependent — capacity-type products with low energy throughput (aFRR-like) make efficiency almost meaningless as a constant parameter.

## 9. Relevance to my study
Directly relevant for market-product comparisons: a model using a constant 85–95 % round-trip efficiency will overstate the value of low-throughput reserve products relative to arbitrage, because standby/auxiliary losses are time-based, not energy-based. Minimal fix: add a constant auxiliary power draw and a load-dependent converter efficiency.

## 10. Lineage links
- Builds on: TUM EES SimSES simulation framework (Naumann et al.).
- Built upon by: Hesse/Jossen group ageing- and efficiency-aware MILP dispatch (e.g., Hesse et al. 2019 Energies — MDPI, excluded), collath2023_lifetimeprofit; cross-ref zheng2022 variable-efficiency SDP (S3).

## 11. Verification log
- Crossref (api.crossref.org/works/10.1016/j.apenergy.2017.10.129): title, 7 authors, Applied Energy 210:211–229, Jan 2018.
- Abstract verbatim from IDEAS (ideas.repec.org/a/eee/appene/v210y2018icp211-229.html); NREL hub confirms publication number.
- SJR: scimagojr.com sourceid 28801 → Q1 (2025, SJR 2.864).
- Full text NOT read (ScienceDirect robots-blocked, OSTI unreachable).
