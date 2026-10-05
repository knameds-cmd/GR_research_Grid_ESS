# S4 — Degradation, efficiency and SoC physics inside market-participation and operation models

Scope: how cycle aging, calendar aging, efficiency and SoC-dependent power capability are represented in BESS bidding and dispatch models, how the representation is made tractable, and how much it changes profit, cycling and dispatch. 14 papers archived (all Q1 per scimagojr.com, SJR 2025).

## 1. Overview: five ways to represent degradation
1. **Throughput / constant marginal cost** ($/MWh discharged, from replacement cost ÷ lifetime throughput). This is the default in most market studies. It is linear and convex, but it over-penalises shallow cycles and ignores SoC and temperature (shi2019, xu2018_cycleagingcost, reniers2021).
2. **Cycle-depth (rainflow) cost** Φ(δ)=aδ^b. It is made tractable by:
   - SoC-segment piecewise-linear marginal costs, a MILP that ISOs can clear (xu2018_cycleagingcost)
   - a convexity proof plus subgradient or online threshold control (shi2019_cycleagingpfp)
   - a simplified two-time-scale rainflow (he2016_pbrcyclelife)
   - a regression surrogate in SoC_k, SoC_{k−1} and C-rate inside ISO clearing (padmanabhan2020).
3. **Semi-empirical calendar + cycle multi-stress models** (SoC, T, DoD, C-rate, t). The foundational form is xu2018_degradationmodel. They are linearised into MILP+MPC (collath2023, maheshwari2020) and reviewed in collath2022.
4. **Physics-based (SPM + SEI)**: NLP in the optimiser. This gives the largest measured gains but is costly to solve (reniers2021).
5. **Opportunity-cost valuation of degradation**. The degradation price is the shadow price of the life budget, found by Lagrangian grid search (he2018_intertemporal) or by DP over state of health (xu2022_dynamicvaluation). It is not the replacement cost.

Efficiency and SoC physics are covered by two papers:
- SoC-dependent (CC-CV) charge limits linearised as an LP; ignoring them loses up to ~65 % of realised arbitrage profit in a lab test (pandzic2019).
- System-level efficiency, where auxiliary and converter losses make round-trip efficiency product-dependent (70–80 % conversion; 23 % total for aFRR-type SCR) (schimpe2018).
- Variable-efficiency SDP: Zheng, Jaworski & Xu 2022 TPWRS 37(6):4785–4795. This belongs to S3 and is not duplicated here.

## 2. Lineage and groups
- **Kirschen / B. Xu / B. Zhang (UW → Columbia)**, with ABB (Oudalov), ETH (Andersson) and ISO-NE (Litvinov). The chain runs xu2018_degradationmodel → xu2018_cycleagingcost → shi2019_cycleagingpfp → xu2022_dynamicvaluation. Related papers by other agents: shi2018_superlineargains, oudalov2007_pfcsizing. Columbia students carry the line on: Zheng (variable efficiency, S3) and Baker (transferable bidder).
- **Tsinghua (Kang, Q. Chen) → CMU (Whitacre, Kar)**: G. He, from he2016_pbrcyclelife to he2018_intertemporal. Follow-up: He et al. 2020 Applied Energy, "economic end of life" (not archived).
- **TUM EES (Jossen, Hesse)**: schimpe2018_efficiency (efficiency) → collath2022_agingreview → collath2023_lifetimeprofit. All are built on the SimSES digital twin.
- **Oxford (Howey) + VITO/EnergyVille**: Reniers' DPhil work, from Reniers 2018 JPS 379:91–102 (simulation) to reniers2021_advancedmodels (1-year cell experiment). Howey also co-authors with Hesse and Kumtepeli.
- **Others**:
  - Argonne/MIT (Botterud): wankmuller2017
  - Waterloo (Bhattacharya): padmanabhan2020, ISO-clearing view
  - Zagreb (Pandžić, a Kirschen postdoc alumnus): pandzic2019
  - TU/e (Paterakis, Gibescu): maheshwari2020.

