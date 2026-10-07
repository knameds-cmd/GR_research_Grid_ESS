---
id: conejo2002_pricetaker
title: "Price-taker bidding strategy under price uncertainty"
authors: ["Conejo, A. J.", "Nogales, F. J.", "Arroyo, J. M."]
year: 2002
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "17(4):1081-1088"
doi: "10.1109/TPWRS.2002.804948"
quartile: "Q1 (SJR 2024, IEEE Trans. Power Systems, SJR 3.629; Q1 Electrical & Electronic Eng. and Energy Eng. & Power Tech.)"
quartile_basis: "latest-only; rule=unchecked; SJR 2002 (publication year) not checked — only later years"
group: "Conejo (Univ. of Castilla-La Mancha, UCLM)"
lineage: "Root of the UCLM/Conejo 'offering strategy' school (all three authors UCLM per OpenAlex). Later UCLM students/co-workers: Ruiz (ruiz2009_mpecoffer), Baringo (baringo2011_robustoffer), Morales (pandzic2013_vppoffer). Advisor-student ties to those authors are widely documented but not re-verified in this session."
streams: [S3_bidding_uncertainty]
market_context: "Generic pool, next-day hourly clearing prices; price-taker producer (case-study market not verified — abstract only says 'realistic case study')"
method_class: "SP"
evidence_read: "abstract only (OpenAlex abstract_inverted_index); full text closed"
oa_link: ""
---

## 1. Research question
How should a price-taking producer build its next-day hourly offers when market-clearing prices are uncertain and only their forecast probability densities are known?

## 2. Setting & assumptions
- Price-taker; next-day hourly clearing prices described by forecast probability density functions (from abstract).
- Self-scheduling profit maximisation under price uncertainty; a "simple yet informed bidding rule" derived from its solution (from abstract).
- Asset: thermal producer (not storage). Detailed unit constraints not verified (full text not read).

## 3. Constraints that drove the model choice
(from abstract) Problem has a "particular structure" exploited for solution; the paper's point is that the stochastic self-schedule can be mapped into a bid rule rather than solving a bid-curve optimisation directly.

## 4. Model
- Objective: expected profit of self-schedule given price pdfs (from abstract).
- Decision variables / constraints: not verified (full text not read).
- Output: hourly bidding rule (price-quantity offers) derived from the self-schedule solution.

## 5. Data & processing
- Price pdfs from "an appropriate forecasting tool" (from abstract). Data source / period not verified.

## 6. Justification
Realistic case study (from abstract). No further detail verified.

## 7. Key results
Not verified (abstract gives no numbers).

## 8. Limitations (stated + critical reading)
- Price-taker; no intertemporal storage state; for storage the hourly bid would have to encode opportunity cost of SoC, which this rule does not address.
- Critical: pdf-based self-schedule → bid rule ignores non-anticipativity across hours when bid curves must be submitted simultaneously for 24 h (later formalised in plazas/pandzic-type two-stage SPs).

## 9. Relevance to my study
Canonical reference for "price-taker bids from price distributions"; useful as the conceptual ancestor when arguing that a battery's bid curve = conditional opportunity-value curve (cf. zheng2022_asdp, which makes this explicit for storage).

## 10. Lineage links
- Builds on: price forecasting work at UCLM (Nogales/Conejo).
- Built upon by (notable): ruiz2009_mpecoffer, baringo2011_robustoffer, pandzic2013_vppoffer; Conejo, Carrión & Morales (2010) book "Decision Making Under Uncertainty in Electricity Markets" (not in archive).

## 11. Verification log
- OpenAlex works/doi:10.1109/TPWRS.2002.804948 → title, authors (all UCLM), vol 17(4) pp 1081-1088, 2002. Abstract reconstructed from OpenAlex inverted index.
- SJR: scimagojr.com source id 28825 (IEEE TPWRS) Q1 2023 & 2024.
- Full text not accessed; all model/data sections limited to abstract.
