# UK storage cost and performance sources (LDES model inputs)

Collected 2026-10-30. Scope: UK government / regulator / consultant reports and GB project disclosures. PNNL and NREL are covered elsewhere (`_notes_intl.md`).

Tags:
- **[V]**: I read the number myself in the primary PDF or workbook saved here.
- **[V\*]**: I read it on the company's own web page through a fetch tool, with no saved file. Quotes may be slightly trimmed.
- **[S]**: secondary source only (trade press, wiki, blog). Treat as weak.
- **[D]**: derived by me from [V] numbers. It is not stated in the source.

Page notation: "p.N (printed M)" means PDF page index N; M is the number printed on the page.

---

## 1. Mott MacDonald for BEIS (2018), *Storage cost and technical assumptions for BEIS*

- Citation: Mott MacDonald (2018). *Storage cost and technical assumptions for BEIS: Summary document*, ref. 395091/02/A, 8 August 2018. Prepared for BEIS.
- URL: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/910261/storage-costs-technical-assumptions-2018.pdf (landing page: https://www.gov.uk/government/publications/storage-cost-and-technical-assumptions-for-electricity-storage-technologies)
- File: `mottmac2018_beis_storage.pdf` / `.txt` (87 pp). Accessed 2026-10-30.
- PDF index = printed page + 8.

### Key conventions [V]
- **Price base: 2012 prices.** p.52 (printed 44): "All costs are presented in 2012 prices."
- **Labelled years.** The projection tables label "Yr 0 (2018)". For non-Li technologies, 2016 literature values are used as year 0. p.48 (printed 40): "we propose to keep the 2016 values as the year 0 (and hence 2018) values".
- **CAPEX scope.** CAPEX covers costs after the EPC contract is awarded: detailed design, equipment, installation and commissioning. Pre-development and grid "infrastructure" costs are given separately. p.46 (printed 38): "CAPEX costs include the costs incurred by the project after appointment of the EPC contractor".
- **Battery oversizing.** For batteries, CAPEX includes extra capacity so the full energy rating holds for the whole life. p.47 (printed 39): "CAPEX is budgeted to ensure that there is sufficient capacity in the system to ensure the full energy capacity is available". **So there is no separate degradation rate.**
- **OPEX scope.** OPEX includes operation, maintenance, insurance and security. It excludes TNUoS, DUoS and BSUoS. Variable cost = 0 for all technologies except hydrogen (p.45, printed 37).
- **No power/energy split.** Costs are given per *use case* at a fixed size, as a project £ total and as £/kW. The only power/energy split available is my [D] two-point fit below.
- **LAES not covered.** "Cryogenic Energy Storage … Not included due to lack of diversity in information sources (1 UK manufacturer)" (p.13, printed 5). "Thermal Energy Storage" in this report means a molten-salt heat store, not LAES (p.21–22, printed 13–14).

### Tables by technology (Medium case unless stated; 2012 £)

Use cases:
- **PL-DA** = network-connected peak lopping, 200 MW / 800 MWh (4 h).
- **WEB** = weekly energy balancing. The section header says "200MW, 800MWh", but every WEB data table lists **Energy Storage 4000 MWh** (20 h). **Ambiguity: I treat WEB as 200 MW / 4000 MWh.**

**Li-ion, PL-DA 200 MW / 800 MWh (p.58–60, printed 50–52)** [V]

| Item | Value | Unit | Note / quote |
|---|---|---|---|
| CAPEX L / M / H | 243.7 / 292.4 / 341.2 | £m (2012) | "CAPEX (Medium) (£) £292,428,420" |
| CAPEX M, Yr0 / 2020 / 2030 / 2040 / 2050 | 1462.1 / 1122.8 / 579.7 / 421.3 / 342.9 | £/kW | Table 16 |
| CAPEX M per kWh, Yr0 | 365.5 | £/kWh [D] | 292.4m / 800 MWh |
| OPEX M, Yr0 / 2030 / 2050 | 23.4 / 9.3 / 5.5 | £/kW/yr | Table 16 |
| Infrastructure (grid) L / M / H | 8.0 / 34.1 / 125.1 | £/kW, flat | Table 16 |
| Pre-development | 1.18 | £m | Table 15 |
| RTE | 85% | AC–AC | Table 15 |
| Usable DoD | 80% | | It is unclear whether 800 MWh is usable or nameplate. |
| Life / cycle life | 15 yr / 5000 cycles | | |
| Construction | 2 yr (100% in one year) | | |
| Availability | 95% | | |

No 8 h or 16 h Li-ion case exists in MM 2018.

**PSH (p.55–56 and 75–77, printed 47–48 and 67–69)** [V]

| Item | PL-DA 200 MW / 800 MWh | WEB 200 MW / 4000 MWh | Unit |
|---|---|---|---|
| CAPEX L / M / H | 218.3 / 272.9 / 363.9 | 240.2 / 316.6 / 582.2 | £m |
| CAPEX M Yr0 → 2050 | 1364.6 → 1186.8 | 1582.9 → 1376.7 | £/kW |
| OPEX M Yr0 → 2050 | 18.6 → 16.2 | 21.6 → 18.8 | £/kW/yr |
| Infrastructure M | 56.9 | 56.9 | £/kW |
| Pre-development | 19.1 | 19.1 | £m |
| RTE | 75% | 75% | |
| Life / cycles | 30 yr / 100,000 | 30 yr / 100,000 | |
| Construction | 4 yr, 25%/yr | 4 yr, 25%/yr | |
| Availability | 95% | 95% | |

Quote: "Pumped Hydro is allotted pre- development costs of approximately four times that of battery storage" (p.46, printed 38).

**CAES, adiabatic cavern assumed (p.56–57 and 77–78, printed 48–49 and 69–70)** [V]

| Item | PL-DA 4 h | WEB 20 h | Unit |
|---|---|---|---|
| CAPEX L / M / H | 181.9 / 200.1 / 218.3 | 211.1 / 287.5 / 363.9 | £m |
| CAPEX M Yr0 → 2050 | 1000.7 → 782.0 | 1437.3 → 1123.3 | £/kW |
| OPEX M Yr0 → 2050 | 13.6 → 10.7 | 13.6 → 10.7 | £/kW/yr |
| RTE | 65% | 65% | |
| Life / cycles | 25 yr / 50,000 | 25 yr / 50,000 | |
| Construction | 3 yr, 50% phasing | 3 yr | |
| Availability | 92% | 92% | |

Quote: "In this study we will assume designs using an adiabatic cavern approach" (p.19, printed 11). The 65% RTE is theoretical: "This efficiency is theoretical as no adiabatic storage projects have been built" (p.19).

**Flow battery, generic vanadium / zinc-bromine (p.61–62 and 79–81, printed 53–54 and 71–73)** [V]

| Item | PL-DA 4 h | WEB 20 h | Unit |
|---|---|---|---|
| CAPEX L / M / H | 545.8 / 655.0 / 764.2 | 836.9 / 1004.3 / 1171.7 | £m |
| CAPEX M Yr0 / 2020 / 2030 / 2050 | 3275.0 / 1620.9 / 634.0 / 349.2 | 5021.6 / 2485.4 / 972.1 / 535.4 | £/kW |
| OPEX M Yr0 → 2050 | 85.3 → 9.1 | 130.8 → 13.9 | £/kW/yr |
| RTE | 70% | 70% | |
| Life | 15 yr | **10 yr** | |
| Cycles | 10,000 | 10,000 | |
| Construction | 2 yr | 2 yr | |

The life differs between the two use cases (15 yr vs 10 yr). The source gives no reason.

**Zinc-based battery, zinc-air / zinc-copper (p.60–61 and 78–79)** [V]

| Item | PL-DA 4 h | WEB 20 h |
|---|---|---|
| CAPEX M | £304.2m; Yr0 1520.9 £/kW | £491.2m; Yr0 2456.2 £/kW |
| CAPEX M 2050 | 414.8 £/kW | 669.8 £/kW |
| RTE | 75% | 75% |
| Life | 15 yr | 10 yr |
| Cycles | 5000 | 5000 |

### [D] Two-point power/energy split (Medium, Yr0, 2012 £)
Method: fit total CAPEX = P × £/kW + E × £/kWh using the PL-DA (800 MWh) and WEB (4000 MWh) cases. This is my calculation, not MM's.

| Technology | £/kWh (energy) | £/kW (power) |
|---|---|---|
| PSH | 13.6 | 1310 |
| CAES | 27.3 | 892 |
| Thermal (molten salt) | 27.3 | 914 |
| Zinc | 58.5 | 1287 |
| Flow | 109.2 | 2838 |

**Caveat for flow and zinc.** The life differs between the two use cases, so these fits mix in replacement or oversizing effects.

---

## 2. AFRY for BEIS (2022), *Benefits of Long Duration Electricity Storage* (+ methodological annex)

- Citation: AFRY Management Consulting for BEIS (2022). *Benefits of Long Duration Electricity Storage*. BEIS Research Paper 2022/019, August 2022. Plus *Methodological annex*.
- URLs:
  - main: https://assets.publishing.service.gov.uk/media/62e9794de90e07142da017ec/benefits-long-duration-electricity-storage.pdf
  - annex: https://assets.publishing.service.gov.uk/media/62ea2384e90e07142ca3e702/benefits-long-duration-electricity-storage-methodological-annex.pdf
  - landing page: https://www.gov.uk/government/publications/benefits-of-long-duration-electricity-storage
- Files: `afry2022_beis_ldes_benefits.pdf/.txt` (46 pp) and `afry2022_beis_ldes_annex.pdf/.txt` (43 pp). Accessed 2026-10-30. Printed page = PDF page.
- Inputs: the annex input table (annex p.41) lists "Technology costs Storage — BEIS". Exhibit 3.11 says "Source: BEIS, supplemented by AFRY". The AFRY data book (Excel) was not found.
- Coverage: vanadium and zinc flow batteries were **not** modelled. Annex p.37: "zinc batteries or vanadium flow batteries were not directly considered in the modelling."

### Exhibit 3.11: capex and opex, **real 2019 £** (main report p.30) [V]
Quote: "Exhibit 3.11 – Storage technology investment costs (real 2019 money)".

| Tech | Duration (h) | 2030 capex £/kW | 2050 capex £/kW | 2030 opex £/kW(/yr) | Hurdle (real) | Build (yr) | Financial life (yr) |
|---|---|---|---|---|---|---|---|
| Li-ion | 1 | 331 | 231 | 5 | 7.3% | 1 | 15 |
| Li-ion | 2 | 449 | 301 | 7 | 7.3% | 1 | 15 |
| Li-ion | 4 | 696 | 427 | 10 | 7.3% | 1 | 15 |
| Li-ion | 6 | 930 | 560 | 11 | 7.3% | 1 | 15 |
| Li-ion | 9 | 1328 | 791 | 13 | **10%** | 1 | 15 |
| LAES | 6 | 1085 | 1018 | 13 | 10% | 2 | 25 |
| LAES | 9 | 1178 | 1105 | 13 | 10% | 2 | 25 |
| LAES | 12 | 1270 | 1192 | 13 | 10% | 2 | 25 |
| CAES | 6 | 993 | 931 | 13 | 10% | 2 | 25 |
| CAES | 20 | 1385 | 1299 | 13 | 10% | 2 | 25 |
| CAES | 72 | 1640 | 1539 | 13 | 10% | 2 | 25 |
| PSH | 6 | 1478 | 1426 | 19 | 10% | 4 | 30 |
| PSH | 20 | 1680 | 1624 | 22 | 10% | 4 | 30 |
| PSH | 72 | 2088 | 2015 | 27 | 10% | 4 | 30 |

Notes on this table:
- **Reading the table.** Hurdle, build time and life are printed once per technology block. The Li-ion "1 15" sits on the 1 h row. I read these values as applying to the whole block. The Li-ion 9 h row prints 10%.
- **Opex units.** The opex unit prints as "£/kW". I read it as per year.
- **Lifetimes.** These are financial lifetimes. p.30: "The lifetimes presented are financial, rather than technical."

### Exhibit 3.12: RTE (main report p.31) [V]

| Technology | RTE |
|---|---|
| Li-ion | 85% |
| LAES | 55% |
| CAES | 60% |
| PSH | 75% |

Plausible cycles per year for 72 h PSH: 20–40.

### PSH lower-capex sensitivity (p.33–34) [V]
Quote: "The lower value is set at a 35% reduction to the base value", based on European PSH capex (p.34). Scenario #3 applies this case.

### [D] Implied incremental energy cost (2030, real 2019 £)

| Technology | Duration step | £/kWh |
|---|---|---|
| Li-ion | 4→6 h | 117 |
| Li-ion | 6→9 h | 133 |
| LAES | 6→12 h | ≈31 |
| CAES | 6→20 h | 28 |
| CAES | 20→72 h | 4.9 |
| PSH | 6→20 h | 14.4 |
| PSH | 20→72 h | 7.8 |

**Li-ion 16 h (not in source).** Linear extrapolation from 9 h gives ≈ £2,260/kW (2030, £2019). This is extrapolation only.

---

## 3. NESO (2025), *FES 2025 Economics Inputs Data Workbook* and *Economics Assumptions*

- Citation: NESO (2025). *Future Energy Scenarios 2025: Economics Inputs Data Workbook*, sheets E.02 and E.03. Also *FES 2025 Economics Assumptions*. Published with FES 2025 on 14 July 2025.
- URLs: https://www.neso.energy/document/374261/download (inputs) and https://www.neso.energy/document/374256/download (assumptions). Index page: https://www.neso.energy/publications/future-energy-scenarios-fes/fes-documents
- Files: `neso_fes2025_econ_inputs.xlsx` and `neso_fes2025_econ_assumptions.xlsx` (sheet/row refs, no pages). Accessed 2026-10-30.
- **Price base: 2025 prices.** Sheet "General": "Any cost values are in 2025 prices unless otherwise stated." [V]
- **Provenance** [V] (Assumptions, "Data Bibliography"):
  - **Batteries:** battery CapEx is sourced from "Modo | Not public data | 2025". Battery OpEx is from the BEIS 2022 report.
  - **CAES and PSH:** CAES and PSH CapEx/OpEx are from the BEIS (AFRY) 2022 report.
- **Finding [D]: FES 2025 = AFRY 2022 × 1.241.** FES non-battery storage values equal AFRY 2022 Exhibit 3.11 multiplied by 1.241. That factor equals the GDP deflator 2019→2025 in sheet EA.01 (100/80.57). Examples: PSH 6 h 1478×1.241 = 1833.8; CAES 6 h 993×1.241 = 1232.1; CAES opex 13×1.241 = 16.1.
  - FES holds the AFRY 2030 value flat for 2025–2030.
  - **So FES is not an independent PSH/CAES/LAES estimate.**

### Sheet E.03: CapEx (£2025/kW) and fixed OpEx (£2025/kW/yr) [V]

| Type | Capex 2025 | 2030 | 2035 | 2050 | Fixed opex | Hurdle |
|---|---|---|---|---|---|---|
| Battery 4 h | 1036.3 | 654.0 | 603.6 | 554.1 | 12.4 | 7.3% |
| Battery 6 h | 1428.0 | 901.2 | 828.3 | 748.9 | 13.6 | 7.3% |
| Battery 9 h | 2050.5 | 1280.3 | 1173.6 | 1050.1 | 16.1 | 7.3% |
| LAES 6 / 9 / 12 h | 1346.2 / 1461.6 / 1575.7 | same | 1325.4 / 1438.9 / 1551.5 | 1263.1 / 1371.0 / 1479.0 | 16.1 | 10% |
| CAES 6 / 20 / 72 h | 1232.1 / 1718.4 / 2034.8 | same | 1212.8 / 1691.8 / 2003.5 | 1155.1 / 1611.7 / 1909.5 | 16.1 | 10% |
| PSH 6 / 20 / 72 h | 1833.8 / 2084.4 / 2590.7 | same | 1817.7 / 2067.1 / 2568.0 | 1769.3 / 2015.0 / 2500.1 | 23.6 / 27.3 / 33.5 | 10% |

Workbook display issue: the hurdle-rate cells show "0.1" when rounded. The underlying values are 0.073 for batteries (seen in the raw dump) and 0.1 for the rest.

[D] Battery per-kWh, 2025:

| Battery | £/kWh |
|---|---|
| 4 h | 259 |
| 9 h | 228 |

For 9 h in 2030: £142/kWh.

### Sheet E.02: lifetime and build time [V]

| Technology | Life (yr) | Build (yr) |
|---|---|---|
| Battery (all durations) | 15 | 1 |
| CAES | 25 | 2 |
| LAES | 25 | 2 |
| PSH | 41 | **2** |

The PSH build time is notably short and differs from AFRY (4 yr) and LCP Delta (4 yr). Flag it.

---

## 4. LCP Delta and Regen for DESNZ (2024), *Scenario deployment analysis for long-duration electricity storage*

- Citation: LCP Delta and Regen (2024). *Scenario deployment analysis for long-duration electricity storage*. DESNZ Research Paper 2023/047, January 2024.
- URL: https://assets.publishing.service.gov.uk/media/659be546c23a1000128d0c51/long-duration-electricity-storage-scenario-deployment-analysis.pdf (landing page: https://www.gov.uk/government/publications/long-duration-electricity-storage-scenario-deployment-analysis)
- File: `lcpdelta2024_desnz_ldes_deployment.pdf` / `.txt` (138 pp). Accessed 2026-10-30. Printed page = PDF page.
- **Price base.** "All costs are provided on a real 2022 basis" (p.51). The Figure 13 axes read "CapEx Cost, £(real, 2022)/kW" (p.45).
- **Year label conflict.** Table 7 labels its first capex row "CapEx 2020". Flag the year-label inconsistency.
- **Basis.** The archetypes are based on MM 2018 (footnote 26 cites "Storage Cost and technical assumptions … Mott McDonald"), the cost-of-capital update and NG ESO. p.44: CapEx levels "were not updated based on the engagement with developers".

### Table 7: archetype assumptions (p.44) [V]

| Attribute | Long-dur. batteries (Li-ion / flow), 6 & 8 h | Low-eff. 6 h (CAES/LAES) | Low-eff. 12 h (CAES/LAES) | PSH medium, 8 & 12 h | PSH long, 16 & 32 h |
|---|---|---|---|---|---|
| RTE | 85% | 60% | 55% | 80% | 80% |
| Variable O&M (£/MWh) | 0 | 0 | 0 | 2 | 2 |
| Construction (yr) | 1 | 1.5 | 2 | 4 | 4 |
| Lifetime (yr) | 20 | 30 | 40 | 50 | 50 |
| Availability | 96% | 95% | 95% | 96% | 96% |
| DoD | 90% | 100% | 100% | 100% | 100% |
| **Degradation (capacity)** | **−2.5%/yr** | N/A | N/A | N/A | N/A |
| CapEx "2020" (£/kW) | 1500–3200 | 880–6000 | 880–6000 | 1200–1900 | 1200–1900 |
| CapEx 2050 (£/kW) | 430–1500 | 750–2000 | 750–2000 | 1100–1800 | 1100–1800 |
| Fixed OpEx (£/kW) | 5 | 10 | 10 | 15 | 15 |
| Hurdle | 7.3% | 7.3% | 7.3% | 6.2–7.3% | 6.2–7.3% |

Quote: "Degradation – Capacity (%) -2.5% N/A".

- **PSH long.** The 2025 low case for "Established LDS Long" is £1,180/kW (p.126).
- **Flagged values.** The PSH lifetime of 50 yr and the CAES/LAES low-efficiency hurdle of 7.3% differ from AFRY (30 yr; 10%).

### Table 4: developer survey, Regen LDES survey (p.40) [V]
Quote: "Pumped hydro £200k-1500k / MWh £15k-25k / MW / Year".

| Technology | CAPEX £/MWh | OPEX £/MW/yr |
|---|---|---|
| PSH | 200k–1,500k | 15k–25k |
| Li-ion | 400k | 26k |
| CAES | 500k | – |
| Flow | 100k–700k | 6.5k–22k |

- **Survey basis.** The unit is "£/cyclable-MWh" (p.40).
- **Reliability.** These are self-reported by a handful of developers, with no price year given. Use them only for ranges.
- **Survey RTEs (Figure 10, p.37)** [V]:

| Technology | RTE range |
|---|---|
| PSH | 78–85% |
| Flow | 70–96% |
| CAES | 55–60% |
| LAES | 55% |
| Hydro-pneumatic | 72% |
| Iron-air | 45% |

---

## 5. Aurora Energy Research (2022), *Long duration electricity storage in GB* (industry-funded, not government)

- Citation: Aurora Energy Research (2022). *Long duration electricity storage in GB*, February 2022 (slides marked "Aurora_2021.1").
- URL: https://auroraer.com/wp-content/uploads/2022/02/Aurora-Report-Long-Duration-Electricity-Storage-in-GB.pdf
- File: `aurora2022_ldes_gb.pdf` / `.txt` (43 pp). Accessed 2026-10-30.
- **LDES capex range** [V], p.11: "Longer-duration (>4hr)" storage CAPEX "£600-5,500/kW". No price year is stated on that slide.
- **Chart values (ambiguous)** [V]. p.31 has charts of Li-ion 4 h / 8 h, VFB 4 h and LAES 8 h capex in "£/kW, real 2020". The text extraction scrambles the chart labels, so I cannot reliably assign numbers to years. The legible captions are:
  - "8 hr Li-ion costs are projected to decrease by 46% by 2030 in the central rollout case"
  - "VFB costs are projected to decrease by 71% by 2030"
  - "LAES costs are projected to decrease by 75.0% by 2030"

  **Read the figure visually before using any value.**

---

## 6. Ofgem (2026), *Window 1: Minded-to decisions – Long Duration Electricity Storage* (consultation)

- Citation: Ofgem (2026). *Consultation – Window 1: Minded-to decisions – Long Duration Electricity Storage*, published 26 June 2026, response deadline 14 August 2026. Final decision expected autumn 2026.
- URL: https://consult.ofgem.gov.uk/energy-generation/ldes-window-1-minded-to-decision/supporting_documents/window-1-minded-to-decisions-long-duration-electricity-storage-consultationpdf (page: https://consult.ofgem.gov.uk/energy-generation/ldes-window-1-minded-to-decision/)
- Files:
  - `ofgem2026_ldes_w1_mindedto.pdf/.txt` (113 pp)
  - `ofgem2026_ldes_w1_impacts.pdf/.txt`, *Assessment of impacts of the proposed LDES portfolio*
  - `ofgem2026_ldes_appendix_qa.pdf/.txt`
  - `neso2026_ldes_q3p2.pdf/.txt`, NESO response to DESNZ Q3 part 2

  Accessed 2026-10-30. Printed page = PDF page.
- **No project costs are published.**
  - The Cost Assessment section (p.17–19) describes method only: P50/P10/P90 treatment, FX standardised at 18 Nov 2025, and a decommissioning-cost (Decommex) benchmark for battery groups.
  - No £ capex per project or per technology is shown. Quote (p.18): "we standardised costs with foreign exchange exposure by applying exchange rates as of 18 November 2025".
- **RTE cap.** p.21: "capping RTE values at 91% where higher values had been submitted" (Li-ion BESS). [V]
- **Energy capacity.** Energy capacity was derived from "continuous discharge capacity, discharge duration and efficiency" (p.21). So MW × hours in Table 6 may differ from developers' headline GWh (see the GB table below).
- **Table 6, "Key project inputs" (Appendix 1, p.70–73)** [V] gives MW, duration (h), RTE (%), regime 25 yr and first operation year for all 73 assessed projects. Non-Li-ion rows are copied into the GB table below.
- **Li-ion LDES RTE.** RTE submitted for 8–18 h Li-ion projects is 83–91% (Table 6). This is the only GB-specific evidence for 8 h and 16 h Li-ion performance. Examples:

| Project | MW | Duration (h) | RTE |
|---|---|---|---|
| Field New Deer | 400 | 18.03 | 85% |
| Field Netherton | 400 | 16.3 | 87% |
| Field Long Stratton | 400 | 16.05 | 90% |
| Field Fyrish | 200 | 16.5 | 87% |
| Sundon | 500 | 8 | 89% |
| Ocker Hill | 145 | 8 | 91% |

No costs are given.

### Related NESO advice docs (no cost numbers)
- `neso_356906.pdf/.txt`: NESO, *Long Duration Electricity Storage – Response to DESNZ Request: Q1 and Q2* (2025). https://neso.energy/document/356906/download
- `neso_356901.pdf/.txt`: NESO, *LDES Advice – Annex 1: Cover letter* (advice given to DESNZ in January 2025). https://neso.energy/document/356901/download

Both are policy and modelling advice. They state that CapEx will come from developer submissions. No cost assumptions are given. [V]

---

## 7. DESNZ (2025/26), *Electricity Generation Costs 2025*: negative result

- URL: https://assets.publishing.service.gov.uk/media/69ba657326909a14239612e3/electricity-generation-costs-report-2025.pdf. File: `desnz2025_generation_costs.pdf` / `.txt`.
- **The report does not cover electricity storage.** A text search finds "storage" only in CCS and hydrogen contexts. [V]
- **Pending: Frazer-Nash review for DESNZ.** DESNZ contracted Frazer-Nash Consultancy, ref PS25247, "Review of electricity storage project costs and technical assumptions". It was awarded 8 Jan 2026 and runs 12 Jan–22 May 2026, value £110,010 [S: Contracts Finder notice https://www.contractsfinder.service.gov.uk/Notice/8faa368d-fd10-44a6-8c23-d66250af0ceb, seen via search snippet]. **I found no published output as of 2026-10-30.** This will be the successor to MM 2018; watch for it.

---

## 8. Invinity Energy Systems (2026), *FY25 results presentation* (company disclosure)

- URL: https://invinity.com/wp-content/uploads/2026/06/Invinity_FY25_Results_FINAL.pdf (results released 1 June 2026). File: `invinity2026_fy25_results.pdf` / `.txt` (15 pp). Accessed 2026-10-30.
- **No £/kWh figures are disclosed** in text form; cost charts may be images. [V]
  - p.9: "On target to achieve a 66% reduction in forecast Endurium cost vs. VS3".
  - p.6: "30+ Year Lifetime" and "No Cycle-Driven Degradation" (company claims).
- **FY2025 volumes** [S, Alliance News / search snippets, not checked in the full RNS]:
  - Revenue and other income £8.7m, plus project grants £9.1m.
  - Sales 31.4 MWh; shipments 24.9 MWh.
  - An average price cannot be derived, because grants are mixed into the totals.
- **Frontier Power.** Frontier reserved up to 2 GWh of Invinity manufacturing capacity (RNS 18 Feb 2025, FCA NSM) [S].

---

## GB project costs and specs

Ofgem Table 6 (p.70–73) [V] is the authoritative source for MW / duration / RTE / first operation as assessed. Developer headline figures are shown alongside.

| Project (developer) | Tech | MW (Ofgem) | Duration h (Ofgem) | MW×h [D] | Developer headline | RTE (Ofgem) | First op. (Ofgem) | Ofgem W1 status | Stated cost | Cost source & reliability |
|---|---|---|---|---|---|---|---|---|---|---|
| Coire Glas (SSE) | PSH | 1440 | 32 | 46 GWh | "1.4GW … at least 45GWh" [V\*: https://www.coireglas.com/project]; earlier "1,300MW … 30GWh" [V\*: SSE Renewables release 9 Aug 2024] | 82% | 2033 | Minded-to (Table 1) | "over £1.5bn" (2023) and "£2bn" (later) | [S] trade press citing SSE Mar 2023 release; SSE primary page not retrievable (404). No current SSE figure; SSE says >£100m spent [V\*]. FID was targeted "late 2025 or early 2026" with construction "second half of 2026" [V\*, 9 Aug 2024]. **Low reliability; the cost predates the design change to 45 GWh.** |
| Cruachan II (Drax) | PSH | – | – | – | 600 MW | – | (was "as soon as 2030") | **Withdrew; did not bid into Window 1** | c.£500m (Jul 2023) | [V\*] Drax release 25 Jul 2023: "£500 million underground pumped storage hydro plant", "No investment decision has yet been taken". [V\*] Drax trading update 1 May 2025: "The projected cost of Cruachan II has risen over the past two years". **The £500m figure is stale.** |
| Loch Kemp Storage (Statera) | PSH | 660 | 22.3 | 14.7 GWh | "up to 600MW" [V\*: lochkempstorage.co.uk/plans-and-progress]; older 9 GWh [S] | 80% | 2030 | Minded-to | £550m | [S] blog only, undated, possibly for an older 300 MW design. **Unreliable.** Developer site: construction begins 2027, operational 2030 [V\*]. |
| Earba (Gilkes Energy / Foresight) | PSH | 1800 | 15 | 27 GWh | 1.8 GW / 40 GWh consented 2025 [S] | 79% | 2033 | Minded-to | US$2.5bn | [S] Industrial Info, Apr 2025. The Foresight stake (Oct 2026) was undisclosed. **Low reliability; currency is USD.** |
| Glenmuckloch | PSH | 182 | 9.1 | 1.66 GWh | consent "up to 400MW"; 210 MW + wind farm for sale [S] | 61% | 2030 | Ranked 23, not in minded-to list | £250m | [S] "£250m Glenmuckloch energy project up for sale". This is the sale value of a combined PSH + wind project, **not a build cost.** |
| Loch na Cathrach | PSH | 500 | 8 | 4.0 GWh | – | 78% | 2030 | Ranked 24, not minded-to | – | – |
| TeesCAES (Storelectric) | CAES | 50 | 30 | 1.5 GWh | "50MW 30-hour" [V\*: storelectric.com, 26 Jun 2026] | 62% | 2029 | Minded-to | none found | – |
| Carrington (Highview Power) | LAES (+ stability island) | not in W1 | 6 | 300 MWh | "300 MWh … 50 MW … for six hours" [V\*: Highview 13 Jun 2024] | – | stability island "August 2026"; LAES "2027" [V\*: Highview 11 Nov 2025] (originally "early 2026") | n/a | £300m funding round, "will enable the construction" | [V\*] Highview release 13 Jun 2024. **This is funding raised, not a stated total capex.** It is the best available proxy ≈ £1,000/kWh or £6,000/kW [D]. Centrica separately committed £70m (part of the round). Moderate reliability as an upper bound. |
| Hunterston (Highview Power) | LAES/BESS hybrid | 300 | 8 | 2.4 GWh | first announced 2.5 GWh (Oct 2024); now "3.2GWh hybrid" (Nov 2025) [V\*] | "See note" (hybrid) | 2030 (Ofgem); stability island "January 2028", full "2030" [V\*] | Ranked 10, **not in minded-to list** | £130m first-phase raise (stability island) | [V\*] Highview 11 Nov 2025. Jun 2024 release: next four 2.5 GWh plants "total anticipated investment of £3 billion" [V\*], i.e. ≈ £750m each [D]. [S] interview "£600m–650m" each. **The GWh figures conflict between sources.** |
| Killingholme 1 (Highview) | LAES/BESS | 300 | 8 | 2.4 GWh | "3.2GWh" [V\*, 23 Sep 2025] | hybrid | 2030 | Ranked 11, not minded-to | – | – |
| Frontier Legacy (Frontier Power, with Invinity) | VFB/Zn | 65 | 8 | 520 MWh | – | 62% | 2029 | Minded-to | none | Ofgem labels it "VFB/Zn". Frontier plans to use Invinity vanadium (VFB) and/or zinc, Eos Z3 or zinc-bromine [S]. **The technology is unresolved.** |
| Frontier, 17 other sites (Botley, Pelham, Bramford 1/2, Navenby, Wymondley, Market, Astwood, Hockcliffe, Grange Lane, Weaver, Ayr, Busby, Norwich, Willington) | VFB/Zn | 85–200 each | 8 | – | Ayr + Busby "350MW/2.8GWh" Eos zinc [S] | 62% | 2030–31 | Ranked 26–48, not minded-to | – | – |
| Hagshaw / Spirebush / LDES Barry / LDES Roosecote / Deeside | VFB | 500 / 100 / 50 / 50 / 50 | 8 | – | – | 69% | 2028–30 | Ranked 51–73, not minded-to | – | – |

### Notes on the GB table
- **Duration may be defined differently.** For several PSH projects, Ofgem's MW × duration differs from the developer's GWh: Earba 27 vs 40 GWh, Loch Kemp 14.7 vs 9 GWh. Ofgem's duration may be standardised to a state-of-charge window and RTE (p.21). Do not mix the two bases.
- **No £ project capex in any primary document.** No primary document I could read gives a current £ capex for any GB LDES project. Ofgem holds the submitted P50/P90 costs but has not published them. Every £ figure above is [S], a funding amount, or stale.
- **RTE ranges.** Ofgem RTE values give the most useful GB-specific performance data:

| Technology | RTE range |
|---|---|
| PSH | 61–82% |
| CAES | 62% |
| VFB | 69% |
| VFB/Zn | 62% |
| Li-ion | 83–91% (capped at 91%) |

---

## Summary of gaps and ambiguities
1. **No GB Li-ion 8 h / 16 h cost from a UK government source.**
   - MM 2018 covers 4 h only.
   - AFRY 2022 and FES 2025 stop at 9 h. FES battery capex comes from non-public Modo data.
   - 16 h can only be extrapolated, ≈ £120–135/kWh incremental (£2019, 2030).
2. **Flow batteries.** The only UK government numbers are MM 2018: generic flow, 2012 £, very high Yr0 values. AFRY and FES exclude flow. LCP Delta's survey gives £100k–700k/MWh.
3. **LAES.** MM 2018 excludes it. AFRY 2022 has it (in 2019 £), and FES 2025 re-indexes AFRY. There is no project capex. Highview's £300m for 300 MWh is a funding proxy only.
4. **Price-year inconsistencies.** MM: 2012 prices with year labels from 2018. LCP Delta: "2020" row label vs real 2022. FES: AFRY 2030 values held flat from 2025.
5. **Pending source.** The Frazer-Nash / DESNZ storage cost review (2026) is not yet published. It is the key pending update.
