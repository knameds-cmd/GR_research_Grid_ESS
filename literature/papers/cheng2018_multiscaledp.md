---
id: cheng2018_multiscaledp
title: "Co-Optimizing Battery Storage for the Frequency Regulation and Energy Arbitrage Using Multi-Scale Dynamic Programming"
authors: ["Cheng, B.", "Powell, W. B."]
year: 2018
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "9(3):1997-2005"
doi: "10.1109/TSG.2016.2605141"
quartile: "Q1 (SJR 2025, Computer Science (misc.))"
group: "Warren B. Powell, CASTLE Lab, ORFE, Princeton University"
lineage: "Powell (Princeton ORFE) group. Bolong Cheng (Princeton EE, per OpenAlex affiliation) co-authored with Powell. Part of the Powell lineage on ADP for storage (e.g., Jiang & Powell, Salas & Powell); advisor tie not verified on a thesis page."
streams: [S2_stacking_cooptimization]
market_context: "US (PJM-style) frequency regulation + energy arbitrage (from abstract; exact market not confirmed)"
method_class: "SDP/DP"
evidence_read: "abstract only (Princeton research portal); full text not accessible (IEEE paywall, no preprint found)"
oa_link: ""
---

## 1. Research question
How to co-optimise a battery for energy arbitrage and frequency regulation when decisions occur at different time scales and load, price and regulation signals are stochastic (from abstract).

## 2. Setting & assumptions
(from abstract)
- Stochastic load demand, electricity prices and regulation signals.
- Charge/discharge decisions at different time scales: slow arbitrage and fast regulation.
- Solving even a single day exactly is "computationally intractable due to the large state space and the number of time steps."
- Price-taker status, data and battery parameters were not read.

## 3. Constraints that drove the model choice
(from abstract) Curse of dimensionality: a fine regulation time step over a full-day horizon. This motivated exploiting the **nested structure** of the problem.

## 4. Model
- (from abstract) A dynamic-programming method that decomposes the problem into smaller subproblems with reduced state spaces at different time scales. This is a multi-scale DP in which the fast-scale (regulation) value feeds the slow-scale (arbitrage) decisions.
- Capacity split, signal modelling and SoC handling: **not read; not recorded**. Do not assume the details without the full text.

## 5. Data & processing
Not read.

## 6. Justification (why the authors argue the approach is valid)
Not read. The abstract claims computational tractability through decomposition.

## 7. Key results
Not read (the abstract gives no figures).

## 8. Limitations (stated + your critical reading)
- Not read.
- Critical reading: as with all Powell-lineage SDP work, the results rely on the fidelity of the stochastic models of price and signal. Product rules (energy-reservation requirements, performance scores) need to be checked in the full text.

## 9. Relevance to my study
- The canonical **multi-timescale stochastic DP** for stacking regulation and arbitrage.
- A methodological alternative to the MILP oracle (mirzaeialavijeh2025_swedenfcrstacking) and to DRL.
- The nested-time-scale decomposition maps naturally onto product hierarchies (e.g., EFA-block capacity commitments with half-hourly energy trading). High priority to obtain the full text.

## 10. Lineage links
- Builds on: presumably Powell-group ADP for storage (e.g., Jiang & Powell's hour-ahead bidding ADP, arXiv 1402.3575). Reference list not read; tie not verified.
- Built upon by (notable): later multi-timescale and DRL co-optimisation work (not itemised). Contemporaneous with dowling2017_multiscalemarkets and shi2018_superlineargains.

## 11. Verification log
- Princeton research portal (collaborate.princeton.edu): IEEE TSG 9(3):1997–2005, May 2018, DOI 10.1109/TSG.2016.2605141.
- Crossref/OpenAlex currently return the 2016 early-access stub (pages "1-1"). The doi.org resolver points to IEEE Xplore document 7558191.
- Semantic Scholar lists DBLP key journals/tsg/ChengP18, consistent with a 2018 issue.
- SJR (id 19700170610): Q1.
- Full text not accessed. All deep fields are abstract-level.
