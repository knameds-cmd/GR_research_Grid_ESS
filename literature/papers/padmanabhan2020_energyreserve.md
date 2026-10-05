---
id: padmanabhan2020_energyreserve
title: "Battery Energy Storage Systems in Energy and Reserve Markets"
authors: ["Padmanabhan, N.", "Ahmed, M.", "Bhattacharya, K."]
year: 2020
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "35(1):215-226"
doi: "10.1109/TPWRS.2019.2936131"
quartile: "Q1 (SJR 2025, IEEE Trans. Power Systems, SJR 4.217)"
group: "Kankar Bhattacharya (Univ. of Waterloo, ECE) with IESO Ontario (M. Ahmed)"
lineage: "Padmanabhan = Waterloo PhD student of Bhattacharya (affiliation + senior authorship; advisor tie not separately verified). Funded by NSERC Energy Storage Technology (NEST) Network."
streams: [S4_degradation_operation, S7_market_design]
market_context: "ISO-level LMP-based co-optimised day-ahead energy + spinning reserve clearing (IESO practice motivates; simulated on modified IEEE RTS)"
method_class: "MILP market clearing with BESS degradation-cost offers (multi-linear regression of DoD/discharge-rate cost)"
evidence_read: "full text (Univ. Waterloo WISE research-spotlight PDF, https://uwaterloo.ca/waterloo-institute-sustainable-energy/sites/default/files/uploads/documents/kankar_bhattacharya_research_spotlight_article_111120.pdf)"
oa_link: "see evidence_read"
---

## 1. Research question
How should an ISO represent BESS (with degradation cost) inside a co-optimised energy + spinning-reserve market-clearing model, and how does the degradation-aware offer change clearing quantities, prices and welfare?

## 2. Setting & assumptions
- ISO-side social-welfare maximisation with DC power flow, 10 % spinning reserve requirement, ISO-monitored SoC ("energy level mode").
- 10 BESS units (250 MW / 240 MWh total) on 5 buses of modified IEEE RTS (loads +25 %), single 24-h day.
- Cyclic aging only (DoD + discharge rate); climate-controlled (no T effect); charging half-cycle causes no aging; calendar aging neglected.
- Spinning-reserve offer cost assumed 25 % of BESS operating cost.

## 3. Constraints that drove the model choice
Degradation cost depends non-linearly on SoC at both ends of a step and on discharge rate; market clearing must stay MILP → linear regression surrogate of the non-linear cost so it can be submitted as an offer component.

## 4. Model
- Non-linear per-step degradation cost: C_k = C_B/(B_E,cap η²) · γ · [(1 − SOC_k)^ω − (1 − SOC_{k−1})^ω] (cycle-life power law in DoD, cost by battery capital C_B).
- Linear surrogate: C_k = a·SOC_k + b·SOC_{k−1} + c·DCR_k + d, DCR = discharge rate (ΔSOC per unit time); fitted a = −36.23, b = 34.80, c = 2.77, d = −2.45 (adj. R² 0.866 vs. 0.932 for non-linear fit).
- Discharge-rate effect linear up to 3C, exponential above (from cited data).
- BESS bid structure: charging bids (price, quantity), discharging offers including degradation coefficients, spinning reserve offers.
- Solver: MIP.

## 5. Data & processing
Cycle-life data from manufacturer/vendor sources and literature (refs [34]–[36] in paper); η = 0.9; IEEE RTS data.

## 6. Justification
Case comparison: (1) no BESS, (2) BESS with simple bids (no degradation), (3) degradation-aware bids; regression fit statistics.

## 7. Key results
- Degradation-aware offers reduce cleared charge/discharge volumes vs. naive bids, yet yield higher social welfare benefit in the reported case.
- LMP at a congested bus reduced by up to 44 % (h14) and 29 % (h18); BESS supply ~10 % of reserve requirement, lowering peak reserve prices.
- No battery-life or cycle-count outcomes reported.

## 8. Limitations (stated + your critical reading)
- Stated: excludes flow batteries; no temperature/calendar aging; assumed reserve cost share; one test day on IEEE RTS; bid data unavailable.
- Critical: linear regression in SOC_k, SOC_{k−1} is not a convex representation of a cycle-depth cost and can assign negative costs; single-day horizon cannot reveal lifetime trade-offs.

## 9. Relevance to my study
Example of the ISO-side ("market rule") view: what degradation information a market lets storage express in offers. Useful contrast with xu2018_cycleagingcost's SoC-segment bids; a market-rule study should state which representation the clearing engine admits.

## 10. Lineage links
- Builds on: cycle-life power laws; IESO storage-participation consultations.
- Related: xu2018_cycleagingcost (segment-based offer alternative).

## 11. Verification log
- OpenAlex (doi:10.1109/TPWRS.2019.2936131): title, authors (Waterloo; IESO/Ain Shams), TPWRS 35(1):215–226; online 2019, issue Jan 2020.
- Full text read from Waterloo WISE PDF (identified as the published paper).
- SJR: scimagojr.com sourceid 28825 → Q1.
