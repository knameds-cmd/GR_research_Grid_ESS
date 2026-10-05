---
id: mauritzen2013_deadbattery
title: "Dead Battery? Wind Power, the Spot Market, and Hydropower Interaction in the Nordic Electricity Market"
authors: ["Mauritzen, J."]
year: 2013
journal: "The Energy Journal"
volume_issue_pages: "34(1):103-124"
doi: "10.5547/01956574.34.1.5"
quartile: "Q1 (SJR 2013, Economics and Econometrics; Energy misc.)"
group: "NHH Norwegian School of Economics / IFN Stockholm (doctoral-era work)"
lineage: "Co-author of tangeras2018_hydrodarealtime (IFN). Advisor not verified."
streams: [S8_empirical_econ]
market_context: "Nord Pool: West/East Denmark wind vs southern-Norway price-area hydro (reservoir) production, daily, ~8 years"
method_class: "econometric (distributed-lag ARMA time series, SURE)"
evidence_read: "full text (IFN WP 908 version https://www.ifn.se/wfiles/wp/wp908.pdf)"
oa_link: "https://www.ifn.se/wfiles/wp/wp908.pdf"
---

## 1. Research question
Do Norwegian hydro reservoirs act as a de-facto "battery" for Danish wind — i.e., how do trade flows, hydro production and prices respond to wind output?

## 2. Setting & assumptions
- Observational; wind output treated as exogenous (zero marginal cost, weather-driven).
- Daily averages (hourly prices averaged), ~2,800-2,900 days; regional aggregates (no plant panel).

## 3. Constraints that drove the model choice
Plant-level hydro decisions and water values are unobserved; strong autocorrelation and weekly seasonality in daily series -> single-equation distributed-lag models with AR/MA terms rather than VAR or structural water-value model.

## 4. Model
d_t = sigma * wind_t + delta' X_t + sum AR(1..7) + MA(1..7) + e_t, with X = consumption (DK, NO), temperature; interactions with net-export/net-import regime dummies. Dependent variables: DK-NO net trade, log area prices, first-differenced southern-Norway hydro output. SURE across price areas.

## 5. Data & processing
Energinet wind (East/West DK), Nord Pool spot prices, DK-NO flows, southern-Norway hydro production; lag selection by AIC; ADF tests.

## 6. Justification
Exogeneity of wind; robustness to controls, lag structures, first differences, Newey-West SEs, SURE.

## 7. Key results
- +1 MWh/h Danish wind -> +0.27 MWh/h exports to Norway (0.32 on net-export days, 0.11 on net-import days).
- +1 MWh/h wind -> -0.40 MWh/h Norwegian hydro production (up to ~40% of Danish wind "stored" in Norwegian reservoirs; -0.46 on export days).
- Doubling wind: price -5.5% (DK-W), -2.0% (DK-E), -0.3 to -0.5% (S. Norway); no significant effect on Norwegian intraday price volatility.

## 8. Limitations (stated + critical reading)
- Actual (not forecast) wind -> attenuation; correlated wind in Sweden may bias hydro effect upward; daily averaging hides hourly arbitrage; transmission-capacity-specific.
- Reduced-form "storage" interpretation: hydro is shifting its own release, not pumping; the study measures implicit storage via trade.

## 9. Relevance to my study
Evidence that interconnector-plus-reservoir flexibility competes with batteries for the same intertemporal arbitrage rent; for GB, Norway/Denmark interconnectors (NSL, Viking) are part of the residual price formation that batteries arbitrage against. Method (distributed-lag response of a storage-like resource to exogenous renewable shocks) is directly applicable to GB battery fleet output vs wind forecast errors.

## 10. Lineage links
- Related: green2012_storingwind (same Denmark-Nordic question, different method; citation link not verified), Førsund hydro theory.
- Built upon by: tangeras2018_hydrodarealtime (same author group).

## 11. Verification log
- RePEc IDEAS (sae/enejou): Energy Journal 34(1):103-124, Jan 2013, DOI 10.5547/01956574.34.1.5.
- SJR Energy Journal sourceid 29391: Q1 in 2013.
- Full text: IFN working paper 908 (pre-publication; numbers may differ slightly from published version).
