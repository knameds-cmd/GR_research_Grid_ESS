---
id: landy2026_hybridstacking
title: "Maximising the economic value of renewable and battery storage hybrids with revenue stacking"
authors: ["Landy, M.", "Schmidt, O.", "Johnson, N.", "Staffell, I."]
year: 2026
journal: "Energy & Environmental Science"
volume_issue_pages: "19(13):4469-4494"
doi: "10.1039/d6ee00776g"
quartile: "Q1 (SJR, journal-level; Energy & Environmental Science is a top-tier Q1 journal in all its SJR categories; pub-year 2026 SJR not yet published — nearest year not separately checked in session)"
quartile_basis: "nearest-year; rule=unchecked (expected pass); SJR 2026 not yet published and SJR 2025 for Energy & Environmental Science not checked in this session"
group: "Iain Staffell, Centre for Environmental Policy, Imperial College London"
lineage: "Staffell/Imperial CEP line (same group as gale2026_balancingbatteries). Landy supervision not verified."
streams: [S1_foundations_value, S2_stacking_cooptimization, S7_market_design]
market_context: "UK case study (co-located vs hybridised renewables + BESS, grid charging on/off, market stacking combinations) plus multi-region comparison (Australia, Nordics, US incl. Texas, Europe, Japan)"
method_class: "revenue-stacking optimisation with explicit efficiency losses and degradation (exact formulation not verified)"
evidence_read: "abstract-level only (search-engine summaries of the RSC page; publisher site blocked in session). Full text NOT read."
oa_link: ""
competitor: "C2 — cross-country, one-model study by the Staffell group (see literature/WATCHLIST.md)"
---

## 1. Research question
When are renewable + storage hybrids economically superior to stand-alone renewables or stand-alone storage, and how does this depend on market access and operating constraints across world regions? (from abstract)

## 2. Setting & assumptions
- UK case study with combinations of revenue stacking under co-located and fully hybridised set-ups; grid charging allowed or not (from abstract).
- Multi-region analysis: Australian, Nordic and most US markets vs Europe, Texas and parts of Japan (from abstract). Price data years, foresight and price-taker assumptions: not verified.

## 3. Constraints that drove the model choice
Not verified.

## 4. Model
Revenue-stacking optimisation model "with explicit efficiency losses and battery degradation" (from abstract). Formulation and solver not verified.

## 5. Data & processing
Not verified.

## 6. Justification
Not verified.

## 7. Key results (from abstract / search summaries)
- "Profitability depends more on market access and operating constraints than on location alone."
- UK: storage becomes strongly profitable only when it can **both charge from the grid and stack revenues across markets**; four-hour duration most cost-effective in the UK case; stand-alone storage tends to beat co-located/hybrid set-ups; optimal storage capacity 252 MW when participating in all markets with grid charging (case-specific).
- Regions: stand-alone storage favourable in Australian, Nordic and most US markets; hybrids superior in Europe, Texas and parts of Japan.

## 8. Limitations (critical reading, to check)
- Market access is varied as bundles (grid charging, market sets), not necessarily as individual product rules; rule interactions and attribution (Shapley) apparently not done. Check whether EAC products and BM skip rates are modelled.

## 9. Relevance to my study
- Invalidates the archive's earlier claim that no study compares countries with one model and one optimiser (S7 gap 5). Our remaining contribution: rule-level (not bundle-level) counterfactuals for a stand-alone battery, regime dependence, and an explicit attribution method.
- Strong citation for the hypothesis "rules (market access) > location" — supports our framing.

## 10. Lineage links
- Builds on: staffell2016_maxvalue; schmidt2019_lcos; Schmidt & Staffell (2023, CANON).
- Sibling: gale2026_balancingbatteries.

## 11. Verification log
- 2026-10-07: authors, journal, 19(13):4469–4494, DOI 10.1039/d6ee00776g, first published 19 June 2026, all authors Imperial CEP — from search-engine summaries of the RSC page. DOI not resolved through a resolver (blocked); re-check with the PDF.
- Full text NOT read.
