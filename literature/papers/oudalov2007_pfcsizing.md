---
id: oudalov2007_pfcsizing
title: "Optimizing a Battery Energy Storage System for Primary Frequency Control"
authors: ["Oudalov, A.", "Chartouni, D.", "Ohler, C."]
year: 2007
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "22(3):1259-1266"
doi: "10.1109/TPWRS.2007.901459"
quartile: "Q1 (SJR 2007, Electrical and Electronic Engineering; Energy Engineering and Power Technology)"
group: "ABB Corporate Research, Switzerland (Oudalov, Chartouni, Ohler)"
lineage: "Industrial research group (ABB CH); seminal reference for all later FCR-battery sizing work (ETH Zurich 1 MW BESS, RWTH, KU Leuven). No advisor-student tie claimed."
streams: [S6_ancillary_products]
market_context: "UCTE/Swiss primary frequency control (today's FCR), symmetric product"
method_class: "simulation-based sizing (time-series simulation on historic frequency) + rule-based SoC control"
evidence_read: "metadata + abstract only (OpenAlex abstract_inverted_index); full text paywalled (IEEE)"
oa_link: ""
---

## 1. Research question
What is the minimum battery capacity (hence lowest cost) that can provide primary frequency reserve while satisfying grid-code requirements, and is such a BESS profitable at European PFC prices? (from abstract)

## 2. Setting & assumptions
- Price-taker capacity provider of symmetric primary frequency reserve.
- Time-series simulation driven by historic measured grid frequency (the abstract says "numerical simulations based on historic measurements"; exact dataset/resolution not verified).
- Battery chemistry in the economic conclusion: lead-acid (as stated in abstract).
- Market: European PFC capacity remuneration ("current European market prices").

## 3. Constraints that drove the model choice
Energy-limited asset must deliver a continuous, frequency-proportional service with no planned recharging window; grid code requires full availability. This makes capacity sizing a reliability problem solved by simulation rather than optimisation (from abstract).

## 4. Model
- Objective: minimum energy capacity that still fulfils PFC technical requirements.
- Control: "novel control algorithm with adjustable state of charge limits and the application of emergency resistors" — i.e., when SoC limits are reached, surplus energy (over-frequency) can be dissipated in resistors instead of being absorbed by the battery, keeping the BESS available.
- Solution: iterate simulation over candidate sizes / SoC limits.

## 5. Data & processing
Historic grid-frequency measurements (UCTE area; period and resolution not verified from full text).

## 6. Justification
Compliance with grid-code technical requirements in simulation over measured frequency; economics at prevailing market prices (from abstract).

## 7. Key results
- An optimised lead-acid BESS "can be a profitable primary frequency control solution" at then-current European PFC prices (from abstract).
- Introduces two SoC-management levers that later became standard in rule debates: SoC-dependent operating limits and an energy sink (resistor) to stay available during long frequency excursions.

## 8. Limitations (stated + your critical reading)
- Pre-dates the regulatory "degrees of freedom" (deadband use, 20% over-fulfilment, set-point trading) formalised by German TSOs in 2015; results depend on 2007 PFC prices and lead-acid costs.
- Dissipating energy in resistors is an efficiency loss and was later replaced by intraday recharge/schedule trades in practice.
- Details not verified from full text.

## 9. Relevance to my study
Origin of the "energy-neutrality / endurance" problem for batteries in symmetric proportional products. Useful as the historical baseline for attributing profitability to rules: the paper shows sizing is driven by the product's continuous-availability requirement, not by arbitrage.

## 10. Lineage links
- Builds on: UCTE Operation Handbook PFC rules.
- Built upon by (notable): thien2017_fcrgermanystrategy, engels2019_fcrgermanytechnoeco, koltermann2022_fcrbalancinggroup; ETH Zurich 1 MW BESS studies (Koller et al. 2015 EPSR — not archived, unverified in this session).

## 11. Verification log
- OpenAlex works/doi:10.1109/TPWRS.2007.901459: title, year, journal, 22(3) 1259-1266, authors all ABB (Switzerland), abstract reconstructed. 535 citations (OpenAlex, Oct 2026).
- SJR (scimagojr.com sid 28825): IEEE TPWRS Q1 2007 in EEE and Energy Engineering.
- Full text NOT read; frequency dataset and numerical sizing results not verified.
