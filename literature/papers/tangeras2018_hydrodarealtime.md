---
id: tangeras2018_hydrodarealtime
title: "Real-time versus day-ahead market power in a hydro-based electricity market"
authors: ["Tangerås, T. P.", "Mauritzen, J."]
year: 2018
journal: "The Journal of Industrial Economics"
volume_issue_pages: "66(4):904-941"
doi: "10.1111/joie.12186"
quartile: "Q1 (SJR 2018 and 2025, Economics and Econometrics)"
group: "Tangerås (IFN Stockholm; EPRG Cambridge associate); Mauritzen (BI Norwegian Business School)"
lineage: "IFN electricity-markets programme; Mauritzen earlier at NHH/IFN (see mauritzen2013_deadbattery). Advisor ties not verified."
streams: [S8_empirical_econ]
market_context: "Nord Pool Sweden SE1-SE4, Elspot (DA) vs Elbas (intraday/real-time), 2010-2013; hydro reservoirs as storage"
method_class: "econometric (theory-derived test of competitive pricing across sequential markets; OLS/IV)"
evidence_read: "full text (author version https://jmaurit.github.io/research/real-time-versus-4.pdf)"
oa_link: "https://biopen.bi.no/bi-xmlui/handle/11250/2620784"
---

## 1. Research question
Can market power of storage-holding (hydro) producers be detected from price relationships between day-ahead and real-time markets, without firm-level cost or bid data?

## 2. Setting & assumptions
- Two-period model: producers with reservoir (intertemporal) flexibility allocate output between DA (firm price) and RT (risky); imperfect competition, possible risk aversion.
- Hourly data 2010-2013; ~110k Elspot obs; ~22k Elbas trades (08:00-12:00); Swedish price areas (split into four in Nov 2011).

## 3. Constraints that drove the model choice
Hydro marginal cost = unobservable shadow value of water, so classic markup tests (price vs cost) are infeasible. The authors derive tests in which water value cancels: for *simultaneous delivery* or *simultaneous trade*, price differences cannot reflect production/storage constraints or risk under perfect competition.

## 4. Model
- Prop. 1/2: under perfect competition, (Q2 - Q1)(f2 - p1) >= 0 for products traded simultaneously; DA-RT price gap independent of producer price risk.
- H1 test: f_{ah,t+1} - p_{iah,t+1} = b0 + b1 |dF/dZ| + b2 peak + b3 |dF/dZ| x peak + controls (inflow, reservoir fill, net exports, HDD) + e; competition implies b1 = 0, b1 + b3 = 0 (slope of aggregate Nordic net-demand curve computed +-0.5 GWh around clearing).
- H2 test: (Q_{t+1}-Q_t)(f - p) = sum_j gamma_j DoW_j + e; since competition implies (Q2-Q1)(f2-p1) >= 0, significantly negative gamma_j reject perfect competition.
- IV: weather (HDD, inflow) instruments demand slope.

## 5. Data & processing
Nord Pool Elspot/Elbas prices and trades, Svenska Kraftnät production/flows, reservoir data. Elbas trades matched to the DA price of the same delivery hour.

## 6. Justification
Theory-derived restrictions that hold for any water value; robustness: IV, transaction costs (0.04 vs 0.11 EUR/MWh), test for binding DA bidding constraints, liquidity checks (lowest-liquidity SE4 shows strongest rejection, against a pure noise story).

## 7. Key results
- Competitive pricing rejected in SE2 (H1: off-peak b1 = +0.080**, peak -0.104***) and in SE3/SE4 (H2: significantly negative day-of-week coefficients; SE4 intercept -703.23**).
- SE1 largely consistent with competition. Evidence of local market power in RT/intraday, consistent with DA-RT arbitrage by storage-holding firms.

## 8. Limitations (stated + critical reading)
- Diagnostic (reject/not reject), not markup magnitudes; may under-detect market power; system-level not firm-level demand slope; thin Elbas liquidity.
- (Critical) Nordic hydro is seasonal storage; mapping to short-duration batteries is about the logic of the test, not magnitudes.

## 9. Relevance to my study
Key methodological idea for storage: when the storage unit's opportunity cost (water value / SoC value) is unobservable, construct tests in which it cancels (simultaneous delivery across sequential markets). For GB batteries, the analogous test compares a unit's prices across simultaneous-delivery venues (DA auction vs intraday vs BM offer vs EAC opportunity cost) for the same settlement period, where SoC value cancels.

## 10. Lineage links
- Builds on / related: Førsund hydro economics; mauritzen2013_deadbattery (same co-author); Ito & Reguant 2016 AER on sequential-market arbitrage (related, citation not verified; cross-ref S7).
- Built upon by: not checked (Lundin & Tangerås, Nord Pool Cournot test, is a related IFN paper).

## 11. Verification log
- BI Open repository: JIE vol 66, issue 4, pp. 904-941, DOI 10.1111/joie.12186 (published 2018); Wiley DOI landing page in search results.
- SJR JIE sourceid 24389: Q1 2018 and 2025.
- Full text: author-posted version.
