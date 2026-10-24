# GB pumped storage (PSH): public revenue sources and top-down checks, 2016-2026

Compiled 2026-10-24 for validating the dispatch model against Dinorwig (DINO-1..6), Ffestiniog (FFES-1..4), Cruachan (CRUA-1..4) and Foyers (FOYE-1..2).

How to read this file:
- **[V]** means I opened the primary file or page and read the number myself.
- **[S]** means the figure comes from a secondary source (press, Wikipedia, or a search summary). Treat it as unverified.
- **[C]** means I calculated it from public data. The method is given.
- All money is nominal £. "FY" means the operator's own financial year.
- Small PDFs (Companies House accounts, Drax results, the 2005 First Hydro presentation) are saved next to this file. They are git-ignored.
- I did not copy any xlsx or csv into the repo. Every one can be downloaded again from the URLs given.

Ownership. First Hydro Company (FHC, Companies House **02444277**) owns Dinorwig and Ffestiniog. It is a 75/25 joint venture. ENGIE holds 75%. The other 25% belonged to Brookfield until CDPQ (La Caisse) agreed to buy it on 24 Sep 2024 [S: https://www.lacaisse.com/en/node/11836 ; https://www.renewableenergyworld.com/hydro-power/cdpq-acquiring-25-of-first-hydro-company-in-uk-from-brookfield/]. The FHC 2024 accounts still mention "ENGIE or Brookfield group companies" [V, FHC accounts 2024, p.30]. Cruachan belongs to Drax Pumped Storage Ltd. Drax bought it from Iberdrola/ScottishPower on 31 Dec 2018 [V: https://www.drax.com/about-us/our-sites-and-businesses/cruachan-power-station/]. Foyers belongs to SSE Generation Ltd (SSE Renewables).

---

## 1. Mandatory Frequency Response (MFR)

### 1.1 What NESO publishes

Landing page: https://www.neso.energy/industry-information/balancing-services/frequency-response-services/mandatory-frequency-response-mfr (read 2026-10-24) [V]

| File | URL | Format | Period | Unit-level? | Content |
|---|---|---|---|---|---|
| MFR prices ("Latest MFR and CFR Prices") | https://www.neso.energy/document/276961/download (file `10_mandatory-frequency-response-prices_oct2026.xlsx`) | xlsx, one sheet per year | **Jan 2007 – Oct 2026**, monthly | **Yes**, by genset: `DINO-1..6`, `FFES-1..4`, `CRUA-1..4`, `FOYE-1..2` | Submitted holding prices in £/MW/h for Primary, Secondary and High each month [V] |
| MFR capabilities | https://www.neso.energy/document/276966/download (`10_mandatory-frequency-response-capabilities_oct2026.xlsx`, 3 MB) | xlsx, one sheet per month | **Jan 2011 – Oct 2026** | Yes, same unit names | Response capability (MW) at 0.2/0.5/0.8 Hz by deload level, for P/S/H, per BMU [V] |
| Frequency response volumes "D9" / "D3" (monthly holding volumes) | 2016-17: https://www.neso.energy/document/54461/download ; 2017-18: /document/96841/download ; 2018-19: /document/180781/download ; 2019-20: /document/114691/download ; 2020-21: /document/169101/download ; 2021-22: /document/191911/download ; 2022-23 (labelled D3, but covers the full year Apr 22–Mar 23): /document/249816/download ; 2023-24: /document/280206/download ; 2024-25: /document/318481/download ; 2025-26: /document/360561/download ; 2026-27 (to Sep 26): /document/381851/download. All are under `https://www.neso.energy`. The page link "2022-23 Volumes D9" (/document/250351) actually holds Apr–Nov 2023 data. | xls/xlsx, one sheet per month | Apr 2015 onward (the 2015-16 file is /document/54471/download) | **Yes**: daily rows of BM_UNIT × {Primary, Secondary, High} MWh | "BM Unit Mandatory Response Holding Volumes", in MW·h held per day [V] |
| Older index (data finder) | https://www.neso.energy/industry-information/industry-data-and-reports/data-finder-and-explorer?page=0 (pages 0–2) | — | — | — | Lists the D3/D9 files and the annual "FFR Market Report" xls files [V] |
| MFR FAQ (updated 16 Jan 2025) | https://www.neso.energy/document/352396/download | docx | — | — | Explains the payment structure (below) [V] |
| 2013–2015 "FFR Market Information" monthly reports (these included mandatory-market holding and bid/offer costs) | e.g. https://www.nationalgrid.com/sites/default/files/documents/FFR%20Market%20Information%20Feb%2015.pdf | pdf | 2013–2015 | Not checked | Old nationalgrid.com links now return 404 [S] |

MFR has **no monthly tender**. Each generator submits its own holding prices through FRPS between the 5th and 15th working day of each month. NESO then dispatches units in merit order. Those prices are what the "Prices" file publishes [V, FAQ].

### 1.2 How MFR is paid

- **Holding payment (£/h)**: paid for capability while the unit is instructed into frequency-sensitive mode (reason codes MF/MP). It equals the held MW × the submitted £/MW/h price, separately for P, S and H [V, FAQ; prices file units "£/MW/h"].
- **Response energy payment (REP, £/MWh)**: paid on the energy actually delivered. It is set in CUSC 4.1.3 off the Market Index Price (MIP). The generator receives MIP×1.25 for extra output and pays MIP×0.75 for reduced output. This is the CAP107 design [S: NESO presentations found via search, e.g. https://neso.energy/document/16316/download ; Ofgem CMP237 decision https://www.ofgem.gov.uk/sites/default/files/docs/2016/11/cusc_response_energy_payment_for_low_fuel_cost_generation.pdf]. I have not checked the current CUSC 4.1.3.9A wording.
- Modes B–E are "Commercial Frequency Response" (CFR) under bilateral terms. Their prices are in the same file. DC/DM/DR are not FSM [V, FAQ].

### 1.3 What the data shows for PSH [C]

I summed the D9 holding volumes (P+S+H, MW·h) for each station and financial year.

| FY | CRUA | DINO | FFES | FOYE | All BMUs (P / S / H, MW·h) |
|---|---|---|---|---|---|
| 2016-17 | 410 | 0 | 0 | 0 | 2.55M / 1.62M / 3.97M |
| 2017-18 | 453 | 0 | 0 | 0 | 2.15M / 1.28M / 3.32M |
| 2018-19 | 220 | 0 | 0 | 119 | 1.73M / 1.01M / 3.41M |
| 2019-20 | 1,421 | 0 | 0 | 133 | 3.09M / 1.97M / 4.26M |
| 2020-21 | 23 | 0 | 0 | 22 | 2.08M / 1.33M / 2.86M |
| 2021-22 | 38 | 0 | 0 | 15 | 3.34M / 2.11M / 4.92M |
| 2022-23 | 173 | 0 | 0 | 0 | 2.44M / 1.43M / 3.95M |
| 2023-24 | 0 | 0 | 0 | 11 | 1.40M / 0.78M / 2.28M |
| 2024-25 | 0 | 0 | 0 | 38 | 0.97M / 0.57M / 1.71M |
| 2025-26 | none listed | | | | |

I then priced those volumes at the unit's submitted price for each month. The implied MFR **holding revenue** is below £3k/yr for Cruachan, except **2019 (~£42k)**, when CRUA was priced at £30/MW/h. Foyers is below £0.5k/yr, and Dinorwig and Ffestiniog are £0.

Dinorwig and Ffestiniog submit low prices (£5.1 / £3.1 / £9.3 per MW/h for P/S/H) but hold zero MFR volume. Their frequency response was bought commercially instead, through FFR tenders and bilateral/CFR deals. **Conclusion: MFR is negligible for PSH. Model it as zero, or as the measured volume × price.**

The capability file (Oct 2026) shows, for example, DINO-1 at 14/39/56 MW of primary at 0.2/0.5/0.8 Hz with a deload of 138 MW, and CRUA-1 at 10/25/37 MW [V].

---

## 2. Fast Reserve (FR)

| Source | URL | Period | Unit-level? | Notes |
|---|---|---|---|---|
| Firm FR "Post Assessment Tender Report" (monthly, pdf) | https://www.neso.energy/document/98796/download (Nov-2017); /document/106111 (Jan-18); /document/108301 (Feb-18); /document/117556 (Jun-18); /document/128321 (Oct-18); /document/132511 (Nov-18); also /document/110141, /112811, /115201, /139336 (2018–Mar 2019, per search, not opened) | ~2016 – Mar 2019 on neso.energy | **Yes**: company + BM unit (`FFES-2/3/4`, `DINO-2`, `CRUA-4`), availability fee £/h, positional fee £/h, energy fee or capped BO £/MWh, MW, window, accepted/rejected | Also lists every live accepted contract, so one report shows the whole contracted book [V for 98796, 132511] |
| FR Market Information Report (monthly, pdf) | https://www.neso.energy/document/106301/download (Mar-18); /document/117936/download (Aug-18) | 2011 – Jun 2021 | Names the provider and unit for accepted tenders in the text | Example: "we contracted 90 MW from First Hydro's FFES-4 unit for twelve months from November-18" [V, 117936] |
| Data-portal datasets "Firm Fast Reserve Post Tender Reports" (Dec-18 → Dec-19, xlsx/pdf) and "Fast Reserve Market Information Reports" (Feb-19 → Jun-21) | Mirror index: https://opennetzero.org/dataset/fast-reserve-tender-reports ; https://opennetzero.org/national-grid-eso/fast-reserve-market-information-reports | 2018-12 → 2021-06 | Yes | The original `api.nationalgrideso.com` host no longer resolves. On `api.neso.energy` the packages (`a2ef92b7-…`, `736f16fb-…`) return "Authorization Error", so they are archived or private. The Wayback Machine returned 429 when I tried [V] |
| Non-BM ASDP instructions | https://api.neso.energy/api/3/action/package_show?id=non-bm-ancillary-service-dispatch-platform-asdp-instructions | Jun 2020 → | Non-BM units only | Does not cover PSH, which are BM units |

Examples of firm FR contracts held by PSH [V, report 132511 "Previously accepted tenders"; 98796]:

| Unit | Term | Availability £/h | Positional £/h | Energy fee / BO cap £/MWh | MW | Window |
|---|---|---|---|---|---|---|
| FFES-4 | 01/11/2017–31/10/2018 | 320 | 320 | 115 | 90 | Mon–Sat 06:00–23:00, Sun 07:00–23:00 |
| FFES-2 | 01/04/2018–31/10/2018 | 175 | 175 | 100 | 90 | same |
| FFES-3 | 01/11/2018–31/10/2019 (excl. Mar-19) | 504 | 0 | 106 | 90 | same |
| FFES-4 | 01/11/2018–31/10/2019 | 250 | 250 | 100 | 90 | same |
| CRUA-4 (ScottishPower) | 01/11/2017–31/03/2018 | 370 | 370 | — | — | from 98796 |
| CRUA-4 (ScottishPower) | 01/11/2018–31/03/2019 | 195 | 194 | 100 | 100 | 06:00/07:00–23:30 |

Rough scale [C]: £250–500/h × ~17 h/day × 365 days ≈ **£1.5–3m per contract per year**. That puts FHC's firm FR at roughly £3–5m/yr in 2018-19.

Firm FR and firm STOR procurement was **suspended in January 2020** "due to the existing method for firm procurement no longer being compliant with the EU's Clean Energy Package" [V, FHC accounts 2020, Strategic report p.1]. After that, FR was bought only as **Optional FR**, which had no tender data. NESO says it stopped the MIR after June 2021 [S, opennetzero mirror text]. **No per-unit Optional FR payments are public.** Quick Reserve replaced FR in Dec 2024 (per the user brief, not re-checked).

---

## 3. Other services

| Service | Do PSH earn from it? | Is per-unit data public? | Where |
|---|---|---|---|
| **Obligatory Reactive Power (ORPS)** | Yes, every unit | **Yes, monthly MVArh per BMU** (lead, lag, total). Revenue = MVArh × the published monthly Default Payment Rate (£/MVArh, "X = 1" column) | Dataset: https://api.neso.energy/api/3/action/package_show?id=obligatory-reactive-power-service-orps-utilisation . Files: historic Oct-2013→Mar-2020 (wide csv) `.../resource/3ee65326-3729-421d-b667-b2164501e4a5/download/reactive-historical-data-apr-2013-to-mar-2020.csv`; Apr-2020→Aug-2026 (long csv) `.../resource/528b03d2-4008-4b65-a732-a001cd835a3b/download/reactive-utilisation-data.csv`; rates 2008→Nov-2026 `.../resource/b00df5b1-4179-44e3-b556-28a836ad619f/download/reactive-default-payment-rate-nov-2026.csv` (base `https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b`). Unit IDs: `DINO_01Z..06Z`, `FFES_01Z..04Z` (company NGPS), `CRUA_01Z..04Z` (DPSL; EPGL before 2019), `FOYE_01Z..02Z` (SSEG) [V]. Rate formula: CUSC Sch.3 App.1, BP = 46,270,000·Im·X / 42,054,693 [V, rate pdf p.1–2] |
| Voltage contracted units (market reactive) | No PSH rows found in the 2026 file | Monthly per BMU | https://api.neso.energy/api/3/action/package_show?id=monthly-utilisation-data-of-voltage-contracted-units [V] |
| **Stability Pathfinder (inertia / SCL)** | **CRUA-3**, under a Phase 1 contract from ~2020 to 31 Mar 2026, as a synchronous compensator | Half-hourly availability flags only, no £ | https://api.neso.energy/api/3/action/package_show?id=stability-pathfinder-service-information . CRUA-3 appears FY23-24 to FY25-26 [V]. Value: "worth up to £5 million per year … over a six-year period", contract started July 2020 [V, Drax FY2020 results p.7]. Phase 1 total was £328m, 12 tenders [S: https://neso.energy/future-energy/projects/pathfinders/stability] |
| **STOR** | Firm STOR (seasonal tenders) until it was suspended in Jan 2020 [V, FHC 2020 accounts]. In day-ahead STOR (from Apr 2021), PSH barely appear: CRUA-3 accepted 7 days (May–Jul 2023), FFES-3 accepted 4 days (May–Jul 2022), other bids rejected [V, SQL on the dataset] | DA auction results are per unit, with £/MW/h clearing price | https://api.neso.energy/api/3/action/package_show?id=short-term-operating-reserve-stor-day-ahead-auction-results (Apr 2021 → Mar 2026). Pre-2020 seasonal STOR tender reports exist but I did not check them |
| **EAC (DC/DM/DR/BR/QR/SR)** | **None**: no DINO/FFES/CRUA/FOYE rows in EAC results-by-unit FY2024 (79 MB archive, streamed and grepped) or FY2026 to date. Also none in the BR 2023-24 file in `data/raw/neso/eac-br-auction-results/` [V] | — | https://api.neso.energy/api/3/action/package_show?id=eac-auction-results . Note that the repo's `data/raw/eac_units/` files are filtered to batteries |
| **FFR (dynamic/static)** | Yes. FHC says the "expiration of the Firm Frequency Response contracts" cut 2020 generation [V, FHC 2020 accounts p.1] | Monthly post-tender reports per unit | The user already holds these (`firm-frequency-response-post-tender-reports`) |
| **Black Start** | All four plants are believed to hold contracts. Dinorwig has two 2 MW diesel black-start sets [V, IPR 2005 slide 7]. Cruachan keeps a 12-hour water reserve [S, Wikipedia] | **No.** Only GB totals are published: 2017/18 £57.7m, 2018/19 ~£49.0m, 2019/20 £54.9m, 2020/21 £66.2m (availability payments £43.4m) [S, from NESO Black Start annual reports and Ofgem decisions, e.g. https://www.ofgem.gov.uk/decision/authority-determination-not-adjust-black-start-costs-incurred-201920] | Contract values are confidential |
| **Optional Spinning Reserve / "spin-gen"** | Plausible: Dinorwig runs in spin-gen and spin-pump modes (12 s and 30 s to load) | **Nothing per unit found** [unverified] | Not found as a separate published dataset |
| Contract enactment (SO trades, constraint contracts) | No PSH rows in FY21-22 → FY26-27 | Per asset and per trade | https://api.neso.energy/api/3/action/package_show?id=balancing-services-contract-enactment [V]. Drax mentions "specific constraint contracts" in 2019 at group level [V, FY2020 results p.7] |
| Constraint Management Intertrip (CMIS) | Not checked | Per unit arming | https://api.neso.energy/api/3/action/package_show?id=constraint-management-intertrip-service-information-cmis |
| BM (BOA, constraints) | Yes, the main source | Yes, Elexon (already held) | — |

### 3.1 ORPS revenue estimate [C]

Method: monthly total MVArh (lead + lag) × that month's Default Payment Rate (X = 1), summed by calendar year. 2026 runs Jan–Aug only.

| Year | DINO MVArh | DINO £ | FFES £ | CRUA £ | FOYE £ |
|---|---|---|---|---|---|
| 2016 | 881,595 | 2,315,810 | 350,497 | 287,656 | 226,775 |
| 2017 | 1,119,546 | 3,282,856 | 364,942 | 269,432 | 160,641 |
| 2018 | 1,045,422 | 3,507,734 | 384,495 | 242,919 | 153,826 |
| 2019 | 866,733 | 2,794,203 | 232,155 | 227,655 | 125,547 |
| 2020 | 689,562 | 1,806,293 | 196,403 | 364,713 | 87,316 |
| 2021 | 699,515 | 3,608,744 | 384,498 | 966,332 | 206,556 |
| 2022 | 551,697 | 6,601,262 | 777,952 | 2,796,179 | 482,613 |
| 2023 | 402,972 | 3,034,949 | 627,966 | 1,726,668 | 440,552 |
| 2024 | 529,225 | 2,360,248 | 222,740 | 1,132,653 | 257,123 |
| 2025 | 265,587 | 1,340,023 | 179,243 | 747,977 | 205,067 |
| 2026 (Jan–Aug) | 252,057 | 1,313,555 | 172,991 | 283,168 | 123,767 |

The rate follows power prices. It peaked at £13.86/MVArh in Jan 2023 and was £2.33 in Apr 2016 and £8.12 in Nov 2026. So **ORPS is worth roughly £2–7m/yr to FHC and £0.2–2.8m/yr to Cruachan**. That is small but not negligible next to FHC turnover.

---

## 4. Top-down revenue checks

### 4.1 First Hydro Company (Dinorwig + Ffestiniog)

**Companies House:** First Hydro Company, no. **02444277** (Dinorwig Power Station, Llanberis). Filing history: https://find-and-update.company-information.service.gov.uk/company/02444277/filing-history . The accounts are scanned image PDFs with no text layer; I read them visually. Calendar-year accounts.

Related companies: First Hydro Finance PLC (03085928), First Hydro Holdings Company, and FHH No1 Ltd [V, FHC 2024 note 6].

Accounting caveat [V, accounting policy "Turnover", e.g. 2024 p.28 and 2022 p.27]:
- Turnover "represents the amounts derived … from the supply of electricity, net of exchange fees, ancillary services and participation in the UK Capacity Market".
- Bilateral trades are **netted half-hourly**: "half hourly netting is performed to disclose all transactions for the relevant period as either revenue or cost of sales".
- So turnover is **not** gross wholesale sales. Pumping energy sits mainly in cost of sales, but within-half-hour flows are netted.
- **"Gross profit" (or turnover − cost of sales) is the closest public match to a model's net revenue** (arbitrage + BM + ancillary + CM − pumping cost). The large "fair value movement on unrealised energy trading commodities" is a mark-to-market timing item and should be removed.
- Under IFRS 15, "Electricity generation recognised under IFRS 15" is probably the contracts-with-customers part (BM/ancillary/CM, with ESO and Elexon as counterparties). The IFRS 9 part is bilateral or traded power. This mapping is my **interpretation and is unverified**. The accounts give no explicit market split.

All figures in £'000. The source for each year's numbers is the accounts that report it (current year or prior-year comparative).

| Year | Turnover | of which IFRS 9 | of which IFRS 15 | Cost of sales | FV mvt unrealised | Gross profit | Turnover − CoS | Operating profit | Depreciation | ≈ EBITDA (OP + dep.) | Profit for year | Generation | Technical availability | Source (accounts year, page) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2015 | 269,634 (restated) | – | – | 115,526 | 1,870 | 155,978 | 154,108 | 96,174 | 6,485 | 102,659 | 83,103 | 2.2 TWh | 91.0% | 2016 a/c p.1, p.9, p.18 |
| 2016 | 269,730 | – | – | 115,435 | 2,944 | 157,239 | 154,295 | 101,846 | 6,620 | 108,466 | 88,277 | 2.5 TWh | 99.5% | 2016 a/c p.1, p.9, p.18 |
| 2017 | 270,881 | 113,080 | 157,388 | 119,604 | (503) | 150,774 | 151,277 | 95,518 | 6,621 | 102,139 | 81,658 | 2.3 TWh | 92.62% | 2018 a/c p.1, p.9, p.21 |
| 2018 | 266,482 | 110,771 | 155,415 | 134,271 | (5,223) | 126,988 | 132,211 | 72,107 | 6,617 | 78,724 | 64,404 | 2.1 TWh | 88.2% | 2018 a/c p.1, p.9, p.21 |
| 2019 | 253,428 | 75,892 | 177,328 | 82,197 | 2,180 | 173,411 | 171,231 | 118,828 | 6,808 | 125,636 | 102,384 | 1.3 TWh | 83.73% | 2020 a/c p.1, p.15, p.29–30 |
| 2020 | 221,549 | 62,332 | 159,149 | 54,207 | (3,757) | 163,585 | 167,342 | 106,921 | 6,754 (+1,181 impairment) | 113,675 (excl. impairment) | 89,969 | 1.1 TWh | 74.31% | 2020 a/c p.1, p.15, p.29–30 |
| 2021 | 357,219 (+20,000 insurance as other income) | 163,423 | 193,699 | 119,841 | (80,663) | 156,715 | 237,378 | 109,888 (incl. £20m insurance) | 7,016 | 116,904 | 89,571 | 1.4 TWh | 64.91% | 2022 a/c p.1, p.14, p.28 |
| 2022 | 518,637 | 285,116 | 233,376 | 233,507 | 58,828 | 343,958 | 285,130 | 270,875 | 9,463 | 280,338 | 222,449 | 1.4 TWh | 62.31% | 2022 a/c p.1, p.14, p.28 |
| 2023 | 449,278 | 299,038 | 150,047 | 163,276 | 51,359 | 337,361 | 286,002 | 254,998 | 9,626 | 264,624 | 200,692 | 1.0 TWh | 47.56% | 2024 a/c p.1, p.15, p.29 |
| 2024 | 321,644 | 134,406 | 187,103 | 88,488 | (23,819) | 209,337 | 233,156 | 129,372 | 10,924 (+785 disposal loss) | 140,296 | 104,141 | 1.3 TWh | 51.93% | 2024 a/c p.1, p.15, p.29 |
| 2025 | 209,742 | 72,084 | 137,283 | 55,661 | (3,211) | 150,870 | 154,081 | 70,577 | 11,467 (+387) | 82,044 | 60,744 | 0.8 TWh | 31.53% | 2025 a/c p.1, p.15, p.29 |

Page numbers are the printed numbers in the accounts. The PDF page is printed page + 1.

PDF links:
- 2025: https://find-and-update.company-information.service.gov.uk/company/02444277/filing-history/MzU0OTA0MzQ3OGFkaXF6a2N4/document?format=pdf&download=0
- 2024: …/MzQ3NzYwNDA3NWFkaXF6a2N4/…
- 2023: …/MzQyODMwNzQ3M2FkaXF6a2N4/…
- 2022: …/MzM5NTAzMzk3M2FkaXF6a2N4/…
- 2021: …/MzMzODc5MzIxM2FkaXF6a2N4/…
- 2020: …/MzMwMDkxNDQyM2FkaXF6a2N4/…
- 2019: …/MzI2MDAzMzA3NGFkaXF6a2N4/…
- 2018: …/MzIyOTU0NDk0NmFkaXF6a2N4/…
- 2017: …/MzIwMTYyOTQxN2FkaXF6a2N4/…
- 2016: …/MzE3MTA3NTU1MGFkaXF6a2N4/…
- 2015: …/MzE0MzA0NzYzOGFkaXF6a2N4/…

Local copies: `FHC_accounts_YYYY.pdf`. I read the 2016, 2018, 2020, 2022, 2024 and 2025 accounts; odd years come from the comparatives.

Qualitative revenue-mix statements [V, Strategic report p.1 of each set of accounts]:
- **2016**: "strong wholesale prices" in Q3–Q4, "price volatility and overnight pump shaping value in the prompt markets", "continued strong performance … around the provision of reliable, fast response products". In the CM, all Dinorwig units and two Ffestiniog units won 1-year contracts at £22.50/kW for DY2020/21. The other two Ffestiniog units won **15-year refurbishment contracts (Oct 2020 – Sep 2035)**.
- **2018**: the CM suspension meant "£5.3m of accrued revenue has not been recognised". The 2020 accounts (note 3, p.30) say instead that "£11m of revenue for the final quarter of 2018" was recognised in 2019. So 2019 turnover is inflated by about £11m of 2018 CM money. The T-4 for DY2021/22 cleared at £8.40/kW.
- **2020**: "Balancing service products were a key contributor to overall gross margin in 2020 despite the absence of firm contracts. The procurement of firm STOR and firm Fast Reserve tendered services was suspended in January 2020 …" Lower generation was blamed on "the expiration of the Firm Frequency Response contracts". Ffestiniog units 1 and 2 were in refurbishment outage. DINO-1 failed in Sep 2020 and was unavailable until ~autumn 2023.
- **2022**: "Balancing service products and energy arbitrage were both key contributors"; "The Company's optional ancillary service products provided strong support". In the CM, the T-4 for DY2025/26 cleared at £30.59/kW (all six Dinorwig units won contracts, and Ffestiniog units 3 and 4 won 15-year refurbishment contracts). FFES-4 won a T-1 contract at £75/kW for DY2022/23.
- **2024**: "Energy arbitrage was a key contributor … decline relative to 2023 … (Q1 2023 was a particularly high value period)". The T-4 for DY2027/28 cleared at £65/kW, with four Dinorwig units contracted and two opting out.
- **2025**: Dinorwig had a station outage of several months over the summer to fit the main inlet valves. The T-4 for DY2028/29 cleared at £60/kW (four Dinorwig units).

### 4.2 Drax: "Pumped storage and hydro" (Cruachan + Lanark and Galloway run-of-river hydro, plus Daldowie until 2022)

Cruachan is **not** reported on its own. The segment also contains roughly 126 MW of run-of-river hydro, which earns ROCs and power sales. Drax says the segment's historical EBITDA was "in the region of £70 million" [V, FY2023 results p.9].

| Year | Adj. EBITDA (£m) | Notes | Source |
|---|---|---|---|
| 2019 | 71 | First year after acquisition; includes Daldowie | Drax FY2020 results, p.7 (https://www.drax.com/wp-content/uploads/2021/02/Drax-Full-Year-Results-25-February-2021.pdf) [V] |
| 2020 | 73 | "Cruachan, Lanark Galloway schemes and Daldowie" | same, p.7 [V] |
| 2021 | 68 | — | Drax FY2021 results, p.7 & p.11 (https://www.drax.com/wp-content/uploads/2022/02/Drax-2021-FYR-Announcement.pdf) [V] |
| 2022 | 171 | "strong system support … and generation" | Drax FY2022 results, p.7 (https://www.drax.com/wp-content/uploads/2023/02/Drax-2022-FYR-Announcement.pdf) [V] |
| 2023 | 230 (incl. EGL); **253 excl. EGL** | EGL applies to run-of-river hydro but **not to pumped storage**. "Primary driver … high level of activity at Cruachan … balancing mechanism, ancillary services and peak off-peak power generation". 2023 included forward sales of peak power (Q1 2023) | Drax FY2023 results, p.2 & p.9 (https://www.drax.com/wp-content/uploads/2024/02/Drax-Full-Year-Results-29-February-2024.pdf) [V] |
| 2024 | 138 | "Strong system support earnings with lower forward power sales" | Drax FY2024 results, p.3 & p.12 (https://drax.com/wp-content/uploads/2025/02/Drax-Full-Year-Results-27-February-2025.pdf) [V] |
| 2025 | 111 | Major planned outages: main inlet valve upgrade on all four units and the super grid transformer. **CRUA-3/4 unavailable from late Dec 2025** after a SPEN grid-connection failure, with restoration expected in 2027 | Drax FY2025 results RNS, 26 Feb 2026: https://data.fca.org.uk/artefacts/NSM/RNS/0530099a-0b74-4e78-8e8e-61ffc9ce9d9a.html [V via fetch] |
| H1 2023 / H1 2025 / H1 2026 | 154 (excl. EGL) / 64 / 47 | — | H1 2023 RNS (https://www.investegate.co.uk/announcement/rns/drax-group--drx/half-year-report/7657772) [S]; H1 2026 RNS (https://www.drax.com/wp-content/uploads/2026/07/Drax-Half-Year-Results-RNS-30.07.2026.pdf) [S] |

Segment revenue (from 2023 the "Flexible Generation" segment = pumped storage + run-of-river hydro + OCGTs; OCGTs only from 2024/25) [V, FY2024 results note "Revenue", pp.46–48; FY2025 RNS]:

| £m | 2023 (restated) | 2024 | 2025 |
|---|---|---|---|
| Electricity sales (external + inter-segment) | 314.4 | 163.3 | 112.6 |
| Renewable certificate sales | 8.7 | 7.3 | 9.6 |
| **Ancillary services** | **30.4** | **24.2** | **21.2** |
| Other income | 27.6 | 28.0 | 28.1 |
| **Total Flexible Generation revenue** | **381.1** | **222.8** | **171.5** |

Electricity sales are mostly sold inter-segment to Biomass Generation (the trading book), not straight to the market. Drax does not say whether "Other income" includes the Capacity Market [unverified].

Group "Ancillary services" revenue before 2023 (all generation: Drax power station, Cruachan, and CCGTs until Jan 2021):
- 2019: £48.0m
- 2020: £36.4m
- 2021: £50.6m
- 2022: £73.0m

Sources: FY2020 results p.42; FY2021 p.28; FY2022 p.24 [V].

Group "system support (balancing mechanism, ancillary services and optimisation)" gross profit was £118m in 2020 and £120m/£129m in 2019. The FY2020 results give both 2019 figures [V, FY2020 p.7 and p.11]. "Cruachan … contributed significantly" [V].

Capacity Market statements:
- Hydro and pumped-storage CM agreements worth "around £10 million in the delivery period October 2024 to September 2025" [V, FY2021 results p.7].
- The Cruachan units 3–4 upgrade (£80m, +40 MW, 2027) is "underpinned by 15-year Capacity Market agreements (>£220 million)" [V, FY2024 results].

### 4.3 SSE: Foyers

I found no separate figures. SSE reports Foyers inside SSE Renewables (hydro), with no pumped-storage line [S, search of SSE results; not exhaustive]. SSE Renewables says Foyers has an "average annual output 213 million units" (GWh) [V, https://www.sserenewables.com/hydro/foyers/]. For a top-down check on Foyers, use bottom-up public data only: BM cashflows, ORPS, CM register and STOR. **Unverified**: whether SSE Generation Ltd's statutory accounts break out hydro.

---

## 5. Physical parameters

### 5.1 Plant data

Primary source: International Power plc, *First Hydro Analysts Conference*, July 2005, archived at https://web.archive.org/web/20140307091954/http://www.iprplc-gdfsuez.com/~/media/Files/I/IPR-Plc/Attachments/presentations-pdfs/2005/hydrosite05.pdf (saved as `FirstHydro_AnalystsConference_IPR_2005.pdf`). The figures date from 2005; since then Dinorwig has had main inlet valve replacements (2023–25) and Ffestiniog has had refurbishments (units 1–2 in 2019–21, units 3–4 in 2024–).

| | Dinorwig | Ffestiniog | Cruachan | Foyers |
|---|---|---|---|---|
| Units | 6 reversible pump-turbines [V, IPR 2005 slide 7] | 4 (separate pump and turbine on one shaft) [V, slide 16] | 4 [V, Drax site]: 2×100 + 2×120 MW per Wikipedia [S] (units upgraded 2005) | 2 × 150 MW reversible [V, SSE page] |
| Generating capacity | 1,728 MW; "each generating up to 288 MW" [V] | 360 MW; "each generating up to 90 MW" [V] | 440 MW [V, Drax] (+40 MW from 2027) | 300 MW [V, SSE] (305 MW in some sources [S]) |
| Pumping power | "pumping at 275 MW" per unit (≈1,650 MW) [V] | "pumping at 75 MW" per unit (300 MW) [V] | Not on Drax page. Elexon SIL for CRUA-1 is −128 MW and for CRUA-3 −113 MW [V, see 5.2] | Pumping flow ">160 t/s" [V, SSE]. Elexon SIL for FOYE-1 is −155 MW [V] |
| Usable storage | "Total water storage capacity ~9 GWh" [V]. Commonly cited as 9.1 GWh [S, MacKay 2009 p.191] | "~1.4 GWh" [V] (1.44 GWh [S]) | Not stated as energy. "can maintain its maximum power production for more than 16 hours" and "storage capacity of 10 million m³" [V, Drax] → ≥ 440 × 16 ≈ **7.0 GWh** [C]. 7 GWh [S, Wikipedia] | Not published by SSE. **~6.3 GWh [S, Wikipedia list of Scottish power stations; unverified]**. Storage is described as enough for a weekly cycle [S, Lander et al. 1978, Proc. ICE] |
| Round-trip ("cycle") efficiency | **74–75%**; "Import 1 MWh, Export ~0.75 MWh" [V, slides 7 and 26] | **72–73%** [V, slide 16] | **Not published** by Drax [unverified]. Assume ~75% [assumption] | **Not published** [unverified] |
| Head | ~536 m (Marchlyn Mawr 636 m to Llyn Peris ~100 m) [S] | — | 396 m [S, Wikipedia citing ScottishPower site information] | 179 m gross [V, SSE] |
| Start / response | Standstill → full load < 2 min; spinning → full load < 20 s [V, slide 7]. Under 16 s to 1,728 MW from spin [S, ABB] | Standstill → full < 5 min; spinning → full < 60 s [V, slide 16] | "full generating capacity in less than 30 seconds" [V, Drax] | "from a standing start in under two minutes"; "less than 30 seconds" if spun in air [V, SSE] |
| Mode-change times (Dinorwig, "typical") | Spin-gen → Generate **12 s**; Shutdown → Generate **90 s**; Pump → Shutdown **360 s**; Spin-pump → Pump **30 s**. So **pump → generate ≈ 7.5 min** via shutdown [V, IPR 2005 slide 21, read from the figure] | — | Not published | Not published |
| Commissioned | 1983 [V] | 1963 [V] | 1965 [S] | 1974/75 (opened 3 Apr 1975) [S] |

### 5.2 Grid-registered dynamic parameters

Source: Elexon Insights API, dataset "dynamic". Example: `https://data.elexon.co.uk/bmrs/api/v1/balancing/dynamic?bmUnit=T_DINO-1&snapshotAt=2026-10-01T12:00:00Z`. Values are as valid at 2026-10-01 [V]. These parameters change over time, so query the model period from the API.

| BMU | SEL (min stable export, MW) | SIL (stable import, MW) | MZT (min) | MNZT (min) | NDZ (min) | NTO / NTB (min) |
|---|---|---|---|---|---|---|
| T_DINO-1 | 150 | −265 | 15 | 15 | 20 | 0 / 0 |
| T_FFES-1 | 55 | −70 | 15 | 15 | 15 | 0 / 0 |
| T_CRUA-1 | 52 | −128 | 15 | 30 | 2 | 0 / 0 |
| T_CRUA-3 | 70 | −113 | 15 | 30 | 2 | 0 / 0 |
| T_FOYE-1 | 110 | −155 | 30 | 30 | 10 | 2 / 2 |

Read SEL as the registered minimum generation per unit.

These are BM-submitted parameters, not physical minima. NDZ, MZT and MNZT can be set commercially. On "minimum generation", the MFR capability file also lists deload levels, e.g. DINO units at 138/118 MW and CRUA-1/2 at 110/84 MW [V].

---

## 6. Gaps and suggested next steps

- **Per-unit revenue that is not public:**
  - Optional Fast Reserve (2020–2024)
  - Black Start
  - optional spinning/"spin-gen" arrangements
  - bilateral CFR
  - pre-2016 Dinorwig commercial response deals
  - firm STOR contract values before 2020 (tender reports may exist, not checked)
- **Per-unit revenue that is public:**
  - BM (Elexon)
  - FFR post-tender (already held)
  - MFR (volumes × prices, negligible)
  - ORPS (MVArh × rate)
  - firm FR tender reports, 2017 – Mar 2019
  - STOR day-ahead (Apr 2021 onward, negligible)
  - CM register
  - Stability Pathfinder: CRUA-3 availability only. Value is ~£5m/yr per Drax.
- **Cruachan efficiency and Foyers storage** have no primary source. Check against Elexon PN/BOALF data by fitting the pump-MWh to generate-MWh ratio over long windows.
- The FHC accounts are images. To get the odd-year narrative (2017, 2019, 2021, 2023), read pages 1–2 of those PDFs.

---

## 7. Summary (15 lines)

1. MFR: NESO publishes per-BMU monthly holding prices (2007–2026) and capabilities (2011–2026). DINO, FFES, CRUA and FOYE are all named.
2. MFR: per-BMU daily holding volumes (D9/D3) are published from FY2015-16. They show DINO and FFES held 0 MFR and CRUA and FOYE held almost none. MFR is below £50k/yr for any PSH, so treat it as ~0.
3. MFR pay structure: holding £/MW/h (self-submitted through FRPS) plus a response energy payment at MIP×1.25 for up / MIP×0.75 for down (CUSC 4.1.3).
4. Fast Reserve: unit-level firm FR tender reports (FFES-2/3/4, DINO-2, CRUA-4 with £/h fees) are public for about 2017 to Mar 2019. Firm tenders stopped in Jan 2020. Optional FR to Dec 2024 is not public per unit.
5. ORPS: public per BMU per month (MVArh) together with the £/MVArh rate. It is worth £1.3–6.6m/yr to Dinorwig, £0.2–2.8m to Cruachan, and £0.1–0.8m each to FFES and FOYE.
6. Stability Pathfinder: CRUA-3 held a Phase 1 contract (~2020 to Mar 2026), "up to £5m/yr" according to Drax. NESO publishes only availability flags.
7. STOR day-ahead (2021 onward) and EAC (DC/DM/DR/BR/QR/SR): PSH are essentially absent. Black Start, spin-gen and CFR values are confidential.
8. FHC (02444277) accounts give calendar-year turnover, cost of sales, gross profit, operating profit and depreciation for 2015–2025. Turnover is netted half-hourly and includes ancillary services and CM.
9. FHC turnover − cost of sales (£m): 154, 154, 151, 132, 171, 167, 237, 285, 286, 233, 154 for 2015 to 2025.
10. FHC EBITDA ≈ (£m): 103, 108, 102, 79, 126, 114, 117 (incl. £20m insurance), 280, 265, 140, 82 for 2015 to 2025.
11. FHC has no market split. Only the IFRS 9 (bilateral/traded) vs IFRS 15 (contracts; likely BM, ancillary and CM) split is given, e.g. 2024: £134m vs £187m.
12. Drax "Pumped storage & hydro" Adj. EBITDA (£m): 71, 73, 68, 171, 230 (253 excl. EGL), 138, 111 for 2019 to 2025. It includes ~126 MW of run-of-river hydro, and Daldowie to 2022.
13. Drax Flexible Generation revenue: £381m in 2023, £223m in 2024, £172m in 2025. Ancillary services within it: £30.4m, £24.2m, £21.2m. Cruachan alone is not reported. Foyers has no separate disclosure.
14. Physical data (IPR 2005 primary): Dinorwig 6×288 MW gen / 275 MW pump, ~9 GWh, 74–75%. Ffestiniog 4×90 / 75 MW, ~1.4 GWh, 72–73%. Dinorwig pump→generate ≈ 6 + 1.5 min.
15. Cruachan: 440 MW, ≥16 h at full output (≈7 GWh), efficiency not published. Foyers: 2×150 MW, ~6.3 GWh [S], efficiency not published. Elexon dynamic data gives SEL/SIL/MZT/NDZ per BMU.
