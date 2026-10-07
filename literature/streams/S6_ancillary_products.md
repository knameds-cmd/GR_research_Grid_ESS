# S6 — Ancillary products: how frequency-response / reserve product rules shape battery operation and economics

Stream scope: papers where a battery provides a *specific* frequency-response or reserve product and the product specification (activation curve, deadband, response time, energy/endurance requirement, SoC-recovery route, performance measurement, penalties, procurement format) is modelled explicitly. Regions: GB, Continental Europe/Germany, Nordics, US (PJM; CAISO not covered), Australia NEM.

Papers written by this stream (13): oudalov2007_pfcsizing, greenwood2017_efrservicedesign, gundogdu2018_efrtriad, lee2019_closedloopgb, cao2024_dcvsefr, fan2025_dccolocatedreforms, thien2017_fcrgermanystrategy, engels2019_fcrgermanytechnoeco, koltermann2022_fcrbalancinggroup, celicortes2025_deterministicfreq, engelhardt2022_fcrnrecovery, xu2018_regdparticipation, gilmore2024_lcofcas.

Related files from other streams that carry S6 content: he2016_pbrcyclelife (S4), shi2019_cycleagingpfp (S4), mirzaeialavijeh2025_swedenfcrstacking, engels2020_fcrpeakshaving and namor2019_multiservicecontrol (S2), cheng2018_multiscaledp (S2), rangarajan2023_batteryfcasdid and tabari2020_payforperformance (S8).

Evidence level: full text read for gundogdu2018, lee2019, fan2025, engels2019, xu2018_regdparticipation, gilmore2024 (working-paper version). The rest are from the abstract only; see `evidence_read` in each file.

---

## 1. Overview

The literature splits into three generations.

1. **Feasibility and sizing for symmetric proportional products (2007–2017).** oudalov2007 asked how small a battery can be while still supplying UCTE primary control continuously. Its answer was SoC-dependent limits plus an energy sink (resistors). The German line (thien2017, then engels2019) formalised the TSO "degrees of freedom": the ±10 mHz deadband, 20% over-fulfilment, set-point (schedule) trades on intraday markets, and the 30-min (later 15-min) energy criterion. It showed that these rules, not cell chemistry, decide feasibility and optimal sizing.
2. **Products designed for storage (GB 2016–2024).** GB EFR (2016) was the first product written with batteries in mind: 1 s response, an envelope with ±9% freedom inside the deadband, and a 30-min rest after 15-min events (greenwood2017, gundogdu2018, lee2019). Dynamic Containment (2020–) succeeded it as the main fast product. DC has a ±0.015 Hz deadband with only 5% delivery up to the ±0.2 Hz knee (100% at ±0.5 Hz) [corrected 2026-10-07], a 15-min Minimum Energy Requirement, State-of-Energy rules with baselines notified 1 h ahead, and an all-or-nothing payment per EFA block (fan2025, cao2024). The rule changes moved the binding constraint from envelope compliance to energy/baseline management.
3. **Performance-based and settlement design (US, DE, NEM).** In PJM RegD under FERC Order 755, the mileage and performance-score rules set the optimal cycle depth and the product mix (he2016, xu2018_regdparticipation, shi2019). tabari2020 finds the rule itself raised the probability of storage deployment by about 37%. In Germany, the implicit settlement of FCR energy through the balancing group adds €0.3–1.1k/MW/month (koltermann2022). In the NEM, the energy content of each product (regulation versus contingency) fixes the optimal battery duration and the long-run price (gilmore2024). Mandatory unpaid PFR consumes 3–4% of warranted cycles.

Across regions, the recurring result is that **the binding constraint is set by the product's energy/endurance and SoC-recovery rules**, and this constraint sets the optimal power/energy ratio:
- FCR DE: 1.6 MW / 1.6 MWh per MW (engels2019).
- DC: about 16 min of energy per MW (fan2025).
- NEM regulation: 3–4 h (gilmore2024).
- PJM RegD: about 0.3 h (xu2018_regdparticipation case).

The capacity price then sets profitability (engelhardt2022: "capacity payment is the strongest factor").

## 2. Lineage

