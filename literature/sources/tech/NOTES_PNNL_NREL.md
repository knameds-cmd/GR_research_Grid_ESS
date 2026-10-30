# International (US lab) storage cost and performance: PNNL and NREL/NLR

Collected 2026-10-30 for the GB LDES model (projects online 2029–2033). Four technologies: Li-ion LFP (8 h and ~16 h), pumped storage hydro (PSH), compressed-air storage (CAES), and vanadium redox flow battery (VRFB). Liquid air (LAES) is covered elsewhere.

Tags:
- **[V]**: I read the value myself in the primary document or dataset cell.
- **[D]**: I computed the value from [V] numbers. The arithmetic is shown, and the value is not printed in the source.
- **[S]**: secondary source only, not checked in the primary.
- **(chart)**: read off a plotted marker, about ±$5/kWh. It is not a printed number.

Page references are "pN / printed". pN is the PDF page index as written in the `=== pN` markers of the .txt file. In the PNNL 2022 main body, printed page = pN − 22; front-matter pages use roman numerals. Spreadsheet references give the sheet name and Excel row number.

Currency is USD throughout. Nothing here is converted to GBP or re-based.

---

## Source A1: PNNL 2022 Cost and Performance Assessment (PNNL-33283)

- **Citation:** Viswanathan V., Mongird K., Franks R., Li X., Sprenkle V. (PNNL); Baxter R. (Mustang Prairie Energy). *2022 Grid Energy Storage Technology Cost and Performance Assessment*. Energy Storage Grand Challenge. PNNL-33283, August 2022.
- **URL:** https://www.pnnl.gov/sites/default/files/media/file/ESGC%20Cost%20Performance%20Report%202022%20PNNL-33283.pdf
- **Accessed:** 2026-10-30.
- **Saved as:** `pnnl2022_cost_performance.pdf`, with text in `pnnl2022_cost_performance.txt` (174 pages).
- **Cost year:** the report does **not** state a dollar year explicitly. It says "data for this report was obtained in the year 2021", and all "current" values are labelled 2021 (p4 / iii; p6 / v). Treat these as about 2021 USD (nominal 2021). This is an inference.
- **Main tables are images.** The cost tables (Figs 4.3, 4.10, 4.14, 4.16) are pictures, so the .txt file does not contain them. I rendered those pages and read them visually.
- **Battery sizes in the detailed tables.** For batteries, the detailed tables cover only 1 MW and 10 MW. The 100 MW and 1,000 MW battery values appear only as chart markers (Fig 4.4, Fig 4.11, ES-2) or in Executive Summary text.

### What "total installed cost" includes (PNNL 2022)

| item | included? | page | quote / label |
|---|---|---|---|
| Battery CAPEX components [V] | storage block (SB), storage balance of system (SBOS), power equipment, controls & communication (C&C), system integration, EPC, project development, grid integration | p29 / 7, Fig 2.2 | "ESSs Included in Total Installed Cost for each Storage Technology" |
| Grid integration [V] | yes: transformer, metering, isolation breakers | p31 / 9 | "costs associated with connecting the ESS to the grid, including transformer cost, metering, and isolation breakers" |
| Project development [V] | yes: permitting, PPA, interconnection agreements, site control, financing | p30 / 8 | "permitting, power purchase agreements, interconnection agreements, site control, and financing" |
| PSH: EPC, project development, grid integration [V] | lumped into a "contingency fee" | p28 / 6 | "captured in a catch-all contingency fee cost component for PSH" |
| CAES: EPC, BOP, grid [V] | inside the "Turbine, Compressor, BOP & EPC Management" $/kW line; BOP includes transmission interconnection and contingency | p83 / 61 | "BOP, which includes permitting, transmission interconnection, natural gas pipeline construction, and contingency" |
| Variable O&M [V] | removed (0) | p31 / 9, fn 6 | "O&M variable cost of $0.0005/kWh … has been removed" |
| Network reinforcement | not mentioned (ambiguous) | | |

### Li-ion LFP (PNNL 2022)

Duration note: PNNL gives 8, 10, 24 and 100 h. Use 8 h, and 24 h as the nearest to ~16 h. Detailed component tables exist only for 1 MW and 10 MW.

