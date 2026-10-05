---
id: mercier2023_eudaarbitrage
title: "The value of electricity storage arbitrage on day-ahead markets across Europe"
authors: ["Mercier, T.", "Olivier, M.", "De Jaeger, E."]
year: 2023
journal: "Energy Economics"
volume_issue_pages: "123:106721"
doi: "10.1016/j.eneco.2023.106721"
quartile: "Q1 (SJR 2023-2025, Economics & Econometrics; Energy (misc.))"
group: "UCLouvain / EnergyVille-KU Leuven (Emmanuel De Jaeger) with Université Laval (Mathieu Olivier)"
lineage: "Mercier (corresponding; affiliations UCLouvain, KU Leuven, U. Laval per OpenAlex). Advisor ties not verified."
streams: [S1_foundations_value, S7_market_design]
market_context: "EU-28 + NO, CH, TR day-ahead hourly prices 2000-2021; Belgian variable grid fees case"
method_class: "MILP"
evidence_read: "abstract only (RePEc/IDEAS); full text not accessible (ScienceDirect robots-blocked; repository copies blocked)"
oa_link: "http://hdl.handle.net/2078.1/275017"
---

## 1. Research question
How large and how variable is the arbitrage value of (technology-neutral) storage on European day-ahead markets over two decades, how do efficiency and duration matter, and how do grid fees affect it?

## 2. Setting & assumptions
(from abstract) Technology-neutral storage; price-taker on historical day-ahead hourly prices; MILP formulation (binary variables presumably for charge/discharge exclusivity or fee structure — not verified); foresight assumption not verified.

## 3. Constraints that drove the model choice
(from abstract) MILP chosen — likely to model non-convex elements such as grid-fee structures; not verified.

## 4. Model
(from abstract) Arbitrage profit maximisation via MILP over hourly DA prices; Belgian variable grid fees applied to charging/discharging in a case study. Formulation not read.

## 5. Data & processing
(from abstract) Hourly day-ahead prices for EU-28 plus Norway, Switzerland, Turkey, 2000–2021.

## 6. Justification (why the authors argue the approach is valid)
Not assessable from abstract.

## 7. Key results
(from abstract)
- Storage arbitrage value varies substantially across countries and over time.
- Round-trip efficiency significantly affects value; durations beyond ~4–6 h add little marginal value.
- Belgian variable grid fees reduce arbitrage value by roughly 20–50 % and substantially reduce market participation.

## 8. Limitations (stated + your critical reading)
Critical (from abstract): DA only (no intraday/balancing/FCR — where most European battery revenue sits); price-taker; historical prices pre-2022 crisis partially.

## 9. Relevance to my study
Rare quantification of a **specific regulatory rule (network tariffs/grid fees)** cutting arbitrage value 20–50 % — exactly the type of rule-to-profit mapping a market-rules study needs; also a long multi-country DA benchmark.

## 10. Lineage links
- Builds on: sioshansi2009_pjmvalue; bradbury2014_rtarbitrage; Zafirakis et al. 2016 (Applied Energy, EU arbitrage — not archived).
- Built upon by (notable): later EU multi-market arbitrage studies (not checked).

## 11. Verification log
- Crossref (10.1016/j.eneco.2023.106721): title, authors, Energy Economics 123, article 106721, July 2023 ✔.
- OpenAlex: affiliations (U. Laval, UCLouvain, KU Leuven), green OA (DIAL handle 2078.1/275017; RePEc licence cc-by-nc-nd) ✔.
- SJR Energy Economics Q1 2023–2025 ✔.
- Full text NOT read; deep fields from abstract only.
