---
doc_id: gb_market_history_en
title: "GB electricity market structure and grid-scale batteries, 2010 → Oct 2026 (with 1990–2009 pre-history)"
compiled: 2026-10-07
audience: "Claude / machine reading. Korean narrative version: GB_market_history_KO.md (same event IDs)."
coverage: "~5 years before grid-scale battery entry (first GB grid-scale battery Dec 2014; commercial entry via the Aug 2016 EFR tender) to Oct 2026"
evidence: "Compiled from three parallel web-search passes (≈200 searches, snippet level only — no full documents opened; publisher, NESO, Ofgem and Elexon pages could not be fetched), plus repo data (data/README.md) and the literature archive. Every row carries a confidence tag."
confidence_legend: "H = date/number seen in a primary-source snippet (gov.uk, legislation.gov.uk, Ofgem, NESO/ESO, Elexon, EMR Delivery Body, EC); M = reputable secondary (Modo Energy, Current±, Energy-Storage.News, Solar Power Portal, law firms, trade press); L = inferred, derived or conflicting"
status: "Working reference. Items in §9 are unverified or conflicting. Re-check H/M items against primary documents before quoting numbers in a paper."
---

# GB market structure and grid-scale batteries — machine-readable history

## 0. How to use

- Event IDs (`E##`) are stable and shared with the Korean version. Cite them in notes, e.g. "E31 (EAC go-live)".
- Columns: `date` (YYYY-MM-DD where known) · `cat` (W = wholesale/market arrangements, B = balancing & imbalance, A = ancillary products, C = Capacity Market, N = network charges/regulation/planning, P = policy/institutions, F = fleet/revenue fact) · `rule change` · `battery mechanism` (why it matters) · `conf` · `src`.
- §1 gives the regime periodisation used throughout. §7 is the analysis. §8 maps it to the study design (`docs/01_next_actions.md`).

## 1. Regime periodisation (proposed for the study)

| regime | period | dominant battery revenue | defining rules | boundary events |
|---|---|---|---|---|
| R0 Pre-history | 1990–2009 | — (no grid-scale batteries) | Pool (1990) → NETA self-dispatch + BM + cash-out (2001) → BETTA (2005); STOR (2007) | E01–E04 |
| R1 Decarbonisation design | 2010–2015 | — (demonstrators only) | EMR: CPF (2013), CfD, CM (2014), EPS; P305 single cash-out (2015) | E05–E14 |
| R2 Contracted entry | 2016–2019 | EFR/FFR contracts + CM (high storage de-rating until Dec 2017) + embedded benefits/Triad | EFR tender (2016); CM de-rating cut (2017); P305 phase 2 (2018); wider BM access (2019); TCR decision (2019) | E15–E25 |
| R3 DC scarcity boom | Oct 2020–2022 | Dynamic Containment (+FFR): ≈90% of revenue | DC launch at £17/MW/h cap (2020); DC-H, EPEX EFA-block auctions (2021); DM/DR (2022); licensing/planning/charging reforms | E26–E36 |
| R4 Saturation & EAC | 2023–2024 | Collapse of frequency-response prices; shift to wholesale + BM | DC saturation (2023); EAC co-optimisation + negative prices (Nov 2023); OBP bulk dispatch (Dec 2023); BR, 30-min rule (Mar 2024); SoE rules (2024); QR (Dec 2024); skip-rate publication (Dec 2024) | E37–E50 |
| R5 Merchant & dispatch reform | 2025 → Oct 2026 | Wholesale + BM ≈60%, ancillary ≈1/3, CM ≈10% (2-h battery, 12 m to Apr 2026; Modo, per design v0 — not re-verified) | QR to non-BM, BR into EAC (2025); GC0166; REMA keeps national pricing (Jul 2025); Gate 2 connections (Dec 2025); SR replaces STOR (Mar 2026); CM price collapse (Mar 2026); FPN requirement for DR services (Jul 2026); LDES cap-and-floor | E51–E70 |

## 2. Master timeline