| parameter | value | unit | cost year & currency | page (pdf / printed) | quote or table label |
|---|---|---|---|---|---|
| Total installed, 100 MW 10 h, 2021 [V] | 356 | $/kWh | ~2021 USD | p8 / vii | "100 MW, 10-hour battery systems of: Li-ion LFP ($356/kWh)" |
| Total installed, 100 MW 4 h, 2021 / 2030 [V] | 385 / 291 | $/kWh | ~2021 USD | p8 / vii | "At 100 MW, 4 hours, LFP … $385/kWh"; "LFP ($291/kWh)" |
| Total installed, 100 MW 8 h, 2021 / 2030 (chart) [V] | ≈362 / ≈272 | $/kWh | ~2021 USD | p47 / 25, Fig 4.4 | chart marker, "Total Installed Costs Ranges – LFP" |
| Total installed, 100 MW 24 h, 2021 / 2030 (chart) [V] | ≈342 / ≈256 | $/kWh | ~2021 USD | p47 / 25, Fig 4.4 | chart marker |
| Total installed, 1,000 MW 8 h, 2021 / 2030 (chart) [V] | ≈343 / ≈258 | $/kWh | ~2021 USD | p47 / 25, Fig 4.4 | chart marker |
| Total installed, 1,000 MW 24 h, 2021 / 2030 (chart) [V] | ≈326 / ≈243 | $/kWh | ~2021 USD | p47 / 25, Fig 4.4 | chart marker |
| Total installed, 10 MW 10 h, 2021 / 2030 [V] | 376.67 / 282.83 ($3,767 / $2,828 per kW) | $/kWh | ~2021 USD | p46 / 24, Fig 4.3 | "Total Installed Cost ($/kWh)" |
| Total installed, 10 MW 24 h, 2021 / 2030 [V] | 359.62 / 268.98 ($8,631 / $6,456 per kW) | $/kWh | ~2021 USD | p46 / 24, Fig 4.3 | same table |
| Split, 10 MW 10 h, 2021 [V] | DC SB 170.36; DC BOS 38.17; Sys. integ. 43.24; EPC 51.97; Proj. dev. 62.37 ($/kWh). Power equip. 73.05; C&C 7.75; Grid integ. 24.81 ($/kW) | mixed | ~2021 USD | p46 / 24, Fig 4.3 | row labels as listed |
| Split, 10 MW 10 h, 2030 [V] | SB 111.48; BOS 28.50; SI 36.69; EPC 44.10; PD 52.92 ($/kWh). PE 64.62; C&C 5.78; GI 21.05 ($/kW) | mixed | ~2021 USD | p46 / 24 | as above |
| Fixed O&M, 10 MW 10 h / 24 h, 2021 [V] | 9.87 / 21.98 (2030: 8.38 / 18.65) | $/kW-yr | ~2021 USD | p46 / 24 | "Fixed O&M ($/kW-yr)" |
| Fixed O&M basis [V] | 0.43% of direct capital (SB, SBOS, power equipment), plus power-equipment refurbishment of 30% every 10 yr | – | – | p39 / 17 | "assumed to be 30% of the power equipment … incurred every 10 years" |
| Variable O&M [V] | 0 (removed) | $/MWh | – | p31 / 9 | see inclusion table |
| RTE (AC-AC, at transformer) [V] | 82.59% (2021) → 84.52% (2030); shown rounded as 83% / 85% | % | – | p44 / 22, Table 4.4 | "LFP 89.55% 91.63% 86.00% 88.00% 82.59% 84.52%" |
| Calendar life [V] | 16 (unchanged in 2030) | years | – | p41 / 19 | "new calendar lives of 16 years for LFP" |
| Cycle life [V] | 2,400 (2021); 2,640 (2030, +10%) at 80% DOD, counted until 80% of rated energy remains | cycles | – | p43 / 21; p44 / 22; p147 / 125, Table 6.4 | "cycle life at 80% DOD for LFP … 2,400" |
| Degradation [V] | Fade is linear with cycles down to end of life at 60% of rated energy; 4,800 cycles at 100% DOD | – | – | p41 / 19, Table 4.2 | "assigns end-of-life condition when available energy is 60% rated energy" |
| Augmentation [V] | SB is augmented each time usable energy reaches the DOD level; DOD 80% at first, 60% after the first augmentation; repeated until 20–25 yr life; augmentation priced at DC SB $/kWh | – | p148 / 126 – p149 / 127 | "Additional augmentations are done each time the available energy of SB reaches 60%" |
| Warranty [V] | LFP: no extra warranty cost | – | – | p39 / 17 | "Li-ion LFP batteries are not expected to incur an additional warranty cost" |
| Recycling / decommissioning [V] | 2.65 $/kWh (2021); 0 (2030) | $/kWh | ~2021 USD | p46 / 24 | "Recycling/Disposal ($/kWh)" |
| Project life / construction [V] | 20–25 yr project life; 1 yr construction | years | – | p144 / 122, Table 6.2 | "Li-ion LFP 20-25 1" |
| Economic life (LCOS) [V] | 20 | years | – | p142 / 120 | "economic life for each project is 20 years" |
| Annual cycling limit (LCOS) [V] | 365 equivalent 100%-DOD cycles per year | – | – | p145 / 123 | "assumed to be 365 cycles per year at 100% DOD" |

### Vanadium redox flow (PNNL 2022)

Duration note: 8 h and 10 h are given.

| parameter | value | unit | cost year & currency | page | quote or label |
|---|---|---|---|---|---|
| Total installed, 100 MW 10 h, 2021 [V] | 385 | $/kWh | ~2021 USD | p8 / vii | "vanadium RFB ($385/kWh)" |
| Total installed, 100 MW 8 h, 2021 / 2030 (chart) [V] | ≈404 / ≈336 | $/kWh | ~2021 USD | p65 / 43, Fig 4.11 | chart marker |
| Total installed, 100 MW 10 h, 2030 (chart) [V] | ≈318 | $/kWh | ~2021 USD | p65 / 43 | chart marker |
| Total installed, 1,000 MW 10 h, 2021 / 2030 (chart) [V] | ≈364 / ≈302 | $/kWh | ~2021 USD | p65 / 43 | chart marker |
| Total installed, 10 MW 10 h, 2021 / 2030 [V] | 407.89 / 338.57 ($4,079 / $3,386 per kW) | $/kWh | ~2021 USD | p64 / 42, Fig 4.10 | "Total Installed Cost ($/kWh)" |
| Split, 10 MW 10 h, 2021 [V] | DC SB 210.44; DC BOS 42.09; SI 39.93; EPC 45.98; PD 52.88 ($/kWh). PE 133.00; C&C 7.80; GI 25.00 ($/kW) | mixed | ~2021 USD | p64 / 42 | row labels |
| Split, 10 MW 8 h, 2021 (table) [V] | DC SB 219; DC BOS 44; SI 42; EPC 48; PD 56 ($/kWh). DC-DC 60; PCS 73; EMS 7.8; GI 25 ($/kW) | mixed | ~2021 USD | p59 / 37, Table 4.7 | "Redox Flow Battery Component Cost for 2021 for 10 MW" |
| Split, 10 MW 8 h, 2030 (table) [V] | DC module 182; BOS 33; SI 36; EPC 41; PD 47 ($/kWh). DC-DC 53; PCS 65; EMS 6; GI 21 ($/kW) | mixed | ~2021 USD | p60 / 38, Table 4.8 | "RFB Component Cost for 2030 for 10 MW" |
| Fixed O&M, 10 MW 10 h [V] | 12.08 (2021); 10.63 (2030) | $/kW-yr | ~2021 USD | p64 / 42 | "Fixed O&M ($/kW-yr)" |
| Fixed O&M basis [V] | 0.43% of direct capital, plus power-equipment augmentation (30%) every 10 yr | – | – | p61 / 39 | "fixed O&M is set to 0.43% of direct capital cost" |
| Warranty [V] | 2.5% of DC SB+BOS (excluding electrolyte), paid every year; 1.25–2.59 $/kWh-yr | $/kWh-yr | ~2021 USD | p61 / 39 | "warranty cost of 2.5% of the DC SB and DC BOS" |
| RTE (AC-AC, at transformer) [V] | 65% (2021 and 2030); DC-DC 71% | % | – | p63 / 41, Table 4.9 | "71% 71% 68% 68% 65% 65%" |
| Calendar life (stacks) [V] | 12 yr; stacks and pumps replaced afterwards | years | – | p62 / 40 | "calendar life used in this report for RFB stacks is 12 years" |
| Cycle life [V] | "Unlimited" (electrolyte) | – | – | p64 / 42; Table 6.4 | "Cycle Life (#) Unlimited" |
| Degradation [V] | Electrolyte degradation about 1% over 25 yr (developer claim) | – | – | p62 / 40 | "electrolyte degradation of 1% over 25 years" |
| Replacement [V] | Stack and pump replacement at end of calendar life; warranty every year | – | – | p148 / 126, Table 6.5 | "Stack Replacement End of calendar life" |
| Recycling, 10 MW 10 h [V] | 26.74 (2021) / 23.02 (2030) | $/kWh | ~2021 USD | p64 / 42 | "Recycling/Disposal ($/kWh)" |
| Project life / construction [V] | 24 yr; 1 yr | years | – | p144 / 122, Table 6.2 | "Vanadium RFB 24 1" |

