---
id: braeuer2019_parallelrevenue
title: "Battery storage systems: An economic model-based analysis of parallel revenue streams and general implications for industry"
authors: ["Braeuer, F.", "Rominger, J.", "McKenna, R.", "Fichtner, W."]
year: 2019
journal: "Applied Energy"
volume_issue_pages: "239:1424-1440"
doi: "10.1016/j.apenergy.2019.01.050"
quartile: "Q1 (SJR 2025, Energy (misc.); Building and Construction; Management, Monitoring, Policy and Law)"
quartile_basis: "pub-year; rule=pass; SJR 2019 Q1 for this journal recorded in engels2019_fcrgermanytechnoeco"
group: "Wolf Fichtner, Chair of Energy Economics, Institute for Industrial Production (IIP), Karlsruhe Institute of Technology"
lineage: "KIT IIP energy-economics group (Fichtner; McKenna then at KIT IIP). Braeuer and Rominger = IIP researchers (per authorship); advisor ties not verified."
streams: [S2_stacking_cooptimization]
market_context: "Germany: behind-the-meter industrial BESS: peak shaving (grid-fee demand charge) + primary control reserve (PCR/FCR) + day-ahead and intraday arbitrage; 50 SMEs"
method_class: "LP"
evidence_read: "abstract only (EconPapers/RePEc); full text not accessible"
oa_link: ""
---

## 1. Research question
Can a BESS in German small and medium-sized enterprises be profitable by pursuing peak shaving, PCR and DA/ID arbitrage **in parallel**? Which load-profile indicators predict profitability? (from abstract)

## 2. Setting & assumptions
(from abstract)
- An industrial plant's energy system as an LP with 15-min resolution.
- Investment (BSS capacity) is optional, so the model co-optimises sizing and operation.
- 50 real SME load profiles.
- Foresight and price assumptions not read.

## 3. Constraints that drove the model choice
(from abstract) An LP keeps the joint sizing-and-operation problem tractable across 50 sites.

## 4. Model
- (from abstract) Objective: minimise total cost (including investment) under peak-shaving, PCR and arbitrage options.
- Capacity split and PCR energy rules: **not read**.

## 5. Data & processing
(from abstract) 50 German SME load profiles. A stepwise linear regression of profitability on new load indicators.

## 6. Justification (why the authors argue the approach is valid)
Not read.

## 7. Key results
(from abstract)
- No single revenue stream is profitable alone; all three together can be profitable for some firms. Most cash flow comes from peak shaving and PCR.
- Fixed 500 kWh BSS: NPV ranges from −€350k (arbitrage only) to about +€200k (all three).
- Variable capacity: optimal size up to 1,200 kWh, profitability index 0.06–0.31.
- Arbitrage adds little under German spreads relative to the degradation it causes.

## 8. Limitations (stated + your critical reading)
- Stated (abstract): needs a more detailed technical battery model and a larger sample.
- Critical reading: German PCR moved to daily and then 4-hour products in 2018–2020, which changes stacking feasibility.

## 9. Relevance to my study
- Evidence that stacking is what flips the economic sign, in a BTM setting.
- A contrast case to FTM merchant stacking.

## 10. Lineage links
- Builds on: German BTM/PCR battery studies.
- Built upon by (notable): later German multi-use BTM studies (e.g., englberger2020_dynamicstacking addresses a similar application set with dynamic allocation).

## 11. Verification log
- Crossref (api.crossref.org/works/10.1016/j.apenergy.2019.01.050): title, authors, Applied Energy 239, pp. 1424–1440, April 2019. Confirmed.
- EconPapers abstract read verbatim.
- SJR (id 28801): Q1 2025.
- Full text not accessed. All deep fields abstract-level.
