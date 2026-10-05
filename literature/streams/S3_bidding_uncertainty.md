# S3 — Bidding / offering strategies for storage under price uncertainty

Scope: how a storage (or closely related flexible) unit should turn uncertain price information into market bids — stochastic programming (SP), robust optimisation (RO), stochastic/approximate dynamic programming (SDP/ADP), price-maker bilevel/MPEC models, and how each treats information structure, non-anticipativity, scenarios, risk, and bid-curve format.
RL bidders → S5; multi-service co-optimisation → S2; degradation → S4; market design → S7.

## 1. Overview
Four method families coexist, separated mainly by **what the bidder is assumed to know at bid time** and **whether its bids move prices**:

1. **Two-stage / multistage SP (price-taker)** — Conejo school. First-stage DA offers are non-anticipative; balancing/RT is recourse per scenario. Bid curves are built from scenario solutions (conejo2002_pricetaker, pandzic2013_vppoffer, krishnamurthy2018_dart). kim2021_vss shows the limits: for a price-taker with full RT flexibility the value of the stochastic solution is **exactly zero**; VSS > 0 only with restricted RT re-trading (γ < 1), price impact, or risk aversion. Measured VSS ≤ 2 % in PJM.
2. **RO** — confidence intervals instead of scenarios; nested intervals give the price points of an offer curve (baringo2011_robustoffer). For storage the worst case is ill-defined hour-by-hour (charge vs discharge hours have opposite worst cases), which is one reason RO storage papers mostly concern scheduling or energy+reserve feasibility (kazemi2017_jointenergyancillary, filed by S2) rather than price-curve bidding.
3. **SDP / ADP / SDDP (value-function bidding)** — the bid is a by-product of the marginal value of stored energy. Hydro OR line: lohndorf2013_addp (SDDP cuts + Markov price states; 4-segment monotone DA bid curves per hour) → lohndorf2023_coordination (DA auction + continuous intraday; information-relaxation upper bounds). Battery line: jiang2015_hourahead (Monotone-ADP; two-threshold hour-ahead bid placed without knowing start-of-hour SoC) → zheng2022_asdp (analytical SDP, sub-second, 22 Markov price nodes, SoC-dependent efficiency) → baker2024_transferablebidder (S5; NN predicts the value function → SoC-segmented bids). European DA+ID: finnah2022_dpid.
4. **Price-maker bilevel / MPEC** — ruiz2009_mpecoffer template (KKT + strong duality + big-M → MILP) applied to storage: mohsenianrad2016_pricemaker (multi-unit nodal; economic price-quantity bids beat self-schedule only under uncertainty), wang2017_lookahead (terminal-SoC look-ahead), nasrolahpour2018_bilevel (DA energy + reserve + balancing; 16 reduced scenarios; ~15 % profit cost of per-scenario SoC feasibility), tomasson2020_offerbid (portfolio; withholding behaviour; custom B&B). Scenario counts stay tiny (3–16) because each scenario duplicates the lower-level KKT system.

**Cross-cutting design dimensions**

| Dimension | Range in this stream |
|---|---|
| Information at bid time | full price-response (zheng2022_asdp) → hour-ahead without SoC knowledge (jiang2015_hourahead) → day-ahead 24-h curve (lohndorf2013_addp, pandzic2013_vppoffer, nasrolahpour2018_bilevel) |
| Non-anticipativity | explicit DA variables without scenario index (mohsenianrad2016_pricemaker, nasrolahpour2018_bilevel, kim2021_vss); implicit via value function/state (SDP papers) |
| Scenario generation | ad-hoc perturbation K = 3 (mohsenianrad2016) → normal wind errors 1,000 → backward reduction 16 (nasrolahpour2018) → regression + SARIMA Monte Carlo 100 (kim2021) → econometric Markov chain + LHS, 20/state (lohndorf2013) → empirical Markov transition counts (zheng2022) |
| Risk measure | almost always risk-neutral in the verified full texts; CVaR not used in any full text read here |
| Bid format | two thresholds (jiang2015); monotone piecewise-linear, I = 3 breakpoints at equal-scenario-mass prices (lohndorf2013); one price-quantity block per product-hour (nasrolahpour2018, mohsenianrad2016); discretised price grid (tomasson2020); SoC-segmented (baker2024) |
| Computational limit cited | MPEC: binaries/big-M grow with scenarios; SDP: state explosion (282k exogenous states in lohndorf2013; 3.6 M post-decision states in jiang2015); answer = relaxation bounds, monotone projection, analytical value-function updates |

