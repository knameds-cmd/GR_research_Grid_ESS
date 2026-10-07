---
id: gilmore2024_lcofcas
title: "The Levelised Cost of Frequency Control Ancillary Services in Australia's National Electricity Market"
authors: ["Gilmore, J.", "Nolan, T.", "Simshauser, P."]
year: 2024
journal: "The Energy Journal"
volume_issue_pages: "45(1):201-229"
doi: "10.5547/01956574.45.1.jgil"
quartile: "Q1 (SJR 2024, Economics and Econometrics; Energy (misc.)) — note Q2 in 2023"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Paul Simshauser, Centre for Applied Energy Economics & Policy Research, Griffith University / EPRG Cambridge; Gilmore & Nolan at Iberdrola Australia (Gilmore also Griffith)"
lineage: "Simshauser (Griffith/EPRG) applied-economics line on NEM entry costs (e.g., Simshauser 2020 Energy Journal 'On entry cost dynamics'). No advisor-student tie."
streams: [S6_ancillary_products]
market_context: "Australia NEM FCAS: regulation raise/lower, 6 s / 60 s / 5 min contingency raise/lower (and 1 s very fast FCAS from 2023)"
method_class: "levelised-cost (LCoFCAS) equilibrium-price analysis + short-run opportunity-cost pricing model"
evidence_read: "full text of working-paper version (EPRG WP 2202, https://www.jbs.cam.ac.uk/wp-content/uploads/2023/12/eprg-wp2202.pdf); journal version not read"
oa_link: "https://hdl.handle.net/10072/430817"
---

## 1. Research question
What are long-run equilibrium (levelised) prices for NEM FCAS products when supplied by utility-scale batteries, as an investment guide in the absence of forward FCAS markets?

## 2. Setting & assumptions
- Eight 5-min FCAS spot markets co-optimised with energy: regulation raise/lower (AGC, keep 50 ± 0.015 Hz ≥ 99% of time); contingency 6 s, 60 s, 5 min raise/lower; FFR (very fast, 0.5–2 s) introduced 2023.
- Utilisation (2020, 4-s data): regulation raise enabled-active in 62% of intervals, lower 31%; average utilisation 18.7% (raise) / 8.5% (lower); contingency reserves activated only for |Δf| > 0.15 Hz, near-zero energy (~0.026% activation).
- Battery: 6% pre-tax WACC, 15-y life, cell life min(4,300 cycles, 15 y), O&M $5/kWh/yr, off-peak charging $30/MWh, repowering 25% capex; capex 2-h $1,100/kW (2021) → $700/kW (2035), 4-h $1,700 → $960/kW, +$70/kW connection.

## 3. Constraints that drove the model choice
No forward FCAS curve and highly volatile, regime-switching spot prices → authors use a levelised-cost equilibrium concept (like LCOE) instead of price forecasting.

## 4. Model
- LCoFCAS = discounted cost / discounted service quantity (capacity × capacity factor × utilisation), Eq. (5).
- Short-run regulation price model for coal: P_R = (P_s − MC)(1 − k_R) when P_s ≥ MC (opportunity cost of withholding).
- Technology comparison: battery, coal, wind, solar.

## 5. Data & processing
NEM 4-s frequency (2020); AEMO frequency distributions 2012 vs 2019; Reliability Panel FOS compliance 2016–2020; FCAS volumes 2013–2021; 5-min price-setter data 2020 (NSW); time-weighted FCAS prices 2003–2021.

## 6. Justification
Compares LCoFCAS with observed prices and with opportunity-cost-based coal supply; argues spot prices mean-revert to LCoFCAS.

## 7. Key results
- Battery LCoFCAS (regulation, simultaneous raise+lower): ~$30/MW/h (2022) → ~$20/MW/h (2030); contingency: $8–10/MW/h (1-h battery, 2022) → $7–8/MW/h (2030).
- Observed bundled prices $32–59/MW/h (recent) vs ~$1.60/MW/h regulation pre-2016 → current prices above battery LCoFCAS (over-investment risk).
- Regulation consumes ~5.25 MWh/MW/day of raise energy → 3–4-h batteries optimal for regulation; deployed NEM average ~1.4 h.
- Mandatory PFR (mid-2020) uses 3–4% of warranted battery cycles (4–6% during ramp-up) unpaid; "mispriced product will be overconsumed".
- > 60% of battery revenues come from FCAS (cited empirical evidence).

## 8. Limitations (stated + your critical reading)
Equilibrium assumption; no locational/network constraints; linear degradation (~3%/yr); single-year price-setter data; working-paper numbers may differ from the published version.

## 9. Relevance to my study
Ties product parameters (utilisation/energy throughput per product, enablement duration, mandatory unpaid PFR, droop setting) to battery cost per MW/h and optimal duration — a cost-side complement to revenue-side rule attribution. Clear NEM case of "product energy content determines optimal battery duration".

## 10. Lineage links
- Builds on: Simshauser NEM entry-cost work; AEMC FFR rule change (2021).
- Built upon by (notable): rangarajan2023_batteryfcasdid (empirical FCAS price impact of batteries; S8).

## 11. Verification log
- OpenAlex works/doi:10.5547/01956574.45.1.jgil: title, 45(1):201-229, authors (Nolan Griffith CAEEPR listed), OA via Griffith hdl 10072/430817 (403 to fetcher). IDEAS RePEc EPRG WP 2202 abstract (identical wording).
- SJR sid 29391: Energy Journal Q1 2024 (Econ & Econometrics; Energy misc.), Q2 2023.
- Read: EPRG working paper 2202 (Jan 2022) full text; published-version numbers not cross-checked.
