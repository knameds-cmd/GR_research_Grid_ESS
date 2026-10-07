---
id: mcconnell2015_energyonly
title: "Estimating the value of electricity storage in an energy-only wholesale market"
authors: ["McConnell, D.", "Forcey, T.", "Sandiford, M."]
year: 2015
journal: "Applied Energy"
volume_issue_pages: "159:422-432"
doi: "10.1016/j.apenergy.2015.09.006"
quartile: "Q1 (SJR 2014/2016 and 2024/2025, Energy (misc.) and others)"
quartile_basis: "bracketed; rule=pass; Q1 in SJR 2014 and 2016 (publication year 2015 itself not checked)"
group: "Melbourne Energy Institute, University of Melbourne (Mike Sandiford, director); Australian-German College of Climate & Energy Transitions"
lineage: "MEI group; McConnell later prominent NEM analyst (Climate & Energy College). No advisor ties claimed."
streams: [S1_foundations_value, S7_market_design]
market_context: "Australian NEM (South Australia focus), energy-only gross pool, 5-min dispatch / 30-min settlement, market price cap A$13,100/MWh, FY2002-2014"
method_class: "LP"
evidence_read: "full text (author copy, https://msandifo.github.io/pdfs/peer/2015_AppEnergy.pdf)"
oa_link: "https://msandifo.github.io/pdfs/peer/2015_AppEnergy.pdf"
---

## 1. Research question
What is the arbitrage and capacity (cap-contract) value of a price-taking storage device in an energy-only market with a very high price cap, how does it vary with storage hours and efficiency, and can storage (e.g., PHES) compete with an OCGT peaker?

## 2. Setting & assumptions
- Price-taker; perfect foresight (full year) and a forecast case using AEMO day-ahead pre-dispatch prices in a rolling half-hourly re-optimisation.
- Half-hourly settlement prices (RRP); FY2002–2014, case study FY2012–13; SA region (31 % wind 2013–14).
- Storage 0.5–10 h; unit power for charge/discharge; base round-trip efficiency 75 %.
- Market: energy-only, price cap A$13,100/MWh (~300× volume-weighted average ~A$45), floor −A$1,000/MWh; FCAS ignored (<0.3 % of spot revenue).
- Capacity value via selling A$300/MWh cap contracts.

## 3. Constraints that drove the model choice
Transparent upper-bound valuation over many years and regions → LP; real forecasts (pre-dispatch) used to test non-anticipativity without building a forecasting model.

## 4. Model
- max Σ_t RRP_t (d_t − c_t) s.t. s_t = s_{t−1} + η(c_t − d_t) (as transcribed from the extraction; exact placement of η not double-checked), 0 ≤ s_t ≤ s_max, 0 ≤ c_t, d_t ≤ 1.
- Rolling version: re-solve each half hour with latest pre-dispatch price vector.
- Solver: COIN-OR CLP.
- Levelised cost of capacity (LCOC) comparison PHES vs OCGT, netting arbitrage revenue below A$300/MWh.

## 5. Data & processing
AEMO half-hourly RRP and pre-dispatch forecasts, FY2002–2014, all NEM regions (SA detailed). Value reported per kW-yr and decomposed by day; distributions of discharge prices (median vs volume-weighted).

## 6. Justification (why the authors argue the approach is valid)
Perfect foresight as upper bound; pre-dispatch strategy recovers ~85 % (comparable to Sioshansi et al. backcast 85 % and Connolly et al. 81 %), so the bound is informative especially for longer durations.

## 7. Key results
- ~90 % of potential value captured with 4 h; little marginal value beyond 6 h.
- Value is spike-driven: practically all arbitrage profit earned on a few days when price hits the cap; e.g., FY2008 median discharge price A$48.85/MWh vs volume-weighted A$189.13/MWh.
- Annual value highly variable: ~A$30/kW-yr (low-volatility years) to > A$200/kW-yr (drought years 2008–10); FY2012–13, 6 h: ~A$65–80/kW-yr (read from figure).
- Pre-dispatch forecast: 85 % of perfect-foresight value at 6 h (70 % at 3 h → > 90 % at 8 h).
- Round-trip efficiency nearly irrelevant because revenue concentrates at the cap — contradicts PJM-based literature.
- Cap contracts stabilise revenue; PHES may compete with new OCGT under the right conditions.

## 8. Limitations (stated + your critical reading)
- Stated: static prices (no price impact), energy market only, no network/location value, ownership questions open, market then oversupplied (~37 % overhang).
- Critical: findings hinge on the price cap level and scarcity frequency — exactly the market-design parameters; no degradation; FCAS market has since grown sharply (post-2017 batteries earn mostly FCAS).

## 9. Relevance to my study
Clean demonstration that a **market rule (price cap / scarcity pricing)** determines the shape of storage value (spike-concentrated, efficiency-insensitive, duration-saturating at 4–6 h). Directly reusable as a design point when contrasting energy-only (NEM, ERCOT) vs capacity-market systems (GB, PJM).

## 10. Lineage links
- Builds on: sioshansi2009_pjmvalue; bradbury2014_rtarbitrage; Connolly et al. (2011).
- Built upon by (notable): NEM battery studies; antweiler2025_newmeritorder (energy-only viability with storage).

## 11. Verification log
- Author PDF header: title, authors, affiliations, Applied Energy 159 (2015) 422–432, DOI 10.1016/j.apenergy.2015.09.006 ✔.
- IDEAS handle v159y2015icp422-432 consistent ✔.
- Crossref/OpenAlex direct check not performed (rate limits) — DOI taken from publisher-typeset author copy.
- SJR Applied Energy Q1 2014, 2016 ✔ (2015 not individually checked).
