---
id: perez2016_degradationmultiservice
title: "Effect of Battery Degradation on Multi-Service Portfolios of Energy Storage"
authors: ["Perez, A.", "Moreno, R.", "Moreira, R.", "Orchard, M.", "Strbac, G."]
year: 2016
journal: "IEEE Transactions on Sustainable Energy"
volume_issue_pages: "7(4):1718-1729"
doi: "10.1109/TSTE.2016.2589943"
quartile: "Q1 (SJR 2025, Renewable Energy, Sustainability and the Environment)"
group: "Goran Strbac (Imperial College London) with Marcos Orchard & Rodrigo Moreno (Universidad de Chile)"
lineage: "Imperial–U. Chile collaboration. Direct extension of moreno2015_multiservicemilp (same Moreno/Moreira/Strbac core) adding Orchard's (U. Chile) battery-prognostics degradation modelling. Pérez affiliated with U. Chile EE (OpenAlex); advisor tie not verified."
streams: [S2_stacking_cooptimization, S4_degradation_operation]
market_context: "Great Britain: balancing-market services + DNO (distribution network) services in a multi-service portfolio (from abstract)"
method_class: "MILP"
evidence_read: "abstract only (OpenAlex, paraphrased by tool); full text not accessible"
oa_link: ""
---

## 1. Research question
In a storage multi-service portfolio, how do battery degradation and operating strategies that mitigate it (notably SoC limits) trade off near-term revenue against lifetime and lifetime value? Which services are most affected? (from abstract)

## 2. Setting & assumptions
(from abstract)
- Multi-service portfolio of balancing-market and DNO services in GB.
- An integrated economic–degradation framework that includes ambient-temperature effects.
- Price, foresight and resolution assumptions not read.

## 3. Constraints that drove the model choice
(from abstract) Some services accelerate wear, so degradation must be co-evaluated with portfolio revenue.

## 4. Model
- (from abstract) Couples the multi-service portfolio optimisation (MILP lineage of moreno2015_multiservicemilp) with a degradation model. SoC-window constraints are the main lever.
- The method class is assumed from the lineage and is not confirmed.
- Capacity split, reserve-energy modelling: not read.

## 5. Data & processing
GB case studies (from abstract); details not read.

## 6. Justification (why the authors argue the approach is valid)
Not read.

## 7. Key results
(from abstract)
- Degradation-reducing SoC strategies lower short-term earnings but usually increase long-term (lifetime) value by extending battery life.
- Degradation mainly affects balancing-oriented services rather than DNO services, which are a smaller share of revenue.

## 8. Limitations (stated + your critical reading)
- Not read.
- Critical reading: SoC limits chosen for ageing interact directly with SoE rules imposed by frequency products. The paper treats them as an operator choice, not a regulatory constraint.

## 9. Relevance to my study
- Shows that **SoC-window constraints have a revenue-vs-lifetime price**. The same mechanism is behind regulatory SoE requirements.
- Bridges stacking and degradation (cross-ref S4).

## 10. Lineage links
- Builds on: moreno2015_multiservicemilp.
- Built upon by (notable): not checked. Related: mirzaeialavijeh2025_swedenfcrstacking (stacking + ageing), collath2023_lifetimeprofit (S4).

## 11. Verification log
- Crossref (api.crossref.org/works/10.1109/TSTE.2016.2589943): title, authors (Aramis Perez et al.), vol 7, issue 4, pp. 1718–1729, Oct 2016. Confirmed.
- OpenAlex affiliations confirmed (U. Chile; Imperial).
- SJR (id 19700177027): Q1 2025.
- Full text not accessed. All deep fields abstract-level.
