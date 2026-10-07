---
id: kim2021_vss
title: "Benefits of Stochastic Optimization for Scheduling Energy Storage in Wholesale Electricity Markets"
authors: ["Kim, H. J.", "Sioshansi, R.", "Conejo, A. J."]
year: 2021
journal: "Journal of Modern Power Systems and Clean Energy"
volume_issue_pages: "9(1):181-189"
doi: "10.35833/MPCE.2019.000238"
quartile: "Q1 (SJR 2021, 2023 and 2024, J. Modern Power Systems & Clean Energy; Q1 Energy Eng. & Power Tech. and Renewable Energy, Sustainability & Environment)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Sioshansi & Conejo (The Ohio State University)"
lineage: "All three at Ohio State (OpenAlex). Kim = Sioshansi PhD student (co-authored follow-up Kim, Sioshansi et al. 2022 TPWRS SDP capacity-value paper per Sioshansi publication list). Conejo link to UCLM offering school."
streams: [S3_bidding_uncertainty]
market_context: "PJM DA + RT energy, APCO zone, 2012; 100 MW / 1,000 MWh pumped-hydro-like storage; price impact via linear price-response"
method_class: "SP (two-stage, NLP with quadratic objective; IPOPT)"
evidence_read: "full text (author copy, https://www.cmu.edu/ceic/people/rsioshan/docs/storage_sp.pdf)"
oa_link: "https://ieeexplore.ieee.org/ielx7/8685265/9334117/09096503.pdf"
---

## 1. Research question
When does stochastic (vs deterministic expected-value) optimisation actually add value for storage scheduling in a two-settlement DA/RT market?

## 2. Setting & assumptions
- Two-stage: DA schedule (c_t, d_t, s_t) committed before RT prices known; RT incremental adjustments Δc^ω_t, Δd^ω_t per scenario.
- Prices linear in storage net purchase: DA α_t + β_t Z_t; RT α^ω_t + β^ω_t Z^ω_t (price-maker via residual price response; β = 0 ⇒ price-taker).
- RT flexibility γ: −γC^max ≤ Δc ≤ γC^max, same for discharge; γ = 1 full, γ = 0 none.
- Storage: S^max 1,000 MWh, C^max = D^max = 100 MW, η = 0.75 round trip, S_0 = 200 MWh; hourly, 24 h; risk-neutral; no imbalance penalties.

## 3. Constraints that drove the model choice
Linear price response chosen as tractability/fidelity compromise (stated). Two-stage SP with quadratic revenue solved by IPOPT in < 1 min.

## 4. Model
- max Σ_t {[α_t + β_t(c_t − d_t)](d_t − c_t) + Σ_ω φ_ω [α^ω_t + β^ω_t(c_t + Δc^ω_t − d_t − Δd^ω_t)](Δd^ω_t − Δc^ω_t)}
- s_t = s_{t−1} + η c_t − d_t (DA and per-scenario RT); power and SoC bounds.
- Non-anticipativity: DA variables scenario-independent.
- Key proposition: if γ = 1 and β = β^ω = 0, VSS = 0 — DA profit term independent of RT schedule, storage acts as pure financial arbitrageur optimised on E[RT price]. VSS > 0 if γ < 1 or prices respond. With price response, simultaneous charge/discharge ("wasting" energy) can be profitable.

## 5. Data & processing
- PJM APCO-zone hourly DA and RT prices regressed (OLS) on load, heating/cooling degrees (65 °F base), month/weekend/hour dummies and interactions; data 1 Apr–30 Jun 2012; temperature Leesville, VA.
- SARIMA: temperature (2,1,0)×(0,1,1)_24; load (1,1,0)×(0,1,1)_24.
- Scenarios: 100 equiprobable Monte Carlo paths (temperature/load → regression → prices); no reduction. Evaluated day 15 May 2012.
- Price-response coefficients: β_t 0.010–0.043; β^ω_t 0.002–0.056.

## 6. Justification
Analytical proof of VSS = 0 case + numerical VSS across γ and β.

## 7. Key results
- VSS by γ: 1.00 → 0.17 %; 0.80 → 0.84 %; 0.70 → 1.08 %; 0.50 → 2.05 % (max); 0.20 → 1.53 %; 0.00 → 0 %. Profits $30,960 (γ = 1) … $9,264 (γ = 0).
- Stylised: γ = 1, β = 0 ⇒ VSS 0.00 %; β = 0.05 ⇒ 0.13 %.
- Price suppression up to $1.99/MWh (DA) and $4.13/MWh (RT scenario) at γ = 0.7.

## 8. Limitations (stated + critical reading)
- Stated: linear price response; DA/RT correlation only implicit; risk-neutral (risk aversion could give VSS > 0 even at γ = 1); no imbalance penalties.
- Critical: single day, single zone; VSS magnitudes small (≤ 2 %) — supports the view that for small price-taking batteries most value lies in RT/intraday flexibility, not in stochastic DA scheduling.

## 9. Relevance to my study
Key theoretical anchor: product rules that restrict RT re-trading (γ < 1: firm DA commitments, balancing penalties, gate closures) are exactly what make stochastic/learning bidders valuable — directly links market-product design to the value of uncertainty-aware bidding.

## 10. Lineage links
- Builds on: krishnamurthy2018_dart (cited as [9]); Conejo two-stage SP school.
- Built upon by: Sioshansi group SDP/capacity-value work.

## 11. Verification log
- DOAJ record + Sioshansi publication page + OpenAlex works/doi:10.35833/MPCE.2019.000238 → 9(1):181-189, Jan 2021, Ohio State.
- Full text: author PDF on CMU site (accepted version).
- SJR: id 21100420330, Q1 2021/2023/2024. Journal is IEEE/SGEPRI-published, not MDPI.