```
Oudalov 2007 (ABB, UCTE PFC sizing)
 ├─ RWTH Sauer: Thien 2017 (M5BAT, degrees of freedom) → Koltermann 2022 (balancing-group energy) → Celi Cortés 2025 (deterministic freq. deviations)
 ├─ KU Leuven Deconinck: Engels 2019 (SAA + chance-constrained FCR control/sizing) → Engels 2020 TSG (FCR + peak shaving, S2)
 ├─ DTU Marinelli: Engelhardt 2022 (Nordic FCR recovery routes) → Cao 2024 (GB DC vs EFR, with Lancaster)
 └─ (EPFL Paolone: Namor 2019, S2)
GB service design: Greenwood 2017 (Newcastle/Taylor) → Gundogdu 2018 (Sheffield/Stone, EFR+Triad) → Lee 2019 (Sheffield/Brown + Mac Dowell, closed-loop EFR+STOR) → Cao 2024 / Fan 2025 (DC reforms, Strathclyde)
US PBR: FERC 755 → He 2016 (Tsinghua/Kang + Pinson) → Shi 2019 / Xu 2018 (UW Kirschen/Zhang) ; Tabari 2020 (empirical policy effect)
NEM FCAS: Gilmore, Nolan & Simshauser 2024 (levelised FCAS cost) ; Rangarajan 2023 (empirical price impact, S8)
Nordic: Engelhardt 2022 (DK) ; Mirzaei Alavijeh 2025 (SE FCR-N/FCR-D, Chalmers)
```

## 3. Groups

| Group | Region | Papers |
|---|---|---|
| ABB Corporate Research (Oudalov) | CH/UCTE | oudalov2007 |
| Sauer, ISEA/PGS RWTH Aachen (+ Moser IAEW) | DE | thien2017, koltermann2022, celicortes2025 |
| Deconinck, KU Leuven/EnergyVille (+ REstore) | DE | engels2019, engels2020 |
| Marinelli, DTU Wind & Energy Systems | Nordic, GB | engelhardt2022, cao2024 |
| Taylor, Newcastle | GB | greenwood2017 |
| Stone/Foster/Gladwin, Sheffield (Willenhall BESS) | GB | gundogdu2018 |
| Brown (Sheffield) + Mac Dowell (Imperial) | GB | lee2019 |
| Campos-Gaona, Strathclyde | GB | fan2025 |
| Kirschen & B. Zhang, Univ. of Washington | US PJM | xu2018_regdparticipation, shi2019, xu2018_cycleagingcost |
| Kang/Chen, Tsinghua + Pinson (DTU) | US PJM | he2016 |
| Simshauser, Griffith/EPRG | AU NEM | gilmore2024 |
| Le Anh Tuan/Steen, Chalmers | SE | mirzaeialavijeh2025 |

## 4. Region × product table

