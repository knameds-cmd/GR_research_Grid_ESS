---
id: cao2024_dcvsefr
title: "Battery energy storage systems providing dynamic containment frequency response service"
authors: ["Cao, X.", "Engelhardt, J.", "Ziras, C.", "Marinelli, M.", "Zhao, N."]
year: 2024
journal: "International Journal of Electrical Power & Energy Systems"
volume_issue_pages: "162:110288"
doi: "10.1016/j.ijepes.2024.110288"
quartile: "Q1 (SJR 2024, Electrical and Electronic Engineering; Energy Engineering and Power Technology)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Mattia Marinelli, DTU Wind and Energy Systems (Distributed Energy Systems); with Nan Zhao, Lancaster University"
lineage: "DTU Marinelli group (Engelhardt, Ziras co-authors also on engelhardt2022_fcrnrecovery). Cao listed at DTU (OpenAlex); supervision tie not verified."
streams: [S6_ancillary_products]
market_context: "GB Dynamic Containment (DC/DCFR) vs Enhanced Frequency Response (EFR)"
method_class: "closed-loop simulation + root-locus stability analysis"
evidence_read: "abstract only (DTU Orbit, Lancaster portal, DOAJ, OpenAlex); full text OA but PDFs blocked to fetcher"
oa_link: "https://orbit.dtu.dk/en/publications/battery-energy-storage-systems-providing-dynamic-containment-freq/"
---

## 1. Research question
How do BESS providing GB Dynamic Containment perform in frequency regulation and SoC management, what configuration limits apply, and how does DC compare with the earlier EFR service? (from abstract)

## 2. Setting & assumptions
- GB power system model with BESS fleet providing DCFR.
- DC SoC management under the ESO "recovery rules" (baseline/SoC management) — specific parameters not verified from full text.
- Factors studied: C-rate, SoC range, SoC-management time delay, imbalance estimation.

## 3. Constraints that drove the model choice
DC SoC management acts with a delay (baseline notified ahead of settlement periods), creating a feedback loop between frequency, SoC and SoC-management power → stability analysis (root locus) needed.

## 4. Model
Closed-loop frequency model with BESS DC droop + SoC-management loop; root-locus analysis of the loop; imbalance estimation from frequency data (from abstract).

## 5. Data & processing
GB frequency data (source/period not verified).

## 6. Justification
Stability analysis plus time-domain simulation; comparison with EFR on frequency quality, SoC level and degradation.

## 7. Key results
- Improper SoC management in DC can produce SoC oscillation that degrades performance.
- With proper configuration (C-rate, SoC range, management delay) DC "offers more favorable outcomes than EFR in terms of frequency quality, SOC levels, and battery degradation" (abstract).
- Numerical values not verified.

## 8. Limitations (stated + your critical reading)
- Technical focus; no market revenue analysis.
- Results tied to the 2020–2023 DC rule set; ESO changed SoC/baseline rules repeatedly (2022 SoE rules, 2023 DM/DR launch).

## 9. Relevance to my study
Shows that the *timing* of permitted SoC recovery (baseline lead time) is a rule parameter with dynamic consequences (oscillation) — relevant if the RL agent learns recovery baselines under DC rules. Supports DC-vs-EFR comparison of rule design.

## 10. Lineage links
- Builds on: greenwood2017_efrservicedesign, gundogdu2018_efrtriad, lee2019_closedloopgb; engelhardt2022_fcrnrecovery (same DTU group, Nordic recovery strategies).
- Built upon by: —

## 11. Verification log
- DTU Orbit, Lancaster portal, OpenAlex works/doi:10.1016/j.ijepes.2024.110288: title, 162:110288, authors; DTU affiliations for Cao/Engelhardt/Ziras/Marinelli, Zhao at Lancaster.
- SJR sid 17985: IJEPES Q1 2024.
- Full text NOT read (orbit.dtu.dk and research.lancaster-university.uk PDFs returned 403; ScienceDirect robots-blocked).