### Pumped storage hydro (PSH, PNNL 2022)

Sizes: 100 and 1,000 MW at 4, 10, 24 and 100 h. The detailed table covers 4 h and 10 h only; 24 h appears in ES text and the chart.

| parameter | value | unit | cost year & currency | page | quote or label |
|---|---|---|---|---|---|
| Total installed, 1,000 MW 10 h [V] | 220.67 $/kWh ($2,207/kW), 2021 = 2030 | $/kWh | ~2021 USD | p90 / 68, Fig 4.16 | "Total Installed Cost ($/kWh)" |
| Split, 1,000 MW 10 h [V] | Reservoir 64 $/kWh. Powerhouse 623, electromechanical 392, contingency 551.67 ($/kW) | mixed | ~2021 USD | p90 / 68 | "Reservoir Construction & Infrastructure ($/kWh)" |
| Total installed, 100 MW 10 h [V] | 262.53 $/kWh ($2,625/kW). Reservoir 76; powerhouse 742; E-M 467; contingency 656.33 | $/kWh | ~2021 USD | p90 / 68; p8 / vii | "$263/kWh for a 100 MW, 10-hour installed system" |
| Total installed, 100 MW 24 h [V] | 143 | $/kWh | ~2021 USD | p8 / vii | "For a 24-hour system, the total installed cost is reduced to $143/kWh" |
| Total installed, 1,000 MW 24 h (chart) [V] | ≈119 | $/kWh | ~2021 USD | p91 / 69, Fig 4.17 | chart marker |
| Cost range method [V] | low/high = 0.9× / 1.1× of point value; no learning to 2030, so 2030 = 2021 | – | – | p88 / 66 | "No learning rates were assigned for year 2030" |
| Fixed O&M [V] | 15.59 (1,000 MW 10 h); 28.19 (100 MW 10 h). Range about 15–52 depending on size and duration | $/kW-yr | ~2021 USD | p90 / 68; p88 / 66, Table 4.29 | "Total fixed O&M ($/kW-year) $28.19 $15.60" |
| O&M split, 1,000 MW 10 h [V] | labour 3.15; parts 5.59; refurbishment 6.85 | $/kW-yr | ~2021 USD | p88 / 66, Table 4.29 | "Labor related … Parts related … Refurbishment related" |
| Variable O&M [V] | none; deep repair and refurbishment are folded into fixed O&M | – | – | p88 / 66 | "have been denoted as total fixed O&M in this study" |
| RTE [V] | 80% (2021 and 2030) | % | – | p89 / 67 | "RTE for PSH systems … at 80%" |
| Calendar life [V] | 60 | years | – | p89 / 67 | "calendar life for PSH has been extended … to be 60 years" |
| Cycle life [V] | Unlimited | – | – | p90 / 68 | "Cycle Life (#) Unlimited" |
| Construction period [V] | 5 yr; the report calls this "moderately optimistic" | years | – | p144 / 122 | "assumed to have a construction period of 5 years" |
| Project life (LCOS) [V] | 60 | years | – | p144 / 122, Table 6.2 | "PSH 60 5" |

Flag: in Fig 4.16, the "Contingency Fee ($/kW)" row for 4 h is identical to the total $/kWh figure (511 and 429). This looks like a labelling or layout quirk in the figure. The 10 h columns add up correctly: 76×10 + 742 + 467 + 656.33 = 2,625.

### CAES (PNNL 2022)

PNNL models **diabatic** CAES, which burns natural gas on discharge (p7 / vi). Only the cavern cost uses adiabatic ("green CAES") project data (p83 / 61). PNNL gives **no separate adiabatic CAES cost**. This is a gap.