| id | year | region | product | frequency / signal data | SoC strategy | key finding |
|---|---|---|---|---|---|---|
| oudalov2007_pfcsizing | 2007 | UCTE/CH | PFC (FCR), symmetric | historic measured frequency (details unverified) | adjustable SoC limits + emergency resistors | minimum-size lead-acid BESS can be profitable at European PFC prices |
| thien2017_fcrgermanystrategy | 2017 | DE | FCR (pre-2019 rules) | CE frequency histogram (unverified) | deadband use, over-fulfilment, intraday schedule transactions | speed/flexibility of recharge decides feasibility; 30-min criterion should be relaxed |
| engels2019_fcrgermanytechnoeco | 2019 | DE | FCR (±200 mHz, ±10 mHz db, 30-min crit., weekly pay-as-bid) | CE frequency 2014–2017 at 10 s; 140,256 one-day samples | P-controller (gain, SoC set-point, deadband, ≤20% over-delivery) + 15-min intraday recharge (100 kW steps) | optimum 1.6 MW/1.6 MWh per MW; payback 3.6–7.1 y; calendar ageing dominates |
| koltermann2022_fcrbalancinggroup | 2022 | DE | FCR + balancing-group settlement | field data, 6 MW BESS | degrees of freedom → 8.68–9 MWh/MW/month extra charge/discharge | +€302–1,068/MW/month from reBAP settlement |
| celicortes2025_deterministicfreq | 2025 | DE/CE | FCR | CE frequency 2014–2023 | rule-based management of deterministic deviations | +37% high-magnitude deviations by 2023; strong seasonality → single-year back-tests biased |
| engelhardt2022_fcrnrecovery | 2022 | DK/Nordic | FCR-N | 3 years frequency + prices + tariffs | hourly reference via intraday vs imbalance settlement vs Energinet exemption | exemption best; otherwise imbalance settlement beats intraday; capacity price dominates profit |
| mirzaeialavijeh2025_swedenfcrstacking (S2) | 2025 | SE | FCR-N, FCR-D up/down + DA | Fingrid 1-min 2022 | MILP perfect foresight with LER endurance rules | €708k/yr per 1 MW/1 MWh (2022); FCR-D up+down stacking dominant |
| greenwood2017_efrservicedesign | 2017 | GB | EFR (+ existing services) | high-res. GB frequency (unverified) | service envelope / deadband design | services should be designed around storage; PHIL shows 80 ms response |
| gundogdu2018_efrtriad | 2018 | GB | EFR Service-2 (±0.015 Hz) + Triad | NGET 1-s, 5 days 2014–2015 | envelope-line selection, SoC band 45–55%, 30-min rest after 15-min event, ±9% recharge | 100% availability vs 98% (SoC hits 0) without rest rule; Triad £2.6–3.8k/event |
| lee2019_closedloopgb | 2019 | GB | EFR + STOR | NG 1-s, week of 1 Jun 2015, closed loop | SoC band 47.5–52.5% at ±9%; 90% pre-STOR | cycles/day fall 2.8→0.9 as fleet grows 100→400 MW; STOR adds 20–80% DoD cycles |
| cao2024_dcvsefr | 2024 | GB | DC vs EFR | GB frequency (unverified) | DC SoC management with delay | wrong SoC-mgmt timing → SoC oscillation; well-tuned DC beats EFR on frequency quality and degradation |
| fan2025_dccolocatedreforms | 2025 | GB | DC LF/HF (EFA blocks, SoE rules) | NGESO frequency 2016–2019 | baselines restoring ≥20% MER/SP, footroom/headroom targets | optimum ~16 min energy; NPV £17.9–41.9m; HF-only best; break-even £5.3/MW/h |
| he2016_pbrcyclelife (S4) | 2016 | US PJM | RegD PBR + energy + spin | PJM RegD 4 s, 4–10 May 2014 | DoD-aware hourly bidding | without mileage pay income −25%; optimal duration ~1.5 h (full text checked by S6) |
| xu2018_regdparticipation | 2018 | US PJM | RegD (capability + mileage, score ≥0.7) | PJM RegD 2013–14 and 2016–17 | threshold on cycle depth (marginal ageing = marginal performance) | +14% profit, life 26→42 months; score/ageing trade-off |
| shi2019_cycleagingpfp (S4) | 2019 | US PJM | pay-for-performance regulation | PJM signals | rainflow-aware online control | >30% cost saving, 3–4× life |
| tabari2020_payforperformance (S8) | 2020 | US ISOs | FERC 755 PfP | — (project data) | — | PfP raised storage-deployment likelihood ~37% |
| gilmore2024_lcofcas | 2024 | AU NEM | regulation, 6 s/60 s/5 min contingency, FFR | NEM 4-s 2020; prices 2003–2021 | — (cost side) | battery LCoFCAS ~$30→20/MW/h (reg.), $7–10 (cont.); 3–4 h optimal for regulation |
| rangarajan2023_batteryfcasdid (S8) | 2023 | AU NEM | FCAS (reg., 6 s) | market outcomes | — | batteries lower FCAS costs, most in short-duration markets |

## 5. Product-rule parameters that change battery economics (documented effects)

