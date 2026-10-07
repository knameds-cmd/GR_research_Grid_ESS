# S2: Stacking and co-optimisation of BESS across markets and services

Scope: optimisation models that co-optimise one battery across several markets or services: energy arbitrage (DA/ID/RT), frequency regulation/response (FCR, FFR, RegD, FCR-N/D), reserves, network or behind-the-meter services, and capacity. Covers revenue stacking, dynamic allocation and multi-timescale DP.

Papers in this stream: 13 files in `papers/`. Evidence depth varies; see the `evidence_read` field in each file. Six were read in full text (shi2018, dowling2017, namor2019, engels2020, biggins2022, mirzaeialavijeh2025), plus one working-paper version (he2011). The other six are abstract-level.

## 1. Overview

Nearly all papers in the stream make four modelling choices, and these are also the levers that market product rules act on:

1. **Capacity allocation across services.** The options are:
   - **fixed** (one split for a day or a contract: shi2018, namor2019, biggins2022);
   - **sequential by market order** (he2011);
   - **dynamic per product period** (hourly or daily: dowling2017, engels2020 daily, mirzaeialavijeh2025 hourly, englberger2020 rolling).

   Englberger also separates **power** allocation from **energy** allocation.
2. **Energy content of frequency/reserve delivery.** Four approaches:
   - **ignored or energy-neutral** (dowling2017: capacity only, mileage offsets tracking);
   - **expected utilisation** (biggins2022: event probabilities);
   - **historical signal replay / scenarios** (shi2018: RegD scenarios; mirzaeialavijeh2025: 1-min frequency through droop curves);
   - **statistical or robust envelope** (namor2019: 95% quantile energy budgets; engels2020: chance constraints via robust SOCP; kazemi2017: max-min worst case).
3. **SoC/SoE management.** This can be:
   - an operator-chosen margin (perez2016 SoC windows for ageing);
   - a statistically sized budget (namor2019, engels2020);
   - a recovery policy (engels2020 linear recharge controller; namor2019 offset profile);
   - an explicit **rule-derived reservation**: biggins2022 reserves P/2 MWh for a 30-min FFR call; mirzaeialavijeh2025 uses worst-case endurance checkpoints of 20 min for FCR-D and 1 h for FCR-N.
4. **Information.** Most studies are deterministic or oracle about prices: dowling2017, mirzaeialavijeh2025, he2011, biggins2022 for DA prices, shi2018 and engels2020 with fixed prices. Uncertainty usually enters through load, the signal or tender acceptance rather than prices. The exceptions are cheng2018 (stochastic prices + signal + load, multi-scale DP) and kazemi2017 (robust over prices and deployments).

Robust findings across the stream:
- Stacking is often **what turns storage profitable**: he2011, braeuer2019, englberger2020, mirzaeialavijeh2025.
- **Frequency services dominate stacked value** in the markets and periods studied: moreno2015 (GB), dowling2017 (CAISO AS +40–100%), mirzaeialavijeh2025 (FCR-D dominant).
- Joint optimisation can be **superlinear** when the frequency signal is close to energy-neutral (shi2018).
- Ignoring product-specific risks inflates value: tender acceptance gives about +28% (biggins2022). Perfect foresight in RT layers is a related bias (dowling2017).

## 2. Chronological lineage

