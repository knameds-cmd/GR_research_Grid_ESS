---
id: chen2022_misobatteryscuc
title: "Battery Storage Formulation and Impact on Day Ahead Security Constrained Unit Commitment"
authors: ["Chen, Y.", "Baldick, R."]
year: 2022
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "37(5):3995-4005"
doi: "10.1109/TPWRS.2022.3144241"
quartile: "Q1 (SJR 2022, Electrical & Electronic Engineering; Energy Engineering & Power Technology)"
group: "Yonghong Chen (MISO market engineering / HIPPO) with Ross Baldick (UT Austin)"
lineage: "ISO-practitioner + academic collaboration; advisor-student tie not applicable/verified."
streams: [S7_market_design]
market_context: "MISO day-ahead SCUC, storage participation model under FERC Order 841 (MO-managed SoC in clearing)"
method_class: "MILP (SCUC) - convex relaxation vs binary formulations"
evidence_read: "metadata + method description from the patent application with identical title (US 2023/0026455, Justia); journal full text not read"
oa_link: ""
---

## 1. Research question
How should battery storage (Order 841 electric storage resources) be formulated in an ISO's day-ahead security-constrained unit commitment so that charge/discharge exclusivity and SoC feasibility hold, the problem stays tractable at MISO scale, and pricing remains consistent? (from patent text / title)

## 2. Setting & assumptions
- MO-managed SoC within day-ahead SCUC; storage submits charge/discharge offers (prices C^p, C^g) with efficiency coefficients alpha, beta mapping MW to SoC.
- Deterministic day-ahead clearing on MISO-scale cases (largest DA SCUC instances; one battery per wind site in tests).

## 3. Constraints that drove the model choice
Mutually exclusive charging/discharging needs binaries (one per battery-interval) that slow very large SCUC MIPs; a convex relaxation is attractive but can produce simultaneous charge/discharge when prices are low/negative.

## 4. Model (per patent description)
- UCED (convex): no binaries; simultaneous charge/discharge can only clear if LMP <= (beta C^p - alpha C^g)/(beta - alpha) - theorems give necessary conditions.
- UCED_BIN: binary u_t with g_t <= g_bar u_t, p_t <= p_bar (1 - u_t).
- UCED_T: tightened SoC constraints s_{t-1} + alpha p_t <= s_bar, s_{t-1} - beta g_t >= s_min (valid inequalities) - guarantee exclusivity in some intervals without binaries.
- UCED_BIN_T: binaries + tightened SoC; warm start and lazy constraints for speed.

## 5. Data & processing
MISO production day-ahead SCUC cases prototyped in MISO's HIPPO platform (details not read).

## 6. Justification
Theorems on when relaxation is exact; computational comparisons of MIP solve times; production-cost impact of added batteries (from patent figures, not quantified here).

## 7. Key results
- Simultaneous charge/discharge under the convex form can only occur below a price threshold set by offers and efficiencies -> relaxation is often exact in practice.
- Tightened SoC inequalities plus lazy constraints keep solve times acceptable for MISO-scale SCUC with batteries.
- Numerical values not extracted (journal not read).

## 8. Limitations (stated + critical reading)
Deterministic DA clearing; MO-managed SoC assumes offers reflect true opportunity costs (cf. bhattacharjee2022_soemanagement on strategic SoE). Evidence here is from a patent text, not the paper.

## 9. Relevance to my study
Shows how an actual ISO operationalises SoC-aware clearing and the price conditions under which relaxations fail (negative/low prices) - relevant when a simulator lets the "market" manage SoC vs the battery self-scheduling. Contrast with GB/EU self-dispatch (portfolio bidding) where SoC is never in the clearing problem.

## 10. Lineage links
- Builds on: FERC Order 841; jiang2023_isodispatch (theory of MO dispatch, later).
- Built upon by (notable): Chen & Tong (Cornell) SoC-dependent bid convexification, IEEE TPWRS letter (IEEE Xplore 10037211; arXiv 2209.02107) - title verified, venue details not verified.

## 11. Verification log
- doi.org/10.1109/TPWRS.2022.3144241 resolves to IEEE Xplore document 9684952, whose title matches (search listing); full citation (vol 37, no 5, pp 3995-4005, 2022) from the reference list of an LBNL preprint (Moreira et al. 2024, eScholarship) - second-hand; IEEE page itself not readable (JS).
- SJR: scimagojr sourceid 28825, Q1 2022.
- Method content from US patent application 20230026455 (same title; MISO HIPPO); journal full text not read.
- 2026-10-06 independent verifier: citation now confirmed first-hand - OpenAlex lists Chen, Yonghong; Baldick, Ross; IEEE Trans. Power Systems 37(5):3995-4005, 2022 (https://api.openalex.org/works/doi:10.1109/TPWRS.2022.3144241). No change needed.
