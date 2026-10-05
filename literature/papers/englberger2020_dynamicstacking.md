---
id: englberger2020_dynamicstacking
title: "Unlocking the Potential of Battery Storage with the Dynamic Stacking of Multiple Applications"
authors: ["Englberger, S.", "Jossen, A.", "Hesse, H."]
year: 2020
journal: "Cell Reports Physical Science"
volume_issue_pages: "1(11):100238"
doi: "10.1016/j.xcrp.2020.100238"
quartile: "No SJR quartile for 2020 (journal launched 2020; first SJR-ranked year 2021). Q1 2021-2025 in all five categories (Energy (misc.); Engineering (misc.); Chemistry (misc.); Materials Science (misc.); Physics and Astronomy (misc.)); SJR 2025 = 1.784"
group: "Andreas Jossen & Holger Hesse, Institute for Electrical Energy Storage Technology (EES), Technical University of Munich"
lineage: "TUM EES (Jossen chair). Englberger = EES doctoral researcher (TUM EES alumni page; mediaTUM author record). Hesse = EES group leader for stationary storage. Same institute as the TUM BESS simulation and aging-aware operation work (see the degradation stream)."
streams: [S2_stacking_cooptimization]
market_context: "Germany: FCR (PCR) + peak shaving + self-consumption increase + spot-market (intraday continuous) trading; BTM and FTM applications on one stationary Li-ion BESS"
method_class: "MILP"
evidence_read: "abstract (Semantic Scholar API, official summary) + TUM institute news summary; full text (CC BY, Gold OA) not retrievable via tools (publisher blocks automated access)"
oa_link: "https://doi.org/10.1016/j.xcrp.2020.100238"
---

## 1. Research question
Can **dynamic stacking**, meaning time-varying reallocation of power and energy capacity among applications, make a BESS profitable under current (2020) German regulation where single applications are not? (from abstract)

## 2. Setting & assumptions
(from abstract)
- Multi-use optimisation framework that **distinguishes behind-the-meter and in-front-of-the-meter applications**.
- It considers how **power capacity** is allotted as well as **energy capacity**.
- Rolling-horizon optimisation with an **integrated degradation model**.
- Driven by real-world data from a stationary Li-ion battery in Germany.
- Price foresight and resolution not confirmed (full text not read).

## 3. Constraints that drove the model choice
(from abstract) Applications differ in metering location (BTM vs FTM) and in their power and energy needs. Static partitioning wastes capacity, which motivates time-varying allocation inside a rolling horizon.

## 4. Model
- (from abstract) Rolling-horizon optimisation allocating power and energy capacity among FCR, peak shaving, self-consumption increase and intraday trading, with integrated degradation. Exact formulation class not confirmed. The MILP label is provisional and must be checked against the full text.
- **Capacity split: dynamic** (the paper's central contribution). The allocation is re-optimised over the rolling horizon rather than fixed.
- FCR energy/SoC rules (German PQ/30-min criterion): **not read**.

## 5. Data & processing
(from abstract) Real-world data from a stationary Li-ion BESS in Germany. Price and load sources not read.

## 6. Justification (why the authors argue the approach is valid)
(from abstract) NPV comparison across application combinations.

## 7. Key results
- (from abstract) Peak shaving + FCR: NPV per € invested = 1.00.
- Adding intraday continuous arbitrage: 1.24.

## 8. Limitations (stated + your critical reading)
- Not read.
- Critical reading: the 2020 German FCR prices and weekly-to-daily product changes strongly affect the results. Dynamic stacking assumes regulation allows the FCR-dedicated capacity to change between product periods.

## 9. Relevance to my study
- Explicit articulation of **static vs dynamic stacking** and of **separate power vs energy allocation**. Both dimensions should be parametrised when comparing stacking-permission rules.
- High priority to read the full text (Gold OA, CC BY) for the allocation constraints.

## 10. Lineage links
- Builds on: TUM EES multi-use and simulation work; the "combining applications" argument (e.g., Stephan et al. 2016, Nature Energy; S1). Reference list not read.
- Built upon by (notable): not checked.

## 11. Verification log
- Crossref (api.crossref.org/works/10.1016/j.xcrp.2020.100238): title, authors, vol 1, issue 11, article 100238, Nov 2020, CC BY 4.0. Confirmed.
- Abstract from the Semantic Scholar API (verbatim publisher summary).
- TUM MEP news page gives the same NPV figures.
- Full text blocked (cell.com 403; ScienceDirect robots).
- SJR (id 21101037113): Q1 2025 in all categories.
- Method-class label provisional.
- 2026-10-06 independent verifier: quartile field clarified - SJR lists no quartile for the 2020 publication year (first ranked year 2021, Q1 2021-2025) (https://www.scimagojr.com/journalsearch.php?q=21101037113&tip=sid). Bibliographic data re-confirmed via OpenAlex (https://api.openalex.org/works/doi:10.1016/j.xcrp.2020.100238).
