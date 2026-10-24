# GB LDES cap and floor: facts from the three source documents

**Sources**
- **[TDD pN]**: Ofgem/DESNZ, *Long Duration Electricity Storage: Technical Decision Document*, 11 March 2025 (`ofgem2025_ldes_technical_decision.txt`).
- **[MTD pN]**: Ofgem, *Window 1: Minded-to decisions – Long Duration Electricity Storage*, consultation published 26 June 2026 (`ofgem2026_ldes_window1_minded_to.txt`).
- **[NERA pN]**: Anstey, Sømme, Wellié (NERA), *Caps and Flaws: Ofgem's appraisal of LDES projects and lessons from interconnectors*, 20 April 2026 (`nera2026_caps_and_flaws.txt`).

**How to read this file**
- `pN` is the `=== pN` marker in the extracted text, which is the PDF page. In TDD and MTD this equals the printed page number. In NERA the printed number is pN−1.
- **(derived)** marks a number I calculated from the documents. The documents do not state it.
- NERA often cites other Ofgem documents that are not among these three: the Financial Framework Decision (FFD, Sep 2025), the MCA Framework (Sep 2025), the NESO methodology (Sep 2025), the Eligibility Outcome (Sep 2025) and the draft licence (Mar 2026). Such facts are tagged "NERA citing X". I have not checked them against X.
- Where the TDD (2025) and later documents disagree, the later position is noted.

---

## 1. Eligibility

| Item | Fact | Cite |
|---|---|---|
| Minimum duration | "8 hours continuous output at full power", and this capacity must be kept "over the full cap and floor regime duration (i.e. 25 years)". | [TDD p19], [TDD p21] |
| How duration is measured | Ability to "discharge continuously at full power for at least 8 hours". For the connections-reform definition: "capable of discharge at full power for at least eight hours, and full power must be at least 50MW or 100MW". | [TDD p21], [TDD p52] |
| Duration in the assessment | Energy capacity (MWh) for modelling was "calculated using each project's continuous discharge capacity, discharge duration and efficiency assumptions". It was treated as fixed over the asset life. Min/max state-of-charge assumptions were standardised. | [MTD p21] |
| Why 8h | The Jan 2024 consultation proposed 6h. Most respondents backed 10h or were unaffected, but some said 10h would delay or kill projects. Raising the threshold above 8h "could delay achieving clean power by 2030". | [TDD p21–22] |
| Minimum capacity | Stream 1: **100 MW**. Stream 2: **50 MW**. The project must also show it can maintain discharge capacity over the regime. | [TDD p19], [TDD p22] |
| TRL | Stream 1 = **TRL 9**, interpreted as "at least two assets of at least 100MW … in working operation, in GB or internationally". Stream 2 = **TRL 8**, interpreted as "an installed, working example that is technologically identical or near identical … of at least 1MW". TRL is self-assessed. | [TDD p19], [TDD p23–25] |
| Technology / lithium-ion | No technology ban. "only PSH and Li-ion batteries will have a TRL of 9 at the start of window one". Li-ion is expected to qualify as well-established. LAES, CAES and flow batteries are expected at TRL 8 (stream 2). For connections reform, Li-ion is treated as "batteries", but "This does not affect their eligibility for the LDES cap and floor regime". | [TDD p24], [TDD p52–53] |
| Outcome by technology | All iron-air, sodium-sulphur and hydrogen applications were rejected at eligibility. Of eligible capacity, Li-ion BESS was **70%**, followed by PSH (the figure shows 16%). | [NERA p4] |
| New build / refurbishment | New builds plus "significant refurbishments or expansions" that add capacity meeting the criteria (e.g. 100 MW over 8h). Only the cost of the new capacity is supported. All revenues of the newly formed asset count in cap and floor calculations. | [TDD p26] |
| Additionality | No further test in window one. Ofgem "will not support projects that can already be deployed without support, including projects that have already taken FID". All LDES are treated as additional for window one. | [TDD p25] |
| Grid connection | Only "Evidence that grid connection application has been submitted", because of connections reform. | [TDD p18], [TDD p20] |
| Planning | Consent in place by the start of project assessment (end Q3 2025). Projects deliverable by 2030 need only show they can secure consent in time, with evidence of engagement and land rights. | [TDD p18–19] |
| Other | Costs at IPA "Outline Business Case" level at minimum, using the IPA 'Level 0' cost breakdown. FEED appropriate to the project's stage. Environmental permits, a generation licence where applicable, and proof of land rights are also required. | [TDD p18], [TDD p20–21] |
| Delivery tracks | Track 1: deliverable by **2030**, backstop **2032**. Track 2: by **2033**, backstop **2035**. Force-majeure delays inside the 2-year grace period carry no penalty. Delivery after the backstop is penalised. | [TDD p15], [TDD p43], [TDD p50] |
| Natural resources | Ofgem "may have regard to best use of scarce natural resources (such as lochs and rivers)". | [TDD p19] |