| ID | date | cat | event | rule change | battery mechanism | conf | src |
|---|---|---|---|---|---|---|---|
| E01 | 1990-04-01 | W | Privatisation; Electricity Pool starts (England & Wales) | Mandatory gross pool for plants ≥50 MW; CEGB split | Starting point of liberalised market | H | ofgem.gov.uk/sites/default/files/docs/1998/02/review-of-electricity-trading-arrangements-background-england-and-wales_0.pdf |
| E02 | 2001-03-27 | W/B | NETA replaces the Pool | Bilateral trading + self-dispatch; Balancing Mechanism (BM); imbalance settlement under the BSC (Elexon) | BM + cash-out are the core of today's battery merchant revenue; SO procures ancillary services separately (no central energy–reserve co-optimisation) | H | elexon.co.uk/about/about-ELEXON/ |
| E03 | 2005-04-01 | W | BETTA | NETA extended to Scotland → single GB market and price | Single national price (kept by REMA in 2025, E58) | H | elexon.co.uk |
| E04 | 2007-04 | A | STOR replaces Standing Reserve | Tendered reserve (≈3 tenders/yr, ≥1.8 GW target) | Pre-battery reserve product; later a battery revenue stream | M | ofgem.gov.uk 2007 demand-side note; strathprints 37021 |
| E05 | 2009-11-05 | B | P217A flagging live | System-management actions flagged/removed from cash-out (scope widened 2015) | Imbalance prices reflect energy balancing | H | elexon.co.uk P217 page |
| E06 | 2010-12 | P | DECC EMR consultation | Proposes CfD FiT, Carbon Price Floor (CPF), EPS, capacity mechanism | Baseline year | M | mondaq 141896 |
| E07 | 2011-07-12 | P | EMR White Paper "Planning our electric future" | Policy package: CPF, CfD, EPS, capacity mechanism | Design behind CM and CfDs | H | gov.uk planning-our-electric-future white paper |
| E08 | 2012-08 | B | Ofgem launches Electricity Balancing SCR (EBSCR) | Review of cash-out signals | Start of scarcity-pricing reform | M | ofgem.gov.uk EBSCR analysis 2018 |
| E09 | 2013-04-01 | P | Carbon Price Floor starts | Carbon Price Support on fossil fuels for power | Coal exit; gas sets the marginal price → spreads track gas | M | cms-lawnow 2014/03 |
| E10 | 2013-12-18 | P | Energy Act 2013 (Royal Assent) | Legal basis for CfD, CM, EPS (450 gCO2/kWh, s.57); RO closes to new entrants Apr 2017 | Legal basis of CM; EPS blocks unabated coal → flexibility from gas, storage, DSR | H | legislation.gov.uk/ukpga/2013/32 |
| E11 | 2014-03 | P | Budget 2014 freezes CPS | Carbon Price Support capped at £18/tCO2 (2016–2020; later extended to 2021) | Caps the carbon component of spreads | M | carbonbrief budget-2014 |
| E12 | 2014-05-15 | B | EBSCR final decision | Marginal pricing, single price, VoLL for demand control, reserve scarcity pricing — staged plan | Sharper, more marginal imbalance prices | H | ofgem.gov.uk EBSCR final policy decision |
| E13 | 2014-08-01 | C | Electricity Capacity Regulations 2014 (SI 2014/2043) in force | Capacity agreements, payments, penalties; technology-neutral auctions | Opens CM revenue | H | legislation.gov.uk/uksi/2014/2043 |
| E14a | 2014-12 (opened ~15 Dec) | F | UKPN Smarter Network Storage, Leighton Buzzard: 6 MW / 10 MWh | Network innovation funding (Ofgem LCNF) | **First GB grid-scale battery** (demonstrator) | M | pv-magazine 2014-12-15; innovation.ukpowernetworks.co.uk SNS |
| E14b | 2014-12-18 | C | First T-4 CM auction (2018/19) | Clears £19.40/kW/yr, ≈49.3 GW | Storage de-rated at ≈96% in early auctions | H | gov.uk provisional results 2014 |
| E14c | 2015-02-26 | P | CfD Allocation Round 1 results | 27 contracts, >2 GW | Start of CfD-backed VRE → spreads, negative prices | H | gov.uk CfD AR1 outcome |
| E14d | 2015-11-05 | B | **P305 phase 1** | Single cash-out price; PAR 500→50 MWh; VoLL £3,000/MWh for demand control; static Reserve Scarcity Price | Single price rewards "helpful" imbalance → basis of battery imbalance/merchant trading | H | elexon P305 guide; ofgem p305d |
| E15 | 2016-08-26 | A | **EFR tender results** | 201 MW, 8 projects (7 companies), 4-year contracts, £7.00–11.97/MW/h, £65.95m; 61 of 64 bids were batteries; full response ≤1 s | First product written for batteries + bankable 4-yr contract → first commercial wave | M | solarpowerportal; KPMG EFR briefing; cms.law |
| E16 | 2016 (Dec) | C | T-4 2020/21 | £22.50/kW/yr; storage de-rating 96.11% | Short-duration batteries over-credited | M | LCCC/EMR dashboards |
| E17 | 2017-06-15 | N | Ofgem CMP264/265 (WACM4) decision | Embedded-benefit (Triad) payments to small embedded generation cut ≈£47/kW → ≈£3–7/kW, phased Apr 2018–2020/21 | Removes Triad income for distribution-connected batteries | H | ofgem.gov.uk CMP264/265 decision |
| E18 | 2017-07 | P | Smart Systems and Flexibility Plan (BEIS/Ofgem) | 29 actions incl. storage licensing, double charging, planning | First official storage barrier-removal agenda | H (month) | gov.uk upgrading-our-energy-system July 2017 |
| E19 | 2017-12 | C | **CM storage de-rating cut** | Duration-based de-rating (NG Duration-Limited Storage assessment, LCP): 0.5 h ≈96% → ≈21% | Ends over-crediting; duration becomes the CM value driver | M | cms-lawnow 2017/12; LCP case study |
| E20 | 2018-02 | C | T-4 2021/22 (record low) | £8.40/kW/yr; 0.5 h storage 17.89% | CM revenue for 0.5–1 h batteries small | M | Burges Salmon |
| E21 | 2018-11-01 | B | **P305 phase 2** | PAR 50→1 MWh (marginal); VoLL £6,000/MWh; dynamic LoLP/RSP | Spikier imbalance prices → higher arbitrage/imbalance value | H | elexon P305 PIR |
| E22 | 2018-11-15 | C | EU General Court, Tempus v Commission | CM state-aid approval annulled → standstill (no auctions/payments) | CM income frozen ≈11 months | M | twobirds; fsr.eui.eu |
| E23 | 2019-02-28 / 2019-12-11 | B | P344 (Virtual Lead Party, secondary BMUs) RID 28 Feb; Wider Access to BM live 11 Dec | Independent aggregators/owners can register BMUs without a supply licence; trade press: BM threshold effectively 100 MW → 1 MW | Small and aggregated batteries can earn in the BM | H (dates) / M (threshold) | elexon P344 guidance; wider-access release |
| E24 | 2019-04-01 | P/N | NGESO legally separated from NGET; Wales removes storage from DNS "generating station" definition | SO independence; Welsh storage ≤350 MW consented locally | Groundwork for market-based balancing; easier consenting | H / M | ofgem gsr024; burges-salmon |
| E25 | 2019-10-24 / 2019-11-21 | C/N | EC re-approves CM (standstill ends); **Ofgem TCR final decision** | CM restored (back-payments). TCR: residual network charges → fixed charges on "Final Demand" only; Triad residual ends | Storage is not Final Demand → escapes residual charges; Triad no longer a value driver | H / H | Hansard 2019-10-24; neso TCR page |
| E26 | 2020-01 | A | Stability Pathfinder Phase 1 | 12 contracts, 12.5 GVA·s inertia, 6 yrs, £328m (synchronous condensers/flywheels; no batteries) | Inertia bought as a separate service | M | current-news |
| E27 | 2020-04 / Q2 | F | GB battery fleet passes 1 GW | — | — | M | energy-storage.news 2020 |
| E28 | 2020-10-01 | A | **Dynamic Containment (DC-Low) launch** | Post-fault fast response; soft launch ≤500 MW; daily pay-as-bid at £17/MW/h cap (≈£150k/MW/yr); 139 MW batteries in first auction; undersupplied (197 MW avg Oct 2020 vs 500 MW target) | Scarcity rent at the cap → boom | H/M | current-news DC first year; modo dc-ng-eso-needs |
| E29 | 2020-10-07 (eff. 2020-11-29) | N | Ofgem storage licensing decision | Storage defined as a subset of generation in the generation licence; condition E1 info to suppliers | Lets suppliers exempt storage imports from final consumption levies (RO, FiT) → reduces double charging | M | ofgem storage licensing decision |
| E30 | 2020-11 | P | CfD AR4 negative-price rule confirmed | No difference payment in any period with negative DA reference price (AR2/3: 6+ consecutive hours) | VRE curtails at negative prices → battery charging opportunities | M | gov.uk CfD bulletin 2020-11-24 |
| E31a | 2020-12-02 | N | Electricity Storage Facilities Order 2020 (SI 2020/1218) in force | Storage (ex pumped hydro) removed from NSIP/DCO (England 50 MW threshold) → local planning | Makes ≥100 MW battery projects practical | H | legislation.gov.uk/uksi/2020/1218 (Burges Salmon gives 28 Jul 2020 — conflict, see §9) |
| E31b | 2020-12-14 | N | CMP334 in force | "Final Demand" = electricity consumed other than for generation/export | Legal hook keeping storage imports out of residual charges | H | ofgem cmp334d |
| E32 | 2021-01-01 | W | Brexit: GB leaves EU day-ahead market coupling (SDAC) | Interconnector capacity sold in explicit auctions; GB data no longer on ENTSO-E (still on BMRS) | Less efficient interconnector flows → more GB volatility; data sourcing changes | H | epexspot SDAC/Brexit; elexon europe |
| E33 | 2021-01-27 / 2021-04-01 | A | DC + BM stacking allowed; STOR moves to day-ahead daily contracts | — | Short merchant-friendly contracts; stacking | M | solarpowerportal; neso 189221 |
| E34 | 2021-09-16 / 2021-11-01 | A | "DC 2.0": day-ahead EFA-block pay-as-clear auctions on EPEX; DC-High launch (cap £12/MW/h) | 4-hour EFA blocks, 6 blocks/day, pay-as-clear | Enables block-level stacking with wholesale | M | modo dc-2-first-week; modo dc update Nov |
| E35 | 2021–2022 | W | Wholesale price crisis | GB DA average £118.29/MWh (2021), £204.03/MWh (2022); N2EX DA record £539.59/MWh (23 Aug 2022) | Record spreads | M | EnAppSys 2022 GB summary |
| E36a | 2022-04-08 / 2022-05-06 | A | Dynamic Regulation (first auction 8 Apr), Dynamic Moderation (live 6 May) | DR: pre-fault, 10 s, 60-min energy; DM: 1 s, 30-min energy | Completes DC/DM/DR suite | M (H: Ofgem Art.18 approvals Mar 2022) | solarpowerportal |
| E36b | 2022-04-25 / 2022-03-10 | N | Ofgem approves CMP308 (BSUoS on Final Demand only from Apr 2023) and CMP343 (banded fixed TDR from Apr 2023) | Generators/storage stop paying BSUoS (≈£7/MWh saving for transmission-connected generators) | Removes the last transmission double-charging channel (effective 2023-04-01) | H | ofgem cmp308; cmp343 |
| E36c | 2022-07-18 | P | REMA consultation launched | Review incl. locational (nodal/zonal) pricing | Siting uncertainty for batteries until 2025 | H | gov.uk REMA launch |
| E36d | 2022-11 / 2023-01-01 | P | Electricity Generator Levy (45% on receipts above £75/MWh, 2023–2028) | Applies to nuclear, renewables, biomass; **storage excluded** | Battery windfall spreads not taxed | M | linklaters; deloitte taxscape |
| E36e | 2022 | F | Revenue peak | Modo index £156k/MW/yr; DC 63% + FFR 25%; fleet 1.93 GW / 2.24 GWh (avg 1.2 h) | Peak of R3 | M | modo 2022 review |
| E37 | 2023 (H1) | A | **DC saturation** | May 2023 DCL avg £1.37/MW/h (lowest since launch, 11th monthly fall); eligible DCH battery capacity 2,229 MW vs 1,099 MW requirement; fleet 2.66 GW | Supply outran a capped requirement → frequency-response rents collapse | M | modo revenue benchmark May 2023 |
| E38 | 2023-04-01 | N | BSUoS (Final Demand only) and banded fixed TDR take effect | see E36b | — | H | ofgem |
| E39 | 2023-10-06 | W | Ofgem approves P415 (VLP access to wholesale market; implemented 2024-11-07) | Virtual Trading Parties; supplier compensation | Aggregated/behind-the-meter flexibility trades without supplier | H / M | ofgem p415 decision; elexon |
| E40 | 2023-10-26 (storage clause eff. 2023-12-26) | N/P | Energy Act 2023 | "Stored energy" generation defined as subset of generation; legal basis for NESO | Statutory certainty for storage | M | nortonrosefulbright energy-act-2023 |
| E41 | 2023-10 / 2023-11 | A | Dynamic FFR retired (last monthly auction Oct 2023) | — | Legacy product ends | M | modo FFR final auction |
| E42 | 2023-11-02 | A | **EAC go-live** (platform 19 Oct; first auction 2 Nov 14:00 for 3 Nov) | DC/DM/DR co-optimised in one auction; £0 floor replaced by −£999.99…+£999.99/MW/h; first negative prices (DRH, DMH) | Stacking across response products in one clearing; negative availability prices for "high" products | H/M | neso EAC news; modo EAC launch |
| E43 | 2023-12-13 | B | **Open Balancing Platform (OBP) stage 1** | Bulk dispatch of many small BMUs/batteries; paused for batteries after 3 days, resumed 8 Jan 2024 | Directly targets battery under-dispatch (skips) | H/M | nationalgrideso first-stages-OBP |
| E44 | 2023 | F | Year outcome | Modo index £51k/MW/yr (−67%); fleet 3.5 GW / 4.6 GWh (1.5 GW added) | Trough begins | M | modo dec 2023; buildout q4 2023 |
| E45 | 2024-03-11 | B | **"15-minute rule" → "30-minute rule"** | MEL/MIL declared as the power sustainable for 30 min | More and longer BM dispatches (1.1→1.4 GWh/day; >15-min actions 5%→14%) | M | modo 30-minute rule |
| E46 | 2024-03-12 | A | **Balancing Reserve (BR) launch** (Ofgem approval 8 Feb) | BMUs >1 MW; day-ahead pay-as-clear; positive/negative over 48 half-hours; 30-min energy | New reserve revenue (≈400 MW PBR early), batteries dominant | H/M | neso BR news; modo BR |
| E47 | 2024-06/07 (effective date unverified) | A | **SoE rules for DC/DM/DR binding** | Recover ≥20% of contracted energy volume per settlement period after an event; insufficient energy at block start = unavailable | Limits over-stacking; requires headroom | M | modo frequency-response rule changes Jul 2024; ofgem decision page |
| E48 | 2024-10-01 | P | **NESO** launches (ESO bought for £630m) | Public independent system operator and planner | Runs connections reform, SSEP, balancing reform | H | neso launch news |
| E49 | 2024-10-10 / 2024-12-13 | P | LDES cap-and-floor decision; Clean Power 2030 Action Plan | Cap-and-floor (≈25 yr, Ofgem); 23–27 GW batteries + 4–6 GW LDES by 2030 (≈4.5 GW batteries at the time) | Revenue floor for ≥8 h storage; official volume targets | M / H | gov.uk clean-power-2030; freeths |
| E50 | 2024-12-03 / 2024-12 | A/B | **Quick Reserve Phase 1** (BM only; replaces Fast Reserve); NESO **skip-rate methodology + data** (from 15 Dec 2024) | QR: full output ≤1 min, co-optimised in EAC; 36 batteries won 95% of volume. Skip rates: "All BM" and "Post-System-Action" metrics | New fast-reserve rent; official skip transparency | H/M | neso QR; neso skip-rates |
| E51 | 2024 | F | Year outcome | Modo ≈£50k/MW/yr (Jan 36.6 record low → Dec 83.7); fleet 4.7 GW / 6.6 GWh; 67% of new builds 2 h | R4 trough and recovery via BM/wholesale | M | modo 2024 review |
| E52 | 2025-03-11 | C | T-4 2028/29 | £60/kW/yr; scaled EFC de-rating 1 h 10.47%, 2 h 20.94% | Duration-specific CM value | M | modo T-4 2028/29 |
| E53 | 2025-04-15 | N | Ofgem approves TMO4+ connections reform (Gate 2) | "First ready, first needed" queue | Culls speculative battery projects | M | ofgem TMO4 decision |
| E54 | 2025-07-10 | P | **REMA Summer Update** | Zonal pricing rejected; "Reformed National Pricing" (RNP) | No locational wholesale price for batteries; locational value via BM/constraints/siting levers | M | cms.law; hsfkramer |
| E55 | 2025-09-02 | A | QR Phase 2: non-BM units admitted | — | Opens QR to non-BM batteries | H | neso QR page |
| E56 | 2025-10-22 | B | Ofgem approves **GC0166** | New BM parameters MDO, MDB, FSoE for limited-duration assets; replaces the 30-minute rule; operational deadline 5 Nov 2026 | Batteries can declare real energy limits → fewer skips | H | ofgem GC0166 decision |
| E57 | 2025-10-29 | A | BR moves into the 14:00 EAC auction | BR co-optimised with QR and DC/DM/DR | Joint optimisation of reserve and response | H | neso EAC page |
| E58 | 2025-12-08 | N | NESO Gate 2 results | 283 GW offers (132 GW pre-2030); 83 GW battery offers; >150 GW battery capacity deprioritised/removed | Reshapes pipeline | M | energy-storage.news; solarpowerportal |
| E59 | 2025 | F | Year outcome | Modo ≈£70k/MW/yr (monthly 47–88); fleet 6.8 GW / 11 GWh (Modo, GB) vs 7.5 GW (DESNZ, UK); BM revenue record £27k/MW/yr (Feb 2025) | Merchant era | M / H | modo monthly; DESNZ battery statistics |
| E60 | 2026-03-11 | C | T-4 2029/30 £27.10/kW/yr; T-1 2026/27 £5/kW/yr | CM prices collapse; 4 h+ assets > half of de-rated battery prequalification | CM share of battery revenue falls; duration shift | M | modo T-4 2029/30; modo T-1 2026/27 |
| E61 | 2026-03-31 | A | **Slow Reserve** live; STOR ends (last auction 30 Mar) | SR: full delivery ≤15 min, sustain ≥120 min; first auction 1,800 MW, gas ≈75%, batteries ≤313 MW | Long-energy reserve favours gas and ≥2 h batteries | H/M | neso STOR page; modo SR day one |
| E62 | 2026-04 | P | DESNZ/Ofgem open letter on battery surplus; RNP Delivery Plan (21 Apr) | Gate 2 batteries 14.8 GW above 2030 range; options to restrain entry. RNP: BM threshold to 1 MW from 2027, FPN to match traded positions, aligned deadlines (decisions H2 2026) | Policy shifts from enabling to rationing battery entry; dispatch rules next | M | ofgem connections-reform-and-battery-capacity-update; gov.uk RNP plan |
| E63 | 2026-04-17 | A | Optional Fast Reserve ends | — | — | H | neso fast reserve |
| E64 | 2026-06 | A | Ofgem decision on NESO Dynamic Response Services amendments | 6 of 8 approved; tiered performance regime and unit suspension rejected | — | H | ofgem decision page |
| E65 | 2026-06-26 | P | LDES Window 1 minded-to decision | 16 projects ≈7.65 GW, 8–22 h; 11 are Li-ion; final decision expected autumn 2026 | Li-ion ≥8 h qualifies for cap-and-floor | M | hilldickinson; energy-storage.news |
| E66 | ~2026-07-01 | B | NESO switches on GC0166 in the control room | Phased; 5 units / 4 lead parties first | — | M | neso GC0166 news |
| E67 | by 2026-07-31 | A | DR-service changes, batch 1 | A BMU with FPN flag FALSE or no valid FPN is unavailable for DC/DM/DR; pre-approved baseline if also in stability services | Ties response availability to BM physical notifications | H/M | ofgem decision effective-by-31-July-26; ess-news 2026-07-06 |
| E68 | 2026 (to Aug) | F | Year to date | Modo monthly £41–70k/MW/yr; fleet 7.2 GW / 11.8 GWh (Q1), 7.6 GW (Q2); Feb 2026 wholesale revenue negative for first time; Jul 2026 wholesale record | — | M | modo 2026 monthly; buildout Q1/Q2 2026 |
| E69 | 2027-01-01 (approved) | A | DR-service changes, batch 2 | Non-BM units must submit operational metering and baseline data | — | H | ofgem decision effective 1 Jan 2027 |
| E70 | 2027-05 (planned) | W | MHHS migration completion (started 2025-10-22) | Market-wide half-hourly settlement | Time-of-use tariffs and aggregated flexibility | H (plan) | ofgem CR055 |