## 2. Chronological lineage
- **2002** conejo2002_pricetaker — price pdfs → self-schedule → bid rule (UCLM root).
- **2009** ruiz2009_mpecoffer — MPEC offering with endogenous LMPs (UCLM).
- **2011** baringo2011_robustoffer — RO offer curves from nested confidence intervals (UCLM).
- **2013** pandzic2013_vppoffer — SP offering of wind + pumped storage VPP, DA + balancing (Conejo/Morales).
- **2013** lohndorf2013_addp — ADDP for hydro storage DA bid curves; UB/LB certification (Vienna/Munich OR).
- **2015** jiang2015_hourahead — Monotone-ADP hour-ahead battery bidding, NYISO (Powell, Princeton).
- **2016** mohsenianrad2016_pricemaker — multi-unit price-maker storage in nodal market (UCR).
- **2017** wang2017_lookahead — bilevel with next-day look-ahead for terminal SoC (Kirschen, UW; co-author Xu).
- **2018** krishnamurthy2018_dart — DA+RT SP storage arbitrage (Botterud, Argonne).
- **2018** nasrolahpour2018_bilevel — stochastic bilevel energy + reserve + balancing (Zareipour/Kazempour).
- **2020** tomasson2020_offerbid — storage portfolio market power, withholding (KTH + Wolak).
- **2021** kim2021_vss — conditions for VSS = 0 in DA/RT storage SP (Sioshansi/Conejo, OSU).
- **2022** zheng2022_asdp — analytical SDP with variable efficiency (Xu, Columbia; Kirschen lineage).
- **2022** finnah2022_dpid — ADP for German DA + intraday storage bidding (Duisburg-Essen).
- **2023** lohndorf2023_coordination — value of DA/intraday coordination by asset type.
- **2024** baker2024_transferablebidder (S5) — learned value function → SoC-segmented bids.

