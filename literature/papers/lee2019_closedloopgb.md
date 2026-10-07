---
id: lee2019_closedloopgb
title: "A closed-loop analysis of grid scale battery systems providing frequency response and reserve services in a variable inertia grid"
authors: ["Lee, R.", "Homan, S.", "Mac Dowell, N.", "Brown, S."]
year: 2019
journal: "Applied Energy"
volume_issue_pages: "236:961-972"
doi: "10.1016/j.apenergy.2018.12.044"
quartile: "Q1 (SJR 2019, Energy Engineering and Power Technology)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Solomon Brown, Dept. Chemical & Biological Engineering, University of Sheffield; with Niall Mac Dowell (Imperial College London, Centre for Environmental Policy)"
lineage: "Brown (Sheffield) corresponding; Mac Dowell (Imperial) co-author. Lee/Homan PhD supervision by Brown not verified."
streams: [S6_ancillary_products]
market_context: "GB EFR (Service 2) and STOR reserve, 2015 vs 2025 inertia scenarios"
method_class: "closed-loop swing-equation simulation (no optimisation)"
evidence_read: "full text (accepted manuscript, http://eprints.whiterose.ac.uk/140156/3/Manuscript_clean.pdf)"
oa_link: "http://eprints.whiterose.ac.uk/140156/"
---

## 1. Research question
How do system inertia, load damping and battery fleet size change battery cycling when batteries provide GB frequency response (EFR) and reserve (STOR), accounting for the feedback of the batteries on frequency itself?

## 2. Setting & assumptions
- EFR Service 2: deadband 49.985–50.015 Hz; full output at 49.5/50.5 Hz within 1 s; ±9% allowed in deadband. SoC rule: target 47.5–52.5%; charge at 9% below 47.5%, discharge at 9% above 52.5%.
- STOR: 2-h dispatch; battery contracts 100 MW of a 200 MW system; SoC raised to 90% half an hour before window; half-hour recharge at 100 MW after dispatch.
- Batteries: 200 MW/100 MWh (EFR), 100/400 MW variants; 200 MW/250 MWh (EFR+STOR). Lossless; 0.5 s response delay.
- Inertia constants by technology (nuclear 5 s, CCGT 8 s, coal/OCGT/biomass 4 s, hydro 3.5 s, RES/interconnectors 0 s); load damping 2.5%/Hz (sensitivity 2.0%/Hz).

## 3. Constraints that drove the model choice
Open-loop replay of historic frequency ignores that batteries change frequency; a closed-loop swing-equation model is needed to back out the underlying imbalance and re-simulate frequency with batteries and future inertia.

## 4. Model
- Inertia I_m = 2E_s/ω0², E_s from committed generation mix.
- Imbalance back-calculated from 1-s frequency + half-hourly generation: D_{t,f0} = D_{t,ft}/(1-0.025(f0-ft)) + I_m(ω_t²-ω_{t-1}²)/(2Δt); frequency re-simulated with battery response.
- Monte-Carlo realisations (25) for STOR dispatch; Poisson wind-loss events (0–360 MW).

## 5. Data & processing
National Grid 1-s frequency, week commencing 1 June 2015; Elexon half-hourly generation; Sheffield PV_Live solar; 2025 mix from NG Future Energy Scenarios.

## 6. Justification
Reproduces observed frequency statistics (σ≈0.055 Hz 2015); sensitivity on inertia and damping.

## 7. Key results
- 2015→2025 inertia drop alone barely changes frequency volatility (σ ≈0.055 → 0.058 Hz with 200 MW EFR).
- Cycling falls with fleet size: ~2.8 (100 MW), ~1.4 (200 MW), ~0.9 (400 MW) equivalent full cycles/day; DoD stays < 10%.
- Lower load damping (2.0%/Hz) substantially raises battery response and SoC volatility.
- Adding STOR superimposes 20–80% DoD cycles on EFR micro-cycling; in sample runs EFR potentially undeliverable 3.25 h on average.

## 8. Limitations (stated + your critical reading)
One summer week; no degradation model (chemistry unknown); single aggregated battery; no economics. Lossless battery hides recharge energy cost.

## 9. Relevance to my study
Shows that per-MW battery cycling (hence degradation cost per £ of availability revenue) is endogenous to total procured volume — a product-volume effect relevant for attributing profitability to rules (saturation reduces cycling, not only prices). Closed-loop imbalance back-calculation is reusable for counterfactual frequency traces under different product mixes.

## 10. Lineage links
- Builds on: greenwood2017_efrservicedesign; NG EFR/STOR specifications.
- Built upon by (notable): cao2024_dcvsefr (closed-loop DC vs EFR).

## 11. Verification log
- OpenAlex works/doi:10.1016/j.apenergy.2018.12.044 (online 2018, issue vol 236 Feb 2019): authors/affiliations (Lee, Homan, Brown: Sheffield; Mac Dowell: Imperial). IDEAS RePEc page: abstract.
- SJR sid 28801: Applied Energy Q1 2019.
- Full text (accepted manuscript) read.