- **2011, he2011_aggregatingvalues** (KU Leuven/FSR). Storage-use rights auctioned sequentially (week-ahead → day-ahead → hour-ahead). Earlier commitments become firm constraints for later stages, which is the market-sequence view of stacking.
- **2015, moreno2015_multiservicemilp** (Imperial, Strbac). Joint MILP portfolio of DNO congestion, arbitrage, reserve and frequency services with P/Q control (GB). Frequency services most profitable.
- **2016, perez2016_degradationmultiservice** (Imperial/U. Chile). Adds degradation and SoC-window strategies to the Moreno portfolio.
- **2016/2018, cheng2018_multiscaledp** (Princeton, Powell). Nested multi-timescale stochastic DP for regulation + arbitrage.
- **2017, dowling2017_multiscalemarkets** (UW–Madison, Zavala). Nested DA/15-min/5-min + AS MILP oracle, CAISO. Shows that time granularity drives value.
- **2017, kazemi2017_jointenergyancillary** (Calgary, Zareipour). Robust max-min co-scheduling of DA energy, spinning reserve and regulation.
- **2018, shi2018_superlineargains** (UW, Zhang/Kirschen line). Peak shaving + RegD: two-stage SP with signal scenarios; proves superlinear gains.
- **2019, namor2019_multiservicecontrol** (EPFL, Paolone). Power and energy budgets per service, frequency quantile energy budget, experimental validation.
- **2019, braeuer2019_parallelrevenue** (KIT, Fichtner). BTM LP with sizing: peak shaving + PCR + DA/ID across 50 SMEs.
- **2020, engels2020_fcrpeakshaving** (KU Leuven/EnergyVille + Centrica). FCR + monthly peak charge: chance-constrained SOCP inside a monthly DP.
- **2020, englberger2020_dynamicstacking** (TUM, Jossen/Hesse). Static vs dynamic stacking, power vs energy allocation, rolling horizon with ageing.
- **2022, biggins2022_tradeornot** (Sheffield, Brown). GB FFR + DA arbitrage. Rule-based SoC reservation, ML tender-acceptance risk, Monte Carlo.
- **2025, mirzaeialavijeh2025_swedenfcrstacking** (Chalmers). Hourly DA + FCR-N/D-up/D-down MILP oracle with 1-min frequency replay, LER endurance checkpoints and ageing.

Cross-stream papers that also stack services, held by other streams: staffell2016_maxvalue (GB arbitrage + STOR; S1), he2016_pbrcyclelife (energy + spinning + performance-based regulation with cycle life; S4/S6), padmanabhan2020_energyreserve (BESS in co-optimised energy + reserve clearing; S4/S7), xu2022_dynamicvaluation (arbitrage vs RegD with lifetime value; S4), walawalkar2007_nyisoarbitrage (arbitrage + regulation NYISO; S1).

## 3. Groups

| Group (PI, institution) | Papers here | Signature |
|---|---|---|
| Strbac, Imperial (with Moreno, U. Chile) | moreno2015, perez2016 | Multi-service portfolio MILP, GB, network + balancing services |
| D'haeseleer/Delarue (KU Leuven) + Glachant (FSR) | he2011 | Business model / sequential auctions |
| Deconinck (KU Leuven/EnergyVille) + Centrica | engels2020 | Chance-constrained FCR SoE + DP |
| Powell, Princeton CASTLE | cheng2018 | Multi-scale stochastic DP / ADP |
| Zavala, UW–Madison (Dowling) | dowling2017 | Multi-timescale market MILP, CAISO |
| B. Zhang / Kirschen, U. Washington | shi2018 (+ S4: xu2018_degradationmodel, xu2022_dynamicvaluation) | Signal-scenario SP, degradation-aware regulation |
| Zareipour/Rosehart, Calgary | kazemi2017 | Robust joint energy-AS scheduling |
| Paolone, EPFL DESL | namor2019 | Power/energy budgets, experimental BESS control |
| Jossen/Hesse, TUM EES | englberger2020 (+ S4: collath2023_lifetimeprofit) | Dynamic multi-use stacking with ageing |
| Fichtner, KIT IIP | braeuer2019 | BTM techno-economic LP with sizing |
| S. Brown, Sheffield (with Mac Dowell, Imperial, in lee2019_closedloopgb, S6) | biggins2022 | GB FFR + arbitrage, tender risk |
| Steen / Le Anh Tuan, Chalmers | mirzaeialavijeh2025 | Nordic FCR stacking, LER endurance encoding |

## 4. Summary table

