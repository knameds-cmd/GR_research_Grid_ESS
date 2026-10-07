---
id: tomasson2020_offerbid
title: "Optimal offer-bid strategy of an energy storage portfolio: A linear quasi-relaxation approach"
authors: ["Tómasson, E.", "Hesamzadeh, M. R.", "Wolak, F. A."]
year: 2020
journal: "Applied Energy"
volume_issue_pages: "260:114251"
doi: "10.1016/j.apenergy.2019.114251"
quartile: "Q1 (SJR 2024, Applied Energy; Q1 in all four categories)"
quartile_basis: "pub-year; rule=pass; SJR 2020 Q1 for this journal recorded in mallapragada2020_longrunvalue"
group: "Hesamzadeh (KTH Royal Institute of Technology) with Wolak (Stanford, Program on Energy and Sustainable Development)"
lineage: "Tómasson = KTH PhD (Hesamzadeh senior; supervision not re-verified). Wolak = leading empirical market-power economist → market-power framing."
streams: [S3_bidding_uncertainty]
market_context: "Nodal pool with merchant storage portfolio exercising market power; stochastic market conditions (details not verified)"
method_class: "MILP (stochastic bilevel → KKT → stochastic bilinear → disjunctive program; custom branch-and-bound with linear quasi-relaxation)"
evidence_read: "abstract only (IDEAS/RePEc record; OpenAlex metadata); full text closed"
oa_link: ""
---

## 1. Research question
How can a profit-maximising merchant storage portfolio with market power compute optimal stochastic offer (discharge) and bid (charge) curves efficiently, and how does its strategic behaviour differ from welfare-maximising storage operation?

## 2. Setting & assumptions
- Price-maker merchant storage portfolio; stochastic setting (from abstract).
- Offers and bids are discretised (from abstract) — i.e., price levels on a grid.

## 3. Constraints that drove the model choice
(from abstract) Non-linear bilevel → single-level stochastic bilinear program via KKT; bilinearity handled by discretising offers/bids into a stochastic disjunctive program; generic MILP solvers slow → bespoke branch-and-bound with linear quasi-relaxation.

## 4. Model
- Upper: expected merchant profit; lower: market clearing (KKT) (from abstract).
- Offer/bid curves: discretised price levels (from abstract); number of steps, monotonicity rules: not verified.
- Algorithm: B&B with linear quasi-relaxation (from abstract).

## 5. Data & processing
Not verified.

## 6. Justification
Computational comparison with existing literature approaches (from abstract).

## 7. Key results
- Merchant storage exercises market power via "demand withholding, generation withholding and under-use", increasing congestion vs welfare-maximising storage (from abstract).
- Superior computational performance vs existing approaches (from abstract; numbers not verified).

## 8. Limitations (stated + critical reading)
- Critical: discretised offers → solution quality depends on grid; scenario count presumably small (not verified).

## 9. Relevance to my study
Names the three withholding mechanisms of strategic storage — useful vocabulary and hypotheses for market-design analysis (GB/Nordic) and for interpreting learned RL bids as possible withholding.

## 10. Lineage links
- Builds on: ruiz2009_mpecoffer; mohsenianrad2016_pricemaker; nasrolahpour2018_bilevel.
- Built upon by: storage market-power literature (e.g., EJOR 2023 monopolistic storage paper surfaced in search; not verified/not in archive).

## 11. Verification log
- IDEAS/RePEc a/eee/appene/v260y2020ics0306261919319385 → authors, vol 260, 2020, DOI, abstract.
- OpenAlex works/doi:10.1016/j.apenergy.2019.114251 → affiliations KTH, KTH, Stanford; article 114251 (OpenAlex year 2019 = online).
- SJR: Applied Energy Q1 2023/2024.
- Full text not read.