## 3. Product specifications (frequency response and reserve)

| product | type | response time | trigger / deadband | energy requirement | procurement | block | live | conf |
|---|---|---|---|---|---|---|---|---|
| EFR | response | detect ≤0.5 s, full ≤1 s | Service 1 ±0.05 Hz; Service 2 ±0.015 Hz | not found | one-off tender, 4-yr, pay-as-bid £7–11.97/MW/h | — | contracts from 2016 tender (E15) | M |
| FFR (dynamic/static) | response | dynamic primary 10–30 s, secondary 30 s–30 min, high 10 s–indef.; static primary 10 s–30 min | dynamic proportional; static trigger | as response window | monthly tenders (+weekly trial) | EFA blocks | start date not verified; dynamic FFR retired Nov 2023 | H (specs) / L (start) |
| DC (L/H) | post-fault response | ≤0.5 s initial, full ≤1 s | 0% within ±0.015 Hz; linear to 5% at ±0.2 Hz knee; linear to 100% at ±0.5 Hz | 15 min at contracted MW (REV = 0.25 h × MW) | 2020 daily pay-as-bid (cap £17); Sep 2021 EPEX EFA-block pay-as-clear; Nov 2023 EAC | 4-h EFA | DCL 2020-10-01; DCH 2021-11-01 | H |
| DM (L/H) | pre-fault | full ≤1 s | ±0.015 Hz deadband; 5% at ±0.1 Hz knee; 100% at ±0.2 Hz | 30 min | EPEX D-1 → EAC | EFA | 2022-05-06 | H |
| DR (L/H) | pre-fault | full ≤10 s | ±0.015 Hz; linear to 100% at ±0.2 Hz | 60 min | EPEX D-1 → EAC | EFA | 2022-04-08 | H |
| BR (P/N) | reserve | to contracted output ≤10 min | BM instruction | 30 min (1-h battery ⇒ SoC ≥50%) | D-1 pay-as-clear; from 2025-10-29 in 14:00 EAC | 48 half-hours | 2024-03-12 | M |
| QR (P/N) | reserve (pre-fault) | full ≤1 min, notice 0 min | instruction | ≈13–15 min hold (sources conflict, §9); recovery ≤3 min | EAC co-optimised 14:00 | half-hours | BM 2024-12-03; non-BM 2025-09-02 | M/H |
| SR (P/N) | reserve (post-fault) | full ≤15 min | instruction | sustain ≥120 min; recovery ≤60 min | daily D-1 auction | windows ≥2 h (+30-min) | 2026-03-31 (replaces STOR) | H |
| Common DC/DM/DR rules | — | — | — | SoE: recover ≥20% of REV per SP; unavailable if insufficient energy at block start (2024); FPN required for BMUs (Jul 2026) | stacking/splitting allowed in EAC | — | — | M/H |

