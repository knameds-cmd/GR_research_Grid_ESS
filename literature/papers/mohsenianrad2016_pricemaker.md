---
id: mohsenianrad2016_pricemaker
title: "Coordinated Price-Maker Operation of Large Energy Storage Units in Nodal Energy Markets"
authors: ["Mohsenian-Rad, H."]
year: 2016
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "31(1):786-797"
doi: "10.1109/TPWRS.2015.2411556"
quartile: "Q1 (SJR 2024, IEEE Trans. Power Systems, SJR 3.629; Q1 Electrical & Electronic Eng. and Energy Eng. & Power Tech.)"
group: "Mohsenian-Rad (UC Riverside)"
lineage: "Single-author, UC Riverside (OpenAlex). Continues Mohsenian-Rad group's storage-market work (e.g., Akhavan-Hejazi & Mohsenian-Rad 2014, IEEE TSG — citation not verified this session; not in archive). Methodologically follows ruiz2009_mpecoffer."
streams: [S3_bidding_uncertainty]
market_context: "Nodal (LMP) day-ahead energy market, DC-OPF clearing; CAISO March 2014 price profiles to calibrate; IEEE 30-bus; one firm owning 4 × 1 GWh storage units"
method_class: "MILP (bilevel → KKT + big-M + strong duality); scenario-based SP and min-max extensions"
evidence_read: "full text (UC Riverside eScholarship compilation PDF, https://escholarship.org/content/qt96z5j2pp/qt96z5j2pp.pdf)"
oa_link: "https://escholarship.org/content/qt96z5j2pp/qt96z5j2pp.pdf"
---

## 1. Research question
How should a single owner of several large, geographically distributed storage units coordinate their price-quantity bids in a nodal market when their operation moves LMPs and is affected by congestion?

## 2. Setting & assumptions
- Price-maker; lower level = ISO DC-OPF economic dispatch determining LMPs.
- T = 24 hourly slots, day-ahead; 4 units at buses {4, 16, 24, 30}, each 1 GWh; IEEE 30-bus (41 lines, 8 generators, 16 loads).
- Base model deterministic (rivals' offers and demand known); extension IV-B: K scenarios of uncertain supply/demand bids; efficiency extension z[t+1] = z[t] − α P^SD + β P^SC (α ≥ 1, β ≤ 1), tested at 80–95 %.
- Energy only; no ancillary services.

## 3. Constraints that drove the model choice
Bilevel with nonconvex upper-level revenue (price × quantity) and complementarity; tractability forced KKT + big-M (L = 1000) + strong duality to get a MILP solvable by CPLEX. Uncertainty kept to a handful of scenarios because each scenario replicates the full lower-level KKT system.

## 4. Model
- Upper level: max Σ_i Σ_t LMP_{n(i),t}·(discharge − charge) subject to SoC dynamics.
- Bids: per unit/hour quantity bids x_i[t] (discharge), y_i[t] (charge) and price bid c_i[t] ($/MWh) → economic (price-quantity) bids; self-schedule bids enforced via c_i = ±L.
- Lower level: DC-OPF (LP) → KKT (eqs 7–27), complementarity linearised (30–45), strong duality (51) removes bilinear revenue.
- Stochastic version (58): bids x, y, c have no scenario index (non-anticipative); SoC z_{i,k}[t] and market outcomes per scenario k; expected profit.
- Robust version (61): maximise min-profit over the discrete scenario set (not a continuous uncertainty set).

## 5. Data & processing
- CAISO March 2014 hourly price pattern (35.1–70.3 $/MWh) used to set generator offers; IEEE 30-bus.
- Scenarios: K = 3, built by perturbing generator price bids (e.g., +1.36, +0.76, −4.23 $/MWh offsets). No statistical scenario generation.

## 6. Justification
Exact MILP equivalence of the bilevel; sensitivity studies on congestion, location diversity, efficiency, economic vs self-schedule bidding.

## 7. Key results
- Congestion can raise profit up to ~200 % (e.g., $585,877 vs $194,696 base).
- Average total generation cost reduction 2.23 % with storage.
- Distributed placement outperforms co-location.
- Economic vs self-schedule bids equal under determinism; under uncertainty economic bidding yields higher expected profit ($192,951 vs $190,104) — price component acts as a filter against adverse clearing.
- Worst-case design: min profit $184,947 → $187,183 but mean $190,104 → $187,421.
- Solve time ≈ 147–152 s per instance.

## 8. Limitations (stated + critical reading)
- Stated: energy only; DC-OPF; single owner; ideal efficiency in base model.
- Critical: K = 3 ad-hoc scenarios — no out-of-sample test; perfect knowledge of rivals' offers in base case; no end-of-horizon SoC value (addressed by wang2017_lookahead).

## 9. Relevance to my study
Clear demonstration of WHY price in the bid matters only under uncertainty (economic vs self-schedule result). Reusable MPEC structure for testing market power of large batteries in a zonal (GB/Nordic) setting by replacing DC-OPF with zonal clearing.

## 10. Lineage links
- Builds on: ruiz2009_mpecoffer; Akhavan-Hejazi & Mohsenian-Rad (2014) TSG.
- Built upon by: wang2017_lookahead; nasrolahpour2018_bilevel; tomasson2020_offerbid.

## 11. Verification log
- OpenAlex works/doi:10.1109/TPWRS.2015.2411556 → single author UC Riverside, 31(1):786-797 (online 2015, issue Jan 2016).
- Full text read from UCR eScholarship 2016 publications PDF (published version).
- SJR: IEEE TPWRS Q1 2023/2024.
