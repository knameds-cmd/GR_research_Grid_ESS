---
id: koltermann2022_fcrbalancinggroup
title: "Balancing group deviation & balancing energy costs due to the provision of frequency containment reserve with a battery storage system in Germany"
authors: ["Koltermann, L.", "Jacqué, K.", "Figgener, J.", "Zurmühlen, S.", "Sauer, D.U."]
year: 2022
journal: "International Journal of Electrical Power & Energy Systems"
volume_issue_pages: "142:108327"
doi: "10.1016/j.ijepes.2022.108327"
quartile: "Q1 (SJR 2022, Electrical and Electronic Engineering; Energy Engineering and Power Technology)"
group: "Dirk Uwe Sauer, ISEA RWTH Aachen / JARA-Energy (Figgener, Zurmühlen)"
lineage: "RWTH ISEA Sauer group; continues thien2017_fcrgermanystrategy line; Koltermann also co-author of celicortes2025_deterministicfreq."
streams: [S6_ancillary_products]
market_context: "German FCR + balancing-group settlement (reBAP imbalance price)"
method_class: "simulation model validated with field data (6 MW BESS)"
evidence_read: "abstract only (RWTH ISEA page + OpenAlex); OA PDF (CC BY) exists on publications.rwth-aachen.de but could not be parsed by fetcher"
oa_link: "http://publications.rwth-aachen.de/record/847118/files/847118.pdf"
---

## 1. Research question
How much energetic imbalance does FCR provision by a battery create in its balancing group (since FCR activation energy is not separately settled in Germany), and what are the resulting balancing-energy costs or gains under German settlement pricing?

## 2. Setting & assumptions
- German FCR: activated energy flows into the provider's balancing group, settled at the imbalance price (reBAP); degrees of freedom (deadband, over-fulfilment) let the operator charge/discharge additional energy.
- Real 6 MW battery used for validation.

## 3. Constraints that drove the model choice
Energy settlement is implicit (via balancing group), so the cost/benefit of SoC management must be simulated against measured frequency and imbalance prices rather than an explicit FCR energy price.

## 4. Model
Simulation of FCR delivery + SoC management, computing balancing-group deviation and its valuation at reBAP; validated with operational field data (from abstract).

## 5. Data & processing
Operational data of a 6 MW BESS; German frequency and reBAP prices (periods not verified).

## 6. Justification
Validation against field data of the 6 MW system.

## 7. Key results
- Regulatory flexibility lets the operator charge or discharge 8.68–9 MWh per MW per month.
- Resulting additional profit €302–1,068 per MW per month from German settlement pricing.
- FCR provision "can be seen as a positive gain for the balancing group" (abstract).

## 8. Limitations (stated + your critical reading)
Abstract-level only; outcome depends on German reBAP design (single price, no separate FCR energy remuneration) and on degrees of freedom that TSOs can revise.

## 9. Relevance to my study
Quantifies a second-order rule effect: how FCR activation energy is *settled* (implicitly via imbalance price vs explicitly) changes battery economics by ~€0.3–1.1k/MW/month. Strong evidence for including "energy settlement of activated reserve" as a product-rule parameter.

## 10. Lineage links
- Builds on: thien2017_fcrgermanystrategy; engels2019_fcrgermanytechnoeco.
- Built upon by (notable): celicortes2025_deterministicfreq.

## 11. Verification log
- OpenAlex works/doi:10.1016/j.ijepes.2022.108327: 142:108327, authors all RWTH/JARA (Sauer also FZ Jülich, HI Münster); abstract.
- RWTH ISEA publication page: title, authors, abstract.
- SJR sid 17985: IJEPES Q1 2022.
- Full text NOT read.
