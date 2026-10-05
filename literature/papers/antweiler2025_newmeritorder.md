---
id: antweiler2025_newmeritorder
title: "The new merit order: The viability of energy-only electricity markets with only intermittent renewable energy sources and grid-scale storage"
authors: ["Antweiler, W.", "Muesgens, F."]
year: 2025
journal: "Energy Economics"
volume_issue_pages: "145:108439"
doi: "10.1016/j.eneco.2025.108439"
quartile: "Q1 (SJR 2024/2025, Economics & Econometrics; Energy (misc.))"
group: "Werner Antweiler (UBC Sauder School of Business) and Felix Müsgens (Chair of Energy Economics, BTU Cottbus-Senftenberg)"
lineage: "Independent economics groups; builds on peak-load pricing/storage efficiency literature incl. junge2022_efficientstorage."
streams: [S1_foundations_value, S7_market_design]
market_context: "greenfield 100% wind+solar+storage (Li-ion battery, hydrogen) energy-only market; calibrated to ERCOT and Germany hourly 2019-2022"
method_class: "analytical long-run equilibrium + NLP numerical (free-entry zero-profit)"
evidence_read: "full text of working-paper version (Ruhr Economic Papers #1064, https://www.rwi-essen.de/fileadmin/user_upload/RWI/Publikationen/Ruhr_Economic_Papers/REP_24_1064.pdf); journal version (CC BY-NC-ND) not read"
oa_link: "https://doi.org/10.1016/j.eneco.2025.108439"
---

## 1. Research question
Can an energy-only market remain viable (recover all fixed costs, avoid permanent zero prices) in a system with only zero-marginal-cost renewables and grid-scale storage, and how are prices formed in such a system?

## 2. Setting & assumptions
- Perfect competition, free entry, single node, perfect foresight; long-run equilibrium (greenfield).
- Linear, mildly price-responsive demand (response capped ~5 %).
- Technologies: onshore wind, utility PV, Li-ion battery (RTE 85 %), hydrogen electrolyser–fuel cell (RTE 31 %); storage energy capacity treated as unlimited (only power capacity priced).
- Hourly data 2019–2022 (35,064 h) for ERCOT and Germany; 2020 and 2050 cost scenarios (IEA-based).

## 3. Constraints that drove the model choice
Need closed-form insight into price formation with zero marginal costs → simplified single-RES/single-storage linear model; realistic weather correlation → numerical model on hourly data.

## 4. Model
- Inverse demand p = θ(q − x + z) ≥ 0 (as summarised).
- Storage balance over the year: η_S Σ max{0,−s_t} x̄_S = Σ max{0,s_t} x̄_S (energy bought × efficiency = energy sold).
- Planner: min C = Σ_i f_i x̄_i + Σ_t p(x̄)²/(2θ) (fixed costs + welfare loss from demand response), equivalent to free-entry zero-profit conditions f_i = Σ_t utilisation_{i,t}·p_t.
- Result structure ("new merit order"): storage types differentiated by efficiency set distinct buying prices and a pooled selling price; five price zones from scarcity peak to zero (curtailment).

## 5. Data & processing
ERCOT and German (SMARD/Bundesnetzagentur) hourly demand and VRE availability 2019–2022; 2,520 cost-parameter combinations for sensitivity.

## 6. Justification (why the authors argue the approach is valid)
Analytical solution of simplified model + numerical calibration on two contrasting systems; extensive cost sensitivity; explicitly framed as "outer limits of feasibility", not a forecast.

## 7. Key results
- Energy-only market "still works": prices stay positive most hours because storage opportunity costs set prices; capacity mechanisms unnecessary unless prices are capped.
- ERCOT 2050 costs: average price ≈ $40.76/MWh, ~0.5 % curtailment, < 0.3 % hours at peak prices; 2020 costs ≈ $62.34/MWh.
- Germany 2050 costs: ≈ €63.54/MWh with 7.5 % curtailment; 2020 costs ≈ €90.64/MWh (battery-only).
- Storage-to-RES capacity ratio stable (~0.25–0.30 ERCOT, ~0.28 DE) across cost variations.

## 8. Limitations (stated + your critical reading)
- Stated: greenfield; four technologies only; unlimited storage energy capacity; single node; stylised demand response; uncertain H2 costs; not a forecast.
- Critical: unlimited energy capacity removes the energy-cost trade-off emphasised by junge2022_efficientstorage; perfect foresight/competition remove risk premia and market power; ancillary services absent.

## 9. Relevance to my study
Most recent theoretical statement that **storage becomes the price-setter** in high-VRE energy-only markets and that price caps are the key rule breaking cost recovery — gives a mechanism to test (do observed battery margins track storage-opportunity-cost pricing?).

## 10. Lineage links
- Builds on: junge2022_efficientstorage; mcconnell2015_energyonly (energy-only + storage); peak-load pricing theory.
- Built upon by (notable): too recent to assess.

## 11. Verification log
- Crossref (10.1016/j.eneco.2025.108439): title, authors (ORCIDs), Energy Economics 145, article 108439, May 2025, licence CC BY-NC-ND 4.0 ✔.
- SSRN 4702939 / EconStor 10419/282991 / RWI REP #1064 working-paper versions identified ✔.
- SJR Energy Economics Q1 2024/2025 ✔.
- Numbers from WP (2024); journal version may differ. Some cost-unit figures in the extraction were ambiguous and are omitted.