## 4. Fleet and revenue by year

| year | GB battery fleet | Modo index £k/MW/yr | main revenue | conf |
|---|---|---|---|---|
| 2014 | 6 MW / 10 MWh demonstrator (SNS) | — | network services | M |
| 2016 | <100 MW | — | — | M |
| 2017 | ≈100 MW (≈50 sites ≥250 kW, Nov 2017) | — | EFR, FFR | M |
| 2018 | ≈0.5–0.6 GW (derived) | — | EFR, FFR, CM, Triad | L |
| 2019 | 0.7–0.9 GW (sources conflict) | — | FFR | L |
| 2020 | >1 GW (Q2), ≈1.2 GW year end | 65 | frequency response (DC from Oct) | M |
| 2021 | ≈1.3–1.4 GW | 123 | DC | M/L |
| 2022 | 1.93 GW / 2.24 GWh (avg 1.2 h) | **156** | DC 63% + FFR 25% | M |
| 2023 | 3.5 GW / 4.6 GWh | 51 (−67%) | FR collapse → wholesale + BM | M |
| 2024 | 4.7 GW / 6.6 GWh (67% of new builds 2 h) | ≈50 | wholesale + BM rising; BR, QR | M |
| 2025 | 6.8 GW / 11 GWh (Modo, GB); 7.5 GW (DESNZ, UK) | ≈70 | wholesale + BM | M/H |
| 2026 YTD | 7.2 GW / 11.8 GWh (Q1); 7.6 GW (Q2) | 41–70 (monthly) | wholesale records; BM weak (Aug) | M |

