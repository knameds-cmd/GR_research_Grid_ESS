---
id: williams2022_marketpower
title: "Electricity storage and market power"
authors: ["Williams, O.", "Green, R."]
year: 2022
journal: "Energy Policy"
volume_issue_pages: "164:112872"
doi: "10.1016/j.enpol.2022.112872"
quartile: "Q1 (SJR 2022, Energy (misc.); Management, Monitoring, Policy & Law)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Richard Green (Imperial College Business School; EPSRC 'Energy Storage for Low Carbon Grids' programme)"
lineage: "Green: supply-function equilibrium tradition (Green & Newbery 1992 JPE). Williams at Imperial Business School; PhD-student status under Green NOT verified."
streams: [S7_market_design]
market_context: "GB wholesale energy market, near-future 2020s system (30 GW wind, 18 GW PV, 43 GW fossil), daily-cycling storage"
method_class: "welfare-maximisation LP / Cournot equilibrium (complementarity-style) on enhanced merit-order stack"
evidence_read: "full text (Gold OA, CC BY; Spiral copy https://spiral.imperial.ac.uk/server/api/core/bitstreams/26e646f9-4aa0-4b00-bf1b-1e8877550089/content)"
oa_link: "https://www.sciencedirect.com/science/article/pii/S0301421522000970"
---

## 1. Research question
How would arbitrage by daily storage change time- and demand-weighted prices, consumer welfare and generator profits in GB in the 2020s, and how much of the welfare gain is lost if storage operators and/or generators exercise market power?

## 2. Setting & assumptions
- 2x2 design: generators competitive vs Cournot oligopoly (N = 8, HHI ~0.125); storage price-taking vs Cournot (N = 4 symmetric operators); storage independent of generators.
- Half-hourly, perfect foresight within each day; daily SoC closure; eta = 0.9; demand elasticity -0.1.
- Storage scenarios: 5 GW/25 GWh, 5 GW/50 GWh, 10 GW/50 GWh. Energy arbitrage only.

## 3. Constraints that drove the model choice
Need endogenous prices (storage large enough to move them) and market-power counterfactuals for both sides; a standard merit order misses part-load/start-up price patterns, so an "enhanced merit-order stack" with multiple tranches per thermal unit is used to keep the problem convex while reproducing realistic price shapes.

## 4. Model
- Competitive case: max gross consumer surplus - variable generation cost s.t. energy balance (demand + charge = generation + discharge), SoC dynamics, capacity limits, daily cycle closure; wind/solar must-run with curtailment.
- Market power: objective augmented with perceived inverse-demand-slope terms beta_g (generators) and beta_s (storage) -> Cournot-equivalent first-order conditions.

## 5. Data & processing
National Grid half-hourly transmission demand 2014 (held constant); renewables.ninja load factors with 2014 weather; fuel+carbon cost ~GBP 26/MWh-fuel; baseline wholesale turnover ~GBP 13bn/yr.

## 6. Justification
Calibrated price shapes via enhanced stack; factorial counterfactuals isolate each source of market power; storage size sensitivities.

## 7. Key results
- Welfare gain from price-taking storage GBP 181-247m/yr; with strategic storage GBP 167-211m/yr (gain reduced 4-21%; cost of storage market power GBP 9-52m/yr).
- Generation market power costs more (~GBP 68-87m/yr) than storage market power.
- Conventional generators lose GBP 168-347m/yr; renewables gain GBP 47-138m/yr; consumer gains roughly mirror conventional losses.
- Strategic 5 GW/25 GWh fleet discharges 6.42 TWh vs 8.44 TWh price-taking (-24%).
- Arbitrage profit before fixed costs (~GBP 105-174m) is near or below estimated fixed costs -> arbitrage alone insufficient for battery cost recovery.
- CO2 rises < 1 Mt/yr (charging losses vs less curtailment).

## 8. Limitations (stated + critical reading)
Daily arbitrage only - no balancing services, reserves (e.g., DC/DM/DR), capacity market or network value, which dominated GB battery revenue; exogenous storage capacity; no transmission constraints; low elasticity may overstate market-power effects. Critical: perfect foresight within day overstates arbitrage capture.

## 9. Relevance to my study
The GB-specific benchmark for energy-arbitrage welfare and for the competitive-vs-strategic counterfactual. Its "factorial counterfactual" design (2x2 conduct x storage size grid) is directly reusable for attributing GB battery outcomes to market rules vs competition. It also documents that arbitrage alone does not recover battery costs in GB -> motivates multi-product rules as the profitability driver.

## 10. Lineage links
- Builds on: sioshansi2010_ownership, sioshansi2014_welfareloss; Green & Newbery 1992 SFE.
- Built upon by (notable): andrescerezo2023_marketstructure is contemporaneous (Spain); not verified further.

## 11. Verification log
- RePEc IDEAS (eee/enepol/v164y2022ics0301421522000970): title, authors, vol 164, 2022, DOI; Spiral record: article number 112872, Gold OA CC BY, published online 11 Mar 2022.
- SJR: scimagojr sourceid 29403, Q1 2017-2024 both categories.
- Full text read from Spiral bitstream (publisher PDF); funding EPSRC EP/K002252/1.
