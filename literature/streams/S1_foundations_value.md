# S1 — Foundations: the value of electricity storage

## (a) Overview
This stream collects the canonical and recent Q1 work that defines *what storage is worth* and *to whom*. Three strands appear. (1) **Private arbitrage value** under price-taker, perfect-foresight LPs on historical prices (NYISO, PJM, U.S. RT markets, NEM, GB, EU-DA). These studies set durable benchmarks: realistic forecasting captures roughly 75–95 % of the perfect-foresight value; value saturates at about 4–10 h of duration; and arbitrage alone rarely pays back capital. (2) **Welfare and ownership.** Storage shifts surplus from producers to consumers, so net social gain is a small fraction of private profit. Ownership and market power can make storage under- or over-used, and in concentrated markets it can even reduce welfare. (3) **Long-run system value vs cost.** Capacity-expansion and peak-load-pricing theory show that system value comes mainly from capacity deferral. In a competitive market without price caps, storage exactly recovers its capital cost. Experience-curve and LCOS work supplies the matching cost trajectories. Across the stream, *value is shaped by market rules*: price caps and scarcity pricing, product eligibility, capacity payments, grid fees and ownership rules.

## (b) Chronological lineage of ideas
- **1999** Graves, Jenkin & Murphy (Electricity Journal): early arbitrage valuation of storage in deregulated markets. *Historical, not archived* (Electricity Journal is Q1 in SJR 1999 in Energy (misc.) but Q2 in recent years and is a practitioner outlet).
- **2007** walawalkar2007_nyisoarbitrage (CMU CEIC, Apt): NYISO zonal screening finds location/ICAP and product eligibility dominate NPV, and regulation beats arbitrage.
- **2009** sioshansi2009_pjmvalue (OSU/NREL): LP/QP benchmark covering foresight capture (~85 %), duration saturation, price-maker erosion (10–20 %) and the welfare split (large CS/PS transfers, small net gain). Builds on Graves et al. (Jenkin a co-author of both).
- **2010** sioshansi2010_ownership, then **2014** sioshansi2014_welfareloss: formal ownership and market-power theory (merchant underuse, consumer overuse, generator-owned harm; welfare loss possible with Cournot generators).
- **2014** bradbury2014_rtarbitrage (Duke): cross-market U.S. RT comparison; optimal sizing is technology-driven and arbitrage IRRs are insufficient.
- **2015** mcconnell2015_energyonly (Melbourne): energy-only NEM. Spike-driven value is efficiency-insensitive and set by the market price cap, which makes the market-rule dependence explicit.
- **2016** staffell2016_maxvalue (Imperial): GB revenue stacking (STOR roughly triples profit) plus an open algorithm. braff2016_windsolarvalue (MIT Trancik): two-dimensional energy/power cost thresholds. desisternes2016_decarbvalue (MIT/Argonne): system value under CO2 limits via UC-constrained expansion.
- **2017–2019** schmidt2017_experiencerates, then schmidt2019_lcos (Imperial, Staffell/Hawkes): cost trajectories and application-specific LCOS. These are the cost counterpart to value.
- **2020** mallapragada2020_longrunvalue (MIT/Princeton GenX): long-run value comes mainly from capacity deferral and declines with penetration. Extends de Sisternes et al.
- **2022** junge2022_efficientstorage (MIT, Schmalensee): KKT theory showing competitive storage earns exactly its capital cost, there is no storage merit order, and the energy-capacity cost ratio sets duration. Extends Schmalensee CEEPR WP 2019 and uses GenX.
- **2023** mercier2023_eudaarbitrage (UCLouvain/Laval): 20 years of EU DA arbitrage; grid fees cut value 20–50 %.
- **2025** antweiler2025_newmeritorder (UBC/BTU): in 100 % VRE + storage energy-only markets, storage opportunity costs set prices and cost recovery holds unless prices are capped. Builds on Junge et al. and the energy-only line (McConnell).

