# S7 - Market design and regulation for storage

Stream scope: how market rules and regulatory choices (participation models, who manages state of charge (SoC), ownership/unbundling, capacity accreditation, scarcity pricing, reform packages) change storage dispatch, revenue, investment and welfare - and, centrally for this study, **how the literature attributes outcomes to market rules**.

Files written for this stream (13): sioshansi2014_capacityvalue, sioshansi2017_capacityrights, jiang2023_isodispatch, bhattacharjee2022_soemanagement, bhattacharjee2025_hybridparticipation, chen2022_misobatteryscuc, williams2022_marketpower, andrescerezo2023_marketstructure, siddiqui2019_merchantinvestment, denholm2020_peakingcapacity, papavasiliou2017_ordcbelgium, grubb2018_ukemr, sakti2018_usparticipation.

Cross-listed S7 files written by other streams (not duplicated): sioshansi2010_ownership, sioshansi2014_welfareloss, junge2022_efficientstorage, antweiler2025_newmeritorder, mcconnell2015_energyonly, mercier2023_eudaarbitrage, he2011_aggregatingvalues, padmanabhan2020_energyreserve, xu2018_cycleagingcost, butters2025_soakingsun.

Evidence depth: full text read for 8 of the 13 new files; 4 are abstract-level (sakti2018, siddiqui2019, papavasiliou2017, grubb2018) and 1 relies on a patent text with the same title (chen2022). Treat the abstract-level files as pointers, not as sources for details.

## 1. Overview - the design levers the literature isolates

| Lever | Question | Key files |
|---|---|---|
| Participation model / offer format | Self-schedule vs price-responsive offers; co-located vs integrated hybrids | bhattacharjee2022_soemanagement, bhattacharjee2025_hybridparticipation, sakti2018_usparticipation |
| Who manages SoC | Market operator optimises SoC inside clearing vs owner self-manages | jiang2023_isodispatch, bhattacharjee2022_soemanagement, chen2022_misobatteryscuc, padmanabhan2020_energyreserve, xu2018_cycleagingcost |
| Ownership / vertical structure | Merchant vs generator- vs consumer-owned vs integrated | sioshansi2010_ownership, sioshansi2014_welfareloss, andrescerezo2023_marketstructure, siddiqui2019_merchantinvestment, williams2022_marketpower |
| Cost recovery / remuneration architecture | Market-based vs rate-based vs capacity-rights auctions; can energy-only prices fund storage | sioshansi2017_capacityrights, junge2022_efficientstorage, antweiler2025_newmeritorder, mcconnell2015_energyonly |
| Capacity accreditation (ELCC / de-rating) | How much firm capacity an energy-limited battery gets; duration rules | sioshansi2014_capacityvalue, denholm2020_peakingcapacity |
| Scarcity pricing | ORDC adders vs capped energy-only prices | papavasiliou2017_ordcbelgium, junge2022_efficientstorage (VOLL vs caps) |
| Reform packages | Ex-post evaluation of GB EMR | grubb2018_ukemr |

## 2. Lineage

- **Ownership/market power line (OSU/Berkeley -> Imperial, Carlos III).** Sioshansi (Oren PhD, Berkeley 2007) builds the two-period Nash framework: sioshansi2010_ownership -> sioshansi2014_welfareloss -> siddiqui2019_merchantinvestment (adds the investment stage; bilevel; ramping-charge remedy). Andrés-Cerezo & Fabra (andrescerezo2023_marketstructure) generalise to investment + vertical integration on a load-duration curve; Williams & Green (williams2022_marketpower) quantify for GB with a 2x2 conduct design.
- **Rights / duality line (Hogan 1992 -> Sioshansi).** FTR logic is transferred to storage: storage-capacity rights (sioshansi2017_capacityrights) and the duality argument for MO dispatch (jiang2023_isodispatch). Efficient-market cost-recovery results (junge2022_efficientstorage, MIT/Schmalensee; antweiler2025_newmeritorder) are the long-run analogue.
- **Participation-model line after FERC Order 841.** Sakti/Botterud/O'Sullivan's US review (sakti2018_usparticipation) -> bilevel MPEC tests of SoE-management and hybrid participation options (Bhattacharjee-Sioshansi-Zareipour 2022, 2025) -> ISO implementation (chen2022_misobatteryscuc, MISO) and SoC-dependent bids (Chen & Tong, Cornell, TPWRS letter; Zheng, Xu et al., Columbia - IEEE TEMPR, not archived because the journal has no settled SJR quartile).
- **Capacity value line (Sioshansi-Denholm, OSU/NREL).** sioshansi2014_capacityvalue (DP + LOLP recursion) -> denholm2020_peakingcapacity (national peak-shaving proxy, 4-hour rule cliff) -> Kim, Sioshansi, Lannoye & Ela 2022/2025 TPWRS (stochastic-dynamic ELCC; storage that also provides regulation) - not archived (full text not obtained).
- **Scarcity pricing (Hogan -> Papavasiliou/Smeers).** ORDC from ERCOT ported to Belgium (papavasiliou2017_ordcbelgium).

