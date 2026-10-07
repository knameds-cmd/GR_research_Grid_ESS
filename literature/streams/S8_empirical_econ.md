# S8 — Empirical and econometric evidence on storage behaviour, earnings and market impact

Stream owner scope: how real batteries and other storage (pumped/reservoir hydro, implicit storage via interconnection) actually behave and earn in markets, and their market impact. Methods covered: reduced-form (DiD, event study, distributed lags), structural/equilibrium estimation, revealed-preference comparison of observed behaviour with optimal benchmarks, and natural experiments from rule changes.
Last updated: 2026-10-06. 12 papers in archive.

## 1. Overview
The peer-reviewed Q1 evidence on *observed* storage behaviour is thin, for one reason: until about 2020, grid batteries were too small for market-level identification, and unit-level storage data were seldom public. The literature therefore falls into four groups:

1. **Structural equilibrium models estimated on market data, with synthetic storage fleets.** Storage is not observed. Its price impact is identified from the estimated supply curve of dispatchable generators: butters2025_soakingsun (Econometrica), with linn2019_storagecostemissions and carson2013_bulkstorageexternality for emissions. Their core identifying assumption is that the dispatchable supply relation does not change with storage capacity.
2. **Reduced-form market-impact studies using the timing and location of storage entry:** lamp2022_caisobatteryarbitrage (an event study of price spreads), kirkpatrick2026_batterycongestion (a nodal DiD with high-dimensional fixed effects plus double-LASSO for unobserved network links), and rangarajan2023_batteryfcasdid (a staggered DiD on NEM FCAS costs).
3. **Revealed behaviour compared with an optimal benchmark:** lamp2022 (observed CAISO fleet output against a perfect-foresight LP), butters2025 (a stochastic DP reaches about 70% of the perfect-foresight value), and hortacsu2019_strategicability (bids against the ex-post best response to observed residual demand; the methods anchor). For hydro storage, tangeras2018_hydrodarealtime builds market-power tests in which the unobservable water value cancels.
4. **Natural experiments from rule or product changes, and adoption:** tabari2020_payforperformance (FERC Order 755 pay-for-performance raised regulation-oriented storage deployment by about 30–37%, DiD) and brown2024_reliabilitybattery (outage events lead to battery adoption, giving a VoLL of about $5,000/MWh).

Implicit storage through hydro and interconnection (green2012_storingwind, mauritzen2013_deadbattery) is the Nordic precursor. It shows how cheaply reservoir hydro arbitrages wind variability (about €1.45/MWh), which is the benchmark rent that batteries now compete for.

**Robust stylised facts across papers**
- **Batteries reduce the prices they earn from, with steep diminishing returns.** Mean CAISO price falls 5.6% for the first 5 GWh but only 2.6% more from 25 to 50 GWh (butters2025). Price spreads fall after entry, though the effect is short-lived in early data (lamp2022). In NEM FCAS the cost cuts scale with MW and are largest in short-duration products (rangarajan2023).
- **Observed operation falls well below the perfect-foresight benchmark.** Correlation of output with price is 0.13 observed against 0.43 optimal, and the observed NPV is negative where the optimal one is positive (lamp2022). The stochastic-optimal value is about 70% of perfect foresight (butters2025). Revenue is extremely skewed: 1% of 5-minute intervals give 69% of revenue (butters2025).
- **Distribution:** consumers gain, while thermal *and* renewable generators lose (butters2025). Ratepayer congestion benefits equal 38–161% of private arbitrage revenue (kirkpatrick2026), so private returns understate social value. The emissions effect has an ambiguous sign and depends on the merit order (carson2013, linn2019).
- **Product rules shape investment and use.** Pay-for-performance raised storage deployment (tabari2020). Subsidy design (a 30% ITC) is pivotal for early adoption (butters2025).

## 2. Lineage
```
Holland & Mansur 2008 ──► carson2013 (short-run emissions, ERCOT) ──► linn2019 (medium-run, endogenous wind)
Gowrisankaran–Reynolds–Samano 2016 JPE (intermittency, AZ IO) ──► butters2025 (dynamic battery equilibrium + adoption)
                                                              └──► lamp2022 (Samano; observed CAISO fleet vs LP)
lamp2022 / carson2013 ──► kirkpatrick2026 (nodal congestion effects, DiD + double LASSO)
Hortaçsu & Puller 2008 RAND ──► hortacsu2019 (bids vs best response; cognitive hierarchy)  [methods anchor]
Førsund hydro economics ──► green2012 (DK implicit storage cost) ~ mauritzen2013 (DK wind → NO hydro) ──► tangeras2018 (DA vs RT market-power tests)
FERC Order 755 ──► tabari2020 (DiD on storage deployment)
De-energisation events ──► brown2024 (event study + dynamic discrete choice, VoLL)
```
Working-paper frontier, not yet in the archive because it is not Q1-published: Karaduman (Stanford GSB WP 4126) on a dynamic equilibrium with incumbents' best responses to storage in South Australia; Reynolds (Arizona WP 25-01) on ERCOT battery revenue, where reserves account for 57% against arbitrage; Ma–Zheng–Qi–Xu (arXiv 2501.13324) on CAISO storage bids, withholding and daily periodic patterns; Eschenbaum (arXiv 2607.13002) on shared autobidders (Tesla Autobidder, Fluence Mosaic) whose NEM battery bids co-move, with a conduct test; and Allcott et al. (WP) on battery bid timing and market efficiency.