## 3. Summary table
| id | year | aging / physics model | tractability trick | market | profit impact vs naive model |
|---|---|---|---|---|---|
| xu2018_degradationmodel | 2018 | Calendar + cycle stress factors (δ, σ, T, t) + SEI two-exponential; rainflow | none (assessment tool) | PJM regulation case | n/a (life assessment) |
| xu2018_cycleagingcost | 2018 | Rainflow Φ(δ)=5.24e-4δ^2.03 (NMC) | J-segment PWL marginal cost on SoC segments; convexity → greedy order; MILP | ISO-NE 2015 DA/RT energy + reserve | No cost: life 1.1 yr, prorated loss −$2.1M/yr. 16-seg vs 1-seg: profit +24 % ($276k vs $223k) at ~8 yr life |
| shi2019_cycleagingpfp | 2019 | Rainflow Φ(u)=5.24e-4u^2.03 | Proof that rainflow cost is convex; subgradient; online threshold policy with bounded gap | PJM pay-for-performance regulation | Linear-throughput model withholds entirely when rainflow earns ~$14/h; online policy saves >30 % cost, 3–4× life vs greedy/MPC |
| he2016_pbrcyclelife | 2016 | DOD power-law cycle life; simplified rainflow | Life-multiplied income objective, MINLP | PJM-style energy + reserve + PBR regulation | Ignoring cycle life misstates profit by ~30 %; PBR +25 % income (partial evidence) |
| he2018_intertemporal | 2018 | Throughput × DOD^k + constant calendar | Lagrangian on life budget → marginal benefit of usage; grid search | CAISO 2016 arbitrage + regulation | LCOD pricing loses most arbitrage value (~$1.9M vs $8.3M life-cycle revenue); ≥12 % loss with regulation |
| xu2022_dynamicvaluation | 2022 | Rainflow + constant calendar | DP over SoH with PWL value function; slope = marginal degradation cost | NYISO RT 2010–20; PJM RegD | Regulation ≈ 2× arbitrage lifetime value; second-life value >50 % of new |
| reniers2021_advancedmodels | 2021 | SPM + SEI growth, thermal (physics) | NLP warm-started from LP | Belgian DA 2014 arbitrage | Measured on cells: +17 % revenue, −30 % degradation, +70 % lifetime revenue vs linear model; profit-prediction error 170 % → 13 % |
| collath2023_lifetimeprofit | 2023 | Linearised LFP calendar (+ cyclic) | MILP-MPC; aging cost tuned by lifetime digital-twin simulation | EPEX intraday 2019–22 | +24.9 % (calendar) and +29.3 % (calendar + cyclic) lifetime profit vs throughput cost (abstract) |
| maheshwari2020_nonlineardeg | 2020 | Non-linear empirical (commercial cell data) | Linearisation + decomposition for long horizons | wholesale (unverified) | not extracted (abstract only) |
| wankmuller2017_degradationarbitrage | 2017 | Two degradation representations | penalty cost in arbitrage objective | MISO arbitrage | Revenue −12 to −46 %; NPV $358 → $194–314/kWh (abstract) |
| padmanabhan2020_energyreserve | 2020 | DoD power law + discharge-rate cost | Multi-linear regression surrogate in ISO MILP clearing | Energy + spinning reserve clearing (IEEE RTS) | Lower BESS volumes, higher welfare; LMP −29 to −44 % at peak bus; no life metric |
| pandzic2019_chargingmodel | 2019 | CC-CV SoE-dependent charge limit, measured η_E | PWL in SoE segments (LP; SOS2 if non-concave) | EPEX DA arbitrage | Constant-power model: −14.6 % energy delivered, realised profit €91 vs €260 at 1C |
| schimpe2018_efficiency | 2018 | Electro-thermal system losses (converter, HVAC, aux) | simulation only | FCR / aFRR (SCR) / PV profiles | Round-trip 70–80 %; total −8 to −13 pp; SCR total 23 % (abstract) |
| collath2022_agingreview | 2022 | Taxonomy (empirical / semi-empirical / physics / ML) | Review: MILP dominant | FCR, SCI, PS, arbitrage | FCR → calendar-dominated; replacement-cost aging price is often far from optimal |

## 4. Cross-cutting findings
- **Naive "no-cost" models are not a benchmark, they are a failure mode.** In xu2018 the asset dies in about 1 year, and in reniers2021 in 1.4 years. Every serious study needs some aging cost.
- **The level of the aging price matters as much as its functional form.**
  - he2018, xu2022 and collath2023 all show that pricing degradation at replacement cost is suboptimal.
  - The right price is an opportunity cost, and it depends on the product mix and price regime, so it is market-rule dependent.
