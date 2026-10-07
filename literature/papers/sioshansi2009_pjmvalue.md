---
id: sioshansi2009_pjmvalue
title: "Estimating the value of electricity storage in PJM: Arbitrage and some welfare effects"
authors: ["Sioshansi, R.", "Denholm, P.", "Jenkin, T.", "Weiss, J."]
year: 2009
journal: "Energy Economics"
volume_issue_pages: "31(2):269-277"
doi: "10.1016/j.eneco.2008.10.005"
quartile: "Q1 (SJR 2009 and 2023-2025, Economics & Econometrics; Energy (misc.))"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Ramteen Sioshansi (Ohio State, ISE) with NREL (Paul Denholm, Thomas Jenkin); Weiss (Point Carbon North America)"
lineage: "Core of the Sioshansi–Denholm storage-valuation line (OSU/NREL). Continues Graves, Jenkin & Murphy 1999 (Jenkin co-author). Feeds sioshansi2010_ownership and sioshansi2014_welfareloss. Advisor-student ties not claimed."
streams: [S1_foundations_value]
market_context: "PJM 2002-2007, hourly LMP (system-average and nodal), energy arbitrage only; generic bulk storage"
method_class: "LP (price-taker) / QP (price-responsive)"
evidence_read: "full text (author copy, https://www.cmu.edu/ceic/people/rsioshan/docs/pjm_arbitrage.pdf)"
oa_link: "https://www.cmu.edu/ceic/people/rsioshan/docs/pjm_arbitrage.pdf"
---

## 1. Research question
How much arbitrage value can storage capture in PJM, how does it depend on efficiency, energy-to-power ratio, fuel prices, location and foresight, and what are the welfare (consumer/producer surplus) effects once a large device moves prices?

## 2. Setting & assumptions
- Small device: price-taker with perfect foresight of hourly prices; large device (1 GW): prices respond linearly to generating load (price-maker).
- Optimised in two-week blocks with a 15-day planning horizon; hourly resolution; six years 2002–2007.
- Round-trip efficiency 80 % base (sensitivities), equal charge/discharge power κ; energy capacity h·κ with h = 1–40 h.
- Backcast test: operate each two-week window using the previous two weeks' prices, valued at actual prices.
- Energy only: capacity and ancillary revenues excluded.

## 3. Constraints that drove the model choice
Need for a transparent upper bound on arbitrage value → LP with perfect foresight; non-anticipativity examined via a simple backcast rather than stochastic programming. Price impact of large storage requires an endogenous price function → monthly linear price–load relations estimated from data turn the problem into a QP.

## 4. Model
- Price-taker: max Σ_t p_t (d_t − c_t) s.t. s_t = s_{t−1} + η c_t − d_t, 0 ≤ c_t, d_t ≤ κ, 0 ≤ s_t ≤ hκ.
- Price-responsive: p_t = a_m + b_m·(L_t + c_t − d_t) (month-specific, restricted least squares); objective becomes quadratic.
- Welfare: ΔCS from lower on-peak/higher off-peak prices × load; ΔPS from generator revenue changes; net = ΔCS + ΔPS (assuming prices = marginal cost).
- Solvers: GAMS 21.7 with CPLEX 9.0 (LP), MINOS 5.5 (QP).

## 5. Data & processing
- PJM hourly prices and loads 2002–2007 (system and individual buses for locational analysis).
- Monthly linear price–load regressions for price response.
- Backcasting = rolling two-week out-of-sample evaluation.

## 6. Justification (why the authors argue the approach is valid)
Perfect foresight = upper bound; backcast shows ≥85 % of that bound is attainable because diurnal and weekday/weekend patterns are predictable. Price response explicitly estimated to bound the price-taker overstatement.

## 7. Key results
- 12-h, 80 %-efficient device: ≈ $60/kW-yr (2002) to > $110/kW-yr (2005).
- Backcasting captures ≈ 85 % or more of perfect-foresight value.
- Duration saturation: 8 h ≈ 85 % of potential, 20 h ≈ 95 %; ~9–10 h sufficient across efficiencies.
- Gas price roughly doubled 2002→2005–07 but arbitrage value rose only 30–60 %.
- Locational premium: individual buses up to $105/kW-yr vs PJM average $77/kW-yr (2006).
- Price impact of a 1 GW device lowers arbitrage value ≈ 10 % (recent years), > 20 % in earlier years.
- Welfare (2007, 1 GW, 16 h): arbitrage $73.7 M, ΔCS +$34.6 M, ΔPS −$30.3 M, net social gain only $4.3 M → storage mainly transfers surplus from producers to consumers.

## 8. Limitations (stated + your critical reading)
- Stated: linear price–load relation illustrative; perfect foresight upper bound; capacity/ancillary services and co-optimisation excluded; ownership more complex; static valuation.
- Critical: no degradation; hourly resolution misses sub-hourly value; no bid/offer mechanics or gate closure; welfare decomposition assumes competitive pricing.

## 9. Relevance to my study
Canonical benchmark for (i) perfect-foresight vs realistic (backcast) capture ratio (~85 %), (ii) price-taker overstatement for large fleets, (iii) the gap between private arbitrage profit and social welfare — directly relevant when attributing battery profits to specific market rules (price formation vs transfers).

## 10. Lineage links
- Builds on: Graves, Jenkin & Murphy (1999); walawalkar2007_nyisoarbitrage.
- Built upon by (notable): sioshansi2010_ownership; sioshansi2014_welfareloss; mcconnell2015_energyonly; bradbury2014_rtarbitrage; staffell2016_maxvalue.

## 11. Verification log
- Crossref (10.1016/j.eneco.2008.10.005): authors, Energy Economics 31(2):269–277, March 2009 ✔.
- Affiliations from full-text author copy ✔.
- SJR (id 29374): Energy Economics Q1 2009, 2010, 2014, 2023–2025 ✔.
- Full text read from author copy hosted on CMU CEIC; numbers quoted from it.