## (c) Research groups
| Group / PI | Institution | Papers in stream | Notes |
|---|---|---|---|
| Ramteen Sioshansi (with Paul Denholm, Thomas Jenkin) | Ohio State ISE (at publication; author pages now hosted by CMU CEIC); NREL | sioshansi2009_pjmvalue, sioshansi2010_ownership, sioshansi2014_welfareloss | Welfare/ownership theory and PJM valuation; NREL co-authors also link to Graves et al. 1999 |
| Jay Apt | Carnegie Mellon Electricity Industry Center | walawalkar2007_nyisoarbitrage | CEIC working-paper series; Apt→Walawalkar advisor tie not verified |
| Lincoln Pratson, Dalia Patiño-Echeverri | Duke Nicholas School | bradbury2014_rtarbitrage | |
| Mike Sandiford (Melbourne Energy Institute) | University of Melbourne | mcconnell2015_energyonly | NEM energy-only focus |
| Iain Staffell, Adam Hawkes | Imperial College London (CEP, Grantham, Chem Eng) | staffell2016_maxvalue, schmidt2017_experiencerates, schmidt2019_lcos | Continuous team; Schmidt first author on cost papers |
| Jessika Trancik | MIT IDSS | braff2016_windsolarvalue | |
| Audun Botterud; Jesse Jenkins; Nestor Sepulveda; Dharik Mallapragada | MIT / Argonne → Princeton ZERO lab; MITEI | desisternes2016_decarbvalue, mallapragada2020_longrunvalue | GenX lineage (Jenkins & Sepulveda) |
| Richard Schmalensee (with Mallapragada) | MIT Sloan/Economics, MITEI | junge2022_efficientstorage | Peak-load-pricing theory with storage |
| Emmanuel De Jaeger; Mathieu Olivier | UCLouvain/KU Leuven; Université Laval | mercier2023_eudaarbitrage | |
| Werner Antweiler; Felix Müsgens | UBC Sauder; BTU Cottbus-Senftenberg | antweiler2025_newmeritorder | |

Advisor–student ties were **not** verified in this stream (the search budget was exhausted). Only co-authorship and affiliation links are asserted.

## (d) Summary table
| id | year | method_class | key assumption | data | main finding |
|---|---|---|---|---|---|
| walawalkar2007_nyisoarbitrage | 2007 | heuristic screening + Monte Carlo NPV | price-taker, daily best windows | NYISO 2001–05 zonal DA, regulation, ICAP | NYC arbitrage NPV>0 (66 % prob.); regulation (flywheel) best upstate; eligibility rules cap revenue |
| sioshansi2009_pjmvalue | 2009 | LP / QP | perfect foresight; linear price–load for price impact | PJM hourly 2002–07 | $60–110/kW-yr (12 h); backcast ≥85 %; 1 GW device: −10–20 % value; net welfare ≪ private profit |
| sioshansi2010_ownership | 2010 | analytical Nash + MCP | 2-period, linear price, inelastic demand | ERCOT 2005 calibration | merchant underuse (<12 % loss); generator-owned up to 100 % loss; consumer overuse |
| sioshansi2014_welfareloss | 2014 | analytical game theory | linear demand, quadratic cost, Cournot | stylised | storage can reduce welfare when generators have market power |
| bradbury2014_rtarbitrage | 2014 | LP | price-taker (abstract) | 7 U.S. RT markets, 2008 | optimal size set by technology (RTE, self-discharge), not volatility; IRRs insufficient |
| mcconnell2015_energyonly | 2015 | LP | price-taker; PF and pre-dispatch forecasts | NEM FY2002–14 (SA) | value concentrated at A$13,100 cap; ~90 % with 4 h; efficiency-insensitive; 85 % with forecasts |
| staffell2016_maxvalue | 2016 | greedy heuristic (LP-validated) | price-taker, PF / no foresight | GB 2013/14 + STOR | reserve ~triples profit; 75–95 % captured without foresight; not viable at 2016 costs |
| braff2016_windsolarvalue | 2016 | LP (abstract) | price-taker hybrid plant | U.S. locations | energy- vs power-cost targets for value-adding storage; location-invariant trajectories |
| desisternes2016_decarbvalue | 2016 | MILP capacity expansion + UC | planner, PF, representative weeks | Texas | 2 h only under strict CO2 caps; 10 h valuable; storage optional if flexible low-C firm power available |
| schmidt2017_experiencerates | 2017 | experience-curve econometrics | price ∝ cumulative capacity^(−b) | global price data | ~US$340±60/kWh stationary, US$175±25/kWh packs at 1 TWh |
| schmidt2019_lcos | 2019 | LCOS + Monte Carlo | 8 % WACC; flat charging price | 21 sources + experts | LCOS −1/3 by 2030, −1/2 by 2050; Li-ion cheapest for most applications by ~2030 |
| mallapragada2020_longrunvalue | 2020 | LP (GenX) | planner, PF | NE- and TX-like systems | value mainly capacity deferral; declines with penetration; 4–16 % of peak at $150/kWh |
| junge2022_efficientstorage | 2022 | LP + KKT theory | constant returns, PF, no cap below VOLL | ERCOT 2007–13 hourly | competitive storage earns zero profit (exact cost recovery); no storage merit order; energy-capacity cost key |
| mercier2023_eudaarbitrage | 2023 | MILP | price-taker (abstract) | EU DA 2000–21, 31 countries | large cross-country variation; >4–6 h little value; Belgian grid fees −20–50 % |
| antweiler2025_newmeritorder | 2025 | analytical + NLP equilibrium | free entry, PF, single node, unlimited storage energy | ERCOT & DE 2019–22 | storage sets prices ("new merit order"); energy-only viable unless capped |

