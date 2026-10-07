---
id: kirkpatrick2026_batterycongestion
title: "Estimating the Congestion Benefits of Batteries When Network Connections Are Unobserved"
authors: ["Kirkpatrick, A. J."]
year: 2026
journal: "The Energy Journal"
volume_issue_pages: "online first 9 Sep 2026; volume/issue/pages not yet assigned"
doi: "10.1177/01956574261469461"
quartile: "BORDERLINE: Q1 (SJR 2024, Economics and Econometrics; Energy misc.) but Q2 in SJR 2025 (and 2023). Energy Journal is on the coordinator's accepted list; flagged."
quartile_basis: "nearest-year; rule=FAIL (provisional); SJR 2026 not yet published, nearest year 2025 = Q2 (Q1 in 2024) — archive entries record The Energy Journal as Q2 in 2023 and 2025 without separating categories; confirm the best category (Energy misc.) when SJR is reachable — if Q1 there, the rule passes"
group: "Kirkpatrick, Dept. of Economics, Michigan State University (environmental/energy econ)"
lineage: "Not verified."
streams: [S8_empirical_econ]
market_context: "CAISO day-ahead nodal LMPs, 757 nodes, 2009-2016; 17 utility battery additions (~60 MW) + 120 MW pumped hydro"
method_class: "econometric (high-dimensional FE DiD + double/pooled LASSO)"
evidence_read: "full text (author WP Jan 2025 https://www.justinkirkpatrick.com/Papers/kirkpatrickEnergyStorageJan2025.pdf)"
oa_link: "https://www.justinkirkpatrick.com/Papers/kirkpatrickEnergyStorageJan2025.pdf"
---

## 1. Research question
How much do grid-scale batteries lower locational prices at their own node and at network-connected nodes (congestion relief), when the network topology and binding constraints are unobserved by the econometrician?

## 2. Setting & assumptions
- Hourly DAM LMPs 1 Sep 2009 - 31 Dec 2016; storage locations/commissioning from DOE Global Energy Storage Database.
- Battery operation is not observed; effect is on prices conditional on system price (LAP).
- Siting assumed exogenous to pre-existing price trends (pre-2017 mandate-era siting).

## 3. Constraints that drove the model choice
Without the network model, which nodes a battery affects is unknown; a KKT view of OPF implies only binding constraints transmit effects, i.e., a sparse set of non-zero cross-node effects -> LASSO's zeroing property is a natural selector. Naive variable selection induces omitted-variable bias, so Belloni-Chernozhukov-Hansen double selection / partialling-out is used.

## 4. Model
- Own-node: p_{n,t} = beta * StorageMW_{n,t} + gamma * p^{LAP}_t + controls(local solar, temperature, precipitation, Aliso Canyon) + FE(node x hour x season x year x weekday) + e. Identification: within node-hour-quarter variation in installed storage.
- Cross-node: "Double Pooled LASSO" — (1) orthogonalise covariates on storage, (2) residualise prices, (3) LASSO selects nodes whose storage affects node n, then post-LASSO OLS.

## 5. Data & processing
CAISO OASIS LMPs (757 pricing nodes), node geolocation matching (measurement error acknowledged), weather; capacity from DOE GESD.

## 6. Justification
Pre-trend and selection-on-observables tests (installation not correlated with pre-period price spreads/trends). KKT-sparsity argument for LASSO. Results interpreted as upper bounds on price effects due to possible unobserved time-varying selection.

## 7. Key results
- Own-node peak reduction e.g. -$1.87/MWh (spring 18:00), -$0.26/MWh (summer).
- Annual benefit per MW: own-node $61,514 + cross-node $18,428 = $79,942/MW-yr (cross-node ~23% of own-node).
- Ratepayer transfer = 38-161% of private arbitrage revenue; total 2009-2016 savings $47.45m.
- Ratepayer benefits + private arbitrage ($49.5k-$208.5k/MW-yr) only partially justify the AB 2514 mandate cost (~$6.5m/MW in 2016).

## 8. Limitations (stated + critical reading)
- Measurement error in node assignment (attenuation); short-run within-season identification only; dispatch unobserved; cannot separate merit-order vs congestion vs market-power channels.
- Transfers (price reductions) not welfare; batteries in sample are small and early, so linear per-MW extrapolation to today's fleets is unsafe (cf. cannibalisation in butters2025).

## 9. Relevance to my study
Shows how to recover locational/system effects of storage when the network (or, analogously, the co-optimisation of products) is a black box. GB analogue: zonal effects in BM (constraint-driven BOAs/skip rates) and in the EAC (locational requirements are limited, but DM/DR volumes by EFA block). The sparse-effect + double-selection idea transfers to "which products/periods does battery entry move?"

## 10. Lineage links
- Builds on: lamp2022_caisobatteryarbitrage, carson2013_bulkstorageexternality, Belloni-Chernozhukov-Hansen (2014) double selection.
- Built upon by: too recent.

## 11. Verification log
- DOI resolves to SAGE Energy Journal record (search result); OpenAlex: Energy Journal, pub. date 2026-09-09, no vol/issue/pages, affiliation MSU Economics.
- SJR Energy Journal sourceid 29391: Q1 2019-2022 and 2024; Q2 2023 and 2025 -> flagged borderline.
- Full text read from author WP (Jan 2025); published version may differ.
