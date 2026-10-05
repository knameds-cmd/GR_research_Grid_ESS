---
id: collath2023_lifetimeprofit
title: "Increasing the lifetime profitability of battery energy storage systems through aging aware operation"
authors: ["Collath, N.", "Cornejo, M.", "Engwerth, V.", "Hesse, H.", "Jossen, A."]
year: 2023
journal: "Applied Energy"
volume_issue_pages: "348:121531"
doi: "10.1016/j.apenergy.2023.121531"
quartile: "Q1 (SJR 2025, Applied Energy, SJR 2.864)"
group: "Andreas Jossen (TUM Chair of Electrical Energy Storage Technology) & Holger Hesse (Kempten UAS / TUM)"
lineage: "Collath = TUM EES doctoral researcher (EES alumni page); follows collath2022_agingreview; same group as schimpe2018_efficiency (SimSES digital-twin lineage)."
streams: [S4_degradation_operation]
market_context: "EPEX SPOT intraday (Germany) arbitrage, price data 2019-2022"
method_class: "MPC with MILP (linearised calendar + cyclic aging) evaluated on a lifetime digital twin"
evidence_read: "abstract only (IDEAS/RePEc; mediaTUM record 1717155) — (from abstract)"
oa_link: "https://mediatum.ub.tum.de/1717155 (PDF timed out / rate-limited when accessed)"
---

## 1. Research question
How should the aging cost in an aging-aware operation strategy be chosen, and how much lifetime profit do more detailed (linearised calendar and cyclic) aging models add compared with an energy-throughput cost, for intraday arbitrage? (from abstract)

## 2. Setting & assumptions
- Lithium iron phosphate (LFP) cell; BESS trading on EPEX SPOT intraday; lifetime simulated on a digital twin; price years 2019–2022. (from abstract)

## 3. Constraints that drove the model choice
Degradation depends on SoC, C-rate and depth of cycle and is controllable by operation; MILP-based MPC requires linearised aging models; the "right" aging-cost value is unknown and the prevalent choice (system cost) is suspected to be wrong. (from abstract)

## 4. Model
- MPC framework; optimiser uses one of three aging cost models: (i) energy-throughput-based; (ii) linearised calendar model; (iii) linearised calendar + cyclic model (LFP).
- Outer loop: whole-lifetime simulation on the digital twin to find the optimal aging-cost value.
- Exact equations, breakpoints, horizon and BESS size NOT read.

## 5. Data & processing
EPEX SPOT intraday prices 2019–2022. (from abstract)

## 6. Justification
Lifetime closed-loop simulation with a (more detailed) aging model in the plant; benchmarks among aging-cost models. (from abstract)

## 7. Key results
- Determining aging cost via the MPC/lifetime framework "can significantly increase the lifetime profitability" vs. setting aging cost from battery system cost.
- Lifetime arbitrage profit +24.9 % with linearised calendar model and +29.3 % with linearised calendar + cyclic model, relative to an energy-throughput aging-cost model.
- Higher 2021–2022 prices and volatility substantially increase achievable lifetime profit. (from abstract)

## 8. Limitations
Full text not read. Single application (intraday arbitrage), single chemistry.

## 9. Relevance to my study
Clearest recent quantification that **calendar aging representation** (SoC-dependent) is worth ~25 % lifetime profit in arbitrage, i.e., more than the cyclic refinement on top (+4.4 pp). Also supports tuning aging cost as a hyper-parameter by lifetime simulation — same role as a reward weight in RL.

## 10. Lineage links
- Builds on: collath2022_agingreview; TUM SimSES; Naumann et al. LFP aging model (likely parameter source — unverified).
- Related: he2018_intertemporal, xu2022_dynamicvaluation (aging price ≠ replacement cost).

## 11. Verification log
- Crossref (api.crossref.org/works/10.1016/j.apenergy.2023.121531): title, 5 authors, Applied Energy 348, art. 121531, Oct 2023.
- mediaTUM record 1717155 confirms bibliographic data; abstract verbatim from IDEAS (ideas.repec.org/a/eee/appene/v348y2023ics0306261923008954.html).
- SJR: scimagojr.com sourceid 28801 → Q1.
- Full text not accessed (mediaTUM PDF timeouts, ScienceDirect robots-blocked).
