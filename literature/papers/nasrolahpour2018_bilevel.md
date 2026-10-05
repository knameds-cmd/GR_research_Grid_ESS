---
id: nasrolahpour2018_bilevel
title: "A Bilevel Model for Participation of a Storage System in Energy and Reserve Markets"
authors: ["Nasrolahpour, E.", "Kazempour, J.", "Zareipour, H.", "Rosehart, W. D."]
year: 2018
journal: "IEEE Transactions on Sustainable Energy"
volume_issue_pages: "9(2):582-598"
doi: "10.1109/TSTE.2017.2749434"
quartile: "Q1 (SJR 2024, IEEE Trans. Sustainable Energy, SJR 4.261; Q1 Renewable Energy, Sustainability & Environment)"
group: "Zareipour & Rosehart (Univ. of Calgary) with Kazempour (DTU)"
lineage: "Nasrolahpour = Calgary PhD (Zareipour corresponding author; supervision not re-verified). Kazempour (DTU) — earlier UCLM bilevel/MPEC work with Conejo & Ruiz (not re-verified this session) → direct heir of ruiz2009_mpecoffer."
streams: [S3_bidding_uncertainty]
market_context: "Pool with DA joint energy + up/down reserve clearing, then real-time balancing market; Alberta (AESO) case 23 Nov 2015 + illustrative 4-generator system; merchant price-maker storage"
method_class: "MILP (stochastic bilevel → MPEC → MILP; KKT + big-M + strong duality + binary expansion)"
evidence_read: "full text (DTU Orbit accepted manuscript, https://backend.orbit.dtu.dk/ws/portalfiles/portal/137096856/A_Bilevel_Model_for_Participation_of_a_Storage_System_in_Energy_and_Reserve_Markets.pdf)"
oa_link: "https://orbit.dtu.dk/en/publications/a-bilevel-model-for-participation-of-a-storage-system-in-energy-a/"
---

## 1. Research question
What are the most profitable strategic price-quantity offers of a merchant price-maker storage across DA energy, DA reserve and balancing markets when net-load (wind) is uncertain at DA time?

## 2. Setting & assumptions
- Price-maker; markets sequential: (1) DA joint energy + reserve clearing; (2) RT balancing per scenario with DA outcomes fixed.
- Information structure: DA offers made before net-load deviation known; balancing offers/deployment per scenario.
- Uncertainty: net-load deviation Q_{t,k} (wind forecast error); rivals' offers known parameters.
- Illustrative: 24 h, 4 generators ($12–$120/MWh), storage 20 MW dis/15 MW ch, 120 MWh, 100 % efficiency. Alberta: 14 aggregated generators (~9.5 GW), storage 100 MW dis/50 MW ch, 400 MWh, 50 % efficiency; reserve requirement 20 % of expected wind.
- No transmission, no ramping.

## 3. Constraints that drove the model choice
- Strategic storage ⇒ bilevel; multiple lower levels (DA + one balancing per scenario) ⇒ MPEC with many complementarity sets.
- Bilinear price×quantity terms in balancing not removable by strong duality ⇒ binary expansion with MW-step ΔP (accuracy vs time trade-off).
- Scenario count must be small (16 after reduction) for MILP tractability.

## 4. Model
- Upper level: max expected profit = DA energy + reserve revenues + Σ_k π_k balancing revenue; storage SoC; mode exclusivity u^dis + u^ch ≤ 1.
- Offers: per hour separate price-quantity pairs — charge bid (ob^ch, pb^ch), discharge offer (ob^dis, pb^dis), up/down reserve price-quantity in each mode; one block per product per hour.
- Lower levels: (b) DA energy+reserve clearing LP; (c) balancing clearing LP per scenario → KKT; big-M; strong duality for DA bilinear; binary expansion for remaining bilinear.
- Non-anticipativity: DA offers scenario-independent.
- Risk measure: none (risk-neutral). Storage energy balance enforced "in expectation" (a.17) in base model.
- Solver: CPLEX/GAMS, i7-5930K, 64 GB.

## 5. Data & processing
- Illustrative: 3 scenarios (prob 0.90, 0.05, 0.05).
- Alberta: 1,000 daily wind scenarios from normal errors (σ = 10 %) → backward scenario reduction to 16.

## 6. Justification
Case-by-case comparison: energy-only vs joint energy+reserve vs DA+balancing; sensitivity to MW-step; per-scenario vs expected-value storage constraints.

## 7. Key results
- Joint DA energy+reserve profit 6 % higher than sequential markets; profit ≈ $1.6k (energy only) → ≈ $7k (energy+reserve) → ≈ $10k expected (DA+balancing, 3 scenarios).
- Strategic offering raises peak energy prices 12–25 %; balancing price can reach $400/MWh (vs $12/MWh) in high-load scenario — market power in balancing.
- Enforcing storage constraints per scenario reduces expected profit by 15 %.
- Runtime: illustrative < 2 min; Alberta ~200 s (100 MW step) to ~4,000 s (25 MW step), profit varies ~5 % across steps.

## 8. Limitations (stated + critical reading)
- Stated: no network/ramping; rivals' offers known; expectation-only SoC; discretisation error.
- Critical: wind scenarios are i.i.d. normal errors (no temporal correlation); expected-SoC constraint is physically infeasible ex post in some scenarios (and the paper quantifies the 15 % cost of fixing it).

## 9. Relevance to my study
Directly relevant to multi-product (energy + reserve + balancing) bidding by batteries: shows how product sequencing and balancing price formation create strategic value; template for GB BM/DC or Nordic FCR/mFRR market-design experiments with a price-maker storage.

## 10. Lineage links
- Builds on: ruiz2009_mpecoffer; mohsenianrad2016_pricemaker; Nasrolahpour et al. (2016) TSTE strategic sizing (not in archive).
- Built upon by: tomasson2020_offerbid (portfolio, stochastic disjunctive B&B).

## 11. Verification log
- DTU Orbit record + OpenAlex works/doi:10.1109/TSTE.2017.2749434 → 9(2):582-598 (issue 2018; online 2017), affiliations Calgary/DTU.
- Full text read: DTU Orbit accepted manuscript.
- SJR: IEEE TSTE Q1 2023/2024.