| parameter | value | unit | cost year & currency | page | quote or label |
|---|---|---|---|---|---|
| Total installed, 1,000 MW 10 h [V] | 112.41 $/kWh ($1,124/kW), 2021 = 2030 | $/kWh | ~2021 USD | p86 / 64, Fig 4.14 | "Total Installed Cost ($/kWh)" |
| Total installed, 1,000 MW 24 h [V] | 50.32 $/kWh ($1,208/kW) | $/kWh | ~2021 USD | p86 / 64 | same |
| Total installed, 100 MW 10 h / 24 h [V] | 122.14 / 54.68 $/kWh ($1,221 / $1,312 per kW) | $/kWh | ~2021 USD | p86 / 64; p8 / vii | "$122/kWh for a 100 MW, 10 hour system" |
| Split [V] | Cavern 6.31 $/kWh (1,000 MW 10 h); turbine, compressor, BOP & EPC management 1,061 $/kW (1,000 MW) and 1,153 $/kW (100 MW) | mixed | ~2021 USD | p86 / 64 | "Turbine, Compressor, BOP, & EPC Management ($/kW)" |
| Cavern cost basis [V] | 6.9 $/kWh point (range 2.7–13.8) | $/kWh | ~2021 USD | p83 / 61, Table 4.28 | "average cost of $6.9/kWh was used as the single-point estimate" |
| Adiabatic power island (reference only) [V] | 890 $/kW (40 MW); 725 $/kW (1,000 MW) | $/kW | ~2021 USD | p83 / 61 | "power island cost for adiabatic CAES was $890/kW for a 40 MW system" |
| Fixed O&M [V] | 9.82 (1,000 MW 10 h); 16.12 (100 MW 10 h) | $/kW-yr | ~2021 USD | p84 / 62; p86 / 64 | "fixed O&M for CAES is estimated to be $16.12/kW-year" |
| Variable O&M / fuel | not given (fuel use not costed in the table) — gap | | | | |
| RTE [V] | 52% (2021 and 2030) | % | – | p85 / 63 | "RTE for CAES … at 52% for 2021 and 2030" |
| Calendar life [V] | 60 | years | – | p84 / 62 | "calendar life for CAES has been extended … to be 60 years" |
| Construction period [V] | 3 | years | – | p144 / 122 | "CAES 60 3" |
| 2030 projection [V] | none: no learning applied, so 2030 = 2021 | – | – | p84 / 62 | "No learning rates were assigned for year 2030" |

---

## Source A2: PNNL Energy Storage Cost and Performance Database v2024 (later PNNL update)

- **Citation:** PNNL (2024). *Energy Storage Cost and Performance Database v2024* (ESGC).
- **URLs:** download page https://www.pnnl.gov/projects/esgc-cost-performance/download-reports; file https://www.pnnl.gov/sites/default/files/media/file/ESGC_Cost_Performance_Database_v2024.xlsx
- **Accessed:** 2026-10-30.
- **Saved as:** `pnnl_esgc_database_v2024.xlsx`, with sheets "Introduction", "Database" (21,864 rows) and "Terms & Abbreviations".
- **No written report.** The download page says the v2024 values "do not currently have an associated report". The only PNNL PDFs are the 2020 and 2022 reports. No 2023 PNNL report was found.
- **Scope (Introduction sheet text box) [V]:** "2023 & 2030 cost and performance estimates are provided for" Li-ion LFP/NMC, VRFB, PSH, CAES and others. Hydrogen and gravitational values are 2021 numbers that were not updated.
- **Cost year:** **not stated.** The estimates are labelled "2023" (current) and "2030". NREL's Cole et al. 2025 lists this database as a source and assumes publication year when the dollar year is missing. Treat as about 2023 USD (inferred).
- **Column layout of the Database sheet:** Technology, Year, Power_MW, Duration_hr, Estimate_type (Low/Point/High), Parameter_category, Parameter, Value. Row numbers below are Excel rows.
- **Low/High for performance.** The note says "low" performance estimates are the *better* values, not the numerically lower ones.
- **Cost components** are defined as in the 2022 report: SB, SBOS, power equipment, C&C, system integration, EPC, project development, grid integration. No variable O&M row exists.

### Li-ion LFP (PNNL v2024): point estimates (Low–High in brackets)

Duration note: 8 h, 10 h and 24 h. There is no 16 h case.

| parameter | value | unit | cost year | ref (sheet Database, row) | label |
|---|---|---|---|---|---|
| Total installed, 100 MW 8 h, 2023 [V] | 352.91 (317.62–388.19); $2,823/kW | $/kWh | ~2023 USD | row 7475 (Point) | "Total Installed Cost ($/kWh)" |
| Total installed, 100 MW 8 h, 2030 [V] | 272.18 (229.92–311.42); $2,177/kW | $/kWh | ~2023 USD | row 9491 | same |
| Total installed, 100 MW 10 h, 2023 / 2030 [V] | 349.07 / 269.00 | $/kWh | ~2023 USD | rows 7547 / 9563 | same |
| Total installed, 100 MW 24 h, 2023 [V] | 338.36 (304.54–372.19); $8,121/kW | $/kWh | ~2023 USD | row 7619 | same |
| Total installed, 100 MW 24 h, 2030 [V] | 260.58 (220.06–298.63) | $/kWh | ~2023 USD | row 9635 | same |
| Total installed, 1,000 MW 8 h, 2023 / 2030 [V] | 334.01 / 257.64 | $/kWh | ~2023 USD | rows 7979 / 9995 | same |
| Total installed, 1,000 MW 10 h, 2023 / 2030 [V] | 331.11 (298–364.21) / 255.60 | $/kWh | ~2023 USD | rows 8051 / 10067 | same |
| Total installed, 1,000 MW 24 h, 2023 / 2030 [V] | 321.98 / 247.63 | $/kWh | ~2023 USD | rows 8123 / 10139 | same |
| Split, 100 MW 8 h, 2023 [V] | DC SB 183.35; DC BOS 34.55; SI 37.77; EPC 39.39; PD 47.27 ($/kWh). PE 63.48; C&C 1.30; GI 19.89 ($/kW) | mixed | ~2023 USD | rows 7454–7461 | parameter names as listed |
| Split, 100 MW 8 h, 2030 [V] | SB 133.33; BOS 27.14; SI 32.04; EPC 32.08; PD 38.39 ($/kWh). PE 55.77; C&C 0.96; GI 16.87 ($/kW) | mixed | ~2023 USD | rows 9470–9477 | same |
| Fixed O&M, 100 MW 8 h / 24 h, 2023 [V] | 7.63 / 20.84 (2030: 6.48 / 17.68) | $/kW-yr | ~2023 USD | rows 7462 / 7606; 9478 / 9622 | "Fixed O&M ($/kW-year)" |
| RTE [V] | 0.83 (2023); 0.85 (2030) | – | – | row 7466 / 9482 | "RTE (%)" |
| Calendar life [V] | 16 | years | – | row 7467 | "Calendar Life (yrs)" |
| Cycle life [V] | 2,400 at 80% DOD; 8,000 at 60% DOD (2030: 2,640 / 8,800). Low (best) case 4,550 / 9,100 | cycles | – | rows 7469–7471 | "Cycle Life at Primary DOD (#)" |
| End of life [V] | 0.6 of rated energy | – | – | row 7472 | "End of Life (%)" |
| Recycling [V] | 2.65 (2023) / 0 (2030) | $/kWh | ~2023 USD | row 7463 | "Recycling ($/kWh)" |
| LCOS project life [V] | 25 yr (8 h); 28 yr (24 h) for 2023 | years | – | rows 7476 / 7620 | "LCOS_Project_Life (yrs)" |

