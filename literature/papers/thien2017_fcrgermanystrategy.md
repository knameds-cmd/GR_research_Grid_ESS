---
id: thien2017_fcrgermanystrategy
title: "Real-world operating strategy and sensitivity analysis of frequency containment reserve provision with battery energy storage systems in the german market"
authors: ["Thien, T.", "Schweer, D.", "vom Stein, D.", "Moser, A.", "Sauer, D.U."]
year: 2017
journal: "Journal of Energy Storage"
volume_issue_pages: "13:143-163"
doi: "10.1016/j.est.2017.06.012"
quartile: "Q1 (SJR 2017, Electrical and Electronic Engineering; Energy Engineering and Power Technology) [Q2 in Renewable Energy category]"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Dirk Uwe Sauer, ISEA / Institute for Power Generation and Storage Systems (PGS), RWTH Aachen; Albert Moser, IAEW RWTH Aachen; JARA-Energy"
lineage: "RWTH Sauer group (M5BAT project); Schweer/vom Stein from Moser's IAEW. Thien doctoral supervision by Sauer not verified in this session."
streams: [S6_ancillary_products]
market_context: "German FCR (Primärregelleistung), 2015 TSO rules with degrees of freedom"
method_class: "simulation + sensitivity analysis of a rule-based EMS (real 5 MW hybrid BESS)"
evidence_read: "abstract + figure captions (ResearchGate listing); full text paywalled"
oa_link: ""
---

## 1. Research question
Which operating-strategy parameters (recharging speed/flexibility, EMS design, use of regulatory degrees of freedom) determine whether an energy-limited BESS can provide German FCR continuously and compliantly? (from abstract)

## 2. Setting & assumptions
- Real system: M5BAT, 5 MW hybrid BESS with multiple battery technologies (Aachen).
- German FCR regulation incl. degrees of freedom: deadband utilisation and over-fulfilment (Fig. 3), valid operating range (Fig. 4), schedule transactions to maintain the 30-min criterion (Fig. 5).
- Frequency histogram used to drive simulations (Fig. 12; source/period not verified).

## 3. Constraints that drove the model choice
Continuous symmetric product with energy-limited asset; compliance depends on the speed with which corrective measures (schedule transactions/recharging) can be executed under market lead times.

## 4. Model
Rule-based EMS simulation; sensitivity over parameters of corrective measures (velocity/flexibility of recharging), degrees of freedom and SoC/SOE limits; outputs: SOE distributions, cycles, energy throughput (Figs. 14–26).

## 5. Data & processing
Historic grid frequency (Continental Europe; details not verified).

## 6. Justification
Based on the strategy actually deployed at M5BAT ("real-world operating strategy").

## 7. Key results
- "Velocity and flexibility of corrective measures (e.g. recharging) and an efficient EMS are prerequisites for FCR operation with BESS under the applicable regulation."
- Results indicate potential benefits from adjusting regulatory requirements, specifically the 30-minute criterion.
- Numerical values not verified (full text not read).

## 8. Limitations (stated + your critical reading)
Rules analysed are pre-2019/2020 (weekly auctions, 30-min criterion); later EU SOGL/German LER rules (15-min criterion, daily 4-h products) change results. No revenue model verified.

## 9. Relevance to my study
Canonical German reference that FCR-battery feasibility is governed by rule parameters (30-min criterion, intraday lead time for set-point trades, deadband/over-fulfilment freedoms) rather than by battery technology. Use as source for the German rule-parameter list.

## 10. Lineage links
- Builds on: oudalov2007_pfcsizing; German TSO "Eckpunkte und Freiheitsgrade bei Erbringung von Primärregelleistung" (2015).
- Built upon by (notable): engels2019_fcrgermanytechnoeco, koltermann2022_fcrbalancinggroup, celicortes2025_deterministicfreq.

## 11. Verification log
- OpenAlex works/doi:10.1016/j.est.2017.06.012: title, 13:143-163, authors and RWTH affiliations (PGS/ISEA, IAEW, JARA). Abstract and figure captions from ResearchGate listing (OpenAlex abstract null). RWTH ISEA page confirms bibliographic data.
- SJR sid 21100400826: J. Energy Storage Q1 2017 (EEE; Energy Eng.).
- Full text NOT read.