## 3. Groups

| Group | PI(s) | Files | Verified ties |
|---|---|---|---|
| OSU ISE -> CMU EPP/ECE | R. Sioshansi | sioshansi2014_capacityvalue, sioshansi2017_capacityrights, jiang2023_isodispatch, bhattacharjee2022/2025, siddiqui2019 (+ S1 files) | Sioshansi PhD Berkeley 2007, chair S. Oren; NREL postdoc 2007-08 (CV). Student ties (Jiang, Madaeni) not verified. |
| U. Calgary | H. Zareipour | bhattacharjee2022/2025 | Bhattacharjee PhD Calgary (stated in paper). |
| UCL / Stockholm + OSU | A. Siddiqui, A. Conejo | siddiqui2019 | senior collaboration |
| Imperial Business School | R. Green | williams2022 | EPSRC EP/K002252/1 programme; student status of Williams not verified |
| UC3M EnergyEcoLab | N. Fabra | andrescerezo2023 | ERC 772331; advisor tie not verified |
| MIT LIDS/MITEI | A. Botterud, F. O'Sullivan | sakti2018 | Byers (S.M. 2018) advisor = Botterud (MIT DSpace) - Byers paper not archived |
| NREL | P. Denholm, W. Cole | denholm2020 | - |
| UCLouvain CORE | A. Papavasiliou, Y. Smeers | papavasiliou2017 | - |
| Cambridge EPRG / UCL | D. Newbery, M. Grubb | grubb2018 | - |
| MISO / UT Austin | Y. Chen, R. Baldick | chen2022 | - |

## 4. Summary table

| id | year | design lever | counterfactual | model | metric | finding |
|---|---|---|---|---|---|---|
| sioshansi2010_ownership (S1) | 2010 | ownership type | merchant / generator / consumer / mixed vs planner | 2-period Nash, ERCOT 2005 | welfare loss vs optimum | merchant < ~12% loss; generator under-use, consumer over-use |
| sioshansi2014_welfareloss (S1) | 2014 | ownership x competition | competitive/Cournot generation x standalone/generator-owned storage | analytical Cournot | sign of welfare change vs no storage | storage can reduce welfare only with strategic generation or generator control |
| siddiqui2019_merchantinvestment | 2019 | merchant investment; ramping charge | merchant vs welfare-maximising investor; with/without ramping charge | bilevel Cournot | welfare, capacity | merchant mis-invests; ramping charge restores optimal capacity (abstract) |
| andrescerezo2023_marketstructure | 2023 | market structure, vertical integration | FB / SB / competitive / monopoly / integrated | 2-stage IO + Spain 2030 sim | CS, welfare, K | vertical integration worst; competitive over-invests |
| williams2022_marketpower | 2022 | conduct (market power) | 2x2 competitive/Cournot generators x storage, 3 sizes | welfare-max/Cournot on GB merit stack | welfare GBP, profits by tech | storage +GBP 181-247m/yr; storage market power cuts gain 4-21% |
| sioshansi2017_capacityrights | 2017 | cost-recovery architecture | rights auction vs market-based vs rate-based | auction LP + duals | auction revenue | rights auction recovers priced + unpriced value ($539 vs $94/day example) |
| jiang2023_isodispatch | 2023 | MO dispatch of storage | MO-dispatched (first best) - theory | multi-period DC-OPF + duality, ISO-NE | rents, welfare, cost recovery | MO dispatch is incentive-compatible, supports efficient investment |
| bhattacharjee2022_soemanagement | 2022 | offer format x SoE manager | self-schedule vs price-responsive; owner vs MO SoE; enforce vs relax | bilevel stochastic MPEC, Alberta | profit, CS, welfare | unenforced owner-SoE enables manipulation; self-schedule-only cuts profit ~64% |
| bhattacharjee2025_hybridparticipation | 2025 | hybrid participation model | co-located vs integrated (+ grid-charging ban, ILR) | bilevel stochastic MPEC, Alberta | profit by component, surplus | totals ~equal; storage profit -36% under integrated model |
| chen2022_misobatteryscuc | 2022 | SoC-aware clearing formulation | convex vs binary vs tightened SoC | MISO SCUC MILP | exactness, solve time | relaxation exact unless prices below offer-efficiency threshold (patent text) |
| sioshansi2014_capacityvalue | 2014 | capacity accreditation method | DP-based ECP vs capacity-factor heuristics | DP + LOLP recursion, 5 US systems | ECP % nameplate | 1 h 41%, 4 h 75%, 10 h 98%; heuristics overstate short storage by up to 22 pp |
| denholm2020_peakingcapacity | 2020 | duration-based RA rules | storage durations x PV/wind penetration | peak-shaving simulation, 18 regions | GW at 100% credit | ~28 GW 4-h nationally; doubles at 10% PV; credit cliff |
| papavasiliou2017_ordcbelgium | 2017 | scarcity pricing (ORDC) | with vs without ORDC adders | Belgian market simulation (21 months) | CCGT cost recovery | adders restore viability (abstract) |
| grubb2018_ukemr | 2018 | GB EMR package | before/after reform, vs predictions | descriptive ex-post | mix, prices, CO2 | coal 46%->7%; auctions cheaper than expected (abstract) |
| sakti2018_usparticipation | 2018 | US participation rules | cross-ISO comparison | review | - | fragmented models; reforms needed at all timescales (abstract) |
| junge2022_efficientstorage (S1) | 2022 | price caps vs VOLL | efficient market vs capped | capacity-expansion LP + KKT | cost recovery | prices to VOLL fund efficient storage; caps create missing money |
| antweiler2025_newmeritorder (S1) | 2025 | energy-only viability | RES+storage only vs capped | long-run equilibrium | prices, cost recovery | storage opportunity costs set prices; capacity mechanisms unnecessary absent caps |

