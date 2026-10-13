---
id: martins2021_ukbusinessmodels
title: "A techno-economic assessment of battery business models in the UK electricity market"
authors: ["Martins, J.", "Miles, J."]
year: 2021
journal: "Energy Policy"
volume_issue_pages: "148(Part B):111938"
doi: "10.1016/j.enpol.2020.111938"
quartile: "Q1 (SJR, journal-level: Energy Policy is Q1 in Energy (misc.) and Management, Monitoring, Policy & Law in the archive's checks for 2007, 2018, 2022 and 2024/2025; SJR 2021 itself not re-checked in this session)"
quartile_basis: "latest-only; rule=unchecked; SJR 2021 (publication year) not checked — archive entries record Energy Policy Q1 for 2007 (walawalkar2007), 2018 (sakti2018), 2022 (williams2022) and 2025 (he2011); no adjacent-year bracket on both sides"
group: "John Miles, Engineering Department, University of Cambridge"
lineage: "Extends the Matlab models of Rappaport & Miles (2017) (aggregated domestic batteries for frequency response and reserve). Miles also co-authored Teng et al. (2015, ICE Energy) on the value of storage in the UK."
streams: [S1_foundations_value, S2_stacking_cooptimization, S6_ancillary_products]
market_context: "UK 2018 (pre-DC): DA (N2EX) and 'BM market' (Elexon) arbitrage, STOR, Fast Reserve, Dynamic FFR, Capacity Market; co-location with residential PV (SEG) and offshore wind (PPA)"
method_class: "LP"
evidence_read: "full text (published version, PDF supplied by user 2026-10-13; not open access — do not redistribute)"
oa_link: ""
---

## 1. Research question
From a business owner's perspective, which battery business models are profitable in the UK electricity market (arbitrage, Capacity Market, frequency response, reserve, co-location with renewables), for three battery chemistries, and which policy mechanisms matter?

## 2. Setting & assumptions
- **Data year**: 2018 only (most recent full year at the time). DA prices from Nord Pool (private communication); "BM market" prices from Elexon's portal (half-hourly; used as a tradable arbitrage price).
- **Batteries** (Table 2): advanced lead-acid (ALA, £100/kWh, RTE 82%), Li-ion NMC (LI, £216/kWh, RTE 91%), lithium titanate (LI-Ti, £563/kWh, RTE 95%); discharge C-rate 2; SoC limited to 90% DoD.
- **Foresight**: LP with perfect foresight, then revenue scaled by a "forecasting parameter" — 80% of the perfect-foresight value in DA, 50% in BM.
- **Ancillary services (2018/19 tender results)**:
  - STOR: availability windows 06:00–11:00 and 17:00–20:00, average £4.12/MW/h (range 0.5–11.5); sustain ≥2 h.
  - **FR = Fast Reserve** (not frequency response): window 06:00–23:00, average £8.15/MW/h (range 4–9); response within 2 min, sustain ≥15 min, minimum 25 MW.
  - Reserve share = 50% of maximum discharge, with energy headroom reserved.
  - DFFR (dynamic FFR): 24/7 availability, so no stacking with arbitrage; £10/MW/h; simulated on 2018 frequency data with a 10% energy response beyond ±0.015 Hz and full response beyond ±0.2 Hz.
- **Capacity Market**: clearing price scenarios £1/5/10 per kW; 1/3/5 stress events per year (benchmarked on 2005–2016 NISMs, average 2.5); penalty risk 0.25/0.5/0.75; average payment of £200k/yr added in the final economics.
- **Economics**: 10-year NPV and payback, 7% discount rate; inverter costs included (£65/kW large-scale; £900 per home domestic).
- Asset size: 50 MWh (framed as 5,000 aggregated 10 kWh home batteries or one large installation).

## 3. Constraints that drove the model choice
- Transparent, adaptable Matlab LP inherited from Rappaport & Miles (2017).
- Services are modelled **separately** (arbitrage alone; arbitrage + STOR; arbitrage + FR; DFFR alone) rather than co-optimised.
- Forecast uncertainty represented by a fixed haircut rather than a forecasting model.

