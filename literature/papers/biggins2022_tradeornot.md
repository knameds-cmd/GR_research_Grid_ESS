---
id: biggins2022_tradeornot
title: "To trade or not to trade: Simultaneously optimising battery storage for arbitrage and ancillary services"
authors: ["Biggins, F. A. V.", "Homan, S.", "Ejeh, J. O.", "Brown, S."]
year: 2022
journal: "Journal of Energy Storage"
volume_issue_pages: "50:104234"
doi: "10.1016/j.est.2022.104234"
quartile: "Q1 (SJR 2025, Energy Engineering and Power Technology; Renewable Energy, Sustainability and the Environment; Electrical and Electronic Engineering)"
quartile_basis: "pub-year; rule=pass; SJR 2022 Q1 for this journal recorded in staffell2016_maxvalue"
group: "Solomon Brown, Dept. of Chemical & Biological Engineering, University of Sheffield"
lineage: "Sheffield process-systems/energy group of S. Brown. Biggins and Homan = Brown's doctoral researchers (per affiliation and authorship pattern; not verified on a thesis page)."
streams: [S2_stacking_cooptimization, S6_ancillary_products]
market_context: "GB: monthly Firm Frequency Response (dynamic FFR) tenders in EFA blocks + N2EX day-ahead arbitrage (pre-2021 FFR regime)"
method_class: "MILP"
evidence_read: "full text (White Rose accepted manuscript, https://eprints.whiterose.ac.uk/id/eprint/183597/1/To_Trade_or_Not_to_Trade_JoES_Resubmit.pdf)"
oa_link: "https://eprints.whiterose.ac.uk/183597/"
---

## 1. Research question
How much can a GB battery earn by doing day-ahead arbitrage around its FFR commitments? How biased are revenue estimates that assume every FFR tender is accepted?

## 2. Setting & assumptions
- Price-taker with deterministic DA prices (perfect foresight within the month). FFR tender outcomes for the month are treated as known when arbitrage is optimised, since results are published before delivery.
- Uncertainty is in **tender acceptance**. This is predicted with ML classifiers and propagated through 500 Monte Carlo scenarios (8 acceptance outcomes over three EFA-block bid parts).
- Hourly resolution, one-month horizon. Real-time check by replaying 1 s GB frequency.
- Asset: about 4 MW / 2 MWh as extracted. Usable SoC 20–100%, η = 90% per direction. No degradation.
- Market: FFR availability fee per hour over EFA blocks. Delivery is required at full power for deviations >0.5 Hz and at P/2.5 for 0.2–0.5 Hz, with a 30-min sustained-delivery requirement.

## 3. Constraints that drove the model choice
- Acceptance outcomes are binary and month-ahead.
- Delivery must be guaranteed for up to 30 min. That requires SoC margins, plus binary flags for when arbitrage eats into the reserved band (penalised as expected loss of availability fee).

## 4. Model
- Objective (per scenario n): min $\sum_t p^{DA}_t(P^c_{nt}-P^d_{nt}) + \lambda_{nt} t_{nt}(\alpha_{nt}\rho_{0.5}+\beta_{nt}\rho_{0.2})$. The second term is the risk-weighted loss of availability fee when the SoC margin is breached.
- **SoE / energy reservation (rule-derived):** $\underline X + P^n/2 \le X_{nt} \le \overline X - P^n/2$ reserves energy for a 30-min full-power call. A tighter band applies when only the low-deviation response (P/2.5) is reserved.
- **Capacity split: fixed by tender outcome** (EFA-block level). Arbitrage uses whatever SoC range is left, hourly.
- **Frequency-signal energy: expected utilisation.** Probabilities ρ0.2 = 0.8 and ρ0.5 = 0.2 come from GB event statistics. Feasibility is then checked by replaying actual 1 s frequency.
- ML: tender acceptance predicted by multinomial Naive Bayes (also tested: DT, RF, kNN, NN). Features are EFA-block availability and the availability-fee-to-power ratio; monthly accuracy is 0.50–0.78.

## 5. Data & processing
- National Grid ESO FFR tender reports (May 2018 – Feb 2020).
- N2EX day-ahead prices.
- NGESO 1 s frequency data.
- Event statistics from GB frequency data 2014–2018.
- Classifier trained on earlier months and tested month-ahead.

## 6. Justification (why the authors argue the approach is valid)
- The Monte Carlo ensemble gives the distribution of income.
- The real-time replay shows that FFR obligations are honoured even while arbitraging.
- Sensitivity on the ρ weights.

## 7. Key results
- Ignoring tender-acceptance uncertainty overestimates mean expected income by about 28%.
- Best case (all bids accepted): about £7.0–9.1k per month of FFR income for 1–1.5 MW. Probabilistic mean: about £5.0–6.5k per month.
- Arbitrage adds about £1.4–1.6k per month under tight SoC bands. FFR remains available about 81% of hours when arbitraging under the expected-utilisation weights.

## 8. Limitations (stated + your critical reading)
- Stated: deterministic arbitrage prices; no degradation; constant event probabilities; classifier drift.
- Critical reading:
  - The FFR regime studied has since been replaced by DC/DM/DR, which have explicit SoE-management rules and EFA-block day-ahead auctions. The numbers are historical.
  - The battery parameters as extracted should be re-checked against the PDF.

## 9. Relevance to my study
- A clear example of a product rule (sustained-delivery duration) being encoded as an SoC margin that directly limits stacking.
- The acceptance-risk layer (classifier plus scenarios) is a reusable idea for auction-based products.
- Useful GB pre-2021 baseline for a before/after comparison of rule changes.

## 10. Lineage links
- Builds on: GB FFR battery studies; Moreno 2015 (moreno2015_multiservicemilp) for GB multi-service MILP.
- Built upon by (notable): later GB revenue-stacking work under the Dynamic Containment suite (S6; e.g., cao2024_dcvsefr for the DC product itself).

## 11. Verification log
- White Rose Research Online record 183597: authors, J. Energy Storage 50, 104234, 2022, DOI.
- Accepted manuscript read through text extraction. The battery rating and power/energy ratio as extracted look internally inconsistent; check the PDF Table 1 before reuse.
- SJR (id 21100400826): Q1 2025 in all three categories.
- Crossref lookup not performed (rate limit); repository metadata used.