Two genealogies are visible:
- **Conejo/UCLM school** (Conejo → Ruiz, Baringo, Morales; Kazempour's earlier UCLM work with Conejo/Ruiz — advisor ties widely documented but not re-verified in this session) → offering SP/RO/MPEC → storage MPECs (nasrolahpour2018_bilevel via Kazempour; kim2021_vss via Conejo at OSU).
- **Kirschen (UW) → Xu (Columbia)**: deterministic bilevel with look-ahead (wang2017_lookahead) → value-function SDP (zheng2022_asdp) → learned value functions (baker2024_transferablebidder). Parallel OR line Powell (jiang2015_hourahead) and Löhndorf/Wozabal (lohndorf2013_addp, lohndorf2023_coordination).

## 3. Groups
| Group | PI(s) | Papers here |
|---|---|---|
| UCLM → Ohio State | A. J. Conejo | conejo2002_pricetaker, ruiz2009_mpecoffer, baringo2011_robustoffer, pandzic2013_vppoffer, kim2021_vss |
| DTU / Calgary | J. Kazempour; H. Zareipour, W. Rosehart | nasrolahpour2018_bilevel (+ kazemi2017_jointenergyancillary, S2) |
| UW → Columbia | D. Kirschen; B. Xu | wang2017_lookahead, zheng2022_asdp (+ baker2024_transferablebidder, S5) |
| Princeton CASTLE | W. B. Powell | jiang2015_hourahead (+ cheng2018_multiscaledp, S2) |
| WU Vienna / TU Munich / Luxembourg / VU | N. Löhndorf, D. Wozabal, S. Minner | lohndorf2013_addp, lohndorf2023_coordination |
| UC Riverside | H. Mohsenian-Rad | mohsenianrad2016_pricemaker |
| Argonne | A. Botterud | krishnamurthy2018_dart |
| Ohio State | R. Sioshansi | kim2021_vss |
| KTH + Stanford | M. R. Hesamzadeh; F. Wolak | tomasson2020_offerbid |
| Duisburg-Essen | J. Gönsch, F. Ziel | finnah2022_dpid |

## 4. Summary table
| id | year | method_class | info structure at bid time | scenarios | data | main finding |
|---|---|---|---|---|---|---|
| conejo2002_pricetaker | 2002 | SP | next-day price pdfs | pdf-based (n.v.) | n.v. | bid rule derived from stochastic self-schedule (abstract) |
| ruiz2009_mpecoffer | 2009 | MILP (MPEC) | rivals/demand uncertain, LMPs endogenous | scenarios (n.v.) | n.v. | bilevel offering reducible to MILP via KKT + duality (abstract) |
| baringo2011_robustoffer | 2011 | RO | price confidence intervals | none (intervals) | n.v. | nested robust MILPs give hourly offer curves (abstract) |
| pandzic2013_vppoffer | 2013 | SP | DA offers before balancing | n.v. | n.v. | SP offering for wind + pumped storage + dispatchable VPP (abstract) |
| lohndorf2013_addp | 2013 | SDP/DP + SP | reservoir level + exogenous Markov state known; 24 DA prices unknown | 20 LHS per state; 30-cluster Markov chain | EEX 2009–11, 18 y inflows | 1.2 % UB–LB gap; +0.7–8.5 % vs deterministic rolling horizon |
| jiang2015_hourahead | 2015 | SDP/DP (ADP) | bid 1 h ahead, start SoC unknown | empirical (distribution-free) | NYISO NYC 2011–12 | ADP +46–68 % revenue vs rule-based; 90–95 % optimal at 4–7 % of DP time |
| mohsenianrad2016_pricemaker | 2016 | MILP (MPEC) | rivals' bids known (det.) or K scenarios | K = 3 perturbations | IEEE 30-bus, CAISO Mar 2014 | congestion ↑ profit up to ~200 %; economic bids > self-schedule under uncertainty |
| wang2017_lookahead | 2017 | MILP (MPEC) | DA; next-day profit discounted | n.v. | IEEE RTS | terminal-SoC look-ahead improves bidding (abstract) |
| krishnamurthy2018_dart | 2018 | SP | DA bids under DA+RT uncertainty | n.v. | "realistic" (n.v.) | stochastic ≫ deterministic (abstract) |
| nasrolahpour2018_bilevel | 2018 | MILP (stoch. MPEC) | DA offers before wind deviation | 1,000 → 16 (backward reduction) | Alberta 23 Nov 2015 | joint E+R +6 % profit; peak prices +12–25 %; per-scenario SoC −15 % profit |
| tomasson2020_offerbid | 2020 | MILP (stoch. disjunctive, B&B) | stochastic (n.v.) | n.v. | n.v. | strategic storage withholds demand/generation, under-uses, ↑ congestion (abstract) |
| kim2021_vss | 2021 | SP (two-stage NLP) | DA before RT prices; RT flexibility γ | 100 MC (regression + SARIMA) | PJM APCO 2012 | VSS = 0 if γ = 1 & no price impact; max VSS 2.05 % at γ = 0.5 |
| zheng2022_asdp | 2022 | SDP/DP | price observed before action (5-min) | Markov chain, 22 nodes/stage | NYISO 4 zones, test 2019 | 56–91 % of perfect-foresight profit; < 1 s/day |
| finnah2022_dpid | 2022 | SDP/DP (ADP) | DA self-schedule then ID | n.v. | German DA/ID (n.v.) | high-dimensional price info essential vs receding-horizon (abstract) |
| lohndorf2023_coordination | 2023 | SP (multistage) + info relaxation | DA auction then hourly continuous ID | scenario tree (n.v.) | n.v. | coordination valuable for pumped hydro; batteries mostly need intraday (abstract) |

n.v. = not verified (full text not read).

## 5. Open gaps (relevant to battery multi-product bidding research)
1. **Risk**: none of the full texts read uses CVaR or another risk measure for storage bidding; kim2021_vss notes risk aversion alone can make VSS > 0. Risk-averse value-function bidding for batteries remains thin in this verified set.
2. **DRO**: no Q1 Wasserstein-DRO *storage bidding* paper by a recognised group could be verified in this session; DRO in this archive appears only for dispatch/reserves (e.g., Kazempour-group EJOR 2022 chance-constrained dispatch, not storage bidding). Out-of-sample guarantees for battery bid curves are an open niche.
3. **Information structure vs market rules**: results hinge on whether the bidder acts after seeing the price (zheng2022_asdp) or commits ahead (jiang2015_hourahead, DA curves). Systematic comparison across GB (BM gate closure, DC/DM/DR products) and Nordic (FCR-N/D, mFRR EAM) rules is missing.
4. **Multi-product SP/SDP for batteries with ancillary services**: price-maker energy + reserve exists (nasrolahpour2018_bilevel) but price-taker multi-product SDP with frequency-response availability + energy remains scarce here (see S2: cheng2018_multiscaledp).
5. **Bid-curve fidelity**: storage bid curves in the literature use 1–4 segments; how segment count, monotonicity rules and SoC-dependence (allowed in CAISO, not in many EU auctions) change value is under-studied.
6. **Scalable price-maker models**: MPECs stay at ≤ 16 scenarios; decomposition or learning-based surrogates for price-maker batteries are an opening (tomasson2020_offerbid is a step).
7. **Certification**: UB/LB gaps (lohndorf2013_addp, lohndorf2023_coordination) are the only rigorous optimality certificates; DRL bidders are almost never benchmarked against information-relaxation bounds.
