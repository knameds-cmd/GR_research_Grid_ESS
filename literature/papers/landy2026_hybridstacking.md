---
id: landy2026_hybridstacking
title: "Maximising the economic value of renewable and battery storage hybrids with revenue stacking"
authors: ["Landy, M.", "Schmidt, O.", "Johnson, N.", "Staffell, I."]
year: 2026
journal: "Energy & Environmental Science"
volume_issue_pages: "19(13):4469-4494"
doi: "10.1039/d6ee00776g"
quartile: "Q1 (SJR, journal-level: Energy & Environmental Science is a top-tier Q1 journal in all its SJR categories; pub-year 2026 SJR not yet published — nearest year not separately checked in session)"
quartile_basis: "nearest-year; rule=unchecked (expected pass); SJR 2026 not yet published and SJR 2025 for Energy & Environmental Science not checked in this session"
group: "Iain Staffell, Centre for Environmental Policy, Imperial College London"
lineage: "Staffell/Imperial CEP line (same group as gale2026_balancingbatteries; same solver GLOP/OR-Tools). Landy supervision not verified."
streams: [S1_foundations_value, S2_stacking_cooptimization, S7_market_design]
market_context: "UK case study (Lyneham solar farm; WS + BM + Dynamic Containment DCL/DCH, 2023 prices) for stand-alone, co-located and fully hybrid RES + BESS; international comparison of 45 markets in 30 countries (US, Europe incl. Nordics, Japan, Australia) with wholesale arbitrage only, 2023"
method_class: "LP"
evidence_read: "full text of main article (published CC BY version, PDF supplied by user 2026-10-13); supplementary appendices 1–14 (data sources, parameter values) NOT read"
oa_link: "https://doi.org/10.1039/d6ee00776g"
competitor: "C2 — cross-country, one-model study by the Staffell group (see literature/WATCHLIST.md, docs/03_competitor_analysis_KO.md)"
---

## 1. Research question
When are renewable + storage hybrids (co-located or fully integrated) economically superior to stand-alone renewables or stand-alone storage, which sizes and operating strategies maximise value, and how does this vary across markets and regulatory designs?

## 2. Setting & assumptions
- **Two-step algorithm**: (1) control strategy = LP dispatch over one year (half-hourly), (2) storage sizing = dichotomy search over power capacity (objective treated as convex).
- **UK case study**: Lyneham solar farm (randomly chosen; two other UK sites as sensitivity). Markets: wholesale (WS), Balancing Mechanism (BM) and Dynamic Containment (DCL/DCH), "as price data from these markets are openly available from the system operator". Year 2023 prices repeated over the project life.
- **International**: 45 markets in 30 countries (CAISO, ERCOT, MISO, PJM, NYISO; ENTSO-E/NESO for Europe; JEPX; AEMO), 252 sub-regions, **wholesale arbitrage only** (other markets lacked consistent data), 2023 prices, Renewables.ninja capacity factors.
- **Configurations**: stand-alone BESS / co-located (RES has export priority, separate decisions) / full hybrid (joint optimisation, shared connection); AC or DC coupling; one-way (RES-only charging) or two-way grid connection.
- **BM**: battery may charge when BM volume < 0 and discharge when > 0, up to that volume, at the BM price (same NIV logic as gale2026).
- **DC**: reserved energy DClow/DChigh bounded by the procured DC volume; price fixed within each 4-h EFA block; activated share of reserve e_low/e_high fixed from historical data.
- **Price-taker** with perfect foresight; "no single storage project can be a price maker", but the authors acknowledge equilibrium feedback at scale.
- **Asset & finance**: calendar (13 yr) + cycle (4,500 cycles) ageing tracked in SoH; replacement at calendar life at 50% of initial CAPEX; daily cycle limit; self-discharge; DoD; 8% discount rate; constant annual revenues.

## 3. Constraints that drove the model choice
- Joint sizing + dispatch across dozens of markets → keep the dispatch problem linear (LP) and separate sizing from dispatch.
- Cycle-life replacement would make the problem path-dependent and non-convex → replacement depends on calendar life only.
- Data: ancillary and balancing price data not consistently available outside the UK → international runs are wholesale-only.