| id | year | method_class | services | key assumption | data | main finding |
|---|---|---|---|---|---|---|
| he2011_aggregatingvalues | 2011 | MILP (sequential) | week-ahead supply cost, DA arbitrage, hour-ahead regulation | Earlier-auction profiles firm; perfect foresight per stage | Belgium 2007, one week | Aggregated value (≈€350k/wk) far exceeds any single use (≤€150k/wk) |
| moreno2015_multiservicemilp | 2015 | MILP | DNO congestion, arbitrage, reserve, frequency regulation, reactive power | (abstract only) | GB case studies | Frequency services most profitable; Q control adds value |
| perez2016_degradationmultiservice | 2016 | MILP (lineage; unconfirmed) | balancing + DNO services | SoC-window ageing mitigation | GB | Ageing-aware SoC limits lower near-term revenue but raise lifetime value; balancing services hit hardest |
| dowling2017_multiscalemarkets | 2017 | MILP | DA/15-min/5-min energy + reg up/down + spin + non-spin | Perfect foresight for one year; regulation energy-neutral (no signal) | CAISO 2015 | AS +43% for battery; DA-only misses 60–90% of value |
| kazemi2017_jointenergyancillary | 2017 | RO | DA energy, spinning reserve, regulation | Non-probabilistic uncertainty sets for prices and deployment | (abstract only) | Risk-controlled joint schedule via duality |
| cheng2018_multiscaledp | 2018 | SDP/DP | regulation + arbitrage | Stochastic price, load, signal; nested time scales | (abstract only) | Multi-scale DP decomposition makes the daily problem tractable |
| shi2018_superlineargains | 2018 | SP | RegD + peak shaving (BTM) | Fixed day-ahead C and peak threshold; known prices; RegD scenario replay | PJM RegD 1 yr; MS data centre, UW building | Joint savings 10.7–12.4% of bill; superlinear gain 2.7–3.9% |
| namor2019_multiservicecontrol | 2019 | MPC (LP day-ahead + RT) | PFR droop + feeder dispatch | Daily-fixed power/energy budgets; 95% quantile frequency-energy budget | EPFL 560 kWh BESS; 2 yr PMU frequency | Feasible simultaneous provision verified experimentally |
| braeuer2019_parallelrevenue | 2019 | LP (+sizing) | peak shaving + PCR + DA/ID arbitrage | (abstract only) 15-min LP | 50 German SMEs | Only the combination is profitable; arbitrage marginal |
| engels2020_fcrpeakshaving | 2020 | SDP/DP + robust SOCP | FCR + monthly peak shaving | Daily FCR capacity; chance-constrained SoE; known prices | 4 yr CE frequency; 2 industrial sites | Combined 14.4 k€/month vs 13.1 FCR-only, 7.2 peak-only |
| englberger2020_dynamicstacking | 2020 | rolling-horizon optimisation (class unconfirmed) | FCR + peak shaving + self-consumption + ID continuous | Dynamic power and energy allocation; ageing model | German real BESS data | NPV/€ invested 1.00 (PS+FCR) → 1.24 (+ID) |
| biggins2022_tradeornot | 2022 | MILP + ML + Monte Carlo | GB dynamic FFR + DA arbitrage | Split fixed by tender outcome; P/2 MWh reserved (30-min call); expected utilisation | NGESO tenders 2018–20, N2EX, 1 s frequency | Ignoring tender risk overstates income by ~28% |
| mirzaeialavijeh2025_swedenfcrstacking | 2025 | MILP (oracle) | Nordic DA + FCR-N + FCR-D up + FCR-D down | Hourly dynamic split; 1-min frequency replay; LER endurance checkpoints; ageing cost | SE3 2022 (ENTSO-E, eSett, Fingrid) | €708k/yr per MW-MWh, 22× DA-only; ageing 1.7%/yr reducible to 1.2% |

## 5. Open gaps for a study of how market product rules drive profitability

1. **Rules are almost never treated as the experimental variable.** Every paper fixes one regime and optimises within it. None sweeps the following as separate counterfactuals on the same asset and data:
   - stacking permission: which products may share MW, symmetric vs asymmetric, split vs co-located MW;
   - energy-reservation and endurance requirements (15/20/30 min or 1 h);
   - SoE-management rules (e.g., GB DC/DM/DR SoE requirements and baseline/recovery allowances).

   mirzaeialavijeh2025 and biggins2022 encode the rules but do not vary them. This is the central gap.