## 5. How the literature attributes outcomes to market rules (methodological patterns)

This is the section most relevant to designing a study in which "market product rules are switchable settings" and RL is deliberately excluded so that revenue differences are attributable to rules.

**P1. Controlled counterfactual simulation with the asset, scenarios and price-formation model held fixed; only the rule changes.**
- bhattacharjee2022_soemanagement uses a full factorial grid (offer format x SoE manager x enforce/relax) on the same Alberta scenarios; bhattacharjee2025_hybridparticipation swaps co-located vs integrated and then adds rule add-ons (grid-charging ban, ILR) one at a time. williams2022_marketpower uses a 2x2 conduct grid x 3 storage sizes.
- Lesson: one-factor-at-a-time plus a factorial design exposes **rule interactions** (e.g., SoE rules matter only when offers are price-responsive). For the GB/Belgium simulator, run a factorial over product rules (e.g., EFA-block vs half-hourly procurement, pay-as-clear vs pay-as-bid, co-optimised vs sequential gate closures) rather than country bundles only.

**P2. Benchmark ladder: no-storage / planner (first best) / second best / market outcome.**
- Nearly every paper anchors comparisons on a welfare-maximising benchmark (sioshansi2010_ownership, andrescerezo2023_marketstructure, jiang2023_isodispatch) and often a no-storage case (sioshansi2014_welfareloss, bhattacharjee2022_soemanagement). A rule's effect is reported as a share of the gap between first best and the status quo.
- For a profit-focused battery study: compute (i) perfect-foresight optimum under each rule set, (ii) the same with a fixed forecast-based policy; the rule effect is the difference within each column, the information effect the difference across columns (cf. butters2025_soakingsun's ~70%-of-perfect-foresight benchmark; mcconnell2015_energyonly's 85% with pre-dispatch forecasts).

**P3. Equilibrium comparison (analytical).** Cournot/Nash or bilevel models derive the sign of a rule's effect (ownership, vertical integration, ramping charge) with propositions; simulation then gives magnitudes (sioshansi2014_welfareloss, siddiqui2019_merchantinvestment, andrescerezo2023_marketstructure). Useful to justify why a price-taker simulator is appropriate (or not): if the battery fleet is small relative to the product market, price-taking is defensible for energy but not for small AS markets where batteries set prices.

**P4. Duality-based decomposition of revenues/rents.** jiang2023_isodispatch and sioshansi2017_capacityrights decompose storage income into rents on power capacity, energy capacity and SoC constraints (dual variables). bhattacharjee2025_hybridparticipation decomposes profit by component and surplus by stakeholder. For the study: decompose battery revenue by product and by binding constraint (power vs energy vs SoC-window) under each rule set - this attributes revenue changes to the rule mechanism rather than only reporting totals, and catches cases where totals are equal but composition changes.

**P5. Accreditation counterfactuals.** sioshansi2014_capacityvalue compares an exact SoC-aware ELCC/ECP with heuristic accreditation; denholm2020_peakingcapacity compares durations under a stylised 4-hour rule. The rule effect is measured as change in credited MW (and implicit capacity revenue). A capacity product in the simulator should therefore credit MW by duration (GB-style de-rating), with the de-rating table itself a switchable rule.

