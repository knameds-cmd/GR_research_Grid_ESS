---
id: denholm2020_peakingcapacity
title: "The potential for battery energy storage to provide peaking capacity in the United States"
authors: ["Denholm, P.", "Nunemaker, J.", "Gagnon, P.", "Cole, W."]
year: 2020
journal: "Renewable Energy"
volume_issue_pages: "151:1269-1277"
doi: "10.1016/j.renene.2019.11.117"
quartile: "Q1 (SJR 2020, Renewable Energy, Sustainability and the Environment)"
group: "Paul Denholm / Wesley Cole - NREL Strategic Energy Analysis Center (ReEDS team)"
lineage: "NREL grid-analysis group; Denholm long-time co-author of Sioshansi (sioshansi2014_capacityvalue). Advisor-student ties not applicable/verified."
streams: [S7_market_design]
market_context: "18 US regions (NERC assessment areas incl. CAISO, ERCOT, PJM, MISO, NYISO, ISO-NE, SPP); resource-adequacy accreditation rules (CPUC/NYISO 4-hour rule)"
method_class: "chronological peak-shaving simulation (deterministic, perfect foresight) - capacity-credit approximation"
evidence_read: "full text of NREL technical report version (NREL/TP-6A20-74184, June 2019, https://www.nrel.gov/docs/fy19osti/74184.pdf); journal version not read"
oa_link: "https://www.nrel.gov/docs/fy19osti/74184.pdf"
---

## 1. Research question
How much 4-h (and longer) battery storage can provide peaking capacity with full capacity credit in each US region, and how does PV/wind deployment change that potential?

## 2. Setting & assumptions
- Deterministic, perfect foresight of load; hourly; 80% round-trip efficiency; no storage outages.
- Storage dispatched solely to shave annual peak net load (reliability-driven, not price-driven).
- Capacity credit = fraction of power rating that reduces annual peak ("peak demand reduction credit", PDRC), not full ELCC.

## 3. Constraints that drove the model choice
National 18-region scope and multiple PV/wind penetrations made full probabilistic ELCC impractical; PDRC is a transparent proxy matching how RA rules (4-hour rule) actually accredit batteries.

## 4. Model
- Iteratively add storage in 0.1%-of-peak steps up to 30% peak reduction; for each target peak, simulate charge when net load < target and discharge otherwise; required energy = max cumulative discharge over the year.
- PDRC < 100% once net-load peaks last longer than the battery duration (e.g., ~67% for a 4-h device facing a 6-h peak) -> "capacity credit cliff".

## 5. Data & processing
FERC Form 714 loads 2007-2013 (+ ISO data), boundary adjustments; PV/wind profiles from reV (NSRDB, WIND Toolkit) at ReEDS-derived penetrations (5-35%); 2020 peak forecasts from NERC 2018 LTRA.

## 6. Justification
Transparent, conservative choice of load years; explicitly recommends regional ELCC validation; consistent with published ELCC studies cited.

## 7. Key results
- Base case: ~28 GW of 4-h storage nationally could provide peaking capacity at 100% credit; +8 GW at 6 h and +34 GW at 8 h (~70 GW total) vs ~261 GW of existing peakers.
- Regional heterogeneity: narrow summer peaks (e.g., California, Florida) favour 4-h storage; broad peaks (NYISO: ~440 MW) do not.
- 10% PV roughly doubles 4-h practical potential (narrower net-load peaks); wind effect inconsistent; saturation when peak shifts to winter.
- Policy: discontinuous 4-hour accreditation rules create a cliff in revenue once PDRC < 100%; longer durations needed after saturation.

## 8. Limitations (stated + critical reading)
Perfect foresight, historical load shapes (no electrification/climate change), no transmission sharing, hourly resolution, no outages, not true ELCC. Critical: reliability-driven dispatch ignores that market-driven batteries may not be full at the peak (cf. sioshansi2014_capacityvalue), so the numbers are upper bounds for merchant batteries.

## 9. Relevance to my study
Explains why accreditation rules (duration-based de-rating, 4-hour rule) are a first-order design lever for battery profitability and why capacity value declines with fleet size. Directly comparable to GB Capacity Market duration-based de-rating factors for batteries; a simulator can include a capacity product whose credited MW depends on duration and fleet saturation.

## 10. Lineage links
- Builds on: sioshansi2014_capacityvalue; NREL ReEDS/reV work.
- Built upon by (notable): Frazier, Cole, Denholm et al. 2020 Applied Energy (storage peaking-capacity expansion) - citation not verified here.

## 11. Verification log
- RePEc IDEAS (eee/renene/v151y2020icp1269-1277): title, 4 authors, Renewable Energy 151(C):1269-1277, 2020, DOI 10.1016/j.renene.2019.11.117.
- SJR: scimagojr sourceid 27569, Q1 2019, 2020, 2024.
- Full text read is the NREL technical report (same title/authors, June 2019) - journal text may differ in detail; numbers taken from the TP. Funding DOE EERE.
