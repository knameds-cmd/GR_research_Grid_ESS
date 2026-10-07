---
id: green2012_storingwind
title: "Storing Wind for a Rainy Day: What Kind of Electricity Does Denmark Export?"
authors: ["Green, R.", "Vasilakos, N."]
year: 2012
journal: "The Energy Journal"
volume_issue_pages: "33(3):1-22"
doi: "10.5547/01956574.33.3.1"
quartile: "Q1 (SJR 2012, Economics and Econometrics; Energy misc.)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Richard Green (then Birmingham, later Imperial College Business School) with Vasilakos (UEA Norwich Business School)"
lineage: "Green: long-running GB/European market-design group (Green & Newbery 1992 lineage); later Williams & Green 2022 Energy Policy on storage market power (S7)."
streams: [S8_empirical_econ]
market_context: "Denmark (DK1/DK2) wind and trade with Nordic hydro system; annual 1996-2009 and hourly 2001-2009"
method_class: "econometric (correlations, GLS with Cochrane-Orcutt; price-weighting decomposition; flow tracing)"
evidence_read: "full text (UEA CCP WP 11-11 https://ueaeco.github.io/working-papers/papers/ccp/CCP-11-11.pdf)"
oa_link: "https://ueaeco.github.io/working-papers/papers/ccp/CCP-11-11.pdf"
---

## 1. Research question
How does Denmark accommodate wind variability via trade with hydro-rich neighbours (implicit storage), and what does this implicit storage cost?

## 2. Setting & assumptions
- Extended "bathtub" (Førsund 2007) theory of hydro-thermal-wind trade as benchmark for optimal trade patterns.
- Empirical: hourly Danish system data 2001-2009 and annual Nordic hydro data 1996-2009.

## 3. Constraints that drove the model choice
Physical flows cannot be attributed to specific stations (Kirchhoff), so the "storage" service is measured through prices and flows (export at low price, import at high price) rather than unit dispatch; Bialek flow tracing used to treat transits.

## 4. Model
- Price regression: p_t on wind output with separate coefficients for congested/uncongested interconnection hours; GLS with Cochrane-Orcutt AR correction.
- Intermittency cost = output-weighted price vs "smoothed" (monthly-average-profile) price; trade cost = valuation of hourly wind deviations at trade-weighted prices.

## 5. Data & processing
Energinet hourly data (wind, thermal, flows, prices), Nordel yearbooks (hydro, reservoirs, inflows).

## 6. Justification
Theory-consistent patterns: annual exports driven by Nordic hydro (r = -0.887) not by Danish wind (r = -0.045); short-run wind deviations co-move with export deviations (r = 0.673). Robustness: excluding 1996-99 and drought year 2003; consistent signs in 17/18 region-years.

## 7. Key results
- Wind lowers DK price by 0.0641 DKK/MWh per MW uncongested vs 0.0986 congested (+53%).
- Intermittency cost: 8.0% of wind value in West DK (5.0-15.3% by year), 4.1% in East DK.
- Trade (storage) cost: 4.3% (DK-W) and 3.1% (DK-E) of wind value; ~DKK 11/MWh (~EUR 1.45/MWh) on average — Nordic hydro provides cheap implicit storage.

## 8. Limitations (stated + critical reading)
- Cannot identify exporting stations; assumes all wind deviations are traded; FiT not market prices determine wind revenues; correlation-heavy, weak causal identification.

## 9. Relevance to my study
Provides an empirical "price of storage" benchmark (spread captured by implicit hydro storage) that a battery must beat. The output-weighted vs time-weighted price decomposition is the same capture-rate metric used today for battery revenue benchmarking (e.g., GB battery indices) and can be applied to Elexon unit data.

## 10. Lineage links
- Builds on: Førsund (2007) hydropower economics; Bialek (1996) flow tracing.
- Built upon by: mauritzen2013_deadbattery (related question; citation not verified); Williams & Green 2022 Energy Policy (S7, same senior author, storage & market power in GB).

## 11. Verification log
- Imperial Spiral record: Energy Journal 33(3):1-22, 2012, DOI 10.5547/01956574.33.3.1; SAGE DOI landing page in search results.
- SJR Energy Journal: Q1 2012.
- Full text: UEA CCP working paper 11-11 (affiliations Birmingham / UEA at that time).
