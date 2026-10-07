---
id: namor2019_multiservicecontrol
title: "Control of Battery Storage Systems for the Simultaneous Provision of Multiple Services"
authors: ["Namor, E.", "Sossan, F.", "Cherkaoui, R.", "Paolone, M."]
year: 2019
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "10(3):2799-2808"
doi: "10.1109/TSG.2018.2810781"
quartile: "Q1 (SJR 2025, Computer Science (misc.); journal Q1 since 2011 per SJR)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Mario Paolone, Distributed Electrical Systems Laboratory (DESL), EPFL"
lineage: "EPFL DESL (Paolone, with R. Cherkaoui). All four authors list DESL as their affiliation. Namor is a DESL doctoral researcher (status not verified). Builds on earlier DESL dispatchable-feeder work by Sossan."
streams: [S2_stacking_cooptimization]
market_context: "Swiss/ENTSO-E CE primary frequency regulation (droop) + dispatchable MV feeder (prosumer self-dispatch); technical, not revenue-driven"
method_class: "MPC"
evidence_read: "full text (arXiv:1803.00978, https://arxiv.org/pdf/1803.00978)"
oa_link: "https://arxiv.org/abs/1803.00978"
---

## 1. Research question
How can one BESS deliver two services at once with guaranteed feasibility: (i) dispatch tracking for a feeder with stochastic prosumption, and (ii) primary frequency regulation? The allocation should be done day-ahead and the services superimposed in real time.

## 2. Setting & assumptions
- No prices. The objective is technical: maximise the PFR droop that can be offered while the dispatch plan stays feasible. An economic objective is sketched in an appendix but not used.
- Day-ahead at 5 min resolution (288 steps); real-time at 1 s. Prosumption forecasts come with upper/lower bounds. Frequency uncertainty comes from two years of historical frequency.
- Asset: EPFL 720 kVA / 560 kWh Li-ion BESS on a 20 kV feeder (about 300 kW peak load, 90 kWp PV). SoC limits [5%, 100%] after an efficiency-margin procedure (96% round trip).

## 3. Constraints that drove the model choice
The need for a feasibility guarantee for both services under uncertainty without solving a stochastic programme in real time. This led to **power and energy budgets** per service, computed day-ahead from forecast intervals and frequency quantiles.

## 4. Model
- Day-ahead: max α (droop, kW/Hz) subject to:
  - power budgets $[P^{\downarrow}_{j,k},P^{\uparrow}_{j,k}]$ for dispatch and for PFR (PFR power = ±0.2α at the 200 mHz limit);
  - cumulative energy budgets $E_{FR,k}=\alpha W_{f,k}$, where $W_{f,k}$ is the integrated frequency deviation bounded by $\mu\pm1.96\sigma$;
  - SoC within $[E_{min},E_{max}]$ for all budget combinations.
- Decision variables also include a daily offset profile F that steers SoC (energy-neutral restoration).
- **Capacity split: fixed per day, by budget.** Power and energy budgets are reserved per service. α is constant over the day, re-optimised daily.
- **Frequency-signal energy: statistical worst case.** A 95% quantile band of integrated frequency deviation per 5-min period is estimated from two years of PMU data. This is a robust budget, not an expected value.
- Real-time: setpoints superimposed, $B_k = B_{d,k} + \alpha^o (f_k - f_n)$. The dispatch part tracks the 5-min plan through a short-horizon energy balance.
- Problem is linear and convex (solver not specified).

## 5. Data & processing
- Two years of grid frequency from the EPFL PMU system.
- Prosumption forecasts from an earlier DESL tool.
- 31-day simulation plus two days of real-world experiments.

## 6. Justification (why the authors argue the approach is valid)
- The budget approach guarantees feasibility at the chosen confidence level.
- Validated experimentally on the 560 kWh BESS: dispatch tracking RMS error about 0.5 kW, with no SoC violations.

## 7. Key results
- Simulation: mean daily α ≈ 217 kW/Hz (about 43 kW of PFR at 200 mHz) alongside dispatch.
- Experiments: α = 584 kW/Hz on day 1 and 127 kW/Hz on day 2. The difference reflects how much capacity the dispatch service needs given that day's forecast uncertainty.

## 8. Limitations (stated + your critical reading)
- Stated: an empirical efficiency margin; no prioritisation when limits are hit; short experiments.
- Critical reading: no prices, so there is no trade-off against revenue. The daily-fixed α is conservative compared with hourly product granularity. The quantile-based energy budget is a design choice that could be compared with the rule-based energy reservations TSOs actually use.

## 9. Relevance to my study
- Gives the "power budget + energy budget" vocabulary for allocating capacity across services.
- Gives a principled, data-driven way to size the energy reserved for a frequency product.
- Useful to contrast data-driven quantile budgets with regulatory rules: rule-implied reservation versus statistically needed reservation could be one way to quantify the cost of a rule.

## 10. Lineage links
- Builds on: DESL dispatchable-feeder control (Sossan et al.). Related: oudalov2007_pfcsizing (BESS for primary frequency control; S6).
- Built upon by (notable): DESL grid-forming multi-service follow-ups (e.g., Electric Power Systems Research 2022, not checked here); engels2020_fcrpeakshaving takes a related chance-constrained route.

## 11. Verification log
- Crossref (api.crossref.org/works/10.1109/TSG.2018.2810781): title, authors, vol 10, issue 3, pp. 2799–2808, May 2019. Confirmed.
- arXiv 1803.00978 full text read.
- SJR (id 19700170610): Q1 2025.
- The DESL roles of Namor and Sossan come from affiliations in the paper. Their PhD/postdoc status is from general knowledge and not re-verified.