---

## 2. Cap and floor mechanics

### 2.1 Core parameters

| Item | Fact | Cite |
|---|---|---|
| Regime length | **25 years** by default, with all capital costs recovered over this period. A shorter regime is allowed by exception but must be **≥20 years**. Costs and benefits of every project are assessed over 25 years whatever duration is requested. | [TDD p16–17], [TDD p54] |
| Window 1 regime requests | 50 requests in total. 2 regime-variation requests: both minded-to reject. 1 regime-duration request: reject. 45 residual-value requests: **41 accepted, 4 rejected** (those tied residual value to negative decommissioning costs). 2 combined duration + residual-value requests: both rejected. All 73 assessed projects are shown with a 25-yr regime duration. | [MTD p38–39], [MTD p70–73] |
| Default parameters (W1) | 25-yr duration, **zero residual value**, indicative default returns of **4.47% at the floor** and **7.48% at the cap**, both **CPIH-real**. | [MTD p37] |
| Cap: definition | Recovers invested capital (debt and equity) plus "a fair return on investment if the assets perform well". Return is based on cost of equity applied to **100% of RAV**. | [TDD p5], [TDD p36], [TDD p61] |
| Cap: CAPM inputs | Equity beta **1.125**, risk-free rate **2.26%** (CPIH-real), total market return **6.9%** (CPIH-real), giving **7.48%** CPIH-real (NERA citing FFD p30). Projects may instead propose a competitive cap below the administrative ceiling. | [NERA p7], [NERA p15 fn18] |
| Floor: definition | Recovers invested capital (debt and equity) plus "a rate of return that is comparable to the cost of debt". The rate comes from a cost-of-debt benchmark applied to **100% of RAV**. | [TDD p5], [TDD p36], [TDD p60–61] |
| Floor: benchmark and date | Notional cost of debt from **iBoxx GBP Non-Financials 15+ BBB**, CPIH-real. It is the average yield over the **20 trading days preceding FID** (NERA citing FFD p25). The TDD had expected the reference date to be the month of the award decision, so FFD later moved it to FID. | [NERA p15 fn16], [TDD p61] |
| Floor: project-finance variant | Lenders compete to fund the floor under Ofgem oversight (a Debt Funding Competition). This floor "covers only debt obligations". If it is above the administrative floor, the licensee repays consumers the difference before any equity distribution. | [TDD p38–40], [TDD p61], [TDD p63–64], [NERA p6], [NERA p15 fn17] |
| Building blocks | Capex (devex, construction capex, repex, spares, IDC, financial transaction costs) forms the **RAV**. Controllable opex, corporation tax, decommissioning and allowed return are added. Pass-through costs (licence fees, property rates/taxes, network rates) are "not subject to cap or floor limits". | [TDD p40–41], [TDD p56–59] |
| Coverage | "Administratively set cap and floor levels cover 100% of eligible project cost". 76% of respondents opposed a floor at 80% of costs. | [TDD p54], [TDD p36] |
| Depreciation / profile | Straight-line over 25 yrs (or longer, or shorter but ≥20), "Annuitised to make cap and floor levels constant in real terms". Grants are netted off. | [TDD p56], [TDD p58] |
| Indexation | "Fixed in real terms for the 25-year regime duration". Index is "potentially CPIH". W1 rates are expressed CPIH-real, and MTD refers to an "inflation-linked regime structure". | [TDD p55–56], [MTD p37], [MTD p39] |
| Tax | Allowance at UK tax rates, annuitised. As an alternative, tax may be a pass-through. | [TDD p60] |
| Cost setting | Preliminary levels are set at PA. **Final levels are set at the Post-Construction Review (PCR, c. 2029–2031)** on economic and efficient outturn costs, then fixed apart from limited reopeners. P90 costs form the **Project Cost Ceiling**: above the PCC, levels are set on the PCC. The Project Assessment Update has moved to after the final award (Autumn 2026). | [TDD p8], [TDD p33–34], [MTD p17–18] |
| Cost-overrun allocation (draft licence) | Non-controllable costs: 100% passed through. Market-related costs, "such as energy purchase costs or marginal cycling costs": passed through using set methods. Capex overruns that are inefficient or above the developer's high estimate: borne 100% by the developer (NERA citing the Mar 2026 draft licence). | [NERA p7] |
| Reopeners | Opex may be re-set once, "no earlier than 10 years into the regime", by either party. Decommissioning reopener applies on a change in law. Capex reopener applies for force majeure. | [TDD p42], [TDD p59–60] |
| Post-regime | Projects that received floor payments use post-regime revenues to offset them "on an NPV-neutral basis". Ofgem does "not expect long-life assets will operate solely on a merchant basis after the cap and floor period ends". | [TDD p5], [TDD p37], [TDD p40] |