### VRFB (PNNL v2024)

| parameter | value | unit | cost year | ref (row) | label |
|---|---|---|---|---|---|
| Total installed, 100 MW 8 h, 2023 [V] | 480.78 (432.70–528.86); $3,846/kW | $/kWh | ~2023 USD | row 17363 | "Total Installed Cost ($/kWh)" |
| Total installed, 100 MW 8 h, 2030 [V] | 438.01 (364.65–495.57) | $/kWh | ~2023 USD | row 19379 | same |
| Total installed, 100 MW 10 h, 2023 / 2030 [V] | 446.23 / 409.37 | $/kWh | ~2023 USD | rows 17435 / 19451 | same |
| Total installed, 1,000 MW 10 h, 2023 / 2030 [V] | 423.83 / 388.54 | $/kWh | ~2023 USD | rows 17939 / 19955 | same |
| Split, 100 MW 8 h, 2023 [V] | DC SB 275.77; DC BOS 62.02; SI 37.68; EPC 41.06; PD 47.22 ($/kWh). PE 114.79; C&C 1.42; GI 20 ($/kW) | mixed | ~2023 USD | rows 17342–17349 (Point) | as listed |
| Fixed O&M, 100 MW 8 h / 10 h [V] | 9.59 / 11.39 (2030: 8.50 / 9.95) | $/kW-yr | ~2023 USD | rows 17350 / 17422 (Point) | "Fixed O&M ($/kW-year)" |
| Stack replacement cost [V] | 542 (2023); 492.7 (2030) | $/kW | ~2023 USD | row 17353 (Point) | "Redox Flow Stack Replacement Cost ($/kW)" |
| Warranty [V] | 1.46 (100 MW 8 h, 2023) | $/kWh | ~2023 USD | row 17352 | "Warranty ($/kWh)" |
| Recycling [V] | 26.58 (100 MW 8 h, 2023) | $/kWh | ~2023 USD | row 17351 | "Recycling ($/kWh)" |
| RTE [V] | 0.65 | – | – | row 17356 | "RTE (%)" |
| Calendar life [V] | 12 (stack) | years | – | row 17357 | "Calendar Life (yrs)" |
| Cycle life [V] | 5,250 at 80% DOD (changed from "Unlimited" in 2022) | cycles | – | row 17359 | "Cycle Life at Primary DOD (#)" |
| End of life [V] | 0.8 | – | – | row 17360 | "End of Life (%)" |
| LCOS project life [V] | 24 | years | – | row 17364 | "LCOS_Project_Life (yrs)" |

Flag: the v2024 VRFB costs are *higher* than the 2022 report's (100 MW 10 h: 446 vs 385 $/kWh). The two editions should not be mixed.

### PSH (PNNL v2024): 2030 = 2023 in every case (no learning)

| parameter | value | unit | cost year | ref (row) | label |
|---|---|---|---|---|---|
| Total installed, 1,000 MW 10 h [V] | 201.99 (181.79–222.19); $2,020/kW | $/kWh | ~2023 USD | rows 14681 / 15041 (2030) | "Total Installed Cost ($/kWh)" |
| Total installed, 1,000 MW 24 h [V] | 89.78 (80.80–98.75); $2,155/kW | $/kWh | ~2023 USD | row 14726 | same |
| Total installed, 100 MW 10 h / 24 h [V] | 278.68 / 122.93 ($2,787 / $2,950 per kW) | $/kWh | ~2023 USD | rows 14501 / 14546 | same |
| Split, 1,000 MW 10 h [V] | Reservoir 25.71 $/kWh. Powerhouse 623, electromechanical 471, EPC indirect + contingency 668.79 ($/kW) | mixed | ~2023 USD | rows 14669–14672 (Point) | "PSH EPC Contractor Indirect Costs + Contingency ($/kW)" |
| Split, 1,000 MW 24 h [V] | Reservoir 14.47 $/kWh. Powerhouse 623; E-M 471; EPC + contingency 713.39 ($/kW) | mixed | ~2023 USD | rows 14714–14717 (Point) | same |
| Fixed O&M [V] | 14.62 (1,000 MW); 27.21 (100 MW) | $/kW-yr | ~2023 USD | rows 14673 / 14493 (Point) | "Fixed O&M ($/kW-year)" |
| RTE / calendar life [V] | 0.80 / 60 yr | – | – | rows 14676–14677 | "RTE (%)", "Calendar Life (yrs)" |

Flag: the reservoir cost per kWh fell sharply compared with 2022 (1,000 MW 10 h: 25.71 vs 64 $/kWh), while the EPC + contingency line rose.

### CAES (PNNL v2024): 2030 = 2023 in every case

