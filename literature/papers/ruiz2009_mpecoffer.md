---
id: ruiz2009_mpecoffer
title: "Pool Strategy of a Producer With Endogenous Formation of Locational Marginal Prices"
authors: ["Ruiz, C.", "Conejo, A. J."]
year: 2009
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "24(4):1855-1866"
doi: "10.1109/TPWRS.2009.2030378"
quartile: "Q1 (SJR 2024, IEEE Trans. Power Systems, SJR 3.629; Q1 Electrical & Electronic Eng. and Energy Eng. & Power Tech.)"
group: "Conejo (UCLM)"
lineage: "Both authors UCLM (OpenAlex). Ruiz = Conejo PhD student at UCLM (widely documented; not re-verified this session). Template for all later storage MPEC/bilevel offering papers (mohsenianrad2016_pricemaker, wang2017_lookahead, nasrolahpour2018_bilevel, tomasson2020_offerbid)."
streams: [S3_bidding_uncertainty]
market_context: "Generic pool, multiperiod network-constrained (DC) market clearing producing LMPs; strategic thermal producer"
method_class: "MILP (bilevel → MPEC → MILP via KKT + duality)"
evidence_read: "abstract only (OpenAlex abstract_inverted_index); full text closed"
oa_link: ""
---

## 1. Research question
How should a strategic (price-making) producer build its offers when LMPs are formed endogenously by a network-constrained, multiperiod market clearing, and rival offers/demand bids are uncertain?

## 2. Setting & assumptions
- Price-maker; LMPs determined by lower-level DC-OPF market clearing (from abstract).
- Multiperiod clearing; uncertainty in demand bids and rival producers' strategies (from abstract) — represented by scenarios (exact count not verified).

## 3. Constraints that drove the model choice
(from abstract) Bilevel problem (upper: producer profit; lower: market clearing/price formation) is nonconvex; reduced to MILP using duality theory and KKT conditions so it can be solved to global optimality with commercial MILP solvers.

## 4. Model
- Upper level: max expected profit of the strategic producer.
- Lower level: multiperiod network-constrained market clearing (LP) → LMPs as duals.
- Reformulation: KKT of lower level + strong duality to linearise price×quantity, complementarity via binaries → MILP (from abstract).
- Offer format, scenario count, solver: not verified.

## 5. Data & processing
Illustrative example + case study (from abstract); details not verified.

## 6. Justification
Exactness of the KKT/duality reformulation for LP lower levels (standard argument); numerical illustration.

## 7. Key results
Not verified (no numbers in abstract).

## 8. Limitations (stated + critical reading)
- Critical: lower level must be convex (LP) for KKT exactness — rules out unit-commitment clearing; uncertainty limited to scenarios of rivals/demand; big-M selection affects correctness.
- For storage: intertemporal SoC coupling sits naturally in the multiperiod upper level, which is why later storage papers inherit this structure directly.

## 9. Relevance to my study
Methodological template for any price-maker battery bidding model (bilevel → MILP). Needed when arguing whether a GB/Nordic battery can be treated as price-taker; the MPEC is the benchmark for "with market power".

## 10. Lineage links
- Builds on: Hobbs, Metzler & Pang (2000) MPEC for strategic bidding (not in archive); conejo2002_pricetaker (price-taker counterpart).
- Built upon by: mohsenianrad2016_pricemaker, wang2017_lookahead, nasrolahpour2018_bilevel, tomasson2020_offerbid; Ruiz, Conejo & Smeers EPEC work (not in archive).

## 11. Verification log
- OpenAlex works/doi:10.1109/TPWRS.2009.2030378 → title, Ruiz & Conejo (UCLM), 24(4):1855-1866, 2009; abstract reconstructed from inverted index.
- SJR: IEEE TPWRS Q1 2023/2024 (scimagojr id 28825).
- Full text not read; formulation statements limited to the abstract.