### 2.2 Revenue assessment and payments

| Item | Fact | Cite |
|---|---|---|
| Which revenues count | "All sources of revenue will be considered for assessment against the cap and floor". The licence definition of "Revenue" was still to be written (decision expected Q2 2026). For refurbishments: "All revenues earned by the … newly formed asset". | [TDD p55], [TDD p26] |
| Actual vs reference revenue | Assessment "will look at the total revenue for the year or five-year period". Operators choose their own trading route (third-party optimiser or in-house), subject to gross-margin reporting and anti-gaming conduct rules. A notional/reference-revenue approach is **not stated**. The text implies actual revenues. | [TDD p44], [TDD p47], [TDD p62] |
| Assessment period | **5 years with an option for 1 year**, chosen by the licensee. Comparison is "on NPV neutral basis". Unlike interconnectors, balances carry over between periods, "meaning final assessment based on full regime duration". Interim payments are trued up. The same period applies to project-finance and balance-sheet projects. | [TDD p44], [TDD p55] |
| NPV discount rate | To be defined in the licence. Value **not stated**. | [TDD p55] |
| Floor top-up | "If it earns less than the floor, consumers cover all the shortfall, provided the project meets its minimum availability threshold." | [TDD p35] |
| Cap sharing | "Soft" cap: excess above the cap is shared through a sharing factor still to be set [TDD p36], [TDD p51]. In the FFD as cited by NERA: "Projects will retain **30 percent** of revenues above the cap and will be required to return the remainder" (i.e. 70% returned) [NERA p7] (citing FFD p29). Excess is repaid "the following year" [TDD p44], [TDD p55]. | as shown |
| Interconnector contrast | Interconnectors have a hard cap with a ±2% availability adjustment. The LDES soft cap is meant to keep availability incentives when revenue is above the cap. | [TDD p51] |
| Between floor and cap | The project keeps market revenue. "The range between the cap and the floor is important to incentivise projects to operate efficiently". MTD speaks of projects operating "within the default cap and floor corridor". | [TDD p35], [TDD p48], [MTD p38] |
| Availability condition (floor) | "Soft floor": a minimum availability threshold must be met each year, otherwise "the floor may be removed for that year". "'availability' may include both charging and discharging capabilities". In low-availability years, "only revenues above the floor level carried over into assessment … against the floor level. All revenue considered for assessment against the cap". Eligibility may be reinstated after a force-majeure outage. Threshold % **not stated** (due by June 2026). | [TDD p50–51], [TDD p56–57], [TDD p62] |
| Funding | "Payments between licensee and NESO, recovered and distributed via network charges". To be legislated in the Planning and Infrastructure Bill. | [TDD p11], [TDD p56] |
| Bill impact (W1) | "Cap and floor payments are expected to be broadly neutral over time in direct bill terms". | [MTD p6] |
| Capacity Market interaction | CM revenue is one component of the W1 revenue stack used in the Financial Assessment [MTD p40], [MTD p42]. The CBA counts changes in LDES CM revenue "which affects payments under the cap and floor regime" [TDD p30]. "mandatory participation in the capacity market" is listed as a possible low-regret anti-gaming measure, still under consideration [TDD p48]. Refurbishments are eligible only if they "cannot secure funding through existing methods like the capacity market" [TDD p26]. An explicit rule on whether a C&F project may hold a CM agreement is **not stated**; the documents assume CM revenue. | as shown |
| Other support | Grants are netted off costs [TDD p58]. Zenobe has a Competition Appeal Tribunal challenge (Case 1754/12/13/25) under the Subsidy Control Act, arguing supported LDES competes with unsupported short-duration storage [NERA p2], [NERA p14 fn2]. | as shown |
| Delivery incentive | "payment on completion": revenues start only when the project is complete. Early delivery "may be eligible for an early delivery reward, starting the cap and floor regime early". | [TDD p48], [TDD p50] |

