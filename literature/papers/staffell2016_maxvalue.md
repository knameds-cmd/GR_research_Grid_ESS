---
id: staffell2016_maxvalue
title: "Maximising the value of electricity storage"
authors: ["Staffell, I.", "Rustomji, M."]
year: 2016
journal: "Journal of Energy Storage"
volume_issue_pages: "8:212-225"
doi: "10.1016/j.est.2016.08.010"
quartile: "Q1 (SJR 2017-2025, Electrical & Electronic Eng. and Energy Eng. & Power Tech.); NOTE: Q2 in 2016 (issue year)"
group: "Iain Staffell — Centre for Environmental Policy, Imperial College London"
lineage: "Imperial (Staffell/Hawkes) storage-economics line; continues to schmidt2017_experiencerates and schmidt2019_lcos (Staffell co-author). Rustomji = Imperial Energy Futures Lab."
streams: [S1_foundations_value, S2_stacking_cooptimization]
market_context: "GB 2013/14 half-hourly wholesale prices + STOR reserve (availability + utilisation); NaS and Li-ion; 322 MW Whitelee wind farm case"
method_class: "heuristic (greedy price-pairing) validated against LP"
evidence_read: "full text (published version, CC BY, Spiral: https://spiral.imperial.ac.uk/bitstreams/c18b414c-e13b-4e21-a1d1-00c8f305b0e5/download)"
oa_link: "https://spiral.imperial.ac.uk/entities/publication/b2b4762b-061d-450b-86c5-219a75eb47d3"
---

## 1. Research question
Which GB revenue streams can grid-scale batteries access, what barriers block them, and how much profit do arbitrage and arbitrage + reserve deliver under perfect and no foresight — enough to justify investment?

## 2. Setting & assumptions
- Price-taker, zero marginal cost, equal charge/discharge efficiency; GB half-hourly prices 1 Apr 2013 – 31 Mar 2014.
- NaS: $474/kW + $372/kWh, 80 % RTE, 5,500 cycles; Li-ion: $1,000/kW + $700/kWh, 90 % RTE, 6,000 cycles; C-rate 0.1–1; lifetime = cycles to 20–30 % capacity fade (degradation not optimised).
- Reserve: STOR availability ~£5/MWh, utilisation ~£89/MWh (2013/14), historic utilisation profiles.
- No foresight: price forecast = previous year's average daily profile per season.

## 3. Constraints that drove the model choice
Desire for an open, fast, transparent tool usable without LP solvers → greedy pairing algorithm (shown to reach the LP optimum for arbitrage); reserve data limited to STOR.

## 4. Model
- Arbitrage (perfect foresight): repeatedly pair highest-price discharge with lowest-price earlier charge period, remove used capacity, stop when no profitable pair (accounting for efficiency); validated against a GAMS LP.
- Arbitrage + STOR: exclude availability windows from arbitrage; ensure minimum SoC before each window, SoC ≤ capacity, ≥ 0; add utilisation discharges; corrective charging between windows.
- No foresight variants: run on forecast prices, settle on actual; reserve utilisation revealed window-by-window.
- Metrics: specific profit (£/kW-yr), rate of return vs required return given lifetime and discount rate.

## 5. Data & processing
GB half-hourly market prices 2013/14; STOR 2013/14 utilisation and prices; Whitelee wind farm final physical notifications; FX 1.5 $/£.

## 6. Justification (why the authors argue the approach is valid)
Algorithm reproduces LP optimum; sensitivity of profit to STOR utilisation randomness (±23.6 % → ~8 % profit variation); perfect vs no foresight bounds.

## 7. Key results
- Arbitrage only: ~£70/kW-yr specific profit at 100 % efficiency; rates of return NaS 1.98 %, Li-ion 1.28 %.
- Arbitrage + STOR: NaS 7.5 %, Li-ion 4.4 % — "could triple their profits" via reserve.
- No foresight: 75–88 % of perfect-foresight profit (arbitrage), 96–98 % (arbitrage + STOR); headline 75–95 %.
- Required returns for break-even ≈ 12.5–15.5 %/yr → not viable at 2016 costs; smaller (3 MW/30 MWh) more profitable per kW than 100 MW/1 GWh.
- Battery + wind time-shifting: max returns NaS 1.89 %, Li 1.22 % — not viable.
- Reviews barriers: asset classification, network-operator ownership bans, standards, liquidity (~5 % of GB trades on spot).

## 8. Limitations (stated + your critical reading)
- Stated: no economies of scale, constant cell cost, price-taker, only STOR (faster services likely more valuable), degradation not an optimisation variable.
- Critical: pre-dates GB EFR/DC auctions that later drove battery revenues; single year; no BM participation; greedy algorithm cannot handle multiple products with co-optimised headroom.

## 9. Relevance to my study
GB-specific baseline: shows reserve **product availability** changes returns by ~3×, and provides open-source algorithm + foresight capture ratios. Natural pre-DC reference point for a GB market-rule profitability study.

## 10. Lineage links
- Builds on: sioshansi2009_pjmvalue; walawalkar2007_nyisoarbitrage; Lund et al. (pairing heuristic).
- Built upon by (notable): schmidt2019_lcos; GB frequency-response studies (S5 stream).

## 11. Verification log
- Crossref (10.1016/j.est.2016.08.010): title, authors, JES 8:212–225, Nov 2016 ✔.
- Spiral record: CC BY 4.0; affiliations from full text ✔.
- SJR (id 21100400826): Q2 in 2016, Q1 2017–2025 (EEE; Energy Eng.) — flagged.
- Full published version read from Spiral.