Caveats: Modo re-based and renamed its index ("ME BESS GB", 2025); some monthly figures exclude CM; do not chain values across vintages. Fleet definitions differ (Modo GB commercial vs DESNZ UK energised vs Solar Media UK ≥250 kW). Modo states frequency response was "nearly 94% of BESS revenues since Jan 2020" (vs design v0's 87% for 2020–22, not verified).

## 5. Capacity Market outcomes

| auction (delivery) | held | £/kW/yr | storage de-rating | battery outcome | conf |
|---|---|---|---|---|---|
| T-4 2018/19 | Dec 2014 | 19.40 | ≈96% (single storage factor) | negligible | M/H |
| T-4 2019/20 | Dec 2015 | 18.00 | ≈96% | — | M |
| T-4 2020/21 | Dec 2016 | 22.50 | 96.11% | large battery wins (not quantified) | M |
| T-1 2018/19 | early 2018 | 6.00 | 0.5 h 21.34% (post-cut) | — | M |
| T-4 2021/22 | Feb 2018 | 8.40 | 0.5 h 17.89% | 4.5 GW nameplate → <1.3 GW de-rated (both auctions) | M |
| (standstill) | Nov 2018 – Oct 2019 | — | — | — | M/H |
| T-1 2019/20 (replacement) | Jun 2019 | 0.77 | — | — | M |
| T-3 2022/23 | Jan 2020 | 6.44 | — | — | M |
| T-4 2023/24 | Mar 2020 | 15.97 (one source 15.40) | — | 117 MW | M/L |
| T-4 2024/25 | Mar 2021 | 18.00 | — | 252 MW | M |
| T-1 2021/22 | Mar 2021 | 45.00 | — | 114 MW | M |
| T-1 2022/23 | Feb 2022 | 75.00 (cap) | — | — | M |
| T-4 2025/26 | Feb 2022 | 30.59 | 2 h 0.397 (repo data) | ≈1 GW new-build batteries | M |
| T-1 2023/24 | Feb 2023 | 60.00 | — | — | M |
| T-4 2026/27 | Feb 2023 | 63.00 | ≈1 h 12%, 2 h 24% | 1.29 GW | M |
| T-4 2027/28 | Feb 2024 | 65.00 (record) | 1 h 8%, 2 h 15% (repo: 0.154) | ≈1 GW new build | M |
| T-1 2024/25 | Feb 2024 | 35.79 | — | 655 MW | M |
| T-4 2028/29 | Mar 2025 | 60.00 | scaled EFC: 1 h 10.47%, 2 h 20.94% | 1.78 GW | M |
| T-1 2025/26 | Feb/Mar 2025 | 20.00 | 1 h 13.64%, 2 h 27.15% | 725 MW (record) | M |
| T-4 2029/30 | Mar 2026 | **27.10** | 2 h 0.220 (repo data); 4 h 41.74% (L) | 1.2 GW de-rated; 4 h+ >½ of de-rated battery prequalification | M |
| T-1 2026/27 | Mar 2026 | **5.00** | — | ≈1 GW prequalified | M |

Repo cross-check (`data/raw/cm_derating_factors.csv`, `data/README.md` §2.2): 2 h de-rating 0.567 (T-4 2022/23) → 0.397 (2025/26) → 0.154 (2027/28) → 0.220 (2029/30).

## 6. Repo data anchors (computed from `data/raw/`, see `data/README.md`)

- EAC 2023-11-02 → 2026-10-06, 12 products, no gaps. Median clearing (£/MW/h): DCL 2.15, DCH 1.46, DML 5.05, DMH 0.11, DRL 10.94, DRH −5.66 (85% negative), PQR 3.46, PBR 2.14, PSR 2.16.
- "Sell one product 24/7" annualised value (k£/MW/yr, FY2025): DCL 28.2, DML 54.4, DRL 124.0, PQR 38.8, PBR 35.6, PSR 96.6 — upper bounds only (volume caps, energy requirements).
- 2026-09 perfect-foresight arbitrage on MID, 2 h, £10/MWh throughput cost: ≈£74k/MW/yr; on imbalance price ≈£161k (not tradeable).

## 7. Analysis — which rules made GB batteries a business

### 7.1 Causal chain (system need → product → revenue)

1. **Decarbonisation created the need.** EMR (E07–E14c: CPF, CfD, EPS) drove coal exit and VRE growth → lower inertia and larger frequency deviations → the SO needed faster response than thermal plant provides. Batteries are the cheapest sub-second resource.
2. **NETA's architecture created the shape of the opportunity.** Self-dispatch, bilateral trading and a separate BM (E02) mean the SO buys ancillary services as **explicit, separately priced products** rather than co-optimising them inside a central energy market (US ISO style). A battery can therefore earn a clean availability fee per product — and later stack products (E33, E42).
3. **Product design + contract form triggered entry.** EFR (E15) was written for sub-second response and paid 4-year availability contracts → bankable revenue → first commercial wave. DC (E28) then priced a scarce product at a cap (£17/MW/h) → scarcity rent → 2020–22 boom (index 65 → 123 → 156).
4. **Removing cost and permission barriers mattered as much as new revenue.** Licensing as generation (E29, E40), the TCR/Final Demand definition (E25, E31b), BSUoS on demand only (E36b), NSIP removal (E31a) and the EGL exclusion (E36d) removed double charges and consenting limits that would otherwise have cut margins and project size. Embedded-benefit cuts (E17) removed one early revenue source (Triad) at the same time.
5. **Sharper scarcity pricing created the merchant base.** Single, marginal cash-out with VoLL £6,000/MWh (E14d, E21) plus wider BM access (E23) gave batteries a revenue stream that does not saturate as quickly as capped-volume response products.
6. **Saturation ended the scarcity rent.** DC volume is set by system need (≈1–1.5 GW), not by supply. Once the fleet exceeded it (2,229 MW eligible vs 1,099 MW required for DCH in May 2023), clearing prices fell >90% (E37) → index −67% (E44). EAC co-optimisation and negative prices (E42) lowered response prices further.
7. **Profitability now depends on dispatch access, not product scarcity.** Revenue moved to wholesale + BM (R5). The binding rules are BM access and control-room practice: OBP bulk dispatch (E43), 30-min rule (E45), skip-rate transparency (E50), GC0166 MDO/MDB/FSoE (E56, E66), FPN requirement (E67), BM threshold to 1 MW (E62).
8. **Capacity accreditation steers duration.** Duration-based de-rating (E19) and scaled EFC (E52) cut 2 h credit from 0.567 to ≈0.22, while CM prices fell to £27.10 (T-4) and £5 (T-1) in 2026 (E60). Combined with SR's 2-hour sustain requirement (E61) and LDES cap-and-floor admitting ≥8 h Li-ion (E65), the rule set is pushing new builds from 1–2 h toward 4 h+.
9. **Policy is turning from enabling to rationing.** Gate 2 (E53, E58) and the 2026 battery-surplus letter (E62) show that once entry is profitable and queues are long, the binding constraint becomes grid connection, not market rules.

### 7.2 Regime-dependent rule value (hypotheses to test)

| rule (switch) | value in R3 (2020–22) | value in R4–R5 (2023–26) | why |
|---|---|---|---|
| Fast frequency product exists (DC/DM/DR) | very high (scarcity at cap) | low (saturated; DRH/DMH often negative) | capped requirement vs growing fleet |
| Procurement format (pay-as-bid cap → pay-as-clear EFA blocks → EAC co-optimisation) | moderate (stacking per block) | moderate–high for *allocation*, lowers prices | co-optimisation raises flexibility but intensifies competition |
| Stacking/splitting permission | high (DC + BM from 2021) | high (core of EAC) | lets one MW earn several fees |
| SoE rules (20% recovery) | n/a (guidance) | negative (cost) but small? | binds only when stacking aggressively |
| Single marginal cash-out + VoLL | moderate | high (merchant base) | value grows as VRE volatility rises |
| BM access & dispatch practice (wider access, 30-min rule, OBP, GC0166, FPN) | low–moderate | **high** (BM ≈ main growth lever; skip rate costs ≈7% profit per +10 pp per Gale 2026) | revenue base shifted to BM |
| Network-charge rules (TCR, BSUoS, licensing) | high (cost removal) | high (sustained) | removes £/MWh costs on every cycle |
| CM de-rating | moderate pre-2017 (over-credit), low after | low and falling (price collapse 2026) | duration-based accreditation |
| Contract length (EFR 4-yr vs daily auctions) | high for entry finance (2016–19) | low (merchant/tolling instead) | bankability |

### 7.3 Lessons stated cautiously (for the paper's discussion)

- **Entry vs sustainability.** Scarce, purpose-built fast products with long contracts were the entry catalyst; long-run profitability rests on energy-market access rules (cash-out design, BM dispatch). This matches Landy et al. 2026 ("market access > location", `landy2026_hybridstacking`).
- **Small ancillary markets saturate fast.** GB DC went from undersupplied (Oct 2020) to saturated (H1 2023) in ≈2.5 years with ≈2 GW of entry. Any late-adopter market with a capped fast-reserve requirement should expect the same.
- **The price-taker assumption is regime-dependent.** It is defensible for one 50 MW battery in wholesale markets, but not for the fleet in DC after 2022 or in the BM after 2024 (Dalton & O'Sullivan 2026, WATCHLIST C4).
- **Cost-side rules are part of "market design".** Counterfactuals should include charging/licensing rules, not only revenue products.

## 8. Mapping to the study design (`docs/01_next_actions.md`)

- **Regime split for RQ2 (fixes M1):** simulate R3 (Sep 2021 – Oct 2023, EPEX-era DC/DM/DR data needed) and R4–R5 (Nov 2023 →, EAC data in repo). Report rule values per regime.
- **Event-study dates (M3 supplement):** E28 (2020-10-01), E34 (2021-09-16), E37 (H1 2023), E42 (2023-11-02), E43 (2023-12-13), E45 (2024-03-11), E46 (2024-03-12), E47 (2024 SoE), E50 (2024-12-03), E55 (2025-09-02), E57 (2025-10-29), E61 (2026-03-31), E66/E67 (Jul 2026).
- **Candidate Shapley players (M4):** {fast-response suite exists; EAC co-optimisation/splitting; SoE rule; reserve products BR/QR; BM access/dispatch rules}. Treat CM de-rating and network charges as additive layers outside Shapley; duration (1 h/2 h/4 h) as a scenario dimension.
- **Data gaps implied:** pre-EAC DC results (2020–23), pre-Oct-2025 BR auctions, 1-s frequency, unit-level EAC (`--units`), BOD/BOALF for battery BMUs, DA auction prices (paid; MID as proxy).

## 9. Unverified or conflicting claims

1. FFR start date (monthly tenders existed by 2015; earlier start not confirmed); first battery FFR contract.
2. EFR applied volume (">1.5 GW" vs "4,311 MW of battery bids").
3. SoE rules: exact date they became binding (2024).
4. DC procured volume time series after mid-2022 (only point values).
5. Interim PAR 250 MWh (winter 2014/15): planned, implementation not confirmed.
6. Wider Access "BM threshold 100 MW → 1 MW" is trade-press wording.
7. TCR transmission residual start: Apr 2022 vs Apr 2023 (Ofgem CMP343 decision indicates Apr 2023).
8. BR auction time (08:15 vs 08:45 before the move to 14:00 EAC).
9. QR minimum activation (≈13 min vs 15 min vs "≤5 min").
10. Planning: England storage NSIP removal in force 2020-07-28 (Burges Salmon) vs 2020-12-02 (legislation.gov.uk; used here).
11. Which code modifications removed residual DUoS/BSUoS for storage "from 2021" (believed CMP281, DCP341, P383) and why Ofgem rejected CMP280 (2021-06-30).
12. Energy Act 2023 storage clause effective date (single secondary source).
13. Fleet totals 2016, 2018, 2019, 2021 (derived or conflicting).
14. Modo revenue shares quoted in design v0 (87% FR 2020–22; 60/33/10 split for 12 m to Apr 2026) and BM skip rates 49% (H1 2025) → 38% (H1 2026) (ESS News, July 2026) — not re-verified in this pass.
15. GB DA annual averages other than 2021–22; negative-price hours by year; DC price path (only point values: £17 cap 2020–21, £1.37 May 2023, £1.49/£2.90 Aug 2023).
16. CM 2029/30 1 h and 2 h de-rating (repo data gives 2 h 0.220; search synthesis gave only 4 h 41.74% and 8 h 83.78%, L).
17. Events Jul–Oct 2026 beyond E66–E67 (final LDES awards, RNP balancing decisions, MHHS progress).

## 10. Academic anchors (for citations; see `literature/DOWNLOAD_LIST.md` §4)

- Grubb & Newbery (2018) *Energy Journal* 39(6) — EMR evaluation (`grubb2018_ukemr`, abstract-level).
- Newbery (2016) *Energy Policy* 94:401–410 — capacity auctions; Newbery (2018) *Energy Policy* 113:711–720 — storage economics (GROUPS §12, OpenAlex-verified).
- Staffell & Rustomji (2016) (`staffell2016_maxvalue`); Gale et al. (2026) (`gale2026_balancingbatteries`); Landy et al. (2026) (`landy2026_hybridstacking`); Martins & Miles (2021) (`martins2021_ukbusinessmodels`).
- Greenwood et al. (2017), Gündoğdu et al. (2018), Lee et al. (2019), Cao et al. (2024), Fan et al. (2025) — GB frequency products (S6).
- No peer-reviewed article on P305 itself was found; cite Ofgem/Elexon documents.
- Further candidates from memory (verify first): Staffell (2017) *Energy Policy* 102:463–475; Green & Staffell (2016) *OXREP* 32(2); Newbery (2016) *Applied Energy* 179; Bunn & Yusupov (2015) *Energy Policy* 82; Pollitt & Anaya (2016) *Energy Journal* 37(SI2).

## 11. Source keys (main URLs)

- NESO EAC: https://www.neso.energy/industry-information/balancing-services/enduring-auction-capability-eac
- NESO DC documents: https://www.neso.energy/document/173206/download ; Dynamic Response guidance v13: https://www.neso.energy/document/276606/download
- NESO QR: https://www.neso.energy/industry-information/balancing-services/reserve-services/quick-reserve ; STOR: https://www.neso.energy/industry-information/balancing-services/reserve-services/short-term-operating-reserve-stor ; skip rates: https://www.neso.energy/industry-information/balancing-services/skip-rates
- Ofgem GC0166: https://www.ofgem.gov.uk/sites/default/files/2025-10/Grid%20Code%20GC0166%20-%20Introducing%20new%20Balancing%20Mechanism%20Parameters%20for%20Limited%20Duration%20Assets.pdf
- Ofgem DR-service amendments (Jul 2026): https://www.ofgem.gov.uk/sites/default/files/2026-06/Decision-to-approve-Dynamic-Response-Services%20proposed-amendments-to-the-Terms-and-Conditions-related-to-Balancing-Effective-by-31-July-26.pdf
- Ofgem CMP308: https://www.ofgem.gov.uk/decision/cmp308-removal-bsuos-charges-generation ; CMP343: https://www.ofgem.gov.uk/sites/default/files/2022-03/CMP343%20Decision.pdf ; CMP264/265: https://ofgem.gov.uk/decision/decision-industry-proposals-cmp264-and-cmp265-change-electricity-transmission-charging-arrangements-embedded-generators
- Elexon P305: https://assets.elexon.co.uk/wp-content/uploads/sites/11/2017/03/28161701/Increase-your-understanding-of-P305.pdf ; P344: https://www.elexon.co.uk/bsc/change/releases/p344-implementation-guidance-project-terre-wider-access/
- legislation.gov.uk: Energy Act 2013 https://www.legislation.gov.uk/ukpga/2013/32 ; SI 2014/2043 ; SI 2020/1218 https://www.legislation.gov.uk/uksi/2020/1218/made
- gov.uk: EMR White Paper; CM 2014 provisional results https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/389832/Provisional_Results_Report-Ammendment.pdf ; Clean Power 2030 https://www.gov.uk/government/publications/clean-power-2030-action-plan ; RNP Delivery Plan https://www.gov.uk/government/publications/reformed-national-pricing-rnp-delivery-plan ; DESNZ battery statistics https://assets.publishing.service.gov.uk/media/6a3ea42433bc5beefd3c4bdb/Grid-scale_battery_storage_statistics.pdf
- Modo Energy (revenue, buildout, CM): https://modoenergy.com/research (articles named in the rows)
- EFR tender: https://www.solarpowerportal.co.uk/battery-storage/battery-assets-lead-winning-projects-in-national-grid-tender
- REMA summer update: https://cms.law/en/gbr/legal-updates/rema-summer-update-zonal-pricing-out-reformed-national-pricing-in