---

## 3. Ofgem/NESO project assessment (Window 1)

### 3.1 Structure and decision rule
- The process has three components: **Economic (EA), Financial (FA), Strategic (SA)**. All draw on a **Cost Assessment** and NESO **System Benefit** and **Security of Supply** modelling [MTD p14–15].
- The EA ranking is the "starting point". Projects are then adjusted for FA and SA and finally cut off by capacity. "No single metric, score or threshold has been applied in isolation" [MTD p15–16].
- There are no fixed weights across EA/FA/SA ("balanced view … similar to our approach for Interconnectors") [NERA p14 fn15] (citing MCA Framework para 6.22).
- **FA threshold**: projects with FA score **< 0.60** are treated as higher downside risk. The threshold was "not a pre-determined threshold" but came from a gap in the score distribution [MTD p45].
- **SA scenario threshold**: scenario score **< −100** flags high sensitivity [MTD p55].
- **Capacity**: awards total up to the upper end of NESO's **2.7–7.7 GW by 2035** advice [MTD p61–62], [TDD p15].

### 3.2 Economic Assessment weights (swing weighting) [MTD p29–30]

| Metric | Type | Weight |
|---|---|---|
| Benefit-Cost Ratio (BCR) | Monetised | **40%** |
| Security of Supply (EEU, per MW) | Non-monetised | 19% |
| Avoided Renewable Curtailment (per MW) | Non-monetised | 15% |
| System Operability | Non-monetised | 12% |
| Wider Economic & Social Impacts | Non-monetised | 8% |
| Real-time Flexibility | Non-monetised | 4% |
| Option Value | Non-monetised | 1% |

- Each metric is min-max rescaled to 0–100 across projects before weighting [MTD p29]. The percentages sum to 100% before rounding [MTD p30 fn4].
- (derived) In Tables 8–9 the "Monetised Score" equals the normalised BCR, and each non-monetised score ≈ normalised score × (wᵢ/0.40). For example, Loch Kemp SoS 56.09 → 26.64. So Final Score ≈ BCR_norm + Σ(wᵢ/0.40)·normᵢ, with a maximum of about 250 [MTD p78–85].

### 3.3 Monetised CBA (BCR) [MTD p22–24]
- **BCR = PV(Benefits) ÷ PV(Costs)**. Annual values are discounted "using a discount rate consistent with Green Book guidance". The rate itself is **not stated**.
- Benefits = Consumer SEW + Producer SEW + LDES Owner SEW + Carbon Externality Reduction.
  - Consumer SEW = reduction in wholesale market costs and CfD costs.
  - Producer SEW = wholesale net revenue of producers + **wholesale net revenue of storage** + interconnector congestion rent + CfD revenues.
  - LDES Owner SEW = "Wholesale market temporal arbitrage (initial commitment)".
  - Carbon = reduction in unpriced carbon externality cost.
  - The CfD transfer nets out [MTD p22 fn3].
- Costs = devex, capex, opex, repex over a **25-yr appraisal**. Decommissioning is excluded (it falls after year 25). TNUoS and business rates are excluded as transfers. A **terminal value** is added in the final year, equal to the share of capex (incl. repex) matching remaining economic life.
- Assumed economic life: Li-ion BESS **25 yr**; PSH **40**; VFB **30**; VFB/Zn **30**; LAES/BESS **25**; CAES **25** [MTD p24].
- Input standardisation:
  - Li-ion RTE capped at **91%** [MTD p21].
  - FX fixed at 18 Nov 2025 rates [MTD p18].
  - Benchmarked decommex per installed capacity for battery groups [MTD p19].
  - P10/P50/P90 costs. The optimistic (P10) scenario was dropped [MTD p18], [MTD p54].
- TDD framing: SEW for consumers, producers and LDES owners. "Revenue cannibalisation happens when a new project changes electricity prices, affecting the revenue of other LDES projects". CM costs and C&F payments are welfare transfers [TDD p29–30].

### 3.4 System/welfare modelling

