---
id: butters2025_soakingsun
title: "Soaking Up the Sun: Battery Investment, Renewable Energy, and Market Equilibrium"
authors: ["Butters, R. A.", "Dorsey, J.", "Gowrisankaran, G."]
year: 2025
journal: "Econometrica"
volume_issue_pages: "93(3):891-927"
doi: "10.3982/ECTA20411"
quartile: "Q1 (SJR 2025, Economics and Econometrics; SJR 19.9)"
group: "Gowrisankaran (Columbia, formerly Arizona; NBER/CEPR) with Butters (Indiana Kelley) and Dorsey (UT Austin)"
lineage: "Empirical-IO dynamic-structural tradition (Gowrisankaran; cf. Gowrisankaran-Reynolds-Samano 2016 JPE on intermittency). Advisor-student ties among the three authors NOT verified."
streams: [S8_empirical_econ]
market_context: "CAISO (SP-15 hub), 5-min real-time + hourly day-ahead energy; 4-h Li-ion arbitrage only"
method_class: "econometric + SDP/DP (structural dynamic equilibrium)"
evidence_read: "full text (author-posted final version https://www.jacksonfdorsey.com/papers/soaking-up-the-sun.pdf; NBER w29133)"
oa_link: "https://www.nber.org/system/files/working_papers/w29133/w29133.pdf"
---

## 1. Research question
What are the equilibrium price, distributional and welfare effects of utility-scale batteries in a high-solar market, and when will (subsidised or unsubsidised) private battery investment occur once batteries' own price impact is internalised?

## 2. Setting & assumptions
- Batteries are a competitive fringe (symmetric competitive equilibrium among many small operators; price impact via aggregate fleet K). Monopoly/duopoly operation explored in supplement.
- Stochastic, not perfect foresight: AR(1) shocks to net-load forecast error (eps^L) and dispatchable-supply availability (eps^P); day-ahead forecastable conditions treated as known.
- 5-min real-time operations; finite-horizon DP approximating infinite horizon; adoption model annual.
- Battery: 4-h Li-ion, charge fraction f in [0,1]; degradation embedded through a "perceived" round-trip efficiency chosen to maximise lifetime value using Xu et al. (2016) cycle-aging model.
- Energy arbitrage only (no AS revenue).

## 3. Constraints that drove the model choice
Almost no observed battery operation in sample (~126 MW by 2019), so behaviour cannot be estimated from unit data; batteries' effect must be inferred from how *dispatchable* supply prices respond to residual demand. Battery operation is dynamic (state of charge), needs uncertainty (perfect foresight overstates value ~30%), and the fleet moves prices, so a dynamic equilibrium (not price-taker LP) is needed. Computational burden (~13,000 DPs x 2.88M states) forces discretisation and a reduced-form "flow-return surface" for the adoption stage.

