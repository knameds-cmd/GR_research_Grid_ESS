---
id: he2011_aggregatingvalues
title: "A novel business model for aggregating the values of electricity storage"
authors: ["He, X.", "Delarue, E.", "D'haeseleer, W.", "Glachant, J.-M."]
year: 2011
journal: "Energy Policy"
volume_issue_pages: "39(3):1575-1585"
doi: "10.1016/j.enpol.2010.12.033"
quartile: "Q1 (SJR 2025, Energy (misc.); Management, Monitoring, Policy and Law)"
group: "William D'haeseleer & Erik Delarue (KU Leuven Energy Institute, TME) with Jean-Michel Glachant (EUI Florence School of Regulation); first author at EDF R&D"
lineage: "KU Leuven TME energy-systems group (D'haeseleer and Delarue; their advisor relationship was not verified) and FSR/EUI. He's affiliation in the working paper is EDF R&D; PhD tie not verified."
streams: [S2_stacking_cooptimization, S1_foundations_value, S7_market_design]
market_context: "Belgium 2007 (one week): week-ahead generation-cost minimisation, day-ahead arbitrage, hour-ahead regulation; bulk storage (200 MW charge / 400 MW discharge / 1200 MWh)"
method_class: "MILP"
evidence_read: "full text of the working-paper version (EUI RSCAS 2010/82, http://cadmus.eui.eu/bitstream/handle/1814/14994/RSCAS_2010_82.pdf); journal version not read"
oa_link: "http://cadmus.eui.eu/bitstream/handle/1814/14994/RSCAS_2010_82.pdf"
---

## 1. Research question
Single-use valuations make storage look unprofitable. Can a business model that **sequentially auctions the right to use the storage** across time frames (week-ahead, day-ahead, hour-ahead) aggregate several values without conflicting uses?

## 2. Setting & assumptions
- Deterministic: known costs and prices in each stage (perfect foresight within the stage). The day-ahead stage includes a linear price-impact ("market resilience") term.
- Sequential stages:
  1. week-ahead: a generation-portfolio owner minimises supply cost;
  2. day-ahead: arbitrage profit;
  3. hour-ahead: regulation-energy supply to the TSO.
- Asset: generic bulk storage, √(round-trip) efficiency on each leg. Energy level returns to target at the end of each week and day.

## 3. Constraints that drove the model choice
- Uses at different time frames compete for the same power and energy.
- Commitments made earlier must stay firm.
- Later bidders can only use the remaining capacity, including the "counter-action" headroom created by earlier schedules (for example, discharging against an earlier charge schedule).

## 4. Model
- Each stage solves an optimisation (unit-commitment-style MILP in the week-ahead stage, LP/MILP thereafter) with earlier profiles as fixed constraints.
- Remaining charge capacity = max charge − net prior action. Remaining discharge capacity = max discharge + net prior action. This is a bidirectional offset.
- **Capacity split: sequential and dynamic.** The allocation is time-varying and emerges from the auction order. It is neither a fixed split nor a joint co-optimisation.
- **Reserve/regulation energy:** hour-ahead regulation volumes are known in a perfect-foresight variant. A no-foresight variant checks quarter-hour by quarter-hour that offsetting capacity exists.
- Auction: the right to use the storage goes to the highest bidder at each stage.

## 5. Data & processing
- Belgian 2007 load (one winter week) and a stylised 1,740 MW generation portfolio.
- Belgian day-ahead prices and regulation volumes/prices.

## 6. Justification (why the authors argue the approach is valid)
A conceptual business-model demonstration. Value of each stage alone is compared with the chained aggregate.

## 7. Key results
- Weekly value: week-ahead alone about €100k; day-ahead alone about €150k; hour-ahead alone about €40k; sequential aggregation about €350k or more.
- Regulation energy can be supplied for 67% of the time with foresight and 48% without (as extracted from the working-paper version).

## 8. Limitations (stated + your critical reading)
- Stated: case-specific numbers; no network constraints; single actor; simplified hour-ahead model; regulatory feasibility in Europe uncertain.
- Critical reading: sequential greedy allocation is generally suboptimal compared with joint co-optimisation, but closer to how products actually clear in sequence. Numbers come from one week. The working-paper numbers may differ from the journal version.

## 9. Relevance to my study
- The earliest formal treatment of stacking as a **market-sequence problem**: earlier-clearing products constrain later ones.
- Directly relevant to how auction timing and stacking permission (e.g., GB DC/DM/DR before the BM; CE FCR before aFRR/DA) shape attainable value.
- The "remaining capacity with counter-action" formula is a reusable building block.

## 10. Lineage links
- Builds on: single-application storage valuations (e.g., Walawalkar 2007; see S1).
- Built upon by (notable): moreno2015_multiservicemilp (joint multi-service MILP); later market-design discussions of storage multi-use.

## 11. Verification log
- DOI 10.1016/j.enpol.2010.12.033 resolves (doi.org) to Elsevier PII S030142151000933X, matching the ScienceDirect page for this title.
- Volume, issue and pages (39(3):1575–1585, March 2011) from the IDEAS/RePEc "published in" record.
- Working-paper full text read. The journal version may differ in numbers; deep fields are from the WP.
- SJR (id 29403): Energy Policy Q1 2025.
- He's affiliation (EDF R&D) as printed in the WP.
