---
id: junge2022_efficientstorage
title: "Energy Storage Investment and Operation in Efficient Electric Power Systems"
authors: ["Junge, C.", "Mallapragada, D.", "Schmalensee, R."]
year: 2022
journal: "The Energy Journal"
volume_issue_pages: "43(6):1-24"
doi: "10.5547/01956574.43.6.cjun"
quartile: "Q1 (SJR 2022 and 2024, Economics & Econometrics; Energy (misc.); Q2 in 2023/2025)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "MIT — Richard Schmalensee (Sloan/Economics), MIT Energy Initiative (Mallapragada, Junge)"
lineage: "Extends Schmalensee's CEEPR WP 2019-009 'On the Efficiency of Competitive Energy Storage' (Boiteux–Turvey framework); numerical part uses GenX (Jenkins & Sepulveda), linking to mallapragada2020_longrunvalue."
streams: [S1_foundations_value, S7_market_design]
market_context: "theory + 'Texas-like' (ERCOT) deeply decarbonised system, 7 weather years 2007-2013 hourly; Li-ion vs hydrogen storage"
method_class: "LP (welfare-maximising capacity expansion; KKT analysis)"
evidence_read: "full text of CEEPR WP 2021-001 (https://ceepr.mit.edu/wp-content/uploads/2021/09/2021-001.pdf); journal version not read"
oa_link: "https://ceepr.mit.edu/wp-content/uploads/2021/09/2021-001.pdf"
---

## 1. Research question
In an efficient (welfare-maximising, competitive) power system with multiple generation and storage technologies, what conditions govern storage investment and operation, and do classical results (merit order, zero profit) carry over to storage?

## 2. Setting & assumptions
- Constant returns to scale; perfect foresight; T periods with exogenous inelastic demand valued at ω (VOLL = $50,000/MWh in numerics); prices not capped below VOLL.
- Storage with separate charge power P^A, discharge power P^D and energy capacity E (separately costed), self-discharge χ, efficiencies r_A, r_D; terminal S_T = S_0.
- Dispatchable generators with ramp limits; VRE with availability ρ_t.

## 3. Constraints that drove the model choice
Need analytical results (via KKT) on investment/operation → convex LP with constant returns; to show behaviour under realistic weather variability, a multi-year hourly simulation (61,314 h) in GenX.

## 4. Model
- max W = Σ_t [ω Q_t − ω L_t − v g_t − o_A A_t − o_D D_t] − C_G G − C_R R − C_P^A P^A − C_P^D P^D − C_E E (as summarised).
- s.t. Q_t − L_t = g_t + ρ_t R − C_t − A_t + D_t (curtailment C_t; sign convention reconstructed from a garbled extraction — check paper); S_t = χ S_{t−1} + r_A A_t − D_t/r_D; ramp limits g_t − g_{t−1} ≤ β^U G etc.; capacity bounds; S_T = S_0.
- KKT results: equivalence of welfare optimum and competitive equilibrium with price λ_t; discharge when λ_t ≥ o_D + μ_t (stored-energy shadow value), charge when λ_t is sufficiently below μ_t; any storage technology with positive optimal capacity earns zero profit (energy- and power-capacity costs exactly recovered by shadow prices); **no merit-order rule for storage**; with ramp limits, marginal-cost dispatch can fail.

## 5. Data & processing
ERCOT load 2007–2013 (peak 151 GW scaled, 715 TWh/yr), NREL Wind Toolkit and NSRDB solar; costs: CCGT $817/kW, OCGT $816/kW, CCGT-CCS $1,797/kW, wind $1,085/kW, PV $725/kW; Li-ion $125/kWh + $244/kW; hydrogen $7/kWh + $1,159/kW; CO2 limit e.g. 1 gCO2/kWh.

## 6. Justification (why the authors argue the approach is valid)
Theorems from KKT conditions; numerical case illustrates theory (e.g., Fourier decomposition of storage cycling showing energy-cost ratio sets cycling frequency).

## 7. Key results
- At 1 gCO2/kWh: H2 energy capacity 1,280 GWh vs Li-ion 130 GWh; Li-ion ~220 discharges/yr (daily), H2 ~20 (seasonal); system cost ~$50.7/MWh.
- Li-ion cycling 38 % daily / 32 % weekly modes; H2 68 % seasonal.
- Capital cost of **energy capacity** is critical: ratio of energy- to power-capacity cost determines duration and operating pattern.
- Competitive markets with prices reaching VOLL support efficient storage investment; price caps below VOLL create missing money.

## 8. Limitations (stated + your critical reading)
- Stated: constant returns; perfect foresight (no precautionary storage); no ancillary services; single zone; price caps.
- Critical: zero-profit result is long-run — tells nothing about transitional profitability; relies on scarcity rents at VOLL, which real market rules (caps, capacity mechanisms, administrative scarcity pricing) reshape.

## 9. Relevance to my study
Theoretical anchor: in an ideal market storage earns exactly its capital cost via energy prices (incl. scarcity rents). Any observed excess/deficit profitability can therefore be attributed to deviations — **market rules** (caps, product definitions, capacity payments) or transitional disequilibrium. Useful as the "null model".

## 10. Lineage links
- Builds on: Boiteux (1949)/Turvey peak-load pricing; Schmalensee CEEPR WP 2019-009; desisternes2016_decarbvalue; mallapragada2020_longrunvalue.
- Built upon by (notable): antweiler2025_newmeritorder (energy-only viability with storage).

## 11. Verification log
- Crossref (10.5547/01956574.43.6.cjun): authors, MIT affiliations, Energy Journal 43(6):1–24, Nov 2022 ✔.
- SJR Energy Journal (id 29391): Q1 2022, 2024; Q2 2023, 2025 ✔ (flag borderline).
- Full text: CEEPR WP 2021-001 (Jan 2021); final journal version may differ in numbers/notation.
