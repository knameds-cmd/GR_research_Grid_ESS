---
id: baringo2011_robustoffer
title: "Offering Strategy Via Robust Optimization"
authors: ["Baringo, L.", "Conejo, A. J."]
year: 2011
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "26(3):1418-1425"
doi: "10.1109/TPWRS.2010.2092793"
quartile: "Q1 (SJR 2024, IEEE Trans. Power Systems, SJR 3.629; Q1 Electrical & Electronic Eng. and Energy Eng. & Power Tech.)"
group: "Conejo (UCLM)"
lineage: "Both UCLM (OpenAlex). Baringo = Conejo PhD student at UCLM (widely documented; not re-verified this session). Robust counterpart of conejo2002_pricetaker."
streams: [S3_bidding_uncertainty]
market_context: "Generic pool, hourly offering curves; price-taker producer (thermal)"
method_class: "RO (sequence of robust MILPs)"
evidence_read: "abstract only (OpenAlex abstract_inverted_index); full text closed"
oa_link: ""
---

## 1. Research question
Can hourly offering curves for a price-taker producer be built from price confidence intervals (robust optimisation) instead of price point forecasts or scenario sets?

## 2. Setting & assumptions
- Price-taker; prices described by confidence intervals rather than predictions (from abstract).
- Hourly offering curves to a pool (from abstract). Unit details not verified.

## 3. Constraints that drove the model choice
(from abstract) Avoids needing a full probabilistic price model/scenario tree; each robust MILP is "meaningful and easy-to-solve".

## 4. Model
- Confidence intervals are successively divided into nested subintervals; for each subinterval a robust MILP is solved; the collection of solutions provides the points of hourly offering curves (from abstract).
- Monotonicity: nested-interval construction is designed to yield consistent (non-decreasing) price-quantity points — inferred from construction, not verified in text.
- Uncertainty set form (box/budget) and solver: not verified.

## 5. Data & processing
Not verified.

## 6. Justification
Not verified beyond abstract.

## 7. Key results
Not verified.

## 8. Limitations (stated + critical reading)
- Critical: robust (worst-case within interval) offers are conservative; no SoC/intertemporal opportunity cost — for storage, worst-case price in each hour is ill-defined because charge and discharge hours have opposite worst cases.
- No probabilistic out-of-sample guarantee.

## 9. Relevance to my study
Shows a non-scenario way to generate price-quantity bid curves (nested intervals ↔ bid segments). Useful contrast to SP bid-curve construction (pandzic2013_vppoffer, lohndorf2013_addp).

## 10. Lineage links
- Builds on: Bertsimas & Sim (2004) budgeted RO (not in archive); conejo2002_pricetaker.
- Built upon by: robust offering papers for wind/storage (e.g., Attarha et al. 2018 TSTE adaptive RO for wind+CAES; not included — authorship not verified this session).

## 11. Verification log
- OpenAlex works/doi:10.1109/TPWRS.2010.2092793 → Baringo & Conejo (UCLM), 26(3):1418-1425, 2011; abstract from inverted index.
- SJR: IEEE TPWRS Q1 2023/2024.
- Full text not read.