## (e) Open gaps for a study quantifying how specific market rules drive battery profitability
1. **Rule-level attribution is missing.** Most valuation studies change markets, years or technologies, not individual rules. Only mcconnell2015 (price cap) and mercier2023 (grid fees) isolate one rule. Nobody has systematically decomposed battery profit into contributions from gate-closure timing, product duration/symmetry, pay-as-bid vs pay-as-clear settlement, availability vs utilisation payments, de-rating factors or network charges.
   - **2026-10-07 update:** still holds. `landy2026_hybridstacking` varies market-access bundles and `gale2026_balancingbatteries` varies the skip rate, but neither decomposes profit by individual rule.
2. **Price-taker bias versus market-design feedback.** The welfare/price-impact strand (sioshansi2009, 2010, 2014) and the long-run strand (junge2022, antweiler2025) show that value erodes and redistributes as fleets grow. Merchant-profit studies (staffell2016, mercier2023) remain price-takers. Linking rule changes to equilibrium price formation, for example saturation of ancillary products, is open.
3. **Long-run theory vs short-run disequilibrium.** Theory predicts zero economic profit in competitive markets, yet observed early-mover returns (GB DC, ERCOT ancillaries) were high. Quantifying how much excess return comes from transitional product scarcity versus structural rule features is untested.
4. **Multi-product foresight.** The capture ratios (75–95 %) come from single-market arbitrage. Foresight losses under sequential multi-market rules (DA → ID → balancing, product-specific gate closures) are poorly benchmarked in this foundational literature.
5. **Value vs cost alignment.** LCOS (schmidt2019) and value studies use incompatible units and assumptions. A rule-specific "required spread" or "break-even product price" metric that combines LCOS with per-rule revenue is lacking.
6. **Ownership/market-power rules.** sioshansi2010/2014 predict ownership-dependent dispatch, but empirical tests across regimes with different ownership/unbundling rules (EU network-ownership ban vs U.S. utility-owned storage) are scarce in Q1 storage-value work.
7. **European / GB coverage of system value.** Long-run system-value work (desisternes2016, mallapragada2020, junge2022) is U.S. (Texas/Northeast) centric. Equivalent capacity-deferral value analyses under GB/Nordic capacity-mechanism rules are missing.

## Dropped / not archived candidates
- **Graves, Jenkin & Murphy 1999** (Electricity Journal): historical; journal not Q1 in recent SJR years and practitioner-oriented. Mentioned only.
- **Zafirakis et al. 2016** (Applied Energy 184:971–986, doi:10.1016/j.apenergy.2016.05.047; the seed DOI 10.1016/j.apenergy.2016.03.102 was **wrong** and belongs to an unrelated CCS paper): verified bibliographically. Not archived because it focuses on PHS/CAES rather than BESS, the only OA copy is a .docx manuscript that could not be read, and the slot went to mercier2023 (newer, broader EU DA coverage with a grid-fee rule result).
- **Lamp & Samano 2022** (Energy Economics): left to the empirical/econometrics stream.
- **Arbabzadeh et al. 2019** (Nature Communications) and **Sepulveda et al. 2021** (Nature Energy, LDES design space): long-duration/deep-decarbonisation focus that overlaps with desisternes2016/mallapragada2020. Not archived and not bibliographically verified here.
- **Butters, Dorsey & Gowrisankaran, "Soaking up the sun"**: later confirmed as *Econometrica* 93(3):891–927 (2025) and archived in S8 as `butters2025_soakingsun` [updated 2026-10-07]. **Karaduman (grid-scale storage)**: no peer-reviewed journal version confirmed. Not archived.
- **Brijs et al. 2019** (J. Energy Storage 25:100899, KU Leuven, CWE short-term arbitrage): identified via Crossref. Left for the multi-market stream.