| parameter | value | unit | cost year | ref (row) | label |
|---|---|---|---|---|---|
| Total installed, 1,000 MW 10 h [V] | 102.54 (89.45–122.75); $1,025/kW | $/kWh | ~2023 USD | rows 233 / 545 (2030) | "Total Installed Cost ($/kWh)" |
| Total installed, 1,000 MW 24 h [V] | 45.89 (38.61–60.67); $1,101/kW | $/kWh | ~2023 USD | row 272 | same |
| Total installed, 100 MW 10 h / 24 h [V] | 112.53 / 50.31 | $/kWh | ~2023 USD | rows 77 / 116 | same |
| Split, 1,000 MW 10 h [V] | power 966.47 $/kW (869.82–1,063.11); cavern 5.89 $/kWh (2.47–16.44) | mixed | ~2023 USD | rows 223–224 (Point; Low/High blocks adjacent) | "CAES Capital (Turbine, Compressor, BOP, & EPC Management) ($/kW)" |
| Fixed O&M [V] | 9.18 (1,000 MW 10 h); 15.43 (100 MW 10 h) | $/kW-yr | ~2023 USD | rows 225 / 69 (Point) | "Fixed O&M ($/kW-year)" |
| RTE [V] | Point 0.55; "Low" (best) 0.69 at 1,000 MW and 0.65 at 100 MW; High 0.52 | – | – | rows 202 (Low), 228 (Point) | "RTE (%)" |
| Calendar life [V] | 60 | years | – | row 229 | "Calendar Life (yrs)" |

Flag: the database does not say whether the v2024 CAES is diabatic or adiabatic. The 0.65–0.69 "best" RTE suggests adiabatic-type performance in the best case. This is an inference.

---

## Source B1: NREL "Cost Projections for Utility-Scale Battery Storage: 2025 Update"

- **Citation:** Cole W., Ramasamy V., Turan M. (2025). *Cost Projections for Utility-Scale Battery Storage: 2025 Update*. NREL/TP-6A40-93281, June 2025. NREL has since been renamed National Laboratory of the Rockies (NLR).
- **URLs:** https://www.nrel.gov/docs/fy25osti/93281.pdf, which now redirects to https://docs.nlr.gov/docs/fy25osti/93281.pdf. Landing page: https://research-hub.nlr.gov/en/publications/cost-projections-for-utility-scale-battery-storage-2025-update/
- **Accessed:** 2026-10-30.
- **Saved as:** `nrel2025_cole_battery_cost_projections.pdf`, with text in the matching .txt (26 pages). Printed page = pN − 7 from p8 on.
- **Cost year:** 2024 USD (p5 / iv: "values in 2024$").
- **Scope:** Li-ion (LFP cells), 4 h reference system. Other durations come from a linear energy + power fit over 1–10 h. Nothing beyond 10 h, and no VRFB, PSH or CAES.

| parameter | value | unit | cost year | page (pdf / printed) | quote or label |
|---|---|---|---|---|---|
| Total overnight capex, 4 h, 2024 [V] | 334 | $/kWh | 2024 USD | p13 / 6, Fig 1; p15 / 8 | "The 2024 starting point of $334/kWh" |
| 2024 split (bottom-up) [V] | energy 241 $/kWh; power 372 $/kW (fit 379, adjusted down by 7) | mixed | 2024 USD | p13 / 6 | "energy cost is $241/kWh, and the power cost is … $372/kW" |
| Capex formula [V] | Total ($/kW) = Energy ($/kWh) × Duration (h) + Power ($/kW); fitted over 1–10 h | – | – | p13 / 6 | "Total Cost ($/kW) = Energy Cost ($/kWh) * Duration (hr) + Power Cost ($/kW)" |
| Derived 8 h, 2024 [D] | 241×8 + 372 = 2,300 $/kW ≈ 287.5 $/kWh | $/kWh | 2024 USD | from p13 / 6 | arithmetic only |
| Derived 16 h, 2024 [D] | 241×16 + 372 = 4,228 $/kW ≈ 264 $/kWh. This **extrapolates** beyond the 1–10 h fit | $/kWh | 2024 USD | from p13 / 6 | arithmetic only; use with caution |
| 2024 bottom-up breakdown, 4 h [V] | cabinets 210; inverter 26; SBOS 5; EBOS 44; labour 2; permitting & interconnection 2; sales tax 17; contingency 7; EPC overhead 6; profit 14 | $/kWh | 2024 USD | p13 / 6, Fig 1 (rendered) | category legend of Fig 1 |
| What capex includes [V] | EBOS includes transformer, switchgear, SCADA, MV-HV substation, transmission line and network-upgrade equipment; contingency included | – | – | p11 / 4 | "MV to HV substation equipment, transmission line, and network upgrade related equipment" |
| What capex excludes [V] | interconnection upgrade costs are excluded from "Permitting & interconnection". This partly conflicts with the EBOS wording above | – | – | p11 / 4; p26 / 19 | "Cost of interconnection upgrades are not included in these costs" |
| 4 h projection, 2030, low / mid / high [V] | 207 / 279 / 354 | $/kWh | 2024 USD | p23 / 16, Table 2 | "2030 0.62 0.84 1.06 207 279 354" |
| 4 h projection, 2029 / 2033, mid [V] | 286 / 257 | $/kWh | 2024 USD | p23 / 16, Table 2 | Table 2 rows |
| 2035 / 2050, mid [V] | 243 / 178 | $/kWh | 2024 USD | p23 / 16 | Table 2. The text on p15 / 8 prints "$234/kWh" for 2035 mid, which looks like a typo (ES and Table 2 say 243) |
| Fixed O&M [V] | 4% of the $/kW capital cost of a 4 h battery; **includes augmentation** to hold rated capacity | %/yr | – | p18 / 11 | "The FOM value selected is 4% of the $/kW capacity cost" |
| Fixed O&M, 4 h 2024 [D] | 0.04 × 334 × 4 ≈ 53 $/kW-yr. The chart marker reads about 56 | $/kW-yr | 2024 USD | p18 / 11; p19 / 12 Fig 8 | derived |
| Variable O&M [V] | 0 | $/MWh | – | p18 / 11 | "we have adopted zero for the VOM" |
| Degradation / augmentation [V] | Augmentation sits inside FOM; assumes about 1 cycle/day; FOM may be too low at higher cycling | – | – | p18 / 11 | "assume that this FOM is consistent with providing approximately one cycle per day" |
| RTE [V] | 85% | % | – | p19 / 12 | "The round-trip efficiency is chosen to be 85%" |
| Lifetime [V] | 15 (conservative) | years | – | p19 / 12 | "The lifetime we selected is 15 years" |
| Cycle life | not given | | | | |
| Construction time | not given (see ATB) | | | | |