| Rule parameter | Where | Documented effect on battery operation / economics | Source ids |
|---|---|---|---|
| **Energy / endurance requirement** (30-min → 15-min criterion; DC MER 15 min; Nordic LER 20 min FCR-D / 1 h FCR-N; regulation/reserve energy holdbacks) | DE, GB, SE, US | Sets the minimum MWh per MW sold, so it fixes the optimal P/E: 1.6 MWh/MW (DE, 30 min); ~16 min of energy (GB DC); 15-min regulation and 1-h spin holdbacks (He). Relaxing the criterion is flagged as a lever. | engels2019, thien2017, fan2025, mirzaeialavijeh2025, he2016 |
| **Deadband width** (FCR ±10 mHz; EFR ±0.015/±0.05 Hz; DC ±0.015 Hz deadband with only 5% delivery up to the ±0.2 Hz knee and 100% at ±0.5 Hz; DM knee ±0.1 Hz, full ±0.2 Hz; DR linear to 100% at ±0.2 Hz; NEM contingency >0.15 Hz) [corrected 2026-10-07 from "DC ±0.2 Hz"] | all | Narrow bands mean continuous micro-cycling and energy drift: EFR cycles about 1.4/day at 200 MW. DC's low-delivery zone up to ±0.2 Hz means near-zero activation energy in normal operation, so availability revenue comes with little degradation. | lee2019, gundogdu2018, gilmore2024, cao2024 |
| **Freedom inside the deadband / envelope** (±9% in EFR deadband; FCR deadband utilisation) | GB, DE | The main SoC-recovery lever with no market trade needed. Without it, SoC hits 0% and availability/SPM falls (98% vs 100%). | gundogdu2018, lee2019, thien2017 |
| **Over-fulfilment allowance** (DE: up to 20%) | DE | Lets the battery steer SoC through the activation response. Needs P ≥ 1.25 × contracted power, which oversizes the inverter. | engels2019, thien2017 |
| **SoC-recovery route and lead time** (intraday set-point trades 15-min blocks, 5-min lead, 100 kW steps; DC baselines 1 h ahead, ≥20% MER per SP, ramp ≤5%/min; Nordic intraday vs imbalance vs TSO exemption) | DE, GB, DK | Faster and cheaper routes let more MW be sold per MWh. The exemption agreement gives the highest profit in DK. Imbalance settlement beats intraday trading. A recovery delay can destabilise SoC (oscillation under DC). DC baseline costs reach about −£4.6m PV for LF. | engelhardt2022, cao2024, fan2025, engels2019, thien2017 |
| **Rest / suspension rules after long events** (EFR: 30-min rest after 15 min outside deadband) | GB | Keeps 100% availability and allows recharge at ±9%. Worth up to £646 per Triad day when stacked. | gundogdu2018 |
| **Activation-energy settlement** (DE implicit via balancing group at reBAP; FCR-N explicit energy pay; DC no energy pay) | DE, Nordic, GB | DE: +€302–1,068/MW/month from the energy shifted through the degrees of freedom. HF DC is more profitable than LF because its charging energy has value (NPV £41.9m vs £22.1m). | koltermann2022, fan2025, mirzaeialavijeh2025 |
| **Performance measurement and mileage payment** (PJM score ≥0.70; mileage ratio about 3 for RegD) | US PJM | Removing mileage pay cuts income about 25% and shifts capacity to spinning reserve. The required score sets an optimal cycle-depth threshold, trading profit against life (26→69 months). Order 755 raised deployment by about 37%. | he2016, xu2018_regdparticipation, shi2019, tabari2020 |
| **Penalty severity** (DC all-or-nothing block deduction; DE penalty-free probability constraint; EFR SPM scaling) | GB, DE, US | Harsh penalties push operators to over-size energy, as in the chance constraint Pr{penalty}≤0.005 behind the 1.6 MWh kink. Graded SPM gives softer incentives. | fan2025, engels2019, gundogdu2018 |
| **Response time** (EFR 1 s; FCR 30 s; NEM 6 s/1 s FFR) | GB, DE, AU | Fast products favour inverter-based storage and remove thermal competitors. Short-duration NEM markets show the largest price falls after battery entry. | greenwood2017, rangarajan2023, gilmore2024 |
| **Product granularity / procurement format** (weekly pay-as-bid → daily 4-h marginal (DE); EFA-block day-ahead DC; hourly D-1/D-2 Nordic; 5-min co-optimised NEM) | all | Shorter blocks let batteries recover SoC between blocks and stack products hourly; FCR-D up+down stacking dominates in SE. Pay-as-bid needs a WAP assumption in models. | engels2019, fan2025, mirzaeialavijeh2025, gilmore2024 |
| **Symmetric vs asymmetric products** (FCR symmetric; DC LF/HF split; FCR-D up/down) | DE, GB, SE | Asymmetric products let batteries sell the direction that suits their SoC. HF-only DC needs only 35.7 MWh per 100 MW. | fan2025, mirzaeialavijeh2025 |
| **Mandatory unpaid response** (NEM mandatory PFR, droop 1.7%) | AU | Uses 3–4% of warranted cycles with no pay. Droop settings limit full participation in faster FCAS. | gilmore2024 |
| **Total procured volume / fleet saturation** | GB, DE, AU | Per-MW cycling falls as the fleet grows (lee2019), and capacity prices fall (fan2025 break-even, engels2019 price scenarios, rangarajan2023), so the profitability window closes. | lee2019, fan2025, engels2019, rangarajan2023 |
| **Frequency-data non-stationarity** (deterministic hourly deviations, seasonality) | CE | The implied energy requirement changes year to year (+37% large deviations by 2023), so a single-year back-test misstates feasibility. | celicortes2025 |