2. **The way the rule is encoded changes the measured value.** The stream mixes expected utilisation, signal replay, robust or quantile budgets, and no signal at all. A rule study should hold the encoding fixed, or report sensitivity across encodings. Ideal: rule-based deterministic reservation for compliance plus replay for actual SoC drift.
3. **Superlinearity depends on the regime.** Shi's superlinear gain relies on an energy-neutral RegD-type signal. Nobody tests whether it survives droop products with persistent one-sided deviations, or explicit SoE reservation rules. A natural hypothesis for a rule study.
4. **Dynamic allocation granularity is underexplored as a policy lever.** Studies use daily (engels2020), hourly (mirzaeialavijeh2025), monthly or EFA-block (biggins2022) or rolling (englberger2020) re-allocation, but none isolates the value of finer product periods, for example weekly → daily → 4-hour FCR, or EFA-block → half-hourly. dowling2017 shows granularity matters for energy, not for reserve products.
5. **Sequential clearing vs joint co-optimisation.** he2011 models market order explicitly. Most later work co-optimises jointly with foresight, which overstates attainable value when products clear in sequence (e.g., GB response auctions before wholesale/BM; CE FCR before aFRR/DA). The gap between sequential and joint optimisation under real gate-closure order is not quantified.
6. **Uncertainty in prices and acceptance under multi-product rules.** Oracle bounds dominate. Only biggins2022 (acceptance), kazemi2017 (robust) and cheng2018 (SDP) treat uncertainty, and none does so with a multi-product rule set. That is an opening for SP/DRO or RL policies evaluated under each rule regime, linking to S3 and S5.
7. **Degradation interacts with SoE rules** (perez2016, mirzaeialavijeh2025). No study separates the profit lost to regulatory SoE constraints from the profit lost to ageing-motivated SoC limits.
8. **GB post-2021 response suite is missing from the optimisation literature in this stream.** Existing GB optimisation studies (moreno2015, biggins2022) predate the DC/DM/DR suite and its SoE rules. GB DC product papers in S6 (e.g., cao2024_dcvsefr) are simulation or control studies, not stacking optimisation.
   - **2026-10-07 update:** `casella2024_ukbessmilp` (Q1, Renewable Energy 2024) now encodes GB dynamic frequency response services with DA/ID and imbalance in a MILP, and the preprint Xia et al. 2026 (`WATCHLIST.md` C3) adds EAC co-optimisation and SoE rules. Gap 1 (rules as the experimental variable) is unaffected.

## 6. Dropped or deferred candidates (and why)

- **Stephan et al. 2016, Nature Energy** ("Limiting the public cost of stationary battery deployment by combining applications", ETH, Schmidt). A value-foundations/policy paper better placed in S1. Not added here; no file exists yet, so S1 may want it.
- **Walawalkar 2007:** covered by S1 (walawalkar2007_nyisoarbitrage); cross-reference only.
- **Xu, Shi, Kirschen, Zhang 2018, "Optimal battery participation in frequency regulation markets"** (IEEE TPWRS; arXiv 1710.10514, full text read). Regulation only, with no energy stacking (confirmed in the text). Belongs to S4/S6.
- **Megel, Mathieu & Andersson** (multiple services under forecast error). Only the PSCC 2014 conference version was located; no journal version verified, so excluded.
- **Akhavan-Hejazi & Mohsenian-Rad 2014** (IEEE TSG; independent storage in energy + reserve with wind). A price-maker bilevel model, closer to S3/S7; full text not obtained; not added.
- **Xu, Dvorkin, Kirschen et al.**, comparison of US storage regulation-market participation policies. No journal version located before the web-search budget ran out; not added.
- **Nitsch 2021** (agent-based, DLR): left to S7/S8.
- **Steriotis et al. 2022, IEEE TSTE** (stacked revenues via flexibility markets, with Pandžić). Distribution flexibility markets; not verified in depth; deferred.
- **"Balancing with batteries: The impact of revenue stacking and skip rates on battery energy storage profitability in Great Britain"** (J. Energy Storage, 2026; ScienceDirect PII S2352152X26019924). Seen in search results only; authors and metadata not verified. Highly relevant to GB rule effects; flagged for S6/S8 follow-up.
- Preprints seen (arXiv 2609.03767 lifetime multi-service stacking; arXiv 2609.18349 mean-CVaR multi-market) were excluded as preprint-only.

## 7. Verification notes
- Quartiles were checked on scimagojr.com (2025 values) for: IEEE TPWRS, IEEE TSG, IEEE TSTE, Applied Energy, Energy Policy, J. Energy Storage, Cell Rep. Phys. Sci., Nature Energy, IJEPES.
- Bibliographic fields were checked through Crossref, OpenAlex, publisher or repository pages, and the doi.org resolver, as logged in each file.
- Crossref, OpenAlex and Semantic Scholar rate limits meant a few records rely on institutional repository metadata.
