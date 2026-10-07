---
id: kazemi2017_jointenergyancillary
title: "Operation Scheduling of Battery Storage Systems in Joint Energy and Ancillary Services Markets"
authors: ["Kazemi, M.", "Zareipour, H.", "Amjady, N.", "Rosehart, W. D.", "Ehsan, M."]
year: 2017
journal: "IEEE Transactions on Sustainable Energy"
volume_issue_pages: "8(4):1726-1735"
doi: "10.1109/TSTE.2017.2706563"
quartile: "Q1 (SJR 2025, Renewable Energy, Sustainability and the Environment)"
quartile_basis: "latest-only; rule=unchecked; SJR 2017 (publication year) not checked — only later years"
group: "Hamidreza Zareipour & William Rosehart, University of Calgary (with N. Amjady, Semnan; M. Ehsan, Sharif)"
lineage: "Zareipour group (Calgary). Kazemi's affiliation in OpenAlex is Islamic Azad Univ. Shahreza. Kazemi's advisor relationship was not verified."
streams: [S2_stacking_cooptimization, S3_bidding_uncertainty]
market_context: "Day-ahead energy + spinning reserve + regulation (case-study market not confirmed)"
method_class: "RO"
evidence_read: "abstract only (OpenAlex abstract); full text not accessible"
oa_link: ""
---

## 1. Research question
How should a merchant battery schedule participation across day-ahead energy, spinning reserve and regulation markets jointly, while managing the risk from uncertain prices and uncertain energy commitments (deployment of reserves)? (from abstract)

## 2. Setting & assumptions
(from abstract)
- Uncertain forecast prices and uncertain energy commitments (reserve and regulation deployment), described with a **non-probabilistic** (uncertainty-set) model.
- Risk is controlled through the size of the uncertainty set.
- Resolution, horizon and battery parameters were not read.

## 3. Constraints that drove the model choice
(from abstract) No reliable probability distributions for prices and deployments, hence a robust max-min formulation. Tractability is obtained through duality and linearisation.

## 4. Model
- (from abstract) Max-min profit problem over energy, spinning reserve and regulation, converted to an equivalent single-level maximisation through duality theory and linearisation (giving a MILP/LP).
- **Reserve/regulation energy: robust (worst-case within the uncertainty set) energy commitments** (from abstract).
- Capacity split and SoC details: not read.

## 5. Data & processing
Not read (the abstract mentions a case study).

## 6. Justification (why the authors argue the approach is valid)
Case-study validation (from abstract); details not read.

## 7. Key results
Not read.

## 8. Limitations (stated + your critical reading)
Not read. Critical reading: robust worst-case deployment can be very conservative. The outcome depends on how the uncertainty budget is calibrated, which is where product delivery rules (duration and energy requirements) would enter.

## 9. Relevance to my study
- A representative **robust** co-optimisation of energy, spinning reserve and regulation from a renowned group. It is the methodological opposite of expected-value deployment.
- Useful as a reference for "worst-case deployment" treatment when comparing reservation rules.

## 10. Lineage links
- Builds on: robust optimisation for market offering; storage bidding literature (S3). Reference list not read.
- Built upon by (notable): later robust/DRO storage bidding (not itemised; see S3).

## 11. Verification log
- doi.org resolves 10.1109/TSTE.2017.2706563 to IEEE Xplore document 7932132.
- OpenAlex (api.openalex.org/works/doi:10.1109/TSTE.2017.2706563): authors, institutions, vol 8, issue 4, pp. 1726–1735, 2017.
- Crossref lookup rate-limited (not completed).
- SJR (id 19700177027): Q1 2025.
- Full text not accessed. All deep fields are abstract-level. Note: the OpenAlex abstract was returned through a summariser, so its wording is a paraphrase.
