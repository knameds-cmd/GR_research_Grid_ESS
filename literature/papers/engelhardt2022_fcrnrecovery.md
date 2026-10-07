---
id: engelhardt2022_fcrnrecovery
title: "Energy recovery strategies for batteries providing frequency containment reserve in the Nordic power system"
authors: ["Engelhardt, J.", "Thingvad, A.", "Zepter, J.M.", "Gabderakhmanova, T.", "Marinelli, M."]
year: 2022
journal: "Sustainable Energy, Grids and Networks"
volume_issue_pages: "32:100947"
doi: "10.1016/j.segan.2022.100947"
quartile: "Q1 (SJR 2022, Energy Engineering and Power Technology; Electrical and Electronic Engineering; Control and Systems Engineering)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Mattia Marinelli, DTU Wind and Energy Systems (Distributed Energy Systems)"
lineage: "Marinelli group (DTU); Thingvad = former DTU PhD in Marinelli group (EV FCR-N), here at Hybrid Greentech; Engelhardt/Zepter/Gabderakhmanova DTU (Bornholm EnergyLab). Supervision ties not verified in this session."
streams: [S6_ancillary_products]
market_context: "Nordic FCR-N (and FCR-D context), DK2 / Energinet rules incl. exemption agreement"
method_class: "multi-year time-series simulation of energy-management strategies"
evidence_read: "abstract only (DTU Orbit + OpenAlex); CC-BY full text on Orbit returned 403"
oa_link: "https://orbit.dtu.dk/en/publications/energy-recovery-strategies-for-batteries-providing-frequency-cont/"
---

## 1. Research question
Which energy-recovery (SoC restoration) strategy compliant with Nordic FCR rules maximises regulating capacity and profit for a battery, given long frequency-bias periods and the Nordic requirement of 100% delivery certainty?

## 2. Setting & assumptions
- Nordic synchronous area FCR; DK2 market/tariffs; 100% delivery certainty mandated.
- Three strategies: (1) hourly reference-power adjustment traded on the intraday market; (2) hourly reference adjustment settled on the balancing (imbalance) market; (3) Energinet (Danish TSO) exemption agreement.

## 3. Constraints that drove the model choice
Long-duration frequency bias in the Nordic system drives batteries to SoC limits; legal recovery routes differ in lead time and cost, so they are compared by simulation over multi-year data.

## 4. Model
Simulation of FCR delivery + recovery strategies over three years; profit = capacity payments − energy/tariff costs (from abstract).

## 5. Data & processing
Three years of historical frequency, market and tariff data (years/resolution not verified).

## 6. Justification
Strategies respect regulatory requirements; multi-year back-test.

## 7. Key results
- Capacity payment is "the strongest factor that determines profit".
- Highest regulating power and profit with the Energinet exemption agreement.
- Without an exemption, balancing-market settlement beats intraday trading despite slightly higher energy costs.

## 8. Limitations (stated + your critical reading)
Abstract-level; Nordic FCR rules were overhauled in 2022–2024 (new technical requirements incl. LER endurance, FCR-D down, EU harmonised rules) — results tied to pre-reform Danish rules.

## 9. Relevance to my study
Shows the *route* by which SoC recovery is allowed (intraday trade vs imbalance settlement vs TSO exemption) materially changes how much capacity a battery can sell per MWh — a key rule parameter for Nordic vs GB comparison.

## 10. Lineage links
- Builds on: oudalov2007_pfcsizing; Thingvad et al. (EV FCR-N, DTU).
- Built upon by (notable): cao2024_dcvsefr (same group, GB DC); mirzaeialavijeh2025_swedenfcrstacking (Swedish FCR, archived by another stream).

## 11. Verification log
- DTU Orbit + OpenAlex works/doi:10.1016/j.segan.2022.100947: 32:100947, authors/affiliations (DTU; Thingvad at Hybrid Greentech ApS), abstract. SSRN preprint exists (10.2139/ssrn.4093894, Crossref).
- SJR sid 21100371258: SEGAN Q1 2022 (EEE, Energy Eng., Control).
- Full text NOT read.
