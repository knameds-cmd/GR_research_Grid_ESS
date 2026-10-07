---
id: hortacsu2019_strategicability
title: "Does Strategic Ability Affect Efficiency? Evidence from Electricity Markets"
authors: ["Hortaçsu, A.", "Luco, F.", "Puller, S. L.", "Zhu, D."]
year: 2019
journal: "American Economic Review"
volume_issue_pages: "109(12):4302-4342"
doi: "10.1257/aer.20172015"
quartile: "Q1 (SJR 2019 and 2025, Economics and Econometrics)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Hortaçsu (U Chicago, NBER) and Puller (Texas A&M, NBER); Luco (Texas A&M); Zhu (Shanghai Lixin Univ.)"
lineage: "Extends Hortaçsu & Puller 2008 RAND (ERCOT balancing-market bids vs ex-post best response). Advisor-student ties (e.g., Zhu) not verified."
streams: [S8_empirical_econ]
market_context: "ERCOT balancing energy market, unit/firm-level bid functions, Aug 2002-Jan 2003 (methods anchor; not storage)"
method_class: "econometric (structural: ex-post best response benchmark + cognitive-hierarchy bidding model, minimum distance)"
evidence_read: "full text (pre-publication version https://www.cireqmontreal.com/wp-content/uploads/2018/05/puller.pdf)"
oa_link: "https://www.cireqmontreal.com/wp-content/uploads/2018/05/puller.pdf"
---

## 1. Research question
How far do firms' observed bids deviate from (ex-post) Nash best responses, what explains heterogeneity in strategic sophistication, and how much efficiency is lost?

## 2. Setting & assumptions
- 99 hourly auctions (weekdays 18:00-18:15), 12 firms, step bid functions (<= 40 elbows); unit marginal costs; congested hours (26%) excluded.
- Forward-contract positions inferred where bid function crosses marginal cost.

## 3. Constraints that drove the model choice
Observed bids reject Nash; smaller firms leave money on the table. A model nesting non-strategic (level-0: vertical bid at contract position) to fully strategic behaviour is needed; additive separability of bid functions allows recursive level-k computation without fixed points.

## 4. Model
- Ex-post best response: residual demand RD_i(p) = D - sum_{j != i} S_j(p) from rivals' actual bids; optimal markup by inverse residual-demand elasticity net of contract position.
- Poisson cognitive hierarchy: level-k best-responds to rivals distributed over levels < k; tau_i = exp(X_i' gamma) with firm size, manager education.
- Estimation: minimum distance between observed and type-mixture predicted bids.

## 5. Data & processing
ERCOT bid and dispatch data, unit cost estimates (heat rates, fuel prices), demand; manager education from LinkedIn.

## 6. Justification
Model fit: CH explains 67% of profit variation vs 49% for best response. External test: 2,300 MW nuclear outage (Oct-Nov 2002) — large firms steepen bids, small firms do not respond to rivals' cost shocks (supports level-0).

## 7. Key results
- Except the largest firm, no firm captures more than half of potential (best-response) profits; $1,000-4,000/h left on the table.
- Raising low-type firms to median sophistication raises efficiency 9-16%.
- Mergers that raise sophistication can increase efficiency despite higher concentration.

## 8. Limitations (stated + critical reading)
- Six-month window early in market life; fringe unmodelled; congestion hours dropped; static auctions — no intertemporal (SoC) linkage, so applying to storage requires replacing marginal cost with an opportunity-cost (water/SoC value) model.

## 9. Relevance to my study
Methods anchor for "revealed-preference bid analysis": compute each storage unit's ex-post best response to the residual demand it actually faced and measure profit capture — the bid-level analogue of perfect-foresight arbitrage benchmarks in lamp2022. With GB data (Elexon BOD bid-offer pairs, EAC unit bids and clearing results), one can build residual supply curves per service/EFA block and test whether battery optimisers (autobidders) behave like level-0 (price-taking), best-responders, or coordinated (cf. Eschenbaum 2026 arXiv on shared NEM autobidders).

## 10. Lineage links
- Builds on: Hortaçsu & Puller 2008 RAND (ERCOT bids vs best response); Camerer-Ho-Chong 2004 cognitive hierarchy model.
- Built upon by: storage-bid analyses using the same benchmark logic (e.g., CAISO storage bid withholding studies, NEM autobidder conduct — working papers).

## 11. Verification log
- AEA article page: AER 109(12), Dec 2019, pp. 4302-42, DOI 10.1257/aer.20172015.
- SJR AER sourceid 22697: Q1 2019, 2025.
- Full text: CIREQ-hosted 2018 version (pre-publication).
- Included as a methods anchor (not storage-specific) to support the GB identification section.
