---
id: bhattacharjee2022_soemanagement
title: "Energy Storage Participation in Wholesale Markets: The Impact of State-of-Energy Management"
authors: ["Bhattacharjee, S.", "Sioshansi, R.", "Zareipour, H."]
year: 2022
journal: "IEEE Open Access Journal of Power and Energy"
volume_issue_pages: "9:173-182"
doi: "10.1109/OAJPE.2022.3174523"
quartile: "Q1 (SJR 2022-2025, Electrical & Electronic Engineering; Energy Engineering & Power Technology)"
group: "Zareipour (U. Calgary ECE) with Sioshansi (Ohio State / CMU)"
lineage: "Bhattacharjee = PhD University of Calgary (Zareipour group; affiliation stated in companion paper bhattacharjee2025_hybridparticipation), later NYISO. Sioshansi = Oren (Berkeley) PhD 2007."
streams: [S7_market_design]
market_context: "Alberta single-bus energy-only market (2015 data); FERC Order 841 SoE-management options"
method_class: "bilevel stochastic MPEC -> MILP (KKT + big-M + binary expansion)"
evidence_read: "full text (author PDF https://www.cmu.edu/ceic/people/rsioshan/docs/storage_mkt_participation.pdf)"
oa_link: "https://www.cmu.edu/ceic/people/rsioshan/docs/storage_mkt_participation.pdf"
---

## 1. Research question
How do participation-model choices allowed under FERC Order 841 - self-schedule vs price-responsive offers, and owner-managed vs MO-managed state of energy (SoE) - affect a strategic storage firm's profit, prices and welfare, and can owner-managed SoE be exploited for price manipulation?

## 2. Setting & assumptions
- One strategic (price-making) storage firm; rivals' offers fixed; demand uncertainty via equiprobable scenarios; storage offers scenario-invariant.
- Hourly (3-h illustrative, 24-h Alberta case); single bus.
- Terminal SoE heuristic e_{s,|H|} = gamma e_0; efficiency beta; charge/discharge exclusivity via binaries.
- Deviation from MO dispatch penalised at clearing price.

## 3. Constraints that drove the model choice
Need to capture how the MO's clearing (lower level) responds to storage offers -> bilevel; uncertainty needed because self-scheduling is only suboptimal when the firm cannot adapt to realisations. Bilinear price x quantity terms force binary expansion (discretisation) for MILP tractability, which limits horizon length.

## 4. Model
- Upper level: max expected profit = sum_s phi_s sum_h lambda_{s,h} (net discharge) - deviation penalties; decisions: self-scheduled quantities, offer prices/quantities, actual dispatch, owner-managed SoE.
- Lower level (per scenario): MO min cost s.t. load balance, generator capacity and ramping, storage power bounds, and - in the MO-managed case - SoE dynamics e^m_{s,h} = e^m_{s,h-1} - p^dis + beta p^ch with terminal constraint.
- Designs compared: (i) self-schedule only; (ii) price-responsive offers, owner-managed SoE; (iii) price-responsive offers, MO-managed SoE; (iv) MO enforces vs relaxes SoE feasibility.
- Solved in GAMS 34.3 / Gurobi 9.1.1 (NEOS).

## 5. Data & processing
Illustrative 4-generator system (100/75/50/50 MW, $12-$300/MWh, ramp limits); Alberta 2015 load (avg 9,162 MW), ~200 units aggregated to 14 archetypes, storage 40 MW/200 MWh, beta = 0.9, 3 scenarios from consecutive days.

## 6. Justification
Exact MPEC reformulation (KKT, Slater holds); controlled illustrative cases isolating each mechanism (uncertainty, ramping, SoE relaxation); Alberta case for magnitudes; benchmarks: no storage and perfectly competitive storage.

## 7. Key results
- Under uncertainty, restricting storage to self-schedules can drive expected profit to zero in the illustrative case; price-responsive offers cut generation cost ~30%.
- If the MO does not enforce SoE feasibility on owner-managed storage, the firm profits from submitting physically infeasible schedules to move prices: storage profit +3% to +78% (and +1,300% in a ramp-constrained case where consumer welfare fell 29%).
- Alberta: price-responsive offers with relaxed SoE: storage profit $3.52m vs $3.37m with SoE enforced vs $1.23m self-schedule-only vs $0.86m if storage is perfectly competitive.
- Recommendation: MO must enforce SoE feasibility (or penalise) when owners self-manage SoE.

## 8. Limitations (stated + critical reading)
Binary-expansion approximation; very short horizons; single bus; single strategic firm; 3 scenarios; RT imbalance settlement of deviations not modelled. Critical: monopoly bounding case overstates manipulation magnitudes; Alberta has no co-optimised reserves.

## 9. Relevance to my study
Directly isolates SoC-management rules as a market-design lever with an explicit counterfactual grid (2 offer formats x 2 SoE managers x enforce/relax). The design of "rule toggles" with fixed asset and fixed scenarios is a ready template for attributing revenue differences to rules. Also shows a rule interaction: SoE rules matter only when offers are price-responsive.

## 10. Lineage links
- Builds on: jiang2023_isodispatch (first-best ISO dispatch), MPEC strategic-storage literature (e.g., ruiz2009_mpecoffer), FERC Order 841.
- Built upon by (notable): bhattacharjee2025_hybridparticipation.

## 11. Verification log
- DOI 10.1109/OAJPE.2022.3174523 resolved via doi.org -> IEEE Xplore 9776576; Vol 9, pp 173-182, 2022 from Sioshansi CMU publication list.
- SJR: scimagojr sourceid 21101059747, Q1 2022-2025 both categories.
- Full text (author manuscript) read; funding NSF 1808169, NSERC, NSERC Energy Storage Technology Network.
