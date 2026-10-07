---
id: sioshansi2014_capacityvalue
title: "A Dynamic Programming Approach to Estimate the Capacity Value of Energy Storage"
authors: ["Sioshansi, R.", "Madaeni, S. H.", "Denholm, P."]
year: 2014
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "29(1):395-403"
doi: "10.1109/TPWRS.2013.2279839"
quartile: "Q1 (SJR 2014, Electrical & Electronic Engineering; Energy Engineering & Power Technology)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Sioshansi (Ohio State ISE) with Denholm (NREL)"
lineage: "Sioshansi = Oren (Berkeley) PhD 2007 and NREL postdoc 2007-08 (CV) -> long-running Sioshansi-Denholm collaboration. Madaeni (then PG&E) co-authored several OSU capacity-value papers with Sioshansi; advisor tie NOT verified."
streams: [S7_market_design]
market_context: "Five US utility systems (PG&E, SCE, NV Energy, PNM, FirstEnergy), 1998-2005; storage dispatched against day-ahead energy prices (CAISO NP15/SP15, PJM AEP hub, system lambda)"
method_class: "SDP/DP + probabilistic reliability (LOLP/ELCC/ECP)"
evidence_read: "full text (author PDF https://www.cmu.edu/ceic/people/rsioshan/docs/storage_cv.pdf)"
oa_link: "https://www.cmu.edu/ceic/people/rsioshan/docs/storage_cv.pdf"
---

## 1. Research question
How much firm capacity (ELCC / equivalent conventional power) does an energy-limited storage device contribute when it is operated by a profit-maximising owner on energy prices, given that its availability at shortage hours depends on its state of charge?

## 2. Setting & assumptions
- Price-taking, perfect-foresight arbitrageur; operator is "naive" to shortages (dispatches on day-ahead prices, not on LOLP); on a shortage the device discharges at full power if l_t > 0 and planned charging is suspended.
- Hourly, 8 years; 100 MW, eta = 0.8, 1-10 h duration, start empty; no mechanical outages of storage.
- Two-state generator outage model (EFOR from NERC GADS), deterministic loads scaled to baseline LOLE 2.4 h/yr.

## 3. Constraints that drove the model choice
Capacity value of storage cannot be computed from a fixed availability profile (as for thermal units) because availability = SoC, which is path-dependent and itself altered by shortage events. A DP over discretised SoC both gives the profit-maximising schedule and allows a forward recursion of the SoC probability distribution conditional on shortages.

## 4. Model
- DP: state l_t in {0, R, ..., hR}; decisions s_t, d_t in {0, R}; l_{t+1} = l_t + s_t - d_t; max sum_t pi_t (eta d_t - s_t).
- Availability distribution recursion: xi_{t+1}(y) = p_t xi_t(y + R) + (1 - p_t) sum_{lambda in I_{t+1}(y)} xi_t(lambda), with p_t = LOLP; xi_t(0) acts as an effective forced-outage rate.
- Capacity value metrics: ELCC (load increase at constant LOLE) and ECP (equivalent conventional capacity at same LOLE).
- Benchmark heuristic: "maximum generation" capacity-factor approximation (Tuohy & O'Malley) over top 10/100/1000 load hours.

## 5. Data & processing
EIA Form 860 fleets, NERC GADS EFORs, FERC Form 714 hourly loads, 1998-2005; CAISO DA prices (NP15/SP15), PJM AEP hub, utility system lambda where no market.

## 6. Justification
Exact treatment of SoC-reliability coupling; comparison against widely used capacity-factor approximations across 5 systems x 8 years.

## 7. Key results
- Average annual ECP (% of nameplate): 1 h 40.7%, 2 h 55.5%, 4 h 74.6%, 8 h 93.7%, 10 h 97.9%.
- Inter-annual variability up to ~40 percentage points (PG&E 4 h: ~60% in 1999 vs ~99% in 2004), driven by misalignment between price peaks and shortage hours.
- Capacity-factor approximations overestimate short-duration storage by up to ~22 pp and are sensitive to the number of hours chosen.

## 8. Limitations (stated + critical reading)
Single device (no fleet saturation), no transmission, no storage forced outages, energy-only market (no capacity payment influencing dispatch), DA rather than RT prices. Critical: results depend on dispatch rule — capacity accreditation is a joint function of physics and the market incentives the owner faces, which is exactly the design lever later formalised by Kim, Sioshansi et al. (2022, 2025 TPWRS).

## 9. Relevance to my study
Basis for interpreting GB Capacity Market de-rating factors for 0.5-4 h batteries (duration-dependent de-rating). Shows that capacity value is endogenous to the market signal the battery follows: in a rule-switchable simulator, toggling whether the battery must hold SoC for capacity obligations changes both energy/AS revenue and its accredited capacity.

## 10. Lineage links
- Builds on: Tuohy & O'Malley capacity-factor approach; Madaeni-Sioshansi-Denholm capacity value of CSP/thermal storage.
- Built upon by (notable): Kim, Sioshansi, Lannoye & Ela 2022 TPWRS 37(3):1809-1819 (stochastic-dynamic version), Kim et al. 2025 TPWRS 40(3) (storage providing regulation); denholm2020_peakingcapacity.

## 11. Verification log
- DOI 10.1109/TPWRS.2013.2279839 resolved via doi.org -> IEEE Xplore document 6601729; vol/issue/pages from Sioshansi CMU publication list (Vol 29, No 1, pp 395-403, Jan 2014); NREL research-hub record lists same title.
- SJR: scimagojr sourceid 28825, Q1 2013-2024 both categories.
- Full text read (author PDF): authors' affiliations (OSU; PG&E; NREL), funding DOE DE-AC36-08GO28308.
