---
id: gale2026_balancingbatteries
title: "Balancing with batteries: The impact of revenue stacking and skip rates on battery energy storage profitability in Great Britain"
authors: ["Gale, E.", "Schmidt, O.", "O'Cinneide, A.", "Johnson, N.", "Staffell, I."]
year: 2026
journal: "Journal of Energy Storage"
volume_issue_pages: "166:122328"
doi: "10.1016/j.est.2026.122328"
quartile: "Q1 (SJR 2025 = nearest available year; SJR 2026 not yet published. J. Energy Storage Q1 per staffell2016_maxvalue (Q1 2017–2025) and collath2022_agingreview (SJR 2025))"
quartile_basis: "nearest-year; rule=pass; SJR 2026 not yet published, nearest year 2025 = Q1 for J. Energy Storage (see staffell2016_maxvalue / collath2022_agingreview)"
group: "Iain Staffell, Centre for Environmental Policy, Imperial College London (with O. Schmidt, N. Johnson); industry co-authors at Gore Street Capital (Gale, O'Cinneide) and dvlp.energy (Schmidt)"
lineage: "Staffell/Imperial CEP line: staffell2016_maxvalue -> Schmidt & Staffell 2023 (OUP book, CANON) -> this paper and landy2026_hybridstacking. Model validated against the staffell2016 algorithm and EnergyStorage.ninja. Supervision (CRediT): Schmidt, O'Cinneide, Staffell supervised Gale."
streams: [S2_stacking_cooptimization, S7_market_design]
market_context: "GB wholesale (Elexon MID used as the 'day-ahead' price) + Balancing Mechanism approximated by the system (imbalance) price and NIV; 1 Jul 2020 – 30 Jun 2023, 30-min; no frequency response, reserve or Capacity Market"
method_class: "LP"
evidence_read: "full text (published CC BY version, PDF supplied by user 2026-10-13)"
oa_link: "https://doi.org/10.1016/j.est.2026.122328"
competitor: "C1 — closest Q1 competitor (see literature/WATCHLIST.md, docs/03_competitor_analysis_KO.md)"
---

## 1. Research question
How much more does a GB battery earn by stacking the Balancing Mechanism (BM) on top of wholesale arbitrage, and how much of that gain is lost to "skip rates" (being passed over despite offering the cheapest action) and to imperfect price capture under pay-as-bid?

## 2. Setting & assumptions
- **Markets**: wholesale (WS) and BM only. Frequency response, reserve products and the Capacity Market are explicitly left out (listed as future work).
- **Prices**: WS price = Elexon Market Index Price (ref. [63], i.e. MID, not a paid DA auction series). BM price = public marginal (system) price; BM volume and direction = net imbalance volume (ref. [64]).
- **BM representation**: in each SP the battery may only discharge into a short system (positive NIV) or charge from a long system (negative NIV), up to the size of the imbalance (an IF rule with three branches). The battery earns the **marginal** price → upper bound; pay-as-bid is handled only through a price-capture sensitivity.
- **Foresight**: perfect foresight over the whole period; price-taker.
- **Asset (base case)**: 100 MW / 100 MWh (1 h), round-trip efficiency 90.25% (95% × 95%), marginal cost £0.50/MWh for charge and discharge (degradation proxy), daily cycle limit 100 (non-binding).
- **Period**: 1 Jul 2020 – 30 Jun 2023, 30-min resolution (pre-EAC; spans the 2021–22 price crisis).

## 3. Constraints that drove the model choice
- "A small number of grid services" without non-linear constraints → LP is enough (GLOP via Google OR-Tools, Python). A faster solver (order of magnitude) was chosen to make multi-market optimisation tractable, at a 0.4–4% revenue deficit vs benchmark algorithms.
- No data on real battery BM bids → pay-as-bid cannot be modelled directly; replaced by a uniform discount on the BM price.
- No data on which periods batteries are skipped → skip rates modelled as random blocking of BM access.

## 4. Model
- Objective (Eq. 1): max Σ_t [net WS discharge × p^WS − WS discharge × MC + net BM discharge × p^BM − BM discharge × MC − gross WS charge × p^WS − WS charge × MC − gross BM charge × p^BM − BM charge × MC].
- Decision variables: energy charged/discharged in WS and in BM per SP (gross and net of losses).
- Key constraints: SoC balance with charge/discharge efficiencies; power and energy limits; daily cycle limit; BM direction and volume limited by NIV sign and size; WS-only run sets all BM terms to zero (baseline).
- **Skip rates**: Monte Carlo — BM participation blocked in a random share of periods, 5–95% in 5-pp steps, 50 runs per step. Std. dev. across runs ≈1.3% of mean.
- **Price capture**: BM price scaled by 50–100% to mimic bidding below the clearing price.
- Solver: GLOP (LP), OR-Tools.

## 5. Data & processing
- Elexon MID (WS), Elexon system price and NIV (BM), 30-min, Jul 2020 – Jun 2023. Correlation WS–BM price R = 0.79. BM prices more volatile with longer tails; volumes roughly normally distributed and stable over time.
- No forecasting, no train/test split (perfect foresight). Year 1 (Jun 2020 – Jun 2021) is pre-crisis; years 2–3 are crisis years.

