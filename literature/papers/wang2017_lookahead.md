---
id: wang2017_lookahead
title: "Look-Ahead Bidding Strategy for Energy Storage"
authors: ["Wang, Y.", "Dvorkin, Y.", "Fernández-Blanco, R.", "Xu, B.", "Qiu, T.", "Kirschen, D. S."]
year: 2017
journal: "IEEE Transactions on Sustainable Energy"
volume_issue_pages: "8(3):1106-1117"
doi: "10.1109/TSTE.2017.2656800"
quartile: "Q1 (SJR 2024, IEEE Trans. Sustainable Energy, SJR 4.261; Q1 Renewable Energy, Sustainability & Environment)"
group: "Kirschen (Univ. of Washington) with Dvorkin (NYU at publication)"
lineage: "OpenAlex: Wang, Fernández-Blanco, Xu, Qiu, Kirschen at UW; Dvorkin at NYU Tandon (Dvorkin = UW PhD under Kirschen — widely documented, not re-verified this session). Xu (co-author) = Kirschen PhD 2018 → later Columbia group (zheng2022_asdp)."
streams: [S3_bidding_uncertainty]
market_context: "Day-ahead, ramp-constrained multiperiod nodal market; IEEE Reliability Test System; merchant price-maker battery"
method_class: "MILP (bilevel → KKT + linearisation)"
evidence_read: "abstract only (OpenAlex abstract_inverted_index); full text closed"
oa_link: ""
---

## 1. Research question
How should a merchant price-maker storage operator set its end-of-day state-of-charge when bidding into the day-ahead market, given that it is the next day's initial SoC?

## 2. Setting & assumptions
- Price-maker; lower level clears a ramp-constrained multiperiod market (from abstract).
- Look-ahead: discounted profit opportunities of the following day included to optimise end-of-day SoC (from abstract).
- Network and ramping constraints in IEEE RTS (from abstract).
- Uncertainty treatment (deterministic vs scenarios) and battery parameters: not verified.

## 3. Constraints that drove the model choice
(from abstract) Bilevel → single-level MILP via linearisation and KKT. Look-ahead (two-day) horizon chosen because final SoC strongly affects profitability.

## 4. Model
- Upper level: storage bidding over day 1 plus discounted day-2 profit (from abstract).
- Lower level: ramp-constrained multiperiod market clearing (from abstract).
- Bid format, scenario structure, discount factor: not verified.

## 5. Data & processing
IEEE Reliability Test System (from abstract); others not verified.

## 6. Justification
Numerical comparison with/without look-ahead under ramping and network constraints (from abstract).

## 7. Key results
Not verified (abstract states benefits qualitatively).

## 8. Limitations (stated + critical reading)
- Critical: two-day deterministic look-ahead is a heuristic surrogate for an infinite-horizon value of terminal SoC; the later Xu-group work replaces it with an explicit opportunity-value function (zheng2022_asdp).

## 9. Relevance to my study
The "terminal SoC value" problem is central to any daily battery bidding model (DA auctions in GB/Nordics); cite as motivation for value-function terminal conditions.

## 10. Lineage links
- Builds on: ruiz2009_mpecoffer; mohsenianrad2016_pricemaker.
- Built upon by: zheng2022_asdp (Xu, a co-author, moves to value-function approaches).

## 11. Verification log
- OpenAlex works/doi:10.1109/TSTE.2017.2656800 → all 6 authors and affiliations, 8(3):1106-1117, 2017; abstract reconstructed from inverted index.
- SJR: IEEE TSTE id 19700177027, Q1 2023/2024.
- Full text not read (IEEE closed; ResearchGate blocked).