## 4. Model
- Objective: maximise Σ profit − fixed OPEX − annuity × CAPEX (co-located: storage developer's incremental profit over the RES baseline; full hybrid: joint profit).
- Decision variables: WS charge/discharge, BM charge/discharge, DC low/high reserved energy, RES-to-storage and RES-to-grid flows, SoC, SoH.
- Key constraints: grid-connection limit on the sum of all flows including DC reservations (Eq. 12); storage power limit on total throughput (Eq. 14); energy balance with efficiencies, self-discharge and DC activation (Eq. 19); SoC ≤ SoH × DoD × energy capacity (Eq. 20); daily cycle limit (Eq. 18); BM direction/volume (Eq. 7); DC volume and EFA-block price (Eqs. 8–9).
- Solver: GLOP (Google OR-Tools), Python.

## 5. Data & processing
- 2023 prices from system/market operators; UK BM and DC from NESO/Elexon (exact series in SI Appendix 5, not read).
- Wind/solar profiles from Renewables.ninja (2023 weather). Sites chosen by a weighted max-min p-dispersion algorithm over the largest wind/solar farms.
- Costs: RES CAPEX by region from the GNESTE database; storage costs constant across countries.

## 6. Justification
- Sensitivity to price year (2020, 2022 vs 2023): optimal storage size changes little, NPV changes a lot.
- Sensitivity to discount rate and to UK site (sizing robust, profit site-dependent).
- Cycling check: mean 1.21 cycles/day in the UK revenue-stacking case (median 0.96 internationally), in line with warranties and observed GB/Australian cycling; the calendar-life replacement simplification is argued not to change the number of replacements.

## 7. Key results
- **UK, co-located with a 100 MW solar farm (1 h battery)**: profitable only with **grid charging + WS + BM**; DC "marginally increases profits" (2023, a saturated year); optimal capacity 252 MW when all markets + grid charging; annual profit ≈£4m with most profit from BM.
- **Duration**: a 106 MW, 4-h system gives the highest profit (≈£8.5m/yr); profitable capacity range narrows as duration rises. 4 h is "the most cost-effective compromise" across most markets.
- **Stand-alone vs hybrid (UK)**: stand-alone storage has the highest NPV for both solar and wind (the battery can use the whole grid connection). Full hybrids beat co-location. Table 4 (PDF text extraction; check column mapping): stand-alone 4-h storage 114 MW, IRR ≈24%, NPV ≈£99.6m, payback 5 yr.
- **New-build UK hybrids (all merchant)**: 95 MW solar + 115 MW storage (NPV ≈£103m); 195 MW wind + 95 MW storage (NPV ≈£217m). 24/7 hybrid PPA break-even ≈£120/MWh (solar) and ≈£100/MWh (wind).
- **International (wholesale only)**: stand-alone storage favoured across most of Australia, the US except Texas, and Nordic countries; solar or solar–wind hybrids favoured in Texas, parts of Japan and much of southern/central Europe; wind + storage in the UK, Ireland, Netherlands, Denmark, Baltics. Storage CAPEX threshold for hybrid viability ranges from ≈£60/kWh (Norway, hydro competition) to ≈£1,560/kWh (South Australia) and scales with log(std. dev.) of wholesale prices. Fully merchant wholesale-only storage is "usually marginal or loss-making".
- **Headline**: "profitability depends more on market access and operating constraints than on location alone" — where market access means the ability to **charge from the grid** and to **stack WS, BM and ancillary revenues**.

## 8. Limitations (stated + critical reading)
- Stated: one price year repeated; constant 8% discount rate; simplified efficiency/degradation; exchange at clearing price up to market volume (no bid acceptance — "data are proprietary"); no future cost trends; curtailment only from grid capacity.
- Critical reading:
  - "Market access" is varied as **bundles** (which markets, grid charging yes/no), not as individual product rules; no attribution across rules and no interaction analysis.
  - UK ancillary scope is DC only (no DM/DR/BR/QR/SR, no Capacity Market); 2023 is a single post-saturation year, so DC's contribution is small by construction.
  - International comparison is wholesale-only, so it compares price volatility and RES profiles, not market designs; the authors call their international results "conservative" where balancing/ancillary/capacity revenues matter.
  - BM treated like gale2026 (NIV-constrained marginal price) → same upper-bound caveat.

## 9. Relevance to my study
- Invalidates the archive's earlier claim that no study compares countries with one model (S7 gap 5) — but at the level of **wholesale-only, bundle-level** comparison. Our remaining contribution: rule-level attribution for a stand-alone battery, across regimes, including ancillary products and the Capacity Market.
- Supports our hypotheses: (i) DC added little in 2023 (saturation; regime dependence), (ii) market access rules matter more than location, (iii) 4-h duration preferred when ancillary revenues fade (consistent with the CM de-rating and SR trends in `literature/context/`).
- Their future-work list is a citable gap statement: "comparative work is needed on how interconnection rules, network charges, and 'hybrid definitions' in regulation affect revenue stacking", plus "probabilistic representations of bid acceptance and service activation".
- Formulation pieces we can reuse: DC as reserved energy within procured volume with fixed EFA-block price; grid-connection constraint including reservations; SoH tracking with calendar + cycle ageing.

## 10. Lineage links
- Builds on: Schmidt & Staffell (2023, CANON; ref. 34); staffell2016_maxvalue; Hesse et al. (degradation, ref. 62); Renewables.ninja (Staffell & Pfenninger 2016).
- Sibling: gale2026_balancingbatteries (cited as ref. 81).

## 11. Verification log
- 2026-10-07: bibliographic data from search-engine results.
- 2026-10-13: **main text read** from the published PDF supplied by the user (CC BY 4.0): Energy Environ. Sci. 2026, 19, 4469–4494; received 4 Feb 2026, accepted 17 Jun 2026, published 19 Jun 2026; all authors Imperial CEP. The supplementary information (Appendices 1–14: data sources, parameter tables, regional case studies) was not supplied and not read.
- Table 4 values come from PDF text extraction, where column order can be scrambled; re-check against the PDF before quoting.