---

## Source B2: NREL/NLR Annual Technology Baseline (ATB) 2025, Electricity

- **Citation:** NLR (National Laboratory of the Rockies) (2026). *2025 Electricity Annual Technology Baseline*. Golden, CO. http://atb.nlr.gov/. The workbook gives this citation.
- **Web pages:**
  - https://atb.nlr.gov/electricity/2025/utility-scale_battery_storage
  - https://atb.nlr.gov/electricity/2025/pumped_storage_hydropower
  - Data page: https://atb.nlr.gov/electricity/2025/data
- **Workbook URL:** https://data.openei.org/files/8759/2025_v1_Workbook_08-27-2026.xlsx (OEDI submission 8759).
- **Accessed:** 2026-10-30. https://atb.nlr.gov/electricity/2026/utility-scale_battery_storage returned 404, so ATB 2025 is the latest edition.
- **Saved as:** `nrel_atb2025_workbook_v1.xlsx`, about 8.5 MB.
- **Cost year:** 2023 USD. The Preface sheet, row 15, says "The base year and dollar year are updated to 2023." The battery sheet (row 10) and PSH sheet (row 12) both say "All values are given in 2023 U.S. dollars".
- **Technologies covered:** the ATB has **no CAES and no VRFB** technology pages.

### Li-ion (ATB 2025, sheet "Utility-Scale Battery - R&D")

The reference system is "60 MW, 240 MWh storage (4 hours)" (row 12). Durations are 2, 4, 6, 8 and 10 h; there is no 16 h case. Scenarios are Advanced, Moderate and Conservative.

| parameter | value | unit | cost year | ref (sheet, row / col) | label |
|---|---|---|---|---|---|
| Energy cost component, 2024 / 2030 Moderate [V] | 234.01 / 186.05 (2023: 304.21) | $/kWh | 2023 USD | row 20, cols G / M (F = 2023) | "Battery Energy Capital Cost ($/kWh)" |
| Power cost component, 2024 / 2030 Moderate [V] | 361.34 / 340.02 (2023: 469.74) | $/kW | 2023 USD | row 26 | "Battery Power Capital Cost ($/kW)" |
| Overnight capital cost (OCC), 8 h: 2023 / 2024 / 2030 Moderate [V] | 2,903.4 / 2,233.4 / 1,828.4 | $/kW | 2023 USD | row 114, cols H / I / O | "Overnight Capital Cost ($/kW)" |
| OCC 8 h per kWh [D] | 362.9 / 279.2 / 228.6 | $/kWh | 2023 USD | ÷8 | derived |
| OCC 8 h, 2030 Advanced / Conservative [V] | 1,300.3 / 2,188.4 | $/kW | 2023 USD | rows 113 / 115, col O | same |
| OCC 10 h: 2024 / 2030 Moderate [V] | 2,701.4 / 2,200.5 (≈270 / 220 $/kWh [D]) | $/kW | 2023 USD | row 117 | same |
| CAPEX (OCC + construction financing + grid connection), 8 h, 2030 Moderate [V] | 1,998.0 (≈250 $/kWh [D]) | $/kW | 2023 USD | row 80, col O | "CAPEX ($/kW)" |
| Grid connection cost (GCC) [V] | 104.12, flat for all durations and years | $/kW | 2023 USD | rows 155–169 | "Grid Connection Costs (GCC) ($/kW)" |
| CAPEX check [D] | 2,233.42 + 79.215 + 104.12 = 2,416.755 = CAPEX 8 h 2024 (row 79/80, col I), so GCC is **added on top of** OCC | – | – | rows 97, 114, 165 | arithmetic |
| Fixed O&M, 8 h: 2024 / 2030 Moderate [V] | 89.34 / 73.14. This is 4% of OCC and includes augmentation | $/kW-yr | 2023 USD | row 131 | "Fixed Operation and Maintenance Expenses ($/kW-yr)" |
| Variable O&M [V] | 0 | $/MWh | – | rows 138–152 | "Variable Operation and Maintenance Expenses ($/MWh)" |
| RTE [V] | 0.85 | – | – | rows 172–186 | "Round-Trip Efficiency" |
| Technical life [V] | 15 | years | – | row 68 | "For 15-year technical life (values in 2023$)" |
| Construction duration [V] | 1 | year | – | row 41 | "Construction Duration yrs" |
| Expanded Cost Drivers case, 8 h 2030 Conservative [V] | 2,382.3 OCC (vs 2,188.4 in the R&D case) | $/kW | 2023 USD | sheet "Utility-Scale Battery - Expand", row 115, col O | pilot case including supply-chain effects |
| Fixed O&M includes augmentation (web) [V] | yes | – | – | battery web page | "The FOM costs include battery augmentation costs" |

Flag: the 2023 base-year cost (4 h: 1,686.6 $/kW ≈ 422 $/kWh) is much higher than 2024 (1,297.4 $/kW ≈ 324 $/kWh). The 2024 value matches Cole et al.'s $334 (2024$) after deflating. Projections for 2030 start from the 2024 value.

### PSH (ATB 2025, sheet "Pumped Storage Hydropower")

All resource classes are defined at **10 h** duration (row 17). Costs depend on location and are split into 15 national cost classes.

