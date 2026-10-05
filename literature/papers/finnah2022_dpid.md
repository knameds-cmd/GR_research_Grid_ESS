---
id: finnah2022_dpid
title: "Integrated day-ahead and intraday self-schedule bidding for energy storage systems using approximate dynamic programming"
authors: ["Finnah, B.", "Gönsch, J.", "Ziel, F."]
year: 2022
journal: "European Journal of Operational Research"
volume_issue_pages: "301(2):726-746"
doi: "10.1016/j.ejor.2021.11.010"
quartile: "Q1 (SJR 2024, European J. of Operational Research, SJR 2.239; Q1 in all five categories)"
group: "Gönsch (Univ. Duisburg-Essen; corresponding) with Ziel (Univ. Duisburg-Essen; known for electricity-price forecasting)"
lineage: "Finnah = Duisburg-Essen doctoral researcher (supervision not verified). Methodological heir of lohndorf2013_addp / Powell ADP; Ziel contributes high-dimensional price forecasting."
streams: [S3_bidding_uncertainty]
market_context: "German day-ahead auction (60-min slots, 15-min subdivision) + intraday market (form not verified); storage self-schedule bidding"
method_class: "SDP/DP (ADP)"
evidence_read: "abstract only (IDEAS/RePEc record + OpenAlex reconstructed abstract); full text not read"
oa_link: "https://www.sciencedirect.com/science/article/pii/S0377221721009565 (hybrid OA per OpenAlex; not accessed)"
---

## 1. Research question
How should a storage owner coordinate self-schedule (quantity) bids in the German DA auction with subsequent intraday trading when intraday prices are more volatile and high-dimensional price forecasts are used?

## 2. Setting & assumptions
- DA + intraday, Germany (from abstract); DA auction with 60-min slots subdivided into 15-min intervals; intraday trades residual volumes with higher volatility (from OpenAlex abstract); self-schedule bids (quantities, no price) per title.
- Price-maker/taker status, intraday representation (continuous vs auction), battery parameters: not verified.

## 3. Constraints that drove the model choice
(from abstract) Accounting for fast ramping (15-min structure) in a high-dimensional price-forecast state makes exact DP intractable ⇒ ADP.

## 4. Model
ADP for integrated DA + ID decisions (from abstract); state, basis functions, algorithm: not verified.

## 5. Data & processing
Real-world (German) data (from abstract); periods not verified.

## 6. Justification
Benchmarked against state-of-the-art receding-horizon (expected-value) approaches; capturing the high-dimensional price information is reported essential for competitive performance (from abstract).

## 7. Key results
Not verified.

## 8. Limitations (stated + critical reading)
- Critical: self-schedule bids discard the price-filter benefit of economic bids (cf. mohsenianrad2016_pricemaker result).

## 9. Relevance to my study
European DA+ID coordination for batteries with forecasting inputs — complements lohndorf2023_coordination; read full text before using as benchmark.

## 10. Lineage links
- Builds on: lohndorf2013_addp; jiang2015_hourahead; Ziel price-forecasting work.
- Built upon by: not assessed.

## 11. Verification log
- IDEAS/RePEc a/eee/ejores/v301y2022i2p726-746 → authors, 301(2):726-746, 2022, DOI, abstract.
- SJR: EJOR id 22489, Q1 2023/2024.
- OpenAlex works/doi:10.1016/j.ejor.2021.11.010 → all three authors Univ. Duisburg-Essen; Gönsch corresponding; OpenAlex year 2021 = online, issue 2022.