| Item | Fact | Cite |
|---|---|---|
| Models | NESO "GB-focused Day Ahead model" and "Balancing Mechanism model" (sequential). **BM-model outputs were excluded from EA ranking** because of "residual optimisation degeneracy". The BM outputs were kept for the FA. PLEXOS outputs are referred to in the FA. | [MTD p22 fn3], [MTD p31], [MTD p44] |
| FES base case | **Holistic Transition**, weather year **2013**, base costs = adjusted P50 (excl. business rates and TNUoS). | [MTD p51–52] |
| Sensitivities | FES **Electric Engagement** and **Falling Behind**; weather years **1990** and **1997**. A pessimistic cost case was run but left out of the aggregate score. | [MTD p52] |
| FES vintage | NERA refers to NESO's **2025 FES** for the counterfactual, and to "Holistic Transition" as base. The TDD capacity range is from **FES 2024**. | [NERA p8], [NERA p11], [TDD p15] |
| Years modelled | "Modelling was undertaken for a defined set of years, with results interpolated" (SoS). The specific years are **not stated**. Appraisal horizon is 25 years. | [MTD p25], [MTD p23] |
| Counterfactual | Project-specific "modified marginal additional" approach. Counterfactual = FID + NFID − 0.5·C(x); factual adds C(x). The capacity gap is removed from the project's transmission zone first, then evenly from non-FID projects (NERA citing NESO methodology pp. 23–24). | [NERA p11], [MTD p25] |
| Constraints / location | NESO uses a "static comparison method": first an unconstrained market model, then network constraints from **Beyond 2030 (2024)** (NERA citing NESO methodology p13). Because the BM model was dropped, "locational differences are less fully reflected within the monetised assessment than originally envisaged". Location still enters through counterfactual design, System Operability (scored against NESO CP2030 Operability Annex 3 regional needs) and SA diversity. NESO's zonal redispatch sensitivity was "not … a sufficient basis for adjusting the proposed portfolio". | [NERA p10], [MTD p26], [MTD p32], [MTD p53] |
| Security of supply | Resource-adequacy model. **EEU** across multiple weather years and outage scenarios, using a marginal additional approach, normalised per MW. Originally to be monetised as EEU×VoLL, now **non-monetised** because the reference scenario is not comparable. | [MTD p25], [MTD p31–32] |
| Price effects / cannibalisation | Captured inside SEW: wholesale price changes for consumers and producers, plus "Wholesale Market Net Revenue - Storage" in Producer SEW. Explicitly named in the TDD. | [MTD p23], [TDD p29–30] |
| Real-time flexibility | Qualitative (intraday/BM). The only differentiator was "Short-term power capability above continuous capacity". | [MTD p28] |

### 3.5 Financial Assessment [MTD p37–45]
- Revenue stack: **Ancillary Services, Balancing Mechanism, Capacity Market, Wholesale Temporal Arbitrage (Initial Commitment), Re-optimisation** [MTD p40].
  - Arbitrage and BM come from NESO modelling.
  - Ancillary services: a pool from modelled balancing costs, allocated in proportion to System Operability scores.
  - CM: from recent auction outcomes and derating factors.
  - Re-optimisation: a "common approach" for all projects [MTD p41–42].
- Modelled BM and arbitrage revenues were "adjusted using the **minimum observed difference** from project-submitted data". Re-optimisation is a factor of arbitrage [MTD p44].
- FA score = estimated revenues ÷ project floor over the regime. A score <1.00 means below the floor on average [MTD p43]. NERA: "projected annual revenues (before payments to consumers) as a percentage of the project's floor level" [NERA p14 fn13].
- FA scenario analysis (alternative FES, weather and revenue sensitivities) was **removed** [MTD p44], [MTD p54].
- Applicants' own revenue forecasts are used only "for comparative and calibration purposes" (NERA citing MCA Framework p40) [NERA p14 fn12].

### 3.6 Strategic Assessment [MTD p51–56]
- Inputs: scenario analysis (aggregate rank deviation across the 4 sensitivities) and a deliverability rating (Red/Amber/Green) covering schedule, grid, planning, IT/OT security and supply chain.
- Diversity: one VFB/Zn project (Frontier Legacy) was added for technology diversity.
- Grid-queue position is treated as "largely outside their control" and handled through award conditions [MTD p53].

---

## 4. Window 1 minded-to list

**Totals and counts**
- 171 applications, 52.6 GW [NERA p4].
- 77 eligible: 45% of applicants, 55% of capacity [NERA p4], [MTD p7].
- All but 6 of 35 Track 2 applications were rejected at eligibility [NERA p4].
- 4 withdrew, so **73 assessed** [MTD p7], with a total of **29,349.6 MW** (derived from Table 2) ("nearly 30 GW" [MTD p5]).
- **16 minded-to awards totalling 7,645 MW** [MTD p6], [MTD p11], "just below the upper limit of the advised range (7,700MW)" [MTD p62].
- **57 assessed projects not selected** (derived).

