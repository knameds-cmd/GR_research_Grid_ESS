---
id: wankmuller2017_degradationarbitrage
title: "Impact of battery degradation on energy arbitrage revenue of grid-level energy storage"
authors: ["Wankmüller, F.", "Thimmapuram, P. R.", "Gallagher, K. G.", "Botterud, A."]
year: 2017
journal: "Journal of Energy Storage"
volume_issue_pages: "10:56-66"
doi: "10.1016/j.est.2016.12.004"
quartile: "Q1 (SJR 2025, J. Energy Storage, SJR 1.795; Q1 Energy Eng. & Power Tech., EEE, Renewable Energy)"
quartile_basis: "pub-year; rule=pass; SJR 2017 Q1 for this journal recorded in staffell2016_maxvalue"
group: "Audun Botterud (Argonne National Laboratory / MIT LIDS) with Argonne battery group (Gallagher) and KIT"
lineage: "Wankmüller = KIT student at Argonne (affiliations KIT + ANL); Botterud = senior author (ANL energy systems; MIT LIDS). Advisor relation not verified."
streams: [S4_degradation_operation, S1_foundations_value]
market_context: "MISO historical energy prices; price-taker arbitrage"
method_class: "LP/MILP arbitrage with degradation penalty (details not read)"
evidence_read: "abstract + OSTI record excerpt only — (from abstract)"
oa_link: "https://www.osti.gov/servlets/purl/1393934 (accepted manuscript; could not be fully read)"
---

## 1. Research question
How does battery degradation (and the way it is represented) change the energy-arbitrage revenue and NPV of grid-level Li-ion storage, and can a degradation penalty in the arbitrage objective improve lifetime profitability? (from abstract)

## 2. Setting & assumptions
- Price-taker arbitrage on historical MISO prices; 1C battery; end-of-life (EOL) criteria varied in sensitivity. (from abstract)

## 3. Constraints that drove the model choice
Limited prior work combining degradation modelling with arbitrage optimisation; two degradation representations compared. (from abstract)

## 4. Model
"Two different representations of battery degradation" and a penalty-cost term in the arbitrage objective. Formulation not read — do not reuse without the PDF.

## 5. Data & processing
MISO historical prices (years/nodes not verified).

## 6. Justification
Sensitivity across degradation representations and EOL criteria. (from abstract)

## 7. Key results
- NPV (10 % discount rate) falls from $358/kWh without degradation to $194–314/kWh with degradation.
- Degradation reduces arbitrage revenue by 12–46 % depending on assumptions.
- Penalising cycling in the objective improves profitability over the BESS life. (from abstract)

## 8. Limitations (stated + your critical reading)
Not read. Likely: price-taker, perfect foresight, single market.

## 9. Relevance to my study
Early, widely cited range (12–46 % revenue loss) for "how much degradation matters" in pure arbitrage; useful as a benchmark magnitude and for the lesson that the penalty weight is a tuning parameter, not a physical constant.

## 10. Lineage links
- Built upon by: he2018_intertemporal (opportunity-cost penalty), collath2023_lifetimeprofit (lifetime-optimal aging cost).

## 11. Verification log
- OpenAlex (doi:10.1016/j.est.2016.12.004): title, 4 authors with KIT/ANL/MIT affiliations, JES 10:56–66, 2017; OSTI repository location.
- OSTI purl excerpt (abstract-level text) read; full manuscript text could not be parsed.
- SJR: scimagojr.com sourceid 21100400826 → Q1 (2025, SJR 1.795).