**P6. Ex-post counterfactual price reconstruction.** papavasiliou2017_ordcbelgium recomputes historical prices with ORDC adders; Grubb & Newbery compare outturns with ex-ante predictions (weak attribution because several instruments changed simultaneously). For GB, natural experiments exist (e.g., DC launch 2020, EAC go-live 2023, Capacity Market de-rating changes), but this stream found no Q1 paper exploiting them causally - see S8 (empirical) for econometric designs such as difference-in-differences (rangarajan2023_batteryfcasdid, Australia).

**P7. Long-run equilibrium / cost-recovery tests.** junge2022_efficientstorage and antweiler2025_newmeritorder test whether a rule (price cap vs VOLL, energy-only vs capacity mechanism) lets the zero-profit long-run equilibrium hold. Translating to a battery study: report whether each rule set lets a reference battery recover annualised capex, not just relative revenue.

Practical template distilled for the planned study: fixed battery + fixed historical price/volume data -> rule toggles (product definitions, procurement timing, SoC/headroom rules, de-rating, scarcity pricing) -> deterministic optimiser (perfect foresight and rolling forecast) -> factorial results -> decomposition by product and binding constraint -> benchmark ladder (best-rule, worst-rule, perfect-foresight upper bound) -> cost-recovery test.

## 6. Open gaps

1. **No archived Q1 study attributes GB battery outcomes to product-rule changes with a counterfactual design.** S6 holds GB service-design and operation papers (greenwood2017_efrservicedesign on EFR design; cao2024_dcvsefr and fan2025_dccolocatedreforms on Dynamic Containment and its reforms), but none runs a welfare/revenue counterfactual across rule sets of the kind in Section 5, and none covers the 2023 Enduring Auction Capability (co-optimised day-ahead response/reserve auction) or Balancing Mechanism dispatch rules. (This stream could not run new searches late in the session; a targeted search may still find Applied Energy/Energy Policy papers - verify before claiming novelty.)
2. **Capacity Market de-rating of short-duration batteries in GB** (equivalent firm capacity methodology, 2017-18 de-rating cuts) lacks an archived Q1 evaluation; the Dent/Durham-Edinburgh line (Edwards et al. 2017, SEGN) could not be verified in this session.
3. **Rule interactions across sequential markets** (AS procurement timing vs energy gate closure vs SoC headroom) are studied for US co-optimised markets (bhattacharjee2022_soemanagement, padmanabhan2020_energyreserve) but not for European sequential, self-dispatch designs where SoC never enters the clearing.
4. **Attribution with price endogeneity in small AS markets.** Most models either assume price-taking (fine for energy) or a monopoly bounding case (bilevel); intermediate saturation of capped-volume AS products (DC/FCR) is not modelled with a rule-switch design.
5. **Cross-country comparisons** (GB vs Belgium vs Nordics vs Korea) with one asset and one optimiser are absent; existing cross-country work is energy-arbitrage only (mercier2023_eudaarbitrage).
6. **Korean context:** no archived Q1 work on storage participation under a cost-based pool with regulated capacity payments - a clear gap for the "lessons for Korea" angle.

## 7. Dropped / not archived candidates (reason)
- Parra & Mauger 2022 Energy Policy (EU legal framework): not verifiable in session (search budget exhausted; OpenAlex/Crossref rate-limited).
- Sioshansi et al. 2022 TPWRS storage-modeling review (37(2):860-875): verified on CMU list but core content is modelling-review (overlaps S1/S2); not archived.
- Byers & Botterud 2020 IEEE TSTE 11(2):1106-1109 (VRE+storage capacity-value synergy): verified (OpenAlex), but a 4-page letter, closed access; thesis full text blocked (403).
- Mays 2021 Energy Policy (flexibility incentives) and Mays et al. capacity-market papers: bibliographic data could not be verified (OpenAlex/Crossref 429).
- Edwards, Sheehy, Dent & Troffaes 2017 SEGN (nightly rechargeable storage and capacity adequacy): not verifiable in session.
- Newbery 2018 Energy Policy (economics of storage): likely S1 core; not verified.
- Kim, Sioshansi et al. 2022 and 2025 TPWRS (capacity value): DOIs from CMU list but no full text/abstract read.
- Zheng, Xu et al. "Energy Storage State-of-Charge Market Model" (IEEE Trans. Energy Markets, Policy & Regulation): journal lacks settled SJR quartile; excluded under Q1 rule.
- Chen & Tong "Convexifying market clearing of SoC-dependent bids" (IEEE TPWRS letter, Xplore 10037211): venue volume/pages unverified; mentioned in lineage only.
- Tarel, Korpås & Botterud 2024 Energy Systems (long-run equilibrium, RES + storage only): SJR quartile not checked; excluded as lower priority (overlaps antweiler2025_newmeritorder).
