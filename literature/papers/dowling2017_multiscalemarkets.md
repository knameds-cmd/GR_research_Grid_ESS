---
id: dowling2017_multiscalemarkets
title: "A multi-scale optimization framework for electricity market participation"
authors: ["Dowling, A. W.", "Kumar, R.", "Zavala, V. M."]
year: 2017
journal: "Applied Energy"
volume_issue_pages: "190:147-164"
doi: "10.1016/j.apenergy.2016.12.081"
quartile: "Q1 (SJR 2025, Energy (misc.); Renewable Energy, Sustainability and the Environment)"
quartile_basis: "pub-year; rule=pass; SJR 2017 Q1 for this journal recorded in greenwood2017_efrservicedesign"
group: "Victor M. Zavala, Chemical & Biological Engineering, University of Wisconsin–Madison"
lineage: "Zavala group (UW–Madison). Dowling = postdoc with Zavala at the time (paper affiliation), later faculty at Notre Dame (paper PDF hosted on dowlinglab.nd.edu). Kumar = Zavala group member."
streams: [S2_stacking_cooptimization, S1_foundations_value]
market_context: "CAISO 2015: day-ahead IFM (1 h), FMM (15 min), RTD (5 min) energy + regulation up/down, spinning and non-spinning reserves; Daggett node"
method_class: "MILP"
evidence_read: "full text (author-hosted PDF, https://dowlinglab.nd.edu/assets/447125/2017_a_multi_scale_optimization_framework_for_electricity_market_participation.pdf)"
oa_link: "https://dowlinglab.nd.edu/assets/447125/2017_a_multi_scale_optimization_framework_for_electricity_market_participation.pdf"
---

## 1. Research question
How much revenue do flexible assets (a battery and a CHP unit) leave on the table if valued only on day-ahead energy? What is the upper-bound value of co-optimising across day-ahead, 15-min and 5-min energy markets plus ancillary services?

## 2. Setting & assumptions
- Price-taker with **perfect foresight** over the full year of 2015 CAISO prices, giving an upper bound. Solved as one year-long deterministic MILP.
- Nested time grid: day → 24 h (IFM, AS awards) → 4 × 15 min (FMM) → 3 × 5 min (RTD). Virtual-bidding-like positions are allowed across layers.
- Battery: 1 MW / 1 MWh, η = 95% per direction. CHP: 1 MW electric with steam demand.
- Regulation: capacity payment only. Mileage payments are assumed to exactly offset tracking costs, and regulation energy is treated as neutral.

## 3. Constraints that drove the model choice
- Market timescales are nested and each settles separately, so decisions must be indexed per layer and linked (a position in the faster layer is a deviation from the slower one).
- Generator mode binaries (CHP) make it a MILP.
- Perfect foresight is chosen deliberately to bound value; the authors note an EMPC/rolling version is future work.

## 4. Model
- Objective: max (energy revenue across IFM/FMM/RTD + AS capacity revenue − fuel cost).
- Decisions: hourly AS capacity awards (reg up/down, spin, non-spin), energy positions per layer, and storage charge/discharge per 5 min.
- **Capacity split: dynamic, hourly AS awards.** Headroom and footroom constraints prevent double-counting capacity across energy and AS, and SoC must support the awarded capacities.
- **Frequency-signal energy: not modelled.** There is no AGC signal; regulation is treated as an energy-neutral capacity product.
- Solver: Gurobi. Instances have about 1 M continuous variables and about 2 M constraints; solved in minutes.

## 5. Data & processing
- CAISO 2015 LMPs (IFM, FMM, RTD) and AS prices at Daggett.
- Synthetic demand profiles for the CHP case.
- No forecasting.

## 6. Justification (why the authors argue the approach is valid)
- A deliberately optimistic upper bound for screening technology value.
- Decomposes revenue by timescale and product to show where value lies.

## 7. Key results
Battery, $/yr:
- energy only, all layers: $139.1k;
- energy + regulation, all layers: $199.6k (+43%);
- day-ahead only: $10.5k (energy) and $72.8k (with AS);
- real-time only: $115.0k and $141.8k.

Across technologies:
- Day-ahead-only studies miss about 60–90% of the attainable revenue.
- AS raise revenue potential by 40–100% depending on flexibility.

## 8. Limitations (stated + your critical reading)
- Stated: perfect information; crude mileage/regulation-energy treatment; CAISO-specific.
- Critical reading:
  - With no regulation signal, SoC drift from AGC and any energy-reservation rule are ignored. This inflates the value of stacking regulation with arbitrage.
  - With a year-long perfect-foresight MILP, value differences between layers partly reflect foresight on the volatile RTD prices.

## 9. Relevance to my study
- Canonical evidence that the time granularity of products is itself a driver of value.
- The nested time-index formulation can be reused for products with different gate closures and resolutions (e.g., EFA blocks vs. half-hourly BM/wholesale).
- A useful "no energy-reservation rule" benchmark against which rule-constrained models can be compared.

## 10. Lineage links
- Builds on: the storage arbitrage-valuation literature (S1) and multi-market participation studies cited in the paper. Individual references were not itemised in this read.
- Built upon by (notable): not checked in this session. Contemporaneous with cheng2018_multiscaledp (online 2016), which tackles the same multi-timescale problem stochastically.

## 11. Verification log
- DOI, volume and pages as printed on the author PDF (10.1016/j.apenergy.2016.12.081; Applied Energy 190, 147–164). Consistent with the EconPapers/IDEAS listing (v190, pp. 147–164).
- Crossref direct lookup not done (rate-limited).
- Full text read from the author-hosted PDF.
- SJR (id 28801): Q1 2025.
- Dowling's postdoc status inferred from the paper affiliation plus the Notre Dame hosting; not verified further.
