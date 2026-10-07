---
id: he2016_pbrcyclelife
title: "Optimal Bidding Strategy of Battery Storage in Power Markets Considering Performance-Based Regulation and Battery Cycle Life"
authors: ["He, G.", "Chen, Q.", "Kang, C.", "Pinson, P.", "Xia, Q."]
year: 2016
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "7(5):2359-2367"
doi: "10.1109/TSG.2015.2424314"
quartile: "Q1 (SJR 2025, IEEE Trans. Smart Grid, SJR 4.363; Q1 every year 2011-2025)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Chongqing Kang / Qixin Chen / Qing Xia (Tsinghua Univ., EE) with Pierre Pinson (DTU)"
lineage: "G. He = Tsinghua PhD in Kang/Chen group (later CMU postdoc with Whitacre -> he2018_intertemporal). Advisor relation inferred from authorship/affiliation; not separately verified."
streams: [S4_degradation_operation, S6_ancillary_products]
market_context: "PJM-style joint day-ahead energy, spinning reserve and performance-based regulation (capability + mileage payments, RegD)"
method_class: "MINLP (life-cycle income objective with DOD-dependent cycle life; decomposed rainflow approximation)"
evidence_read: "partial full text via ResearchGate extraction (https://www.researchgate.net/publication/276270804); not checked against publisher PDF"
oa_link: "none found"
---

## 1. Research question
How should a battery bid jointly into energy, reserve and performance-based regulation markets when bidding decisions change cycle depth and therefore battery cycle life, and how much does accounting for cycle life change profitability?

## 2. Setting & assumptions
- Price-taker bidding in joint DA energy / spinning reserve / regulation; regulation pays capability price plus performance-weighted mileage (RegD mileage ≈ 3× RegA).
- Battery life = min(cycle life, float/calendar life); cycle life from DOD power law.
- Regulation-induced energy fluctuation decomposed into two time scales for cycle counting.

## 3. Constraints that drove the model choice
Regulation creates many shallow cycles superimposed on arbitrage cycles; exact rainflow counting inside the bid optimisation is intractable → simplified two-time-scale cycle calculation, and income maximised over the (endogenous) lifetime rather than per-day.

## 4. Model
- Cycle life: N(d) = N_fail,100 · d^{−k_P} (k_P ≈ 0.8–2.1 by chemistry); equivalent 100 %-DOD cycles n_eq = n_d · d^{k_P}.
- Objective (as extracted): max Income_total = min(T_cycle, T_float) · W · Income_day — i.e., maximise daily income times the resulting life (W = working days/yr).
- Simplified rainflow (decomposition of hourly energy changes from regulation into two components) with < 5 % deviation from exact rainflow (as extracted).
- Solved as MINLP (GAMS/MATLAB).

## 5. Data & processing
PJM market-price and regulation-signal data (details not extracted). Base case as extracted: 30 MW / 1 h battery.

## 6. Justification
Comparison with exact rainflow for the counting approximation; case comparisons with/without cycle-life consideration and with/without PBR.

## 7. Key results (as extracted, single-source — re-check)
- Optimal strategy limits daily equivalent 100 %-DOD cycles to ~3.4 to preserve ≥ 10-year life.
- Ignoring cycle life overstates/understates profitability by ~30 % (profit-rate effect).
- PBR raises gross income by ~25 % vs. non-performance-based regulation payment.
- Collath et al. 2022 review (collath2022_agingreview, Table) attributes to "He et al." an arbitrage case with life extended 6.3 → 10 yr at −19.2 % daily revenue (may refer to this paper; unconfirmed).
- The extraction labelled the base-case technology as a vanadium flow battery; this conflicts with the Li-ion framing elsewhere and is UNVERIFIED.

## 8. Limitations (stated + your critical reading)
- Lifetime-multiplied objective treats life as endogenous but ignores discounting and price evolution.
- Non-convex MINLP; no guarantee of global optimum.
- Exact parameters unknown here (evidence partial).

## 9. Relevance to my study
Early demonstration that **product design (PBR mileage payment)** and degradation interact: mileage pay rewards exactly the throughput that ages the battery. A market-rule study comparing pay-for-performance vs. capacity-only regulation should include this trade-off.

## 10. Lineage links
- Builds on: DOD-cycle-life power laws; PJM PBR (FERC Order 755).
- Built upon by: he2018_intertemporal; later Chinese ancillary-market bidding studies.

## 11. Verification log
- Crossref (api.crossref.org/works/10.1109/TSG.2015.2424314): title, authors, TSG 7(5):2359–2367, Sept 2016.
- Content: ResearchGate extraction only; full PDF not accessed (IEEE closed, no preprint found). Mark all numbers "to re-check".
- SJR: scimagojr.com sourceid 19700170610 → Q1.

### Verification addendum (cross-check by S6 stream, 2026-10-06)
The S6 agent read the full text (DTU Orbit accepted version) and confirmed the values flagged above as "to re-check": a 30 MW / 30 MWh vanadium redox flow battery with 70% round-trip efficiency, 3.42 equivalent cycles per day, about 25% lower income without performance-based pay, and an optimal duration of about 1.5 h. The "vanadium flow battery" claim is therefore verified.