## 4. Model
- Objective (Eq. 5): max Σ_t Pr·(Dr − Cr) − Dr·DisCost, with discharge cost from capital cost / (cycle life × usable energy × efficiency) and an iterative correction factor matching modelled and calculated cycling costs (Eqs. 6–8).
- Constraints: SoC balance (Eq. 1); SoC bounds (Eq. 2); charge/discharge limits from C-rates (Eqs. 3–4); during service windows, discharge capacity reduced by the reserved amount and SoC floor raised by the headroom (Eqs. 9–10).
- DFFR: rule-based SoC simulation on second-level frequency (Eqs. 11–12), cycle life from average DoD.
- Renewables: "Forecasting" (LP + haircut) vs "Threshold" algorithm (charge/discharge when BM price is 1/3 standard deviation below/above its 2018 mean).

## 5. Data & processing
- 2018 DA and BM prices; NG-ESO 2018/19 STOR and Fast Reserve tender reports; NG-ESO 2018 frequency data; EMR portal CM auction data; NISM counts 2005–2016; UKPN 2014 domestic PV data; Renewables.ninja for Scroby Sands (60 MW) offshore wind.

## 6. Justification
- The forecasting haircuts (80% DA, 50% BM) are justified by citing other storage-forecasting studies.
- Threshold vs forecasting comparison shows the LP-based revenue is reached only at higher capture levels for low-C-rate batteries.
- Sensitivity of NPV and payback to CM payment (±50%), inverter cost (±10%), battery cost (+15/−10 or −20%) and discount rate (±2.5 pp).

## 7. Key results
- **Arbitrage**: BM-based arbitrage revenue exceeds DA for all chemistries (ALA +139%; LI-Ti more than double), driven by C-rate and BM volatility. Arbitrage alone is not viable: payback 16.9 yr (ALA), >20 yr (LI, LI-Ti).
- **Arbitrage + Fast Reserve**: best case. NPV £12.6m (ALA), £7.9m (LI); payback 3.3 yr (ALA), 5.7 yr (LI).
- **DFFR only**: NPV ≈£5.2m (LI, LI-Ti); payback < 9 yr for all chemistries (abstract: 6.6 yr for Li-ion frequency response).
- **Arbitrage + STOR**: payback 9.4 yr (ALA), 15.1 yr (LI); STOR's short windows leave room for arbitrage.
- **CM**: annual revenue £34k–£490k depending on clearing price and penalty risk — highly uncertain.
- **Renewables co-location**: charging from PV pays when SEG ≤ 4 p/kWh; from wind when PPA ≤ £40/MWh; but NPVs/paybacks unattractive.
- Low-cost ALA (£80/kWh) makes ancillary scenarios pay back in < 10 yr.

## 8. Limitations (stated + critical reading)
- Stated: one battery in the market — **"a saturated market with existing battery systems would reduce profitability"** because the ancillary markets are "quite shallow"; uncertain SEG/PPA rates; simplified costs (no BOS, O&M overheads).
- Critical reading:
  - "BM market" arbitrage assumes one can trade at the Elexon BM/system price without volume limits; this overstates achievable value (compare gale2026's NIV constraint).
  - Single year (2018), fixed revenue haircut, services not co-optimised (Gale 2026 makes the same critique).
  - All products studied (STOR, Fast Reserve, DFFR) have since been replaced (SR 2026, QR 2024, DC/DM/DR 2020–22).

## 9. Relevance to my study
- **Pre-DC baseline** of UK battery business models (2018): the "before" point for the regime story (R2 in `literature/context/GB_market_history_EN.md`). Shows that before DC, viability relied on Fast Reserve / DFFR availability fees plus CM, and that arbitrage alone did not pay.
- The authors' saturation warning (shallow ancillary markets) anticipated the 2023 DC collapse — a useful citation for the regime-dependence hypothesis.
- Reserve-headroom constraint (Eqs. 9–10) is the same structure as our Layer 1 service constraints.

## 10. Lineage links
- Builds on: Rappaport & Miles (2017); staffell2016_maxvalue (reserve can triple revenue); Teng et al. (2015).
- Built upon by: gale2026_balancingbatteries (cites as ref. [50] and critiques separate-service modelling).

## 11. Verification log
- 2026-10-07: bibliographic data from search results.
- 2026-10-13: **full text read** from the published PDF supplied by the user (© Elsevier, all rights reserved — not committed to the repo). Confirmed: received 9 Feb 2020, revised 29 Aug 2020, accepted 28 Sep 2020, online 25 Nov 2020; Cambridge Engineering affiliation for both authors.