**Selected projects** [MTD p13], with first operation and EA rank from [MTD p34], and RTE/track from [MTD p70–73]. MWh is **not stated** in the documents; the column below is MW × duration (derived).

| EA rank | Project | Technology | Region | MW | Duration (h) | MWh (derived) | RTE % | First op. | Track |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Loch Kemp Storage | PSH | N_Scotland | 660 | 22.3 | 14,718 | 80 | 2030 | 1 |
| 2 | Coire Glas | PSH | N_Scotland | 1,440 | 32 | 46,080 | 82 | 2033 | 2 |
| 3 | TeesCAES | CAES | NE_England | 50 | 30 | 1,500 | 62 | 2029 | 1 |
| 4 | Earba PSH | PSH | N_Scotland | 1,800 | 15 | 27,000 | 79 | 2033 | 2 |
| 5 | Field Netherton | Li-ion BESS | N_Scotland | 400 | 16.3 | 6,520 | 87 | 2030 | 1 |
| 6 | Field New Deer | Li-ion BESS | N_Scotland | 400 | 18.03 | 7,212 | 85 | 2030 | 1 |
| 7 | Field Rigifa | Li-ion BESS | N_Scotland | 200 | 18.03 | 3,606 | 85 | 2030 | 1 |
| 8 | Field Fyrish | Li-ion BESS | N_Scotland | 200 | 16.5 | 3,300 | 87 | 2030 | 1 |
| 9 | Field Long Stratton | Li-ion BESS | E_England | 400 | 16.05 | 6,420 | 90 | 2033 | 2 |
| 12 | East Claydon Storage | Li-ion BESS | E_England | 500 | 12 | 6,000 | 90 | 2030 | 1 |
| 14 | Ocker Hill BESS | Li-ion BESS | W_Midlands | 145 | 8 | 1,160 | 91 | 2029 | 1 |
| 15 | Sundon Storage | Li-ion BESS | E_England | 500 | 8 | 4,000 | 89 | 2030 | 1 |
| 16 | Drakelow (Innova) | Li-ion BESS | W_Midlands | 385 | 8.7 | 3,350 | 91 (capped) | 2030 | 1 |
| 17 | Frontier Legacy | VFB/Zn | N_Wales | 65 | 8 | 520 | 62 | 2029 | 1 |
| 18 | Springwell | Li-ion BESS | E_Midlands | 400 | 11.1 | 4,440 | 91 | 2030 | 1 |
| 19 | Thornton BESS 2 | Li-ion BESS | E_Midlands | 100 | 11.11 | 1,111 | 90 | 2029 | 1 |
| | **Total** | | | **7,645** | | **≈136,937** | | | |

**Notes on the selected list**
- **Developer**: not stated. Appendix 6 names only project companies, e.g. "Field Fyrish Ltd.", "Field Netherton Ltd.", and "Coire Glas Hydro Pumped Storage Scheme" [MTD p92], [MTD p95]. "(Innova)" appears only as part of a project name.
- **Connection date**: not stated. Only "First Operation" year is given.
- **Preliminary cap/floor values (£)**: not published for any project. Only the default 4.47%/7.48% CPIH-real rates [MTD p37] and an Above/Below-threshold FA flag are given. All 16 selected are "Above" except Frontier Legacy ("Below") [MTD p47–49].
- **Mix (derived)**:
  - By technology: PSH 3 projects / 3,900 MW; Li-ion 11 / 3,630 MW; CAES 1 / 50 MW; VFB/Zn 1 / 65 MW.
  - By region: N_Scotland 5,100 MW; E_England 1,400; W_Midlands 530; E_Midlands 500; N_Wales 65; NE_England 50.
- **Largest concentration**: "The largest concentration of projects is in Scotland" [MTD p56].
- **High-ranked projects not selected** [MTD p64–66], [MTD p101–105]:
  - Failed FA threshold: Hunterston LAES/BESS (EA rank 10), Killingholme 1 LAES/BESS (11), Glenmuckloch PSH (23), Loch na Cathrach PSH (24).
  - Failed scenario threshold: Kincardine Li-ion (13; score −156), Neilston BESS 2 (25; −123).
