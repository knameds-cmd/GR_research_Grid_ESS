---
id: brown2024_reliabilitybattery
title: "The value of electricity reliability: Evidence from battery adoption"
authors: ["Brown, D. P.", "Muehlenbachs, L."]
year: 2024
journal: "Journal of Public Economics"
volume_issue_pages: "239:105216"
doi: "10.1016/j.jpubeco.2024.105216"
quartile: "Q1 (SJR 2024 and 2025, Economics and Econometrics; Finance)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "David P. Brown (Univ. of Alberta, Canada Research Chair in Energy Economics) and Lucija Muehlenbachs (Univ. of Calgary; RFF)"
lineage: "Not verified."
streams: [S8_empirical_econ]
market_context: "California residential solar and solar-plus-storage; PG&E/IOU Public Safety Power Shutoff (PSPS) outages 2013-2020"
method_class: "econometric (event-study DiD + dynamic discrete choice, nested fixed point)"
evidence_read: "full text (RFF WP 23-10 https://media.rff.org/documents/WP_23-10.pdf); published numbers taken from journal abstract"
oa_link: "https://media.rff.org/documents/WP_23-10.pdf"
---

## 1. Research question
What is households' willingness to pay for reliability (value of lost load, VoLL), revealed by battery adoption after wildfire-prevention outages?

## 2. Setting & assumptions
- Key insight: solar-only systems do not avert outages; solar-plus-storage does -> differential response identifies reliability value.
- Zip-code panel; outages assigned from feeder data via population grid.

## 3. Constraints that drove the model choice
Stated-preference VoLL is unreliable; PSPS outages are driven by weather/fire-risk indices, giving quasi-exogenous variation; adoption is a forward-looking, irreversible choice with falling costs and subsidies -> dynamic discrete choice to recover WTP in $/MWh.

## 4. Model
- Event study: storage adoption on customer-outage hours with leads/lags (-12..+8 months), zip FE, month-year FE, quadratic zip trends; solar-only adoption as placebo outcome.
- Dynamic discrete choice (none / solar / solar+storage), payoff = bill savings - net capex - unobserved cost + phi * expected outage MWh averted (storage only); AR(1) state transitions; ML with beta = 0.869; heterogeneity by income quartile.

## 5. Data & processing
CPUC de-energization database (PSPS, Oct 2013-Sep 2020); California DG interconnection data (Jan 2014-Jun 2020); SGIP battery cost data; tariffs; NREL irradiance; Census.

## 6. Justification
Placebo (solar-only shows no response), alternative trends, weighting schemes, continuous vs discrete treatment, Goodman-Bacon decomposition (positive weights), storage add-ons check.

## 7. Key results
- Storage capacity +45% in treated zip codes (WP); responses concentrated in high-income zips.
- Published VoLL ~ $4,980/MWh (journal abstract; WP: mean $4,292/MWh, range $2,477-5,239 by income quartile).
- Residential losses from PSPS outages ~ $406m (journal abstract; WP $322m for 2018-2019).

## 8. Limitations (stated + critical reading)
- Zip-level exposure; omitted alternative defensive spending (generators) -> lower bound; assumes batteries fully avert outages; behind-the-meter, not wholesale-market behaviour.

## 9. Relevance to my study
Not a bidding paper, but (i) a clean revealed-preference + event-study design built on a technology contrast (storage vs non-storage units) — the analogue of a battery-vs-non-battery DiD in GB balancing services; (ii) gives an empirical VoLL anchor relevant for scarcity pricing / reserve valuation in market-design counterfactuals.

## 10. Lineage links
- Builds on: dynamic adoption models (e.g., De Groote & Verboven 2019 AER on solar subsidies — related, not verified as cited); VoLL literature.
- Built upon by: not checked.

## 11. Verification log
- RePEc IDEAS: JPubE vol 239, 2024, DOI 10.1016/j.jpubeco.2024.105216, authors Brown & Muehlenbachs.
- SJR JPubE sourceid 29009: Q1 2024, 2025.
- Full text: RFF WP 23-10 (Apr 2023); published estimates differ (VoLL $4,980/MWh, $406m) — use published values when citing.
