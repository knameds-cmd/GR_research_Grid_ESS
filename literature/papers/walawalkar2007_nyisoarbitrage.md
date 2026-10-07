---
id: walawalkar2007_nyisoarbitrage
title: "Economics of electric energy storage for energy arbitrage and regulation in New York"
authors: ["Walawalkar, R.", "Apt, J.", "Mancini, R."]
year: 2007
journal: "Energy Policy"
volume_issue_pages: "35(4):2558-2568"
doi: "10.1016/j.enpol.2006.09.005"
quartile: "Q1 (SJR 2007 and 2024/2025, Energy (misc.) and Management, Monitoring, Policy & Law)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Jay Apt — Carnegie Mellon Electricity Industry Center (CEIC), Tepper/EPP, Carnegie Mellon University"
lineage: "CMU CEIC (Apt) group; Walawalkar was CMU-affiliated at the time (OpenAlex affiliation). Advisor-student tie Apt->Walawalkar plausible but NOT verified here. Same CEIC working-paper series later hosts Sioshansi's storage papers."
streams: [S1_foundations_value]
market_context: "NYISO (2001-2005), zonal DA energy (NYC / NY East / NY West), regulation, ICAP; NaS battery (arbitrage) and flywheel (regulation)"
method_class: "heuristic revenue screening + Monte Carlo NPV (no optimisation solver)"
evidence_read: "full text of CEIC working-paper version CEIC-06-04 (https://www.cmu.edu/ceic/assets/docs/publications/working-papers/ceic-06-04.pdf); journal version not read — numbers may differ slightly"
oa_link: "https://www.cmu.edu/ceic/assets/docs/publications/working-papers/ceic-06-04.pdf"
---

## 1. Research question
Are emerging storage technologies (sodium-sulfur batteries for arbitrage, flywheels for regulation) economically viable in the restructured New York (NYISO) market, and how do location and service choice (energy arbitrage vs regulation) change the NPV?

## 2. Setting & assumptions
- Price-taker; historical NYISO prices 2001–2004 (2005 added in final economics). Zones aggregated into NYC (J,K), NY East, NY West.
- Arbitrage valued by a heuristic daily rule: for each day pick the highest-revenue discharge window and lowest-cost charge window; operator assumed to bid on a seasonal forecast of peak hours from historical data (i.e., not full perfect foresight optimisation).
- Discharge durations 2 h, 4 h, 10 h (arbitrage); 24-h continuous availability for regulation (paid for both charging and discharging when following the ISO signal).
- NaS: 1 MW / 10 MWh, capital $1.15–2.25 M, O&M $15–90 k/yr, 5,000–20,000 cycles, 12–20 yr life, base round-trip efficiency ≈83 %. Flywheel: 1 MW / 0.25 MWh, $0.55–0.75 M.
- Finance: 10 % discount rate, 10-year project; Monte Carlo over cost/revenue ranges.
- ICAP (capacity) revenues included; T&D upgrade deferral ($150 k/MW-yr) discussed separately.

## 3. Constraints that drove the model choice
Lack of data for a global co-optimisation across energy and reserves (e.g., distribution of reserve pick-up hours) and wide, poorly documented capital-cost ranges for pre-commercial technologies → simple per-service revenue screening plus Monte Carlo on costs rather than a joint optimisation.

## 4. Model
- Per-day arbitrage revenue R_d = Σ_{t∈discharge window} p_t·P − Σ_{t∈charge window} p_t·P/η, windows chosen per day and region.
- Regulation revenue = availability price × capacity over 24 h (plus energy effects).
- NPV over 10 yr with Monte Carlo sampling over capital/O&M/revenue ranges; probability of positive NPV reported.
- No formal solver; spreadsheet/statistical analysis.

## 5. Data & processing
- NYISO zonal DA (and RT) LBMPs, regulation prices, ICAP auction prices 2001–2005 (hourly).
- Mean on/off-peak prices 2001–2004: NYC $66.43/$44.12 per MWh; NY West $47.46/$33.91.
- ICAP: NYC $6.96–11.86/kW-month vs $0.25–1.70 rest of state (2004–05).
- No train/test split (historical screening).

## 6. Justification (why the authors argue the approach is valid)
Revenue distributions computed directly from multi-year market data; Monte Carlo over costs gives probability of profitability rather than a single point; comparison across zones and services isolates location and product effects.

## 7. Key results
- NYC 10-h NaS arbitrage: annual net revenue $87–180–240 k/MW-yr (min–avg–max); mean NPV ≈ +$190 k, 66 % probability of NPV > 0.
- NY East NaS: mean NPV −$475 k (7 % P(NPV>0)); NY West −$560 k (2 %).
- Flywheel regulation (NY East): mean NPV ≈ $454 k — higher and less uncertain than arbitrage (regulation prices less volatile).
- Efficiency matters: sacrificing efficiency "can have a significantly adverse effect on the economics".
- Market rules: storage then excluded from 10-min spinning reserve (≈15 % of regulation revenue foregone); deferral benefits could pay back a unit in ~4 years.

## 8. Limitations (stated + your critical reading)
- Stated: capital-cost uncertainty; no joint optimisation of energy + ancillary services; regulatory uncertainty on flywheel regulation performance evaluation.
- Critical: heuristic daily windows (no SoC carry-over, no intra-day multiple cycles); price-taker; regulation energy-neutrality and performance penalties not modelled; pre-dates pay-for-performance (FERC 755).

## 9. Relevance to my study
Earliest Q1 example of **market-rule-driven value**: location (NYC ICAP and price levels) and product eligibility (exclusion from spinning reserve) dominate storage NPV. Useful as historical baseline for "regulation > arbitrage" finding and for the argument that eligibility rules directly cap revenue.

## 10. Lineage links
- Builds on: Graves, Jenkin & Murphy (1999, Electricity Journal — historical, not archived); Butler et al. (2003, Sandia reports).
- Built upon by (notable): sioshansi2009_pjmvalue; bradbury2014_rtarbitrage; staffell2016_maxvalue; many multi-service studies (see S2 stream).

## 11. Verification log
- Crossref (api.crossref.org/works/10.1016/j.enpol.2006.09.005): title, authors, Energy Policy 35(4):2558–2568, published-print April 2007 ✔.
- OpenAlex: authors Walawalkar & Apt (CMU), Mancini (no affiliation listed) ✔; online 2006.
- SJR (scimagojr id 29403): Energy Policy Q1 in 2007, 2024, 2025 ✔.
- Content from CEIC working paper CEIC-06-04 (same title/authors); journal-version numbers NOT cross-checked.