- **FA failures by technology (derived from Table 3)**: 15 projects below the FA threshold. These are all 4 rated VFB projects, both LAES/BESS, 7 of 16 VFB/Zn and 2 of 5 PSH. No Li-ion BESS or CAES project fell below. Deeside submitted no CFFM [MTD p49–50].
- **Capacity cut-off (derived)**: the next project in adjusted order (Neilston BESS 3, 300 MW) would have taken the total above 7,700 MW [MTD p57], [MTD p64].

**Timeline**

| Event | Date | Cite |
|---|---|---|
| Window 1 opened | April 2025 (2-month window) | [TDD p13] |
| Eligibility outcome | September 2025 | [MTD p7] |
| Data Submission Form deadline | 18 Nov 2025 | [MTD p14] |
| Minded-to published | 26 June 2026 (TDD had planned Q1 2026) | [MTD p1], [TDD p31] |
| Consultation close | **14 August 2026** | [MTD p9] |
| Final awards | **Autumn 2026** (TDD planned Q2 2026) | [MTD p6], [MTD p67] |
| Post-award cost update | After final award | [MTD p17] |
| PCR | Start c. 2029, PCR c. 2030/31 | [TDD p8], [TDD p13] |
| Window 2 | Consultation on future windows in 2026, decision on a second window "by 2027", informed by the SSEP. W1 losers are not excluded, but there is "no automatic route". | [MTD p6], [MTD p68] |

---

## 5. NERA's main criticisms

1. **Opaque, black-box modelling.** MCA results "hinge on NESO's simplified electricity market model, which is a black box to project developers and investors". Ofgem has not published reasons for individual eligibility decisions [NERA p4].
2. **High discretion and no explicit weights.** Swing-weighting, "critical success factors" and relative scoring involve "a high level of discretion". FA thresholds were not set in advance. There is "very little detail" on how EA, FA and SA are combined [NERA p5–6], [NERA p14 fn15].
3. **Results are sensitive to assumptions and may be reversed.** For interconnector Window 3, Ofgem's minded-to backed 1 of 7 projects, and the final decision backed 3. That change followed a near-fourfold revision of SEM capacity assumptions:
   - MaresConnect SEW moved from −£1,100m…−£700m to −£200m…+£200m.
   - LirIC moved from −£1,000m…−£600m to −£200m…+£40m.

   NERA expects similar pressure on LDES assumptions, such as the FES choice of Holistic Transition, and notes it is unclear how the FES sensitivities enter the decision [NERA p8–9], [NERA p15 fn25].
4. **Constraint-cost modelling is unreliable.** For interconnectors, NESO's ex-post "constraint reduction factor" cut constraint costs by up to **79%**. Post-2035 factors were 69% / 79% / 68% for Leading the Way / Consumer Transformation / Falling Short. NESO's LDES approach is deterministic and static (unconstrained run plus Beyond 2030 constraints). It cannot react to FES 2025 capacity changes or network changes, and Beyond 2030 covers only the 2030s. A proper treatment "would require stochastic constrained optimisation" with locational and national prices [NERA p9–10], [NERA p15 fn27].
5. **Dispatch under national pricing can worsen constraints.** LDES behind constraints (e.g. north of B6) dispatch to the national price and must be redispatched in the BM at consumer cost. EirGrid proposes import/export limits for supported LDES [NERA p15 fn29].
6. **The modified marginal-additional counterfactual is distortionary.** A capacity gap of 0.5·C(x) that scales with project size "will systematically favour larger projects" if marginal returns decrease. Including non-FID capacity in the counterfactual "may overstate the capacity that will be available and systematically understate each project's benefits" [NERA p10–12], [NERA p15 fn33].
7. **Ofgem estimates revenues rather than using applicants' figures.** The FA estimates revenues from NESO modelling and Ofgem's own calculations "Instead of relying on a project's own revenue submissions". It excludes projects with high expected floor payments [NERA p5].
8. **Free option and zombie projects.** The scheme "offers developers and investors a free option without stiff penalties for non-delivery". Under NFFO-1 to NFFO-5, about **60%** of awarded projects never materialised. Zombie projects may lead Ofgem to conclude wrongly that deliverable storage has low benefits [NERA p12], [NERA p15 fn34].
9. **Inefficient mix.** Consumers "should be concerned that Ofgem will commission an inefficient combination of volumes and technologies" [NERA p12].

Other NERA numbers:
- Eligible projects range **50–1,800 MW**; Window 3 interconnectors ranged 750–1,400 MW [NERA p15 fn31].
- The process takes up to 15 months to final award [NERA p3].

