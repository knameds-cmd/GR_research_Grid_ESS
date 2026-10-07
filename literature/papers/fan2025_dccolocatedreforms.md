---
id: fan2025_dccolocatedreforms
title: "Co-Located Battery Energy Storage Optimisation for Dynamic Containment Under the UK Frequency Response Market Reforms"
authors: ["Fan, F.", "Nwobu, J.", "Campos-Gaona, D."]
year: 2025
journal: "CSEE Journal of Power and Energy Systems"
volume_issue_pages: "11(1):340-351"
doi: "10.17775/CSEEJPES.2023.01210"
quartile: "Q1 (SJR 2025, Electrical and Electronic Engineering; Electronic, Optical and Magnetic Materials; Energy (misc.); Q1 every year 2022-2025; Q2 in 2021, Q4 in 2020)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "University of Strathclyde, Dept. Electronic & Electrical Engineering (Campos-Gaona, Fan); Offshore Renewable Energy Catapult (Nwobu)"
lineage: "Strathclyde wind/power-electronics group; no advisor-student tie verified."
streams: [S6_ancillary_products]
market_context: "GB Dynamic Containment LF/HF (EFA-block day-ahead auctions, SoE rules, baselines) co-located with 432 MW offshore wind farm"
method_class: "multi-year techno-economic simulation + PSO (derivative-free) sizing/strategy optimisation"
evidence_read: "full text (accepted manuscript, https://strathprints.strath.ac.uk/86798/1/Fan_etal_CSEE_JPES_2023_Co_located_battery_energy_storage_optimisation_for_dynamic_containment.pdf)"
oa_link: "https://strathprints.strath.ac.uk/86798/"
---

## 1. Research question
What BESS power/energy, energy-target (foot/headroom) and SoC limits maximise NPV of a wind-co-located BESS selling Dynamic Containment under the post-2021 GB reforms (EFA-block procurement, State-of-Energy rules, operational baselines)?

## 2. Setting & assumptions
- DC: responds to |Δf| > 0.2 Hz (deadband ±0.2 Hz) [**correction 2026-10-07:** the NESO DC specification is deadband ±0.015 Hz, small linear delivery up to 5% at the ±0.2 Hz knee point, then linear to 100% at ±0.5 Hz (NESO DC service documents, e.g. neso.energy/document/173206). "±0.2 Hz" is either the paper's simplification or an extraction error — check the full text before reuse]; Minimum Energy Requirement (MER) = 15 min full delivery in each direction; SoE rule: initial head/footroom ≥ MER at window start and ≥ 20% MER restored per 30-min SP via baselines; baseline ramp ≤ 5% of contracted DC/min; baseline amplitude ≤ 2.5% of DC capacity at first/last minutes; baseline submitted 1 h ahead (three SP latency); non-compliance = full payment deduction for the block; 4-h EFA windows; unit cap 100 MW.
- Price-taker; DC price assumed £8/MW/h (both LF/HF; soft-launch LF ~£17/MW/h cited); baselines priced at N2EX day-ahead; imbalance via Elexon SSP/SBP; BSUoS/TNUoS included; CfD £117.1/MWh for wind.
- LMO Li-ion degradation (calendar + rainflow cycle), min SoC 20%, EoL at 80% capacity; 8% discount rate.
- Configurations: non-power-exchange (NPE) and power-exchange (PE) with additional converter.

## 3. Constraints that drove the model choice
SoE-rule compliance and degradation depend on the multi-year sequence of second-scale frequency and baseline decisions; NPV is non-smooth in design variables → simulation-in-the-loop with PSO instead of MILP.

## 4. Model
- max NPV = −CAPEX − connection + Σ_m [Σ_e (R_DC + R_BL + ΔR_CfD + ΔR_EIC − ΔC_BSUoS) − ΔC_TNUoS − OPEX]/(1.08)^{m/12}.
- Variables: P_B, E_B, P_DC^LF, P_DC^HF, footroom/headroom targets, SoE-limit parameters α_ch, α_dis, auxiliary converter P_A.
- Constraints: 1 ≤ P_DC ≤ min(P_B η_C,100); energy sufficiency (x_LF P_LF + x_HF P_HF) ηη/4 ≤ (1−σ)E_B; ≥20% MER restoration per SP; baseline ramp; σ=20%.
- Solver: particle swarm optimisation; repeated random initialisations converge to same solution.

## 5. Data & processing
NGESO GB frequency 2016–2019 (resolution not stated in extraction); N2EX day-ahead prices (Nord Pool) 2016–2019; Elexon imbalance prices; NGESO BSUoS; CfD reference 2017–2019; multi-year simulation until EoL.

## 6. Justification
Compliance with SoE rules in "almost all" of ~1,460 EFA blocks/yr; sensitivity on DC price (break-even £5.3/MW/h for LF+HF).

## 7. Key results
- Optimal sizes: LF-only 105.3 MW/83.7 MWh (11.7 y life); HF-only 100 MW/35.7 MWh (15 y); LF+HF 116.8 MW/87.8 MWh (11.3 y) → P/E ratio ~1.3–2.8 h⁻¹; full-response duration ~16–16.8 min (just above 15-min MER).
- NPV (£m): LF-only 22.13, HF-only 41.85, LF+HF 17.90; DC payment PV 52.5–62.1 dominates; baseline costs −4.6 (LF) to +0.18 (HF).
- PE configuration not optimal (P_A=0); PE LF+HF NPV £16.59m, life 10.8 y (more cycles/DoD).
- Break-even DC price for linked LF+HF ≥ £5.3/MW/h.

## 8. Limitations (stated + your critical reading)
Frequency unpredictability in baseline target not modelled; LMO model underestimates low-SoC ageing; planning-stage (no short-term wind forecast uncertainty); flat future DC price; PSO no global guarantee; DM/DR not modelled. Constant £8/MW/h ignores the 2023–24 DC price collapse.

## 9. Relevance to my study
The most explicit encoding of GB DC rule parameters (MER 15 min, 20% MER/SP restoration, baseline ramp/amplitude/lead time, all-or-nothing block payment) inside an investment model; shows the 15-min MER fixes energy sizing (~16 min) and HF-only is far more profitable because charging (HF) is "paid" energy. Directly reusable parameter set for an RL environment of GB DC.

## 10. Lineage links
- Builds on: NGESO DC service terms; cao2024_dcvsefr (parallel); gundogdu2018_efrtriad (EFR predecessor).
- Built upon by: —

## 11. Verification log
- Strathprints record 86798 (DOI); SciOpen page: vol 11, issue 1, pp. 340-351, Jan 2025 (online 8 Sep 2023); OpenAlex works/doi:10.17775/CSEEJPES.2023.01210: authors/affiliations.
- SJR sid 21101017898: CSEE JPES Q1 2022–2024 (EEE; Energy misc.).
- Full text (accepted manuscript) read.
- 2026-10-06 independent verifier: quartile field updated - SJR 2025 now published (Q1, SJR 2.240); Q1 2022-2025 (https://www.scimagojr.com/journalsearch.php?q=21101017898&tip=sid). Bibliographic data re-confirmed: SciOpen gives 11(1):340-351, online 2023-09-08, print 2025-01 (https://www.sciopen.com/article/10.17775/CSEEJPES.2023.01210); authors/order confirmed by OpenAlex.
