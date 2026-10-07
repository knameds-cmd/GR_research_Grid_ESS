---
id: carson2013_bulkstorageexternality
title: "The private and social economics of bulk electricity storage"
authors: ["Carson, R. T.", "Novan, K."]
year: 2013
journal: "Journal of Environmental Economics and Management"
volume_issue_pages: "66(3):404-423"
doi: "10.1016/j.jeem.2013.06.002"
quartile: "Q1 (SJR 2013, Economics and Econometrics; Management, Monitoring, Policy and Law)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Carson (UC San Diego Economics); Novan (UC Davis ARE)"
lineage: "Advisor-student ties not verified. Novan's later storage/renewables work links to Bushnell (UC Davis)."
streams: [S8_empirical_econ]
market_context: "ERCOT 2007-2009, hourly balancing-market prices, CEMS unit emissions; generic bulk storage arbitrage"
method_class: "econometric (reduced-form marginal emissions) + rule-based arbitrage simulation"
evidence_read: "full text (https://econweb.ucsd.edu/~rcarson/papers/Carson_Novan2013.pdf)"
oa_link: "https://econweb.ucsd.edu/~rcarson/papers/Carson_Novan2013.pdf"
---

## 1. Research question
Do private arbitrage returns of bulk storage align with its social returns once emissions externalities of shifting fossil generation from peak to off-peak are accounted for?

## 2. Setting & assumptions
- Price-taker 1 MWh storage; charge in daily minimum residual-demand hour, discharge in maximum hour (perfect foresight, one cycle/day).
- Losses alpha in {0, 0.1, 0.2, 0.3}. Renewables inframarginal. ERCOT treated as electrically isolated (clean mapping from storage to affected fossil units).

## 3. Constraints that drove the model choice
No storage in sample, so storage effect must be built from estimated hour-specific marginal emissions of dispatchable generation; ERCOT's islanded grid avoids interstate leakage problems.

## 4. Model
- E_{h,d} = beta_h G_{h,d} + alpha_{h,m} + e (hour-specific marginal emission rates, 36 month FE) for CO2, SO2, NOx.
- Delta emissions per MWh stored = e'_offpeak - (1-alpha) e'_peak.
- Private profit = (1-alpha) P_peak - P_offpeak, frequency-weighted by month.

## 5. Data & processing
ERCOT generation by fuel and balancing prices (hourly, 26,117 h), EPA CEMS (276 units), residual demand = load - wind.

## 6. Justification
Cross-validated against Holland & Mansur (2008) (real-time pricing, demand-variance approach): CO2 +0.18 vs +0.19 t/MWh. Sensitivity to alpha and to social cost of carbon.

## 7. Key results
- With alpha=0.2: CO2 +0.19 t/MWh stored, SO2 +1.89 lb/MWh, NOx -0.15 lb/MWh.
- Private arbitrage ~$27.94/MWh; external cost ~$4.09/MWh at $21/tCO2 (-> $12.67 at $65/t); net social ~$23.85/MWh, but negative in 5 months.

## 8. Limitations (stated + critical reading)
- Arbitrage only; deterministic timing rule; short-run marginal emissions (no investment response; contrast linn2019_storagecostemissions); capped SO2/NOx; Texas-specific coal-off-peak merit order (largely obsolete after coal retirements and solar).

## 9. Relevance to my study
Template for "storage as a marginal-unit shifter": estimate hour-specific marginal responses (price or emissions) from system data, then integrate over a storage dispatch. For GB, the same structure gives a quick external-value overlay for RL bidding (carbon-aware reward) using hourly marginal emissions estimated from Elexon fuel-type data.

## 10. Lineage links
- Builds on: Holland & Mansur 2008 (ReStat), Sioshansi et al. 2009 (S1).
- Built upon by: linn2019_storagecostemissions (same question, medium run with investment response), later storage-emissions literature (not enumerated).

## 11. Verification log
- OpenAlex: JEEM 66(3):404-423, 20 Jun 2013, authors UCSD / UC Davis.
- SJR JEEM sourceid 23352: Q1 2013 and 2025.
- Full text: authors' posted PDF of the published article.
