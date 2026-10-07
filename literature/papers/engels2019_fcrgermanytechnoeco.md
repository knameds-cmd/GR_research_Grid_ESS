---
id: engels2019_fcrgermanytechnoeco
title: "Techno-economic analysis and optimal control of battery storage for frequency control services, applied to the German market"
authors: ["Engels, J.", "Claessens, B.", "Deconinck, G."]
year: 2019
journal: "Applied Energy"
volume_issue_pages: "242:1036-1049"
doi: "10.1016/j.apenergy.2019.03.128"
quartile: "Q1 (SJR 2019, Energy Engineering and Power Technology)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Geert Deconinck, KU Leuven ELECTA / EnergyVille; industry co-author Bert Claessens (REstore NV)"
lineage: "Engels affiliated with KU Leuven + EnergyVille + REstore (industry-academic PhD under Deconinck, inferred from affiliations; thesis not checked). Same team: Engels et al. IEEE TSG 2020 FCR + peak shaving (not archived here)."
streams: [S6_ancillary_products]
market_context: "German FCR (Regelleistung.net weekly auction, pay-as-bid, 2014-2017 rules)"
method_class: "stochastic SAA + chance constraint, solved with differential evolution over controller and sizing parameters"
evidence_read: "full text (arXiv 1903.04251, https://arxiv.org/pdf/1903.04251)"
oa_link: "https://arxiv.org/abs/1903.04251"
---

## 1. Research question
What battery size and FCR controller parameters maximise lifetime NPV of a BESS selling German FCR, accounting for degradation, recharging costs and the TSO penalty/compliance rules?

## 2. Setting & assumptions
- FCR rules: full activation at ±200 mHz; ±10 mHz deadband; 30 s to full activation; 30-min energy criterion in both directions; up to 20% over-fulfilment; recharge by 15-min intraday blocks with 5-min lead time in 100 kW steps; weekly auction, pay-as-bid (weighted-average price assumed).
- Price-taker, 1 MW bid; FCR price scenarios (moderate/low, exponential decline).
- NMC cell (Sanyo UR18650E) first-order RC model; SMA inverter efficiency curve; HVAC thermal model (COP 2.5); calendar ageing ∝ t^0.75 (SoC, T) and cycle ageing ∝ √throughput (Schmalstieg model) with rainflow.

## 3. Constraints that drove the model choice
Penalty risk (insufficient energy) is a rare-event, non-convex function of controller parameters and stochastic frequency → chance-constrained SAA with gradient-free optimiser; full electro-thermal-ageing simulation needed for lifetime costs.

## 4. Model
- Controller (discretised P-control): gain K_p, SoC set-point SoC_0, controller deadband db_p, over-delivery share o_a; SoC restored by reserved recharge power and by over-delivery.
- Objective: min discounted lifetime cost (− FCR revenue + electricity cost + degradation capital loss).
- Chance constraint: Pr{penalty>0} ≤ 0.005 at 99.9% confidence (binomial bound).
- Sizing: P_BESS ≥ 1.25 r; E range 1.0–2.5 MWh per 1 MW FCR; C-rate 0.6–1.5.
- Solver: SAA with Monte-Carlo day samples (50 per iteration) + differential evolution.

## 5. Data & processing
Continental Europe frequency 2014–2017 at 10-s resolution; 140,256 one-day samples built by 15-min rolling windows. FCR prices Regelleistung 2014–2017; intraday and imbalance prices.

## 6. Justification
SAA optimality gap estimates; penalty constraint with statistical confidence; component models validated separately.

## 7. Key results
- Optimal: 1.6 MW / 1.6 MWh per 1 MW FCR (C-rate 1.0); lifetime 10.8 y to 80% capacity.
- Payback (moderate price scenario): 3.6 y at 300 €/kWh, 5.3 y at 400 €/kWh, 7.1 y at 500 €/kWh.
- Calendar ageing dominates (~70–80% of capacity loss); cycle ageing minor.
- Electricity (recharge) costs only 0.94–2.97% of revenue (German exemptions).
- Profitable only if costs low enough or FCR prices do not decline too much.

## 8. Limitations (stated + your critical reading)
Combined model not validated on a real FCR battery; no global optimality; price-taker single 1 MW bid; 2014–2017 rules (pre-15-min criterion, pre-daily 4-h auctions with marginal pricing); FCR only (no stacking).

## 9. Relevance to my study
Best quantitative link between specific FCR rule parameters (30-min criterion → energy; 1.25 r power → over-fulfilment headroom; intraday lead time/granularity → recharge) and optimal P/E sizing. The "kink" at 1.6 MWh shows sizing is set by the compliance (penalty) constraint, not economics — a rule-attribution result. Controller parametrisation is a good RL baseline.

## 10. Lineage links
- Builds on: oudalov2007_pfcsizing; thien2017_fcrgermanystrategy; Schmalstieg et al. ageing model.
- Built upon by (notable): Engels et al. 2020 IEEE TSG (FCR + peak shaving, S2 territory).

## 11. Verification log
- OpenAlex works/doi:10.1016/j.apenergy.2019.03.128: 242:1036-1049; authors/affiliations (KU Leuven ELECTA, EnergyVille, REstore). IDEAS RePEc abstract.
- SJR sid 28801: Applied Energy Q1 2019.
- Full text read via arXiv 1903.04251 (preprint of the journal paper).
