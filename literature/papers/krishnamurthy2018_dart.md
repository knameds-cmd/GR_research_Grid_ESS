---
id: krishnamurthy2018_dart
title: "Energy Storage Arbitrage Under Day-Ahead and Real-Time Price Uncertainty"
authors: ["Krishnamurthy, D.", "Uçkun, C.", "Zhou, Z.", "Thimmapuram, P. R.", "Botterud, A."]
year: 2018
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "33(1):84-93"
doi: "10.1109/TPWRS.2017.2685347"
quartile: "Q1 (SJR 2024, IEEE Trans. Power Systems, SJR 3.629; Q1 Electrical & Electronic Eng. and Energy Eng. & Power Tech.)"
group: "Botterud (Argonne National Laboratory; later MIT LIDS)"
lineage: "All authors Argonne (OpenAlex); Botterud senior author. Argonne CEEESA market-modelling group."
streams: [S3_bidding_uncertainty]
market_context: "US two-settlement (DA + RT) energy market; price-taker storage (ISO/data not verified)"
method_class: "SP"
evidence_read: "abstract only (OpenAlex abstract_inverted_index + OSTI 1358239 record); full text (OSTI PDF) not retrievable in this session"
oa_link: "https://www.osti.gov/biblio/1358239"
---

## 1. Research question
How should a storage owner make DA bidding and operational decisions for arbitrage when both DA and RT prices are uncertain, and how much better is a stochastic formulation than a deterministic one?

## 2. Setting & assumptions
- Stochastic formulation of arbitrage profit maximisation under DA and RT price uncertainty (from abstract/OSTI).
- Decision support "in bidding and operational decisions" and estimation of economic viability (from abstract).
- Price-taker status, scenario method, stage structure, battery parameters: not verified.

## 3. Constraints that drove the model choice
Not verified.

## 4. Model
Stochastic program (two-settlement); structure not verified — do not assume two-stage vs multistage without the full text.

## 5. Data & processing
"Realistic market price data" (from abstract); market and period not verified.

## 6. Justification
Comparison against a deterministic benchmark (from abstract).

## 7. Key results
"Novel stochastic bidding approach does significantly better than the deterministic benchmark" (from abstract); no numbers verified.

## 8. Limitations (stated + critical reading)
- Critical: kim2021_vss later proves that for a price-taker with full RT flexibility the VSS of such DA/RT SPs is zero — so the reported gain must stem from limited RT flexibility, risk, or price-impact assumptions; check which when full text is available.

## 9. Relevance to my study
Most-cited US reference for DA+RT stochastic storage arbitrage; should be read in full before using as benchmark. Pair with kim2021_vss for the "when does stochastic programming matter" argument.

## 10. Lineage links
- Builds on: Conejo-school two-stage SP offering (conejo2002_pricetaker, pandzic2013_vppoffer).
- Built upon by: kim2021_vss (cites it as ref. [9]); Xu-group two-settlement work.

## 11. Verification log
- OpenAlex works/doi:10.1109/TPWRS.2017.2685347 → authors (Argonne), 33(1):84-93; OpenAlex year 2017 = online date, issue Jan 2018.
- OSTI 1358239 bibliographic record (abstract, Argonne/NREL orgs).
- SJR: IEEE TPWRS Q1 2023/2024.
- Full text (osti.gov/pages/servlets/purl/1358239) blocked by robots → all formulation fields left unverified.