## 3. Groups
| Group / PI | Institution | Papers here | Notes |
|---|---|---|---|
| Gowrisankaran, Butters, Dorsey | Columbia (ex-Arizona); Indiana Kelley; UT Austin | butters2025 | Dynamic structural IO; NBER. Advisor–student ties not verified |
| Samano, Lamp | HEC Montréal; UC3M | lamp2022 | Samano co-authored with Gowrisankaran and Reynolds (Arizona IO) |
| Kirkpatrick | Michigan State Econ | kirkpatrick2026 | ML-for-causal-inference applied to networks |
| Carson, Novan | UCSD; UC Davis ARE | carson2013 | Novan is later linked to Bushnell (Davis) on renewables |
| Linn, Shih | RFF | linn2019 | Policy simulation group |
| Trück, Foley | Macquarie Business School | rangarajan2023 | Energy finance / microstructure, NEM |
| Shaffer | Univ. of Calgary (Econ & School of Public Policy) | tabari2020 | Electricity policy |
| Brown, Muehlenbachs | Alberta; Calgary/RFF | brown2024 | Energy IO, revealed preference |
| Tangerås, Mauritzen | IFN Stockholm / EPRG Cambridge; BI | tangeras2018, mauritzen2013 | Nordic market-power tests |
| Green | Birmingham then Imperial | green2012 | Linked to Williams & Green 2022 (S7) on storage market power in GB |
| Hortaçsu, Puller | Chicago; Texas A&M | hortacsu2019 | Bid-data empirical IO (methods) |

## 4. Summary table
| id | year | market | identification | data | finding |
|---|---|---|---|---|---|
| butters2025_soakingsun | 2025 | CAISO energy (5-min RT, hourly DA) | Structural: NLS supply curve with an exclusion restriction (supply invariant to storage); dynamic DP equilibrium; optimal-stopping adoption | Market-level 2016–19; synthetic fleet | Stochastic value ≈70% of perfect foresight; mean price −5.6% for the first 5 GWh; no adoption without subsidy before 2030; a 30% ITC reaches the CA mandate |
| lamp2022_caisobatteryarbitrage | 2022 | CAISO energy | Quantile regressions of fleet output on price/load ventiles against the same regressions on LP-optimal dispatch; event study of entry on spreads | Aggregate fleet output (5-min), 2018–20; entry 2013–17 | Response only in the top 2–3 price ventiles; corr 0.13 vs 0.43; negative observed NPV; spread reduction lasts about 5 weeks |
| kirkpatrick2026_batterycongestion | 2026 | CAISO nodal DA LMP | Node×hour×season×year×weekday FE DiD on installed storage; double pooled LASSO for cross-node effects | 757 nodes, hourly, 2009–16; 17 batteries | ~$80k/MW-yr ratepayer benefit (23% cross-node); 38–161% of private arbitrage |
| rangarajan2023_batteryfcasdid | 2023 | NEM FCAS | Staggered DiD across two states (from abstract) | AEMO FCAS (details unverified) | Batteries cut FCAS costs; effect scales with MW; largest in regulation and 6-second markets |
| carson2013_bulkstorageexternality | 2013 | ERCOT | Hour-specific marginal emission rates (month FE) combined with a rule-based storage cycle | Hourly 2007–09, CEMS 276 units | +0.19 tCO2/MWh stored; private $27.9/MWh vs external $4–13/MWh; net social value negative in some months |
| linn2019_storagecostemissions | 2019 | ERCOT 2030 counterfactual | Estimated wind investment elasticity inside an equilibrium NLP | 2004–08 hourly; 1996–2015 regional panel | Cheaper storage raises CO2 (~2%) unless renewables respond; a carbon price helps |
| tabari2020_payforperformance | 2020 | US ISOs, frequency regulation | DiD: regions covered vs not covered by FERC Order 755 (from abstract) | Storage projects (source unverified) | +30–37% regulation-oriented storage projects |
| tangeras2018_hydrodarealtime | 2018 | Nord Pool SE1–4, Elspot vs Elbas | Theory-derived competitive restrictions in which water value cancels; OLS/IV | Hourly 2010–13, ~22k Elbas trades | Competition rejected in SE2–SE4 (local real-time market power) |
| mauritzen2013_deadbattery | 2013 | DK wind → NO hydro | Distributed-lag ARMA with exogenous wind; SURE | Daily, ~8 years | About 40% of Danish wind is effectively "stored" in Norwegian reservoirs; small price effects in Norway |
| green2012_storingwind | 2012 | DK–Nordic | Correlations; GLS (Cochrane-Orcutt); output-weighted price decomposition; flow tracing | Hourly 2001–09, annual 1996–2009 | Implicit storage cost ≈3–4% of wind value (≈€1.45/MWh) |
| brown2024_reliabilitybattery | 2024 | California BTM (PSPS) | Event-study DiD (storage vs solar-only placebo) plus dynamic discrete choice | Zip panel 2014–20 | VoLL ≈$4,980/MWh; adoption up about 45% in treated zips |
| hortacsu2019_strategicability | 2019 | ERCOT balancing (methods) | Ex-post best response to observed residual demand; cognitive hierarchy; minimum distance | Firm bid functions, 99 auctions 2002–03 | Most firms capture under 50% of best-response profit; raising sophistication improves efficiency 9–16% |