| parameter | value | unit | cost year | ref (row / col) | label |
|---|---|---|---|---|---|
| OCC, Class 1 (cheapest) [V] | 2,584.48 (2023 = 2030 Moderate); 2030 Advanced 2,478.99 | $/kW | 2023 USD | rows 180–181, cols N / U | "Overnight Capital Cost ($/kW)" |
| OCC, Class 8 [V] | 3,706.4; 2030 Advanced 3,555.1 | $/kW | 2023 USD | rows 201–202 | same |
| OCC, Class 15 [V] | 4,714.88; 2030 Advanced 4,522.4 | $/kW | 2023 USD | rows 222–223 | same |
| OCC per kWh at 10 h [D] | Class 1 ≈ 258; Class 8 ≈ 371; Class 15 ≈ 471 | $/kWh | 2023 USD | ÷10 | derived |
| CAPEX incl. construction financing, Class 1 / 8 / 15 [V] | 2,737.3 / 3,925.6 / 4,993.7 | $/kW | 2023 USD | rows 86 / 107 / 128 | "CAPEX ($/kW)" |
| Grid connection (separate line) [V] | 0. The web page says GCC is added by distance, so it is presumably already inside OCC (ambiguous) | $/kW | – | rows 369–413 | "Grid Connection Costs (GCC) ($/kW)" |
| Fixed O&M [V] | 20.98 for all classes and years | $/kW-yr | 2023 USD | rows 227–271 | "Fixed Operation and Maintenance Expenses ($/kW-yr)" |
| Variable O&M [V] | 0.61 | $/MWh | 2023 USD | rows 274–318 | "Variable Operation and Maintenance Expenses ($/MWh)" |
| O&M basis [V] | based on a 1,000 MW plant (from Mongird et al. 2020, PNNL) | – | – | row 16 | "OM Costs are based on nominal plant size of 1000 MW" |
| RTE [V] | 0.80 (web: central value from a 70–87% range) | – | – | rows 321–365 | "Round-Trip Efficiency" |
| Capital recovery period [V] | 30 | years | – | row 38 | "Capital Recovery Period (Years)" |
| Construction duration [V] | 3 yr, with capital spent 80% / 10% / 10% | years | – | rows 41–46 | "Construction Duration yrs" |
| Technical life | not given in the workbook | | | | |
| 2030 projection [V] | Moderate and Conservative: no change. Advanced: −12% by 2050 (0.6%/yr to 2035) | – | – | web page | "no change from baseline CAPEX and O&M costs through 2050" |
| Cost model source [V] | NLR bottom-up PSH model (Cohen, Ramasamy & Inman 2023, revised 2024) | – | – | row 15 | "estimated using the NLR bottom-up PSH cost model" |

Flag: the PSH web-page table header says "2021USD/kilowatt", but the workbook says all values are 2023 USD. The class averages are the same in both ($2,584 and $4,715). The workbook statement is probably authoritative and the web header probably stale.

---

## Cross-source flags and ambiguities

1. **$/kWh is always per kWh of rated energy capacity** at the stated duration, i.e. total cost ÷ (MW × h).
   - PNNL p9 / viii, fn 3: "total installed cost divided by rated energy gives $/kWh".
   - NREL p10 / 3 defines the 4 h duration as output duration.
   - $/kWh figures therefore cannot be compared across durations. Use the $/kW figures or the energy/power split.
2. **Grid connection is treated differently in each source.**
   - PNNL includes a $/kW "grid integration" line (transformer, metering, breakers). Network reinforcement is not mentioned.
   - NREL Cole includes EBOS substation and transmission line but excludes interconnection upgrades.
   - ATB adds a flat $104/kW GCC for batteries. For PSH the GCC line is 0, and grid connection is presumably inside OCC.
3. **Cost years differ:** PNNL 2022 is about 2021 USD (not stated), PNNL v2024 about 2023 USD (not stated), Cole 2025 is 2024 USD, ATB 2025 is 2023 USD. None is GBP; currency and inflation conversion is still to do.
4. **~16 h Li-ion:** no source gives 16 h.
   - PNNL gives 24 h, about 338 $/kWh (100 MW, 2023).
   - ATB and Cole stop at 10 h. The Cole 16 h figure above is an extrapolation.
5. **Li-ion degradation is handled differently.**
   - PNNL prices explicit augmentation in LCOS but not in capex or fixed O&M (FOM about 8–21 $/kW-yr).
   - NREL and ATB fold augmentation into FOM at 4% of capex (about 89 $/kW-yr for 8 h in 2024). The fixed O&M figures are therefore not comparable.
6. **CAES:** PNNL covers only diabatic CAES (52% RTE in 2022; point 55% in v2024). No adiabatic CAES numbers exist in A or B, so this is a gap. Gas fuel cost for diabatic CAES is not in the cost tables.
7. **VRFB:** neither ATB nor Cole covers it. PNNL v2024 changed cycle life from "Unlimited" (2022) to 5,250 cycles, and raised costs.
8. **2030 projections:** PNNL holds PSH and CAES flat (no learning); Li-ion and VRFB use learning rates. ATB holds PSH flat (Moderate). Cole gives yearly values for 2029–2033 (4 h).
9. **Construction or lead time** comes only from modelling assumptions:
   - PNNL: battery 1 yr, CAES 3 yr, PSH 5 yr ("moderately optimistic").
   - ATB: battery 1 yr, PSH 3 yr.
   - No empirical lead-time data.

## Files in this folder from this task

| file | description |
|---|---|
| `pnnl2022_cost_performance.pdf` / `.txt` | PNNL 2022 report |
| `pnnl_esgc_database_v2024.xlsx` | PNNL database. Note: `.xlsx` is **not** covered by the `.pdf`·`.txt` rule; `.xlsx` is now git-ignored too (2026-10-30) |
| `nrel2025_cole_battery_cost_projections.pdf` / `.txt` | NREL Cole et al. 2025 |
| `nrel_atb2025_workbook_v1.xlsx` | ATB 2025 workbook, about 8.5 MB. Git-ignored (2026-10-30) |