## 4. Model
- Supply relationship of dispatchable generators: P^d(Z/K, K) = theta1 + theta2 [K(1 - Z/K)]^(-theta3), with capacity K = kappa * Ztilde^(1-alpha) * exp(eps^P) (lagged dispatchable output Ztilde captures ramping).
- **Assumption 1 (exclusion restriction):** the dispatchable supply relationship depends only on (day, interval, Z, Ztilde, eps^L, eps^P) and is invariant to installed battery capacity -> batteries affect prices only by shifting residual quantity Z.
- Operations: V^d(f,s,Ztilde,eps) = max_q { P^d(...) * q-terms + beta^(1/SD) E V^d(f', s+1, ...) } s.t. power/energy limits; symmetric equilibrium in fleet K.
- Adoption: optimal-stopping by a continuum of potential entrants (adopt now vs wait for cost declines), equilibrium fleet K* from cumulative entry; flow profits from a fitted surface of weekly operating profit on K, renewable share, peaks, fuel, hydro, week FE.

## 5. Data & processing
- CAISO 2016-2019 analysis sample (2015 training for shock processes); 5-min RTM and hourly DAM prices (SP-15), load, wind/solar/dispatchable generation, gas prices, hydro availability; battery capex projections from 25+ sources.
- Supply curve estimated by NLS on DAM prices day-by-day with one-week rolling windows, monotonicity imposed; eps^P recovered from RTM prices by inverting the supply relation; eps^L = realised minus DAM-forecast net load.
- No unit-level battery bids/dispatch (synthetic fleet).

## 6. Justification
Identification of the battery price effect comes from within-sample variation in residual demand along the estimated dispatchable supply curve (Assumption 1). Validated by: forecasting calibration of DAM vs RTM (0.95 scaling), alternative flexible supply form (supplement C), discretisation checks (finite vs infinite horizon), plausibility of simulated charge/discharge (charge midday, discharge evening). Explicitly says counterfactuals are most credible for modest departures from observed bidding environments.

## 7. Key results
- Stochastic operation captures ~70% of perfect-foresight value; degradation reduces lifetime value ~27%.
- 1% of 5-min intervals generate ~69% of battery revenue (extreme-value dependence).
- First 5,000 MWh lowers mean price 5.6% ($35.92 -> $33.90/MWh) and evening peak 10.3%; moving 25,000 -> 50,000 MWh lowers mean only 2.6% (steep diminishing returns).
- 1,000 MWh fleet (annual): LSEs +$124m, dispatchable generators -$126m, wind/solar -$13m, gross surplus +$14m.
- First battery breaks even without subsidy when renewable share ~50% and capex <= ~$264/kWh (projected 2024). Value per kWh at 50% RE falls from ~$280 (10 MWh fleet) to ~$140 (50,000 MWh).
- Without subsidy, negligible adoption through 2030; a 30% ITC (IRA-type) reproduces CA's ~5,000 MWh mandate by 2024.

## 8. Limitations (stated + critical reading)
- Assumption 1 rules out generator bidding responses/exit due to batteries; no strategic interaction with incumbents (contrast Karaduman WP).
- Extrapolation of flow returns beyond 50% RE; exogenous cost path (no learning-by-doing); fixed thermal fleet.
- Arbitrage-only: ignores AS (in CAISO/ERCOT early batteries earned mostly from regulation/reserves; see reynolds WP, lamp2022). Revenue skew means results are very sensitive to price-spike modelling.
- No validation against observed unit-level battery dispatch (data did not exist).

## 9. Relevance to my study
Canonical template for "market-level supply curve + dynamic battery operation + endogenous price impact". For GB multi-product bidding: (i) the 70%-of-perfect-foresight benchmark is a useful calibration target for RL agents; (ii) the cannibalisation curve (value per kWh vs fleet size) is the energy-market analogue of DC/DM/DR price saturation in GB; (iii) the exclusion-restriction logic (supply curve invariant to storage) is exactly what fails in small AS markets where batteries ARE the marginal suppliers -> motivates a different identification for GB EAC.

## 10. Lineage links
- Builds on: sioshansi2009 (S1), carson2013_bulkstorageexternality, Gowrisankaran-Reynolds-Samano 2016 JPE, Xu et al. 2016 degradation (S4), Rust-type optimal stopping.
- Related / follow-on (citation links not verified): Karaduman (Stanford GSB WP 4126, strategic incumbents, South Australia), Reynolds 2025 Arizona WP 25-01 (reserves + arbitrage, ERCOT 2022), Andrés-Cerezo & Fabra 2023 RAND (storage market structure; cross-ref S7).

## 11. Verification log
- Bibliographic data from Econometric Society article page (vol 93, issue 3, May 2025, pp. 891-927, DOI 10.3982/ECTA20411); Wiley listing confirms DOI.
- SJR: scimagojr.com sourceid 19482, Q1 2025.
- Full text read from author-posted PDF. Affiliations from PDF. Advisor ties not verified.
