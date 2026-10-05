---
id: bhattacharjee2025_hybridparticipation
title: "Comparing Participation Models in Electricity Markets for Hybrid Energy-Storage Resources"
authors: ["Bhattacharjee, S.", "Sioshansi, R.", "Zareipour, H."]
year: 2025
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "40(1):650-661"
doi: "10.1109/TPWRS.2024.3397590"
quartile: "Q1 (SJR 2024, Electrical & Electronic Engineering; Energy Engineering & Power Technology)"
group: "Zareipour (U. Calgary ECE) with Sioshansi (CMU EPP/ECE)"
lineage: "Bhattacharjee = PhD University of Calgary (stated in paper), now NYISO; Zareipour group. Sequel to bhattacharjee2022_soemanagement."
streams: [S7_market_design]
market_context: "Alberta energy-only market (2015 data); US hybrid-resource participation models (co-located vs integrated, as in CAISO/SPP/MISO filings)"
method_class: "bilevel stochastic MPEC -> MILP"
evidence_read: "full text (author PDF https://www.cmu.edu/ceic/people/rsioshan/docs/storage_hybrid_mkt_participation.pdf)"
oa_link: "https://www.cmu.edu/ceic/people/rsioshan/docs/storage_hybrid_mkt_participation.pdf"
---

## 1. Research question
For solar-plus-storage hybrids, how do the two participation models used by US ISOs - co-located (separate offers per component) vs integrated (single offer for the plant) - affect hybrid profit, price formation, rivals' profits, consumers and social welfare?

## 2. Setting & assumptions
- Hybrid owner is price-making (monopolist bounding case); rivals' offers fixed; 3 equiprobable scenarios for load/solar/rival offers; offers scenario-invariant.
- Hourly day; single bus; POI limits; IHR has inverter-loading-ratio (ILR) limits and cannot offer supply and demand in the same hour.
- Storage 50 MW/200 MWh, beta = 0.9; solar 150 MW; ILR 1.3 baseline.

## 3. Constraints that drove the model choice
Participation model changes both the offer space and the information the MO sees; capturing price effects of withholding/curtailment needs a bilevel structure. Bilinear revenue terms linearised by strong duality and binary expansion.

## 4. Model
- CHR upper level: max expected profit over separate solar, discharge and charge offers; behind-the-meter charging from curtailed solar; deviation penalties; SoE dynamics and terminal ratio gamma.
- IHR upper level: single offer per hour (supply or demand), aggregate capacity limited by component ratings and ILR.
- Lower level: MO welfare-maximising clearing per scenario; KKT + Fortuny-Amat big-M; GAMS 24.4.6 + CPLEX 12.6.2.
- Sensitivities: prohibition of grid charging (ITC-type rule), ILR 1.1-1.9, degradation cost $5-$25/MWh.

## 5. Data & processing
Stylised 3-h, 4-generator example; Alberta 2015, 23 archetypal generators; solar from NREL SAM + NSRDB.

## 6. Justification
Controlled comparison: same asset, same scenarios, only participation model changes; benchmarks of perfect competition and no hybrid; sensitivity to rules that commonly accompany hybrid models.

## 7. Key results
- Alberta base case: total hybrid profit nearly identical (CHR $214k vs IHR $213k vs $71k if perfectly competitive), but composition differs: storage profit $39k (CHR) vs $25k (IHR, -36%); solar $175k vs $188k.
- Generator profit $27.1m (CHR) vs $26.5m (IHR); consumer welfare $221.7m vs $222.3m; social welfare essentially equal (~$249.03m).
- Illustrative case: IHR lowers hybrid profit 11%; CHR enables more price elevation (generator profit +58%, consumer welfare -3%).
- Grid-charging ban reduces profits modestly (IHR more affected); higher ILR lowers IHR profit (~-$38k from ILR 1.1 to 1.9) and raises curtailment; degradation cost >= $25/MWh erases CHR's advantage.

## 8. Limitations (stated + critical reading)
Single bus, monopoly bounding case, few scenarios, no ancillary services or capacity products, fixed rival offers. Critical: welfare equivalence suggests participation model mainly redistributes surplus; results specific to an energy-only market with high price cap.

## 9. Relevance to my study
Shows the methodological pattern "hold asset + scenarios fixed, swap participation rule, decompose profit by component and surplus by stakeholder". Its finding that participation rules can change revenue composition without changing totals warns that attributing battery revenue to a rule needs component-level decomposition, not just totals.

## 10. Lineage links
- Builds on: bhattacharjee2022_soemanagement, jiang2023_isodispatch.
- Built upon by (notable): none verified yet.

## 11. Verification log
- DOI resolved via doi.org -> IEEE Xplore 10522605 (matching title in search listing); Vol 40, No 1, pp 650-661, Jan 2025 from Sioshansi CMU list; manuscript shows received 15 Sep 2023, accepted 3 May 2024.
- SJR: scimagojr sourceid 28825, Q1 2024.
- Full text (author manuscript) read; funding NSF 1463492, 1808169, 1922666, CMU Electricity Industry Center, NSERC.