## 5. Using public unit-level data (like GB NESO EAC unit results + Elexon BM data) for empirical identification of market-rule effects: designs used in the literature (event study around rule changes, DiD across unit types, bunching, revealed-preference bid analysis)

**GB data advantage.** Unlike CAISO before 2023 (aggregate fleet only; lamp2022) or the NEM FCAS studies (regional costs; rangarajan2023), GB publishes data at the unit level. The NESO EAC auction results give per-unit, per-service (DC/DM/DR H/L, and BR/QR where applicable), per-EFA-block bids, accepted volumes and clearing prices. Elexon/BMRS publishes BOD bid-offer pairs, BOAs, physical notifications (PN/MEL/MIL), metered volumes and SO flags. This makes a unit × service × settlement-period panel possible, with battery and non-battery providers side by side.

### Designs used in the literature, adapted to GB

1. **Event study around rule or product changes**
   - Literature precedents: tabari2020 (FERC Order 755, DiD) and lamp2022 (entry-timing event study with leads and lags −4..+12 weeks).
   - GB events, with dates to be checked against NESO notices: the DC launch (2020), DM/DR launches (2022), the move to EAC co-optimised day-ahead procurement (Nov 2023), and the Balancing Reserve introduction (2024). BM reforms such as the Open Balancing Platform bulk dispatch of batteries also count, as do changes to skip-rate methodology and to the BM registration rules for small storage.
   - Outcomes per unit: share of MW offered to each service, bid price relative to that service's clearing price, BM acceptance rate (the skip rate), and cycling and SoC-management proxies from PN/metered data.
   - Use heterogeneity-robust estimators for staggered adoption (Callaway–Sant'Anna or Sun–Abraham). brown2024 reports a Goodman-Bacon decomposition.
2. **DiD across unit types or services**
   - Literature precedents: brown2024 (storage vs a solar-only placebo) and rangarajan2023 (treated vs control regions).
   - GB version: batteries (treated by a storage-specific rule, e.g., a BM dispatch tool change) against non-storage BM units (CCGT, pumped hydro, demand-side response) in the same period. Alternatively, compare battery behaviour in a service hit by the rule with a service that was not hit. Dose can be MWh/MW duration (1 h vs 2 h assets) where the rule bites differently by duration.
   - Threats: rules usually apply to all units, and spillovers through co-optimisation violate SUTVA. Prefer within-unit cross-service comparisons with unit × day fixed effects, since multi-product units re-optimise their portfolio.
3. **Bunching**
   - Not used in the storage papers reviewed here, but it suits GB rules that have thresholds: minimum bid sizes (1 MW), duration and stacking rules, the 15-minute or 1-hour energy requirements of DC/DM/DR (which tie MW to MWh), and price caps and floors.
   - Bunching of offered MW at the value that makes the energy constraint just bind, or of bid prices at caps, identifies how binding a rule is and lets you back out an elasticity. The NESO EAC MW offers per EFA block are fine-grained enough for this.
4. **Revealed-preference analysis of bids against an optimal benchmark**
   - Literature precedents: hortacsu2019 (ex-post best response to observed residual demand), lamp2022 (observed vs LP perfect foresight), and butters2025 (stochastic DP at about 70% of perfect foresight).
   - GB version: for each battery and day, compute (a) the perfect-foresight multi-product optimum (wholesale DA/ID, EAC services, BM) and (b) a non-anticipative stochastic or RL-policy benchmark. Then measure the capture rate and the deviations by service.
   - With EAC residual supply curves rebuilt from all units' bids, an ex-post best response that takes price impact into account can be computed, following HLPZ. That allows tests of price-taking against strategic or coordinated bidding; Eschenbaum (2026, arXiv) does this for shared NEM autobidders.
   - When the opportunity cost of state of charge is unobserved, use the approach of tangeras2018: compare the same unit's prices for *simultaneous delivery* across venues (EAC vs BM vs intraday for the same EFA block), so that SoC value cancels.
5. **Structural supply-curve identification of market impact**
   - Literature precedent: butters2025.
   - GB use: estimate service-level demand (the NESO requirement, close to inelastic) and non-battery supply curves for each EAC service, then simulate counterfactual battery fleets and rule sets.
   - Caveat: in GB response services batteries *are* the marginal suppliers, so butters2025's exclusion restriction (non-storage supply unaffected by storage) holds only for the non-battery fringe. Model battery entry and exit as endogenous.
6. **High-dimensional fixed effects and ML selection**
   - Literature precedent: kirkpatrick2026.
   - GB use: when many interacting products and periods could be affected by a rule, use double-selection LASSO to find which service × EFA block outcomes respond, avoiding ad hoc choices of outcome.

## 6. Open gaps
1. There is no Q1 paper using **unit-level battery bid data** to compare observed multi-product bidding with an optimal or best-response benchmark. All the existing bid studies are working papers (CAISO storage bids, NEM autobidders, ERCOT). GB EAC and BM data can fill this gap.
   - **2026-10-07 update:** still true for Q1. The preprint Dalton & O'Sullivan 2026 uses unit-level BM bid–offer ladders (price formation, not bidding optimality).
2. There is no causal evidence on **co-optimised ancillary-service auction design** (such as the GB EAC launch) and how it affects storage bidding and prices. tabari2020 covers deployment, not bidding.
3. The causal effect of **battery saturation on AS prices** rests on a single Q1 staggered DiD (rangarajan2023, NEM FCAS), which may use pre-heterogeneity-robust estimators. No GB equivalent exists for the DC/DM/DR price collapse of 2022–23.
4. **Dispatch frictions** are unmeasured: SO under-utilisation of batteries in the BM (skip rates) and its effect on battery revenue and bidding.
   - **2026-10-07 update:** `gale2026_balancingbatteries` (Q1) now quantifies the profit cost of skip rates parametrically (each +10 pp ≈ −7% profit), and the preprint Dalton & O'Sullivan 2026 (`WATCHLIST.md` C4) measures battery marginality in the BM unit by unit (2023–25). An **estimated** acceptance/skip model for batteries is still missing.
5. **Strategic or coordinated behaviour through shared optimisers** (autobidders, route-to-market providers) is documented only in working papers.
6. **Pumped hydro behaviour in GB** (Dinorwig, Cruachan) under BM and EAC rules has no Q1 empirical study that could be verified here.
7. Linking **realised revenue to degradation-aware operation**: observed cycling against warranty-driven constraints has not been estimated empirically (butters2025 calibrates degradation and does not estimate it).

## 7. Cross-references and exclusions
- **Cross-referenced to other streams (not written here):**
  - Williams & Green 2022 Energy Policy, "Electricity storage and market power" (GB): S7, market design.
  - Sioshansi et al. 2009 Energy Economics (PJM storage value with estimated price impact) and Zafirakis 2016: S1, value foundations.
  - Andrés-Cerezo & Fabra 2023 RAND, "Storing power: market structure matters": theory, S7.
  - Ito & Reguant 2016 AER (sequential markets and arbitrage): S7.
  - Gilmore, Nolan & Simshauser 2024 Energy Journal (levelised cost of FCAS, NEM): frequency stream.
- **Dropped because they are working papers only, as of 2026-10-06:** Karaduman, "Economics of grid-scale energy storage in wholesale electricity markets" (Stanford GSB WP 4126 / MIT CEEPR); Reynolds 2025, "Keeping the lights on" (Arizona WP 25-01); Ma, Zheng, Qi & Xu 2025 (arXiv 2501.13324); Eschenbaum 2026 (arXiv 2607.13002); Anunrojwong, Balseiro, Besbes & Xu 2024 (arXiv 2406.18685, theory with calibration); Allcott et al., battery bid timing (WP).
- **Not pursued:** German FCR battery price-effect studies. Those found were engineering or simulation papers (J. Energy Storage, Energy Procedia), not econometric, and the Energy Procedia papers are conference papers.
