---
id: pandzic2013_vppoffer
title: "Offering model for a virtual power plant based on stochastic programming"
authors: ["Pandžić, H.", "Morales, J. M.", "Conejo, A. J.", "Kuzle, I."]
year: 2013
journal: "Applied Energy"
volume_issue_pages: "105:282-292"
doi: "10.1016/j.apenergy.2012.12.077"
quartile: "Q1 (SJR 2024, Applied Energy; Q1 in Building & Construction, Mechanical Eng., Energy (misc.), Management/Monitoring/Policy & Law)"
quartile_basis: "latest-only; rule=unchecked; SJR 2013 (publication year) not checked — only later years"
group: "Conejo (UCLM) with Morales (DTU) and Kuzle (Univ. of Zagreb)"
lineage: "OpenAlex affiliations: Pandžić (Univ. of Washington at publication), Morales (DTU), Conejo (UCLM), Kuzle (Zagreb). Morales = former Conejo PhD student at UCLM (widely documented; not re-verified). Pandžić later joined Kirschen's UW group (affiliation consistent)."
streams: [S3_bidding_uncertainty]
market_context: "Day-ahead + balancing market; VPP = wind + pumped-hydro storage + dispatchable plant (keywords: pumped hydro storage, wind)"
method_class: "SP"
evidence_read: "abstract + keywords only (IDEAS/RePEc record); full text closed"
oa_link: ""
---

## 1. Research question
How should a virtual power plant combining an intermittent source, a storage facility and a dispatchable plant offer into day-ahead and balancing markets to maximise expected profit?

## 2. Setting & assumptions
- VPP portfolio: intermittent (wind) + storage (pumped hydro) + dispatchable unit (from abstract/keywords).
- Markets: day-ahead and balancing (from abstract).
- Uncertainty handled by stochastic programming (from abstract); specific uncertain parameters (wind, DA price, balancing price) and scenario counts not verified.
- Price-taker vs. maker: not verified.

## 3. Constraints that drove the model choice
(from abstract) Need for "mathematical rigor and computational efficiency"; SP chosen to keep a tractable MILP. Details not verified.

## 4. Model
- Objective: expected profit over DA + balancing (from abstract).
- Decision structure: DA offers as first stage, balancing as recourse is the standard Conejo-school structure, but not verified in this paper's text.
- Risk measure: not verified.

## 5. Data & processing
Not verified.

## 6. Justification
Not verified.

## 7. Key results
Not verified.

## 8. Limitations (stated + critical reading)
- Critical: VPP-level aggregation hides individual storage bidding logic; two-stage DA/balancing structure ignores intraday trading and multi-day SoC value (cf. lohndorf2023_coordination).

## 9. Relevance to my study
Represents the Conejo/Morales two-stage DA-balancing offering template with storage inside a portfolio — reference point for "storage behind a VPP/aggregator" bidding in Nordic/GB balancing contexts.

## 10. Lineage links
- Builds on: conejo2002_pricetaker; Morales, Conejo & Pérez-Ruiz (2010) wind short-term trading (not in archive).
- Built upon by: VPP/aggregator SP offering literature (not catalogued here).

## 11. Verification log
- OpenAlex works/doi:10.1016/j.apenergy.2012.12.077 → title, 4 authors + affiliations, vol 105 pp 282-292, 2013.
- IDEAS/RePEc a/eee/appene/v105y2013icp282-292 → abstract, keywords.
- SJR: Applied Energy source id 28801, Q1 2023 & 2024 in all categories.
- Full text not read: formulation details deliberately left unverified.