## 6. Justification (why the authors argue the approach is valid)
- **Validation**: WS-only results within ±1% per month of the Staffell & Rustomji (2016) algorithm (−0.35% over H1 2023 at 100% efficiency; −0.86% at 90.25%); WS and BM results within −0.56% to −5.05% of EnergyStorage.ninja (H1 2023 and April 2023 worst month).
- Insensitivity to the degradation proxy (MC £0.50 → £5 cuts revenue £25k/MW/yr) is used to argue that a detailed SoC/temperature-dependent degradation model is unnecessary for the question.
- Monte Carlo spread of skip results is small (<1% normalised std. dev.), so revenue estimates are "robust" to which periods are skipped.

## 7. Key results
- **Stacking value**: WS + BM £166,123/MW/yr vs WS only £47,234/MW/yr (+252%), full period. The battery makes a net loss in WS but a larger profit in BM; BM provides 71% of revenue.
- **By year**: 2022–2023 £208–209k (WS + BM) vs £58–62k (WS only); 2021 £91k vs £26k. Revenue rises roughly logarithmically with monthly price standard deviation.
- **Volatility**: coefficient of variation of monthly returns 48% (WS + BM) vs 53% (WS only) → stacking diversifies.
- **Skip rates**: second-order polynomial; linearised, each +10 pp skip ≈ −£12k/MW/yr (≈ −7%). At 50% skip, WS + BM still earns +148% over WS only (£117k/MW/yr). Reducing skip from 90% to 80% raises lifetime present value by >23% (£117k/MW at 10% discount, £170k/MW at 4%; 15-yr life).
- **Price capture**: each 10% reduction in the BM bid relative to the marginal price → ≈9% lower annual revenue (range 50–100% capture).
- **Sensitivities**: RTE 100% → 75% cuts revenue 49% (WS + BM) vs 58% (WS only); cycle limit 1/day cuts revenue 60% (WS + BM) vs 28% (WS only), BM uplift falls from 252% to 94%; doubling energy capacity adds only ≈30% revenue (3 h: +50%, 4 h: +60% vs 1 h) — shorter durations most profitable per MWh because BM volumes are limited.
- **Reality check**: modelled ≈£200k/MW/yr (2023, WS + BM) vs Modo benchmark £101k/MW/yr from all sources (Jan–Aug 2023); BM was <1.5% of real battery revenue in 2023 because of skip rates (reported >90% for batteries).

## 8. Limitations (stated + critical reading)
- Stated: random (not process-driven) skip allocation; marginal price assumed (pay-as-bid only by sensitivity); data needs (10⁶–10⁷ points/day) for dispatch logs; proprietary bidding data unavailable; frequency response not included; no capital-cost or investor-return sizing.
- Critical reading:
  - **"BM" is really NIV-constrained imbalance-price trading**, not BOD/BOA-based BM participation. Earning the marginal system price on every MWh up to the full NIV is a strong upper bound; the NIV constraint allows one 100 MW battery to take the whole imbalance.
  - Skip modelled as share of time blocked = acceptance probability (1 − skip), uniform over time. This is the same simplification our design v0 used and that `docs/01_next_actions.md` M2 flagged; the authors themselves call for process-driven, rule-attributed analysis.
  - Pre-EAC, pre-30-min-rule, pre-OBP data (to Jun 2023); the rules analysed in our RQ2 (EAC, SoE, BR/QR/SR, GC0166) are outside the sample.
  - Revenue is extrapolated to a 15-yr lifetime from crisis-period prices (acknowledged as a thought experiment).

## 9. Relevance to my study
- **Closest competitor (C1)**, but the overlap is narrow: WS + BM only, pre-EAC, skip as a parameter. No ancillary services, no rule switches, no regime comparison, no Capacity Market.
- **Directly reusable**:
  - BM-as-NIV-constrained-imbalance formulation as a simple first BM layer (and as the benchmark our empirical acceptance model should improve on).
  - Validation design: compare against the staffell2016 algorithm / EnergyStorage.ninja and against the Modo benchmark.
  - Numbers for sanity checks: WS-only ≈£47k/MW/yr (2020–23 average), skip −£12k/MW/yr per 10 pp, price capture elasticity ≈0.9.
- **Corrects our earlier assumption**: Gale also used Elexon MID as the wholesale price, so results based on MID are directly comparable with Gale (design-review item M5 updated).
- Their concluding paragraph (§6) calls for "empirical research that can attribute skip rates and price capture to specific market conditions and rules" — a citable statement of our gap.

## 10. Lineage links
- Builds on: staffell2016_maxvalue; Schmidt & Staffell (2023, CANON); biggins2022_tradeornot; Biggins, Ejeh & Brown (2022) Energy Reports 8:10518 (aggregator, WS + BM); Pusceddu, Zakeri & Castagneto Gissey (2021) Applied Energy 283:116274 (arbitrage + FFR synergies; not archived); Hübscher et al. (2025, IEEE EEM conference; closest prior on skip rates, 9 months of 2023 data; WATCHLIST); Teng et al. (2015, ICE Energy); martins2021_ukbusinessmodels.
- Built upon by: landy2026_hybridstacking cites it (ref. 81) for probabilistic bid acceptance.

## 11. Verification log
- 2026-10-07: bibliographic data from search-engine results (pii S2352152X26019924).
- 2026-10-13: **full text read** from the published PDF supplied by the user (CC BY 4.0). Confirmed: J. Energy Storage 166 (2026) 122328, doi:10.1016/j.est.2026.122328; received 16 Jun 2025, accepted 19 Apr 2026, online 27 Apr 2026; affiliations as above. Data sources and period from §3.1; numbers from §4 and §6.
- References [41]–[45] were lost in text extraction; not needed for this entry.
