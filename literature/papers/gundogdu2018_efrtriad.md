---
id: gundogdu2018_efrtriad
title: "A Battery Energy Management Strategy for U.K. Enhanced Frequency Response and Triad Avoidance"
authors: ["Mantar Gundogdu, B.", "Nejad, S.", "Gladwin, D.T.", "Foster, M.P.", "Stone, D.A."]
year: 2018
journal: "IEEE Transactions on Industrial Electronics"
volume_issue_pages: "65(12):9509-9517"
doi: "10.1109/TIE.2018.2818642"
quartile: "Q1 (SJR 2018, Electrical and Electronic Engineering; Control and Systems Engineering)"
group: "David Stone / Martin Foster / Dan Gladwin, Electrical Machines & Drives group, University of Sheffield (Willenhall 2 MW/1 MWh BESS)"
lineage: "Gundogdu PhD thesis, University of Sheffield 2019 (White Rose eTheses id 24593) under the Stone/Foster/Gladwin group."
streams: [S6_ancillary_products]
market_context: "GB EFR (Service-2, narrow deadband) + TNUoS Triad avoidance"
method_class: "rule-based EMS + simulation + field experiment"
evidence_read: "full text (accepted manuscript, https://eprints.whiterose.ac.uk/id/eprint/129204/8/BESS_EFR_TRIAD2018.pdf)"
oa_link: "https://eprints.whiterose.ac.uk/129204"
---

## 1. Research question
How can a BESS deliver GB EFR while managing SoC to keep 100% availability, and can EFR be stacked with Triad avoidance (TNUoS peak) revenue?

## 2. Setting & assumptions
- Real asset: Willenhall ESS, 2 MW / 1 MWh Toshiba lithium-titanate, 11 kV, 2 MVA 4-quadrant converter; operational SoC 5–95%.
- Efficiencies: inverter 97%, battery charge 94%, discharge 94%.
- EFR envelope points (Service-2): ±0.015 Hz deadband; full power at 49.5 / 50.5 Hz; ±9% of rated power allowed inside deadband; breakpoints at 49.75 Hz (44.44% S1 / 48.45% S2) and 49.95/50.05 Hz (9%). Full output within 1 s. Ramp limits per zone. Service Performance Measure (SPM) reduces payment when outside envelope.
- Rule exploited: if frequency stays outside deadband > 15 min, provider may rest output for 30 min.
- Price-taker; deterministic simulation on historic days.

## 3. Constraints that drove the model choice
Second-scale compliance (envelope, ramp) must be checked on measured frequency, so a Simulink-type EMS with discrete rules is used rather than optimisation; Triad dates are unknown ex ante, so a warning-triggered SoC-preparation rule is used.

## 4. Model
- Model-1: choose upper/zero/lower envelope line depending on SoC vs target band 45–55% (uses envelope flexibility to steer SoC).
- Model-2: + extended-event timer (15 min outside deadband → 0 output for 30 min).
- Model-3: + charge/discharge at ±9% during rest period to return SoC to band.
- Triad: on warning, SoC target 90–95%; export profile 16:00–19:00 (200/500/300/200/100 kW blocks).
- SoC: SoC_out = SoC_init + ∫P dt/(3600 Q); η_c=η_d=0.94.

## 5. Data & processing
NGET measured frequency at 1 s for selected days: 21 Oct 2015, 4 Dec 2014, 19 Jan 2015, 2 Feb 2015, 20 Dec 2015. Experimental validation on WESS for a 12-h period (21 Oct 2015 trace).

## 6. Justification
Model vs hardware: SoC RMSE 0.19%, SoC MAPE 0.31%, power MAPE ~4.5% (inverter efficiency at < 100 kW).

## 7. Key results
- 21 Oct 2015: Model-1 hits 0% SoC → SPM 0.9828, availability 98%; Models 2–3 min SoC 30.7% / 32.3%, SPM 1.0, availability 100%.
- Triad revenue per event (prep at 10:00): £2,583–3,733 (Model-2) vs £3,229–3,753 (Model-3); Model-3 adds up to £646 (20 Dec 2015, many extended events).
- Earlier Triad preparation (10:00 vs 13:00) yields higher achievable SoC.
- Import/export energy on 21 Oct 2015 falls from 1,744/1,470 kWh (Model-1) to ~1,185–1,225/950–957 kWh (Models 2–3).

## 8. Limitations (stated + your critical reading)
- Few test days; no annual revenue or degradation quantification.
- Triad income assumes correct Triad prediction; Triad mechanism was abolished in 2022 (TCR), so stacking result is historical.
- Relies on the 15-min/30-min rest allowance specific to EFR.

## 9. Relevance to my study
Clean example of how specific rule allowances (±9% in deadband, envelope width, 30-min rest after 15-min events) are the SoC-management levers; shows availability/SPM penalties depend on exploiting them. Rule parameters directly reusable in a GB product-rule attribution model.

## 10. Lineage links
- Builds on: National Grid EFR specification (2016); greenwood2017_efrservicedesign (same service).
- Built upon by (notable): Gundogdu et al. FFR + arbitrage strategies (Sheffield, not archived); cao2024_dcvsefr compares EFR with DC.

## 11. Verification log
- White Rose record 129204 + OpenAlex works/doi:10.1109/TIE.2018.2818642: title, 65(12):9509-9517, all authors Sheffield.
- SJR sid 26053: IEEE TIE Q1 2018.
- Full text read (accepted manuscript). Triad rate reported as "£45.6/kWh" in extraction — likely £/kW; not used here.