## 6. Open gaps

1. **No cross-market attribution study.** No Q1 paper runs a single battery or agent through GB DC/DM/DR, DE FCR/aFRR, Nordic FCR-N/D/FFR and NEM FCAS with the rule parameters toggled one at a time. This is the gap the user's study can fill.
   - **2026-10-07 update:** `landy2026_hybridstacking` (abstract-level evidence) compares regions with one model, but at the level of market-access bundles (grid charging, market sets), not individual product-rule parameters. The gap as defined here (toggle rule parameters one at a time) still stands.
2. **GB DM/DR and post-2023 rules are missing.** No verified Q1 paper models Dynamic Moderation/Regulation or the 2023–24 DC price collapse. fan2025 assumes £8/MW/h flat.
   - **2026-10-07 update:** partly closed (abstract-level evidence): `casella2024_ukbessmilp` (Q1?) models GB dynamic frequency response services; the preprint Xia et al. 2026 co-optimises a battery's stacking of EAC-procured DC/DM/DR with SoE rules (`WATCHLIST.md` C3). The 2023–24 price collapse is still not analysed in a Q1 paper.
3. **aFRR with batteries (DE/EU PICASSO) and Nordic FFR are absent** from the verified set. No Q1 paper was found within this session's budget.
4. **CAISO regulation (Reg-Up/Down mileage) is not covered**; only PJM is.
5. **Learning-based control under product rules is rare.** Most papers use rule-based or threshold controllers (gundogdu2018, engels2019, xu2018_regdparticipation). RL agents that learn recovery baselines or set-point trades under the actual compliance and penalty rules are not in the Q1 literature found here.
6. **Endogenous prices.** Almost all papers are price-takers, while saturation is the key driver of profitability decline in DC, FCR and FCAS.
7. **Evidence quality.** Several core papers (oudalov2007, thien2017, cao2024, engelhardt2022, koltermann2022) were read at abstract level only. Their numbers should be pulled from the full text before quantitative reuse.

## 7. Dropped / not included candidates (S6)

- Fleer & Stenzel 2016 (J. Energy Storage): the journal was Q2 in SJR 2016, so it fails the Q1 rule.
- Fleer et al. 2018 "Price development and bidding strategies… PCR market": published in Energy Procedia (conference), so excluded.
- Koller, Borsche, Ulbig, Andersson 2015 EPSR (ETH Zurich 1 MW BESS): bibliographic verification was blocked by rate limits, so it was excluded rather than left unverified.
- Mirzaei Alavijeh et al. 2025: already in the archive (another stream).
- He et al. 2016 TSG: already in the archive (S4). The S6 full-text check confirms 30 MW/1 h VRFB, 70% round-trip efficiency, the −25% income without PBR, and a 1.5-h optimal duration.
- Rangarajan et al. 2023: already in the archive (S8).
- Lieskoski et al. 2024 (Finland review): not verified within budget, and the group fit is unclear.
