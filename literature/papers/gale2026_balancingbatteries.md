---
id: gale2026_balancingbatteries
title: "Balancing with batteries: The impact of revenue stacking and skip rates on battery energy storage profitability in Great Britain"
authors: ["Gale, E.", "Schmidt, O.", "O'Cinneide, A.", "Johnson, N.", "Staffell, I."]
year: 2026
journal: "Journal of Energy Storage"
volume_issue_pages: "166:122328"
doi: "10.1016/j.est.2026.122328"
quartile: "Q1 (SJR 2025 = nearest available year; SJR 2026 not yet published. J. Energy Storage Q1 in SJR 2024 and 2025 per biggins2022 / collath2022 entries)"
quartile_basis: "nearest-year; rule=pass; SJR 2026 not yet published, nearest year 2025 = Q1 for J. Energy Storage (see staffell2016_maxvalue / collath2022_agingreview)"
group: "Iain Staffell, Centre for Environmental Policy, Imperial College London (with O. Schmidt, N. Johnson)"
lineage: "Staffell/Imperial CEP line: staffell2016_maxvalue -> Schmidt & Staffell 2023 (OUP book, CANON) -> this paper and landy2026_hybridstacking. Gale/O'Cinneide supervision ties not verified."
streams: [S2_stacking_cooptimization, S6_ancillary_products, S8_empirical_econ]
market_context: "GB day-ahead wholesale + Balancing Mechanism (bids/offers), skip rates; three years of half-hourly prices"
method_class: "co-optimisation (exact formulation not verified; likely LP/MILP)"
evidence_read: "abstract-level only (search-engine summaries of the ScienceDirect page and highlights; publisher site blocked in session). Full text NOT read."
oa_link: ""
competitor: "C1 — closest Q1 competitor (see literature/WATCHLIST.md and docs/01_next_actions.md §3)"
---

## 1. Research question
How much do GB battery profits rise when a battery stacks the Balancing Mechanism (BM) on top of day-ahead wholesale arbitrage, and how much does the system operator "skipping" battery bids/offers cost the battery? (from abstract)

## 2. Setting & assumptions
- GB day-ahead wholesale market and the BM; half-hourly resolution; three years of price data (exact years not verified). (from abstract)
- Skip rate treated as an exogenous share of battery bids/offers that are passed over; also "marginal price capture rate" in the BM (from abstract). Price-taker status, foresight and battery durations: not verified.
- Frequency response / EAC products (DC/DM/DR/BR/QR): not mentioned in the abstract-level material — check in full text.

## 3. Constraints that drove the model choice
Not verified (full text not read).

## 4. Model
"Co-optimisation framework" across wholesale and BM (from abstract). Formulation, solver and degradation treatment: not verified.

## 5. Data & processing
Three years of half-hourly GB price data (wholesale and BM). Sources and cleaning not verified. (from abstract)

## 6. Justification (why the authors argue the approach is valid)
Not verified.

## 7. Key results (from abstract / highlights)
- BM participation raises BESS revenues by up to **250%** versus wholesale arbitrage alone.
- Stacking reduces revenue volatility: diversification offsets the BM's higher price volatility.
- Batteries can be skipped "due to lacking information on their status". A **50% skip rate cuts profit by 30%** when operating in both markets; each **+10 percentage points of skipped bids cuts profit by ~7% (~£12k/MW/yr)**.

## 8. Limitations (stated + your critical reading)
- Critical reading (to check in full text): skip rate appears to be modelled as a parameter rather than as an estimated acceptance probability conditional on offer price, NIV direction and unit state (see docs/01_next_actions.md M2). Ancillary services under EAC appear absent. No rule-by-rule counterfactual decomposition is mentioned.

## 9. Relevance to my study
- Directly overlaps the "BM access / skip rate" rule switch. Our differentiation: (i) EAC co-optimised ancillary products, (ii) rule-on/off counterfactual with Shapley attribution, (iii) regime comparison (boom vs post-EAC), (iv) empirically estimated BM acceptance model.
- Useful as a validation anchor for the wholesale+BM layer (orders of magnitude, £/MW/yr per skip point).

## 10. Lineage links
- Builds on: staffell2016_maxvalue; Schmidt & Staffell (2023) *Monetizing Energy Storage* (CANON).
- Sibling: landy2026_hybridstacking (same group, same year).
- Built upon by (notable): too recent.

## 11. Verification log
- 2026-10-07: title, authors, journal, volume 166 (July 2026), article 122328 and DOI 10.1016/j.est.2026.122328 from search-engine results for the ScienceDirect page (pii S2352152X26019924). DOI string came from a search summary, not from a DOI resolver — re-check when the PDF is downloaded.
- Quartile: journal-level, nearest year (2025).
- Full text: NOT read. Every field above marked "(from abstract)" or "not verified" must be re-checked.