- **Which aging mechanism dominates depends on the product.**
  - Cycle-depth models fit arbitrage.
  - Reserve products (FCR, aFRR) produce small DOC around mid-SoC, so calendar and SoC aging, plus standby losses, dominate (collath2022, schimpe2018).
  - A rainflow-only cost under-prices reserve participation's real aging and over-states its efficiency.
- **Measured gains from better models are large.** They range from +24 % to +70 % lifetime profit (xu2018, collath2023, reniers2021). These numbers come mostly from perfect-foresight, single-market studies, though.
- **SoC physics (CC-CV, power derating near limits) can dominate short-run profit errors** in delivery-critical products (pandzic2019).

## 5. Open gaps
1. No study systematically varies **market product rules** (e.g., FCR energy-reservoir / 15–30 min SoC rules, aFRR activation, DA vs intraday granularity, pay-for-performance) while holding a high-fidelity aging model fixed. The rule → stress-factor → profit chain is missing.
2. Calendar aging in reserve-heavy portfolios is rarely co-optimised. The Kirschen/Xu line adds it ex post as a constant.
3. Aging under **uncertainty**: almost all papers use perfect foresight. How errors in the aging price interact with price-forecast errors and RL policies is open (he2018 has a 20 % bias test only).
4. Validation is mostly simulation. Only reniers2021 (cells) and pandzic2019 (cell testbed) validate experimentally; none validates on a utility-scale fleet.
5. RL papers (cross-ref S5: cao2020_drlarbitragedegradation and others) typically use throughput or rainflow costs at replacement-cost prices. The lessons from he2018, xu2022 and collath2023 on tuning the aging price have not been imported.

## 6. Minimal degradation specification for a market-rule study
- **Inside the optimiser or RL agent:** a convex cycle-depth cost (J-segment PWL, J ≈ 8–16, Φ from a cited cell study) **plus** an SoC-dependent calendar term (linearised, e.g., per-hour cost rising with SoC). Throughput cost alone is acceptable only as an ablation.
- **Aging price:** treat it as a hyper-parameter tuned per market-rule scenario by lifetime simulation (collath2023) or by an opportunity-cost loop (he2018 / xu2022). Do not use a single replacement-cost value across scenarios.
- **Ex-post evaluation:** run every policy's SoC trajectory through a richer reference model in a consistent way: rainflow plus calendar plus SEI non-linearity (xu2018_degradationmodel-type), or a semi-empirical LFP/NMC model. Report life loss, full-equivalent cycles (FEC), and lifetime-prorated profit, not just annual revenue.
- **Efficiency:** use a load-dependent converter efficiency plus a constant auxiliary load (schimpe2018) when comparing low-throughput reserve products with arbitrage.
- **SoC physics:** add an SoE-dependent charge limit (pandzic2019) for products that need full power near SoC limits.
- **Ablation set to report:** (a) no aging cost, (b) throughput cost, (c) cycle-depth PWL, (d) cycle-depth + calendar. All four are evaluated with the same ex-post model, across all market-rule scenarios.

## 7. Dropped / not archived
- Kumtepeli et al. 2020 IEEE Access (3D-MILP electro-thermal + semi-empirical aging, TUM/NTU/Oxford): the IEEE Access quartile is borderline (mega-journal, JCR Q2) and the full text timed out.
- Hesse et al. 2019 "Ageing and efficiency aware battery dispatch… MILP": published in Energies (MDPI), so excluded.
- Kumtepeli et al. "Depreciation cost is a poor proxy for revenue lost to aging" (arXiv 2403.10617): preprint/conference, so excluded.
- Kazemi & Zareipour 2018 TSG 9(6):6840–6849, DOI 10.1109/TSG.2017.2724919: the DOI was verified, but no full text or abstract was accessible.
- Gonzalez-Castellanos, Pozo & Bischi 2020 TPWRS 35(1):672–682: verified and read (arXiv 1901.04260), but it is economic dispatch with no degradation and no market. It is listed as a cross-reference under pandzic2019.
- Perez, Moreno et al. 2016 (multi-service degradation, IEEE TSTE): not verified, because the search budget was exhausted.
- Cao et al. 2020 (RL with degradation) and Kwon & Zhu 2022: covered by the RL stream.
- Zheng, Jaworski & Xu 2022 (variable efficiency SDP): covered by S3.
