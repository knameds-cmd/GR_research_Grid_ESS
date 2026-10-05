---
id: sioshansi2010_ownership
title: "Welfare Impacts of Electricity Storage and the Implications of Ownership Structure"
authors: ["Sioshansi, R."]
year: 2010
journal: "The Energy Journal"
volume_issue_pages: "31(2):173-198"
doi: "10.5547/ISSN0195-6574-EJ-Vol31-No2-7"
quartile: "Q1 (SJR 2010, Economics & Econometrics and Energy (misc.); journal Q1 2008-2022 & 2024, Q2 in 2023/2025)"
group: "Ramteen Sioshansi — Integrated Systems Engineering, The Ohio State University"
lineage: "Single-author extension of sioshansi2009_pjmvalue (OSU/NREL line)."
streams: [S1_foundations_value, S7_market_design]
market_context: "ERCOT 2005 (calibration), stylised two-period (off/on-peak) market with linear price-load relation; generic bulk storage"
method_class: "analytical Nash equilibrium + MCP (complementarity) numerical study"
evidence_read: "full text (author copy, https://www.cmu.edu/ceic/people/rsioshan/docs/storage_ownership.pdf)"
oa_link: "https://www.cmu.edu/ceic/people/rsioshan/docs/storage_ownership.pdf"
---

## 1. Research question
When large storage smooths on/off-peak prices, do merchant, generator- or consumer-owned storage operate it at the welfare-maximising level, and which ownership mix minimises welfare loss?

## 2. Setting & assumptions
- Two periods per day: off-peak load l1 (daily minimum), on-peak l2 (daily maximum); perfectly inelastic demand; deterministic (perfect foresight).
- Price p(l) = c0 + c1·l (c1 > 0) — storage is a price-maker.
- Storage of discharge capacity δ (charging δ/η); efficiency η ∈ (0,1), mainly 0.65–0.85 (CAES/flow) and up to 0.9.
- Owners: merchant (arbitrage profit), generators (arbitrage + producer surplus), consumers/LSEs (arbitrage + consumer surplus), social planner (total welfare). N symmetric firms of each type (Nash-Cournot in storage use).
- ERCOT 2005 duopoly-like structure (TXU, Texas Genco; Reliant & TXU retail) for calibration.

## 3. Constraints that drove the model choice
Need closed-form insight into incentive misalignment → two-period linear model admitting explicit first-order conditions; multi-owner interaction requires a complementarity formulation (PATH solver).

## 4. Model
With φ = 1/η:
- ΔCS(δ) = δ c1 (l2 − φ l1); ΔPS(δ) = δ c1(−l2 + φ l1) + ½ δ² c1 (1 + φ²).
- Arbitrage profit Π(δ) = δ[c0(1 − φ) + c1(l2 − φ l1)] − δ² c1(1 + φ²).
- Welfare ΔW(δ) = δ[c0(1 − φ) + c1(l2 − φ l1)] − ½ δ² c1(1 + φ²); δ_W = [c0(1−φ)+c1(l2−φ l1)]/[c1(1+φ²)].
- Propositions: merchants underuse (δ_S = N/(N+1)·δ_W); generators underuse (monopoly generator does not use storage at all); consumers overuse; all converge to δ_W as N → ∞.
- Numerical: Nash equilibria with mixed ownership as MCP solved with PATH.

## 5. Data & processing
ERCOT 2005 hourly loads; daily min/max load define l1, l2; generator costs from heat rates × fuel prices + SO2 + VOM; daily simulations aggregated over the year.

## 6. Justification (why the authors argue the approach is valid)
Analytical propositions hold for any parameters of the linear model; numerical results calibrated to a real concentrated market; sensitivity over efficiency, size and number of firms.

## 7. Key results
- Merchant ownership: welfare loss vs optimum < 12 %, insensitive to size/efficiency.
- Generator ownership: up to 100 % loss (storage idle at η < ~0.75 in duopoly).
- Consumer ownership: overuse; at low efficiencies (≈ < 0.74) storage use can reduce welfare relative to no storage.
- Mixed ownership (1 GW, η = 0.89, duopoly): loss minimised with ~865 MW merchant + 135 MW consumer-owned; more competitive markets favour more consumer ownership.
- Policy: be wary of encouraging generator- or consumer-owned storage; merchant storage tends to minimise welfare losses.

## 8. Limitations (stated + your critical reading)
- Stated: linear price–load is illustrative (non-convex costs, start-ups ignored); two-period structure; inelastic demand; municipal/co-op/integrated-utility ownership not modelled.
- Critical: no uncertainty, no ancillary services, no network; Cournot-in-storage assumption; calibration to 2005 ERCOT predates nodal market.

## 9. Relevance to my study
Formal basis for why **who earns** storage revenue (merchant vs vertically integrated) changes dispatch and welfare — useful counter-argument when interpreting "profitability" as a proxy for social value, and when discussing ownership/unbundling rules (e.g., EU ban on network-owned storage).

## 10. Lineage links
- Builds on: sioshansi2009_pjmvalue.
- Built upon by (notable): sioshansi2014_welfareloss; storage market-power literature (see S7 stream); junge2022_efficientstorage (competitive efficiency side).

## 11. Verification log
- Crossref (10.5547/ISSN0195-6574-EJ-Vol31-No2-7): title, single author, OSU affiliation, Energy Journal 31(2):173–198, April 2010 ✔.
- SJR (id 29391): Q1 in 2010 for both categories; note Q2 in 2023 and 2025 ✔.
- Full text read from author copy (CMU CEIC page); equations transcribed from it.