---

## 6. LDES revenue figures in these documents

- **£/kW/yr merchant revenue, revenue-mix shares, or £ cap/floor levels: not stated** in any of the three documents.
- Qualitative and relative only:
  - Wholesale temporal arbitrage is "the core component of the revenue stack" [MTD p42].
  - All assessed projects' **submitted** FA scores were above the 0.60 threshold, but 15 fell below on **Ofgem-assessed** revenues [MTD p47–49], [MTD p74–77].
  - Regime-variation applicants showed "limited reliance on floor support" [MTD p38].
  - Overall, C&F payments are expected to be "broadly neutral over time in direct bill terms" [MTD p6].
  - Modelled revenues "are not intended to represent realisable market revenues" [MTD p44].
- Interconnector SEW numbers are in §5 item 3 [NERA p8]. They are not LDES revenue figures.

---

## 7. Implications for modelling LDES revenues (grounded in the documents)

1. **Model the regime explicitly as an NPV corridor, not as annual clipping.**
   - Floor and cap are flat real annuities on 100% of RAV at 4.47% / 7.48% CPIH-real (defaults).
   - Assessment is over 5 years (optionally 1) with carry-over and a full-regime NPV true-up.
   - Excess above the cap is paid back the next year.
   - About 30% of above-cap revenue is retained (per FFD via NERA).
   - [TDD p44], [TDD p55], [TDD p58], [MTD p37], [NERA p7]
2. **The floor is conditional on availability.** Missing the threshold removes the floor for that year, while all revenue still counts against the cap. The threshold % is unknown, so treat it as a scenario parameter [TDD p50], [TDD p62].
3. **Count all revenue streams.** Use the same five-part stack Ofgem uses: arbitrage (initial commitment), re-optimisation, BM, ancillary, CM. Capacity Market income is part of the stack, but the rules on CM participation are not settled [TDD p55], [MTD p40–42], [TDD p48].
4. **Pass-through items sit outside the corridor.** Licence fees, property and network rates are pass-through, and NERA reports that energy-purchase and cycling costs may be passed through by formula. Net them consistently [TDD p41], [TDD p59], [NERA p7].
5. **The floor rate is fixed at FID.** It is the 20-day iBoxx BBB 15+ average, so floor levels depend on interest rates at FID. Final £ levels depend on the PCR, with the P90 cost ceiling [NERA p15 fn16], [MTD p18].
6. **Ofgem itself discounts model revenues.** It treats modelled revenues as relative indicators and haircuts them to the minimum observed gap against developer forecasts. Expect a gap between "assessment" revenues and realisable merchant revenues [MTD p44].
7. **Use the official scenario and weather set.** Base case: FES Holistic Transition with weather year 2013. Sensitivities: Electric Engagement, Falling Behind, 1990, 1997. A 2013-only revenue estimate is the "official" central case. Relative rankings move across these cases: Kincardine's rank deviated by −156 in aggregate [MTD p51–52], [MTD p88].
8. **Location matters for value but was weakly captured in W1.** The BM model was excluded from ranking, and constraint modelling is static [MTD p32], [NERA p10]. A model that prices constraints and BM redispatch will differ from Ofgem's ranking. National-price dispatch behind B6 can raise constraint costs [NERA p15 fn29].
9. **Cannibalisation is part of the welfare test.** Storage net revenue changes are counted under Producer SEW, so a revenue model should let prices respond to added storage [TDD p30], [MTD p23].
10. **Use Ofgem's technology assumptions.** Li-ion RTE is capped at 91% and Li-ion life is 25 yr versus PSH 40, VFB 30, CAES 25. MWh is fixed over life, and 8h continuous at full power must be maintained for 25 yrs. For Li-ion this implies oversizing or augmentation, i.e. repex [MTD p21], [MTD p24], [TDD p19], [TDD p41].
11. **Long-duration Li-ion competed strongly.** Li-ion of 16–18h in N. Scotland ranked 5–9. Every Li-ion project passed the FA test, while all rated pure-VFB projects and both LAES hybrids failed [MTD p34], [MTD p47–49]. Duration above the 8h minimum was rewarded via SoS (19%) and ARC (15%) [MTD p25–26], [MTD p30].
12. **Revenue risk extends beyond year 25.** Ofgem expects post-regime arrangements, and consumers recoup floor payments from post-regime revenues NPV-neutrally. Do not assume a pure merchant tail [TDD p37], [TDD p40].
