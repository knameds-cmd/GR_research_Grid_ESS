---
id: braff2016_windsolarvalue
title: "Value of storage technologies for wind and solar energy"
authors: ["Braff, W. A.", "Mueller, J. M.", "Trancik, J. E."]
year: 2016
journal: "Nature Climate Change"
volume_issue_pages: "6(10):964-969"
doi: "10.1038/nclimate3045"
quartile: "Q1 (SJR 2016 and 2024/2025, Environmental Science (misc.); Social Sciences (misc.))"
group: "Jessika Trancik — Institute for Data, Systems, and Society (IDSS), MIT; Santa Fe Institute"
lineage: "Trancik lab (MIT); Braff (MIT MechE) and Mueller (IDSS) co-authors. Line continues in Ziegler et al. 2019 Joule (Trancik lab, storage requirements & costs) — not archived here."
streams: [S1_foundations_value]
market_context: "U.S. locations (incl. Texas wind), hybrid wind/solar + storage plants selling into wholesale markets (historical prices)"
method_class: "LP (revenue-maximising hybrid-plant dispatch; from abstract/figure captions)"
evidence_read: "abstract + figure captions only (nature.com landing page); full text paywalled"
oa_link: ""
---

## 1. Research question
How can storage technologies with very different energy- and power-capacity costs be compared on a common scale for their value to wind and solar plants, and what cost-improvement targets would make them value-adding?

## 2. Setting & assumptions
(from abstract/figure captions) Hypothetical hybrid renewable + storage plants dispatched to maximise revenue against historical wholesale prices at several U.S. locations; value expressed via a metric χ (value of the plant's output relative to a benchmark) versus storage size. Price-taker; other assumptions not verified.

## 3. Constraints that drove the model choice
(from abstract) Storage technologies vary along two cost dimensions (energy, power) → need a two-dimensional cost-threshold framework rather than a single $/kWh metric.

## 4. Model
(from figure captions) Revenue-maximising hybrid plant output; χ value as a function of storage size; value maps over energy cost × power cost compared with technology cost estimates. Formulation not read.

## 5. Data & processing
(from abstract) Historical wholesale prices and wind/solar generation for multiple U.S. locations; technology cost estimates for existing storage types.

## 6. Justification (why the authors argue the approach is valid)
Not assessable beyond abstract: claims location-invariance of optimal cost-improvement trajectories.

## 7. Key results
(from abstract)
- Some storage technologies already add value to solar and wind energy, but cost reduction is needed for widespread profitability.
- Optimal cost-improvement trajectories (balancing energy vs power cost) are relatively location-invariant → can guide industry/government R&D targets.

## 8. Limitations (stated + your critical reading)
Critical: price-taker value of co-located plants under historical prices; ignores system-level price feedback and ancillary services; value metric relative, not investment-grade.

## 9. Relevance to my study
Conceptual tool: separating **energy-capacity** from **power-capacity** cost when asking which market products (energy-heavy vs power-heavy) a battery should target; complements LCOS work (schmidt2019_lcos).

## 10. Lineage links
- Builds on: sioshansi2009_pjmvalue (arbitrage valuation tradition).
- Built upon by (notable): Ziegler et al. 2019 (Joule); junge2022_efficientstorage (energy vs power cost ratio drives duration).

## 11. Verification log
- OpenAlex + nature.com landing page: authors/affiliations, NCC 6(10):964–969, published 13 Jun 2016 (issue Oct 2016) ✔.
- SJR (id 21100198409) Q1 2016, 2024, 2025 ✔.
- Deep fields limited to abstract and figure captions; formulation and numbers NOT verified.
