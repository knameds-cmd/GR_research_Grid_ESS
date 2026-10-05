---
id: andrescerezo2023_marketstructure
title: "Storing power: market structure matters"
authors: ["Andrés-Cerezo, D.", "Fabra, N."]
year: 2023
journal: "The RAND Journal of Economics"
volume_issue_pages: "54(1):3-53"
doi: "10.1111/1756-2171.12429"
quartile: "Q1 (SJR 2023 and 2024, Economics and Econometrics)"
group: "Natalia Fabra (Universidad Carlos III de Madrid, EnergyEcoLab; CEPR) - ERC grant 772331"
lineage: "Andrés-Cerezo (EUI at time of WP); advisor-student tie with Fabra NOT verified. Working-paper versions: Cambridge WP in Economics 20122 / EPRG (2020), CEPR DP 15444."
streams: [S7_market_design]
market_context: "Theory with Spanish wholesale market simulation (2030 targets, ~74% renewables; 2017 REE demand)"
method_class: "analytical IO (two-stage investment + operation game) + simulation"
evidence_read: "full text (working-paper version, https://nataliafabra.org/wp-content/uploads/2020/11/Storing_Power__Market_Structure_Matters.pdf); published version not read"
oa_link: "https://nataliafabra.org/wp-content/uploads/2020/11/Storing_Power__Market_Structure_Matters.pdf"
---

## 1. Research question
How do incentives to operate and invest in storage depend on market structure - competitive storage, independent storage monopoly, market power in generation, and vertical integration of storage with a dominant generator - and what are the consumer and welfare consequences?

## 2. Setting & assumptions
- Two-stage game: storage capacity K chosen first; then production and storage decisions for each demand level.
- Deterministic demand theta distributed by a load-duration curve; linear marginal cost c'(q) = q; dominant firm with share alpha + competitive fringe; convex storage investment cost C(K).
- Storage cannot hold more than K or release more than stored; daily cycles in simulation, 85% round-trip efficiency.
- Demand perfectly inelastic.

## 3. Constraints that drove the model choice
Need to compare investment AND operation across structures with closed-form rankings -> stylised load-duration-curve model; simulation to show magnitudes in a high-renewables system.

## 4. Model
Structures: first best (planner controls production and storage); second best (planner controls storage, market sets production); competitive storage; independent storage monopolist; vertically integrated generator-storage monopolist.
Main propositions:
- P1: first-best K equates C'(K) to the price-threshold spread.
- P2-P3: second-best and competitive storage over-invest relative to first best (K^C > K^SB > K^FB), more so with generation market power alpha.
- P4: independent monopoly under-invests ("storage smoothing").
- P5: vertical integration under-invests (K^I < K^FB) because the firm values only its own cost savings.
- P6: consumer surplus ranking FB > SB = C > {I, M}; vertical integration worst for consumers and welfare.

## 5. Data & processing
Spain 2030 scenario (wind ~47%, solar ~27%, other RES ~12%), 2017 REE hourly demand; storage capacities from 0 to >10,000 MWh; daily cycling.

## 6. Justification
Formal proofs; simulation reproduces qualitative rankings; sensitivity across storage capacities and competitive vs strategic generation.

## 7. Key results
- Market power reduces efficiency via inefficient storage use and distorted investment; vertical integration is the worst structure.
- Spain 2030: average price ~17.3-21.7 EUR/MWh without storage; storage has diminishing marginal value (up to ~24 EUR/MWh marginal value) - below battery cost (~150 EUR/MWh levelised), so arbitrage alone does not justify investment.
- Storage raises wind/solar profits, lowers CCGT profits and emissions; effect on demand-weighted price non-monotonic.
- Policy: prevent dominant generators from owning storage; allocate storage to competitive operators; capacity auctions with price caps/reliability options if support needed.

## 8. Limitations (stated + critical reading)
Inelastic, deterministic demand; load-duration-curve abstraction loses chronology; daily cycles only; no ancillary services; investment cost path exogenous. Numbers above come from the 2020 WP and may differ from the published version.

## 9. Relevance to my study
Adds the investment margin to the ownership/market-power line (sioshansi2010_ownership, williams2022_marketpower): rules that change who owns storage change both dispatch and capacity built. For a Korea/GB comparison, ownership unbundling (e.g., KEPCO-affiliated vs merchant storage) is a design lever that deserves a separate counterfactual.

## 10. Lineage links
- Builds on: sioshansi2010_ownership, sioshansi2014_welfareloss; Crampes & Moreaux pumped-storage model (citation not verified here).
- Built upon by (notable): cited by butters2025_soakingsun file as cross-reference; others not verified.

## 11. Verification log
- RePEc IDEAS (bla/randje/v54y2023i1p3-53): title, authors, RAND J Econ 54(1):3-53, March 2023, DOI 10.1111/1756-2171.12429; Wiley listing shows same DOI. WP record (cam/camdae/20122) states published version.
- SJR: scimagojr sourceid 23672, Q1 2023-2024.
- Full text of 2020 WP read (affiliations, ERC 772331 + Fundación Iberdrola funding).
