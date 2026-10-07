---
id: lamp2022_caisobatteryarbitrage
title: "Large-scale battery storage, short-term market outcomes, and arbitrage"
authors: ["Lamp, S.", "Samano, M."]
year: 2022
journal: "Energy Economics"
volume_issue_pages: "107:105786"
doi: "10.1016/j.eneco.2021.105786"
quartile: "Q1 (SJR 2025, Economics and Econometrics; Energy (misc.))"
quartile_basis: "latest-only; rule=unchecked; SJR 2022 (publication year) not checked — only later years"
group: "Samano (HEC Montréal; empirical IO of electricity) and Lamp (UC3M Madrid)"
lineage: "Samano co-authored Gowrisankaran-Reynolds-Samano 2016 JPE (Arizona IO group) -> tie to butters2025 group. Advisor-student ties not verified."
streams: [S8_empirical_econ]
market_context: "CAISO fleet of utility batteries (aggregate output), RTM/DAM energy, 2018-2020; price-spread analysis 2013-2017"
method_class: "econometric (quantile regression, event study) + LP perfect-foresight benchmark"
evidence_read: "full text (working-paper version https://tintin.hec.ca/pages/mario.samano/Lamp_Samano_batteries.pdf)"
oa_link: "https://tintin.hec.ca/pages/mario.samano/Lamp_Samano_batteries.pdf"
---

## 1. Research question
How do real grid-scale batteries in California actually operate relative to load and prices, do they arbitrage optimally, and did battery entry change wholesale price spreads?

## 2. Setting & assumptions
- Observed behaviour: aggregate CAISO battery output (5-min), 6 Jun 2018 - 1 Mar 2020; 47 facilities (median 1.5 MW / 7.2 MWh; 66% of capacity labelled "arbitrage" in EIA-860).
- Benchmark: price-taking, perfect-foresight LP for a median battery, round-trip efficiency 0.66 (fleet-implied), hourly RTM/DAM prices.
- Entry analysis: weekly 2013-2017.

## 3. Constraints that drove the model choice
Only aggregate CAISO battery output is public (no unit panel), so behaviour is studied as a fleet response; normalisation of output lets observed and LP-optimal dispatch be compared on the same quantile scale. Entry timing (not location) is the only variation available for price effects.

## 4. Model
- Behaviour: quantile/ventile regressions, normalised battery output_t = sum_k beta_k 1{load or price in ventile k} + hour-of-day + day-of-week + month FE; HAC SEs; IV using output lagged 25 h.
- Same regression run on LP-optimal dispatch -> compare beta profiles (revealed-vs-optimal).
- Entry: event study, log max daily RTM spread (weekly) on new battery capacity with leads/lags -4..+12 weeks, month and week-of-year FE, controls renewables/hydro/load; SEs clustered by month. Key assumption: entry timing exogenous to current prices.
- LP: max sum_t p_t (d_t - c_t) s.t. SoC dynamics with eta, power/energy bounds.

## 5. Data & processing
CAISO OASIS (5-min battery output, load, renewables; hourly RTM/DAM prices), EIA-860 (capacity, use labels), DOE Global Energy Storage Database (entry dates). Fleet efficiency estimated from charge/discharge totals.

## 6. Justification
Comparison of the observed response curve to the LP-implied response curve is the paper's revealed-preference test of "optimal arbitrage". Robustness: RTM vs DAM prices, eta in [0.6,1.0], daily/weekly/monthly aggregation, hour-ahead forecasts and forecast errors, net-load specification, HAC and IV.

## 7. Key results
- Batteries respond to prices only in the top 2-3 price ventiles (optimal: 8+); correlation(price, output) 0.13 observed vs 0.43 optimal.
- Max marginal response ~3-4% of mean output per $1/MWh (DAM).
- Battery entry reduces max daily RTM spread, significant at 10%, fading after ~5 weeks.
- Annual arbitrage revenue -$9,032 to $34,798 per MWh of energy capacity; representative 7.2 MWh facility: observed NPV -$2.21m (9 yrs, 5%) vs optimal +$0.347m.

## 8. Limitations (stated + critical reading)
- Aggregate fleet only; cannot separate arbitrage vs regulation/ramping use - much of the "sub-optimality" may be AS provision (CAISO regulation) or RA/contracted dispatch, not mistakes.
- LP benchmark abstracts from uncertainty (perfect foresight overstates attainable profit; cf. butters2025 ~70%).
- Weak identification of price effects (timing-only variation, small fleet).

## 9. Relevance to my study
Direct methodological template for GB: regress observed unit output (BM/BOAs or metered volumes) on price ventiles, repeat on optimal benchmark dispatch, compare profiles. With GB unit-level data (unlike CAISO aggregate) the comparison can be done per unit and per product (EAC DC/DM/DR/BR/QR vs wholesale), separating "AS-committed" hours from arbitrage hours — the main weakness here.

## 10. Lineage links
- Builds on: sioshansi2009 (S1), carson2013_bulkstorageexternality, Gowrisankaran-Reynolds-Samano 2016.
- Built upon by: butters2025_soakingsun (cites), kirkpatrick2026_batterycongestion, Ma-Zheng-Qi-Xu 2025 arXiv (CAISO storage bids).

## 11. Verification log
- DOI/volume/article number via EconPapers record and OpenAlex (pub. date 15 Jan 2022, vol 107, 105786; affiliations UC3M & HEC Montréal).
- SJR Energy Economics sourceid 29374: Q1 2025 both categories.
- Full text: author working-paper PDF (may differ slightly from published version).
