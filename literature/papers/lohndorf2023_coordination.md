---
id: lohndorf2023_coordination
title: "The Value of Coordination in Multimarket Bidding of Grid Energy Storage"
authors: ["Löhndorf, N.", "Wozabal, D."]
year: 2023
journal: "Operations Research"
volume_issue_pages: "71(1):1-22"
doi: "10.1287/opre.2021.2247"
quartile: "Q1 (SJR 2024, Operations Research, SJR 2.557; Q1 Computer Science Applications and Management Science & OR)"
group: "Löhndorf (Univ. of Luxembourg) / Wozabal (TU Munich → VU Amsterdam)"
lineage: "Same authors as lohndorf2013_addp (with Minner). OpenAlex affiliations: Luxembourg; TU Munich. VU Amsterdam research portal lists Wozabal (Operations Analytics, VU) as corresponding author."
streams: [S3_bidding_uncertainty]
market_context: "Auction-based day-ahead + continuous intraday market (European/German-style); assets: battery, pumped hydro, large reservoir hydro"
method_class: "SP (multistage SP with scenario tree + reoptimisation policy; information-relaxation upper bounds)"
evidence_read: "abstract only (VU Amsterdam research portal full abstract; IDEAS); full-text PDF on VU portal returned 403"
oa_link: "https://research.vu.nl/en/publications/the-value-of-coordination-in-multimarket-bidding-of-grid-energy-s"
---

## 1. Research question
How much is it worth for a storage owner to coordinate day-ahead auction bids with continuous intraday trading, versus bidding sequentially, and for which asset types?

## 2. Setting & assumptions
- Multisettlement: DA auction + continuous intraday with hourly intraday trading (from abstract).
- Price impact varies with asset size (pumped hydro high, battery low) (from abstract).
- Stylised model + realistic multistage stochastic program with a stochastic price model (from abstract). Bid format, data period, parameters: not verified.

## 3. Constraints that drove the model choice
(from abstract) Optimal policy not computable ⇒ need bounds: upper bound via information relaxation with optimised bilinear penalties; lower bound via implementable scenario-tree reoptimisation policy.

## 4. Model
- Stylised result: coordinated policy reserving capacity for intraday is optimal; gap to sequential policy increases with intraday price volatility and liquidity (from abstract).
- Multistage SP for DA bidding + hourly intraday trading; scenario-tree generation method yielding a reoptimisation policy (from abstract).
- Novel information-relaxation scheme with bilinear penalties for tight upper bounds (from abstract).

## 5. Data & processing
Stochastic price model for DA and intraday (from abstract); estimation data not verified.

## 6. Justification
Lower vs upper bound comparison shows near-optimality for all assets (from abstract).

## 7. Key results (from abstract)
- Coordination most valuable for flexible assets with high price impact (pumped hydro).
- Small, low-impact batteries: DA participation less important; intraday trading appears sufficient.
- Inflexible reservoirs without pumps: intraday hardly profitable; DA dominates.
- Policy near-optimal for all assets.

## 8. Limitations (stated + critical reading)
- Critical: no ancillary-service products; conclusions on batteries depend on assumed intraday liquidity — in markets where batteries earn mainly from frequency products (GB, Nordics) the coordination problem shifts to energy vs reserve.

## 9. Relevance to my study
Strongest OR evidence that market-product structure (auction vs continuous, liquidity) determines the value of coordinated multi-product bidding — central to my "how product rules shape RL battery multi-product bidding" question. Information-relaxation bounds are a rigorous way to certify a learned bidder's gap.

## 10. Lineage links
- Builds on: lohndorf2013_addp; Brown, Smith & Sun (2010) information relaxation duality (not in archive).
- Built upon by: battery intraday/multi-market OR literature (not assessed).

## 11. Verification log
- IDEAS/RePEc a/inm/oropre/v71y2023i1p1-22 + VU research portal + OpenAlex works/doi:10.1287/opre.2021.2247 → 71(1):1-22 (issue Feb 2023; OpenAlex year 2022 = online).
- SJR: Operations Research Q1 2023/2024.
- Full text not read (VU PDF 403; INFORMS robots-blocked).
