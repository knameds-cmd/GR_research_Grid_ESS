---
id: jeong2023_deepbid
title: "Deep Reinforcement Learning Based Real-Time Renewable Energy Bidding With Battery Control"
authors: ["Jeong, J.", "Kim, S. W.", "Kim, H."]
year: 2023
journal: "IEEE Transactions on Energy Markets, Policy and Regulation"
volume_issue_pages: "1(2):85-96"
doi: "10.1109/TEMPR.2023.3258409"
quartile: "Q1 (SJR 2025: Economics & Econometrics; Energy (misc.); Management, Monitoring, Policy & Law; SJR 1.449). Journal launched 2023; SJR publishes quartiles only from its first ranked year (2025 shown) - quartile for 2023 not available."
quartile_basis: "nearest-year; rule=pass; journal launched 2023, first SJR-ranked year 2025 = Q1"
group: "Hongseok Kim (Sogang University, Dept. of Electronic Engineering) with Seung Wan Kim (Chungnam National University at time of publication; now KENTECH, SEND Lab)"
lineage: "Sogang Hongseok Kim group; Jeong (Sogang / ETRI) is first author of the group's DRL-for-renewables line (DeepComp, Applied Energy 2021, with H. Kim). Seung Wan Kim co-author -> direct lineage to the KENTECH SEND Lab. Advisor-student relation Jeong-H. Kim consistent with affiliations, not independently verified."
streams: [S5_rl_learning]
market_context: "Real-time energy market bidding of a renewable producer (solar / wind) with co-located battery; deviation penalties; price-taker"
method_class: "RL/DRL"
evidence_read: "abstract (OpenAlex) + public code repository metadata (github.com/Jaeik-Jeong/DeepBid); full text not accessible (closed access, no preprint found) -> deep fields (from abstract)"
oa_link: "https://github.com/Jaeik-Jeong/DeepBid (code only)"
---

## 1. Research question
Renewable bidding and battery control are usually studied separately; can a joint DRL policy that bids considering the battery's ability to compensate forecast errors, and then uses residual battery capacity for price arbitrage, raise a renewable producer's total real-time-market profit?

## 2. Setting & assumptions
(from abstract) Renewable producer bids into a real-time energy market; revenue reduced by deviation penalties; battery first compensates generation forecast error, then performs arbitrage. Uncertain prices and renewable generation. Exogenous (historical) data; price-taker implied. Time resolution, asset sizes: not verified.

## 3. Constraints that drove the model choice
(from abstract) Joint uncertainty in price and generation with sequential coupling through SoC -> sequential decision making under uncertainty addressed with DRL rather than separate forecast-then-control.

## 4. Model
(from abstract) "DeepBid": DRL-based bidding combined with battery control; bid determined considering error compensability of the battery; second-stage battery control for arbitrage. Specific algorithm, MDP state/action/reward and hyper-parameters: **not verified (full text not read)**. Repository contains notebooks for "comparisons and performance analysis" and builds on the group's DeepComp (DRL error-compensable forecasting) and space-time CNN PV aggregation.

## 5. Data & processing
(from abstract) "Extensive simulations with real solar and wind generation data". Data sources, period, split, seeds: not verified.

## 6. Justification (why the authors argue the approach is valid)
(from abstract) Comparison with "existing bidding strategies" where the bid equals the forecast value, and with a pure compensation strategy.

## 7. Key results
(from abstract) DeepBid "substantially increases the total profit" vs existing bidding strategies, achieving revenues as high as forecast-based bidding with deviation penalties as low as the compensation strategy. Numbers not verified.

## 8. Limitations (stated + your critical reading)
- Not assessable in detail without full text. From the abstract: no mention of a perfect-foresight or stochastic-programming benchmark, nor of seed variance.
- Public code release (GitHub, 135 commits) is a reproducibility strength relative to most of this stream.

## 9. Relevance to my study
Direct lineage (Seung Wan Kim co-author) linking the SEND Lab to DRL-based bidding of renewable+storage. Useful as the in-group precedent when justifying the move from RL to optimisation for attribution: the same problem (bid + battery control under penalties) can be cast as a two-stage stochastic program whose outputs are attributable to settlement rules (deviation penalty design).

## 10. Lineage links
- Builds on: Jeong & Kim, DeepComp (Applied Energy vol. 294, 2021, per RePEc listing; DOI not verified here); Hongseok Kim group's PV aggregation forecasting.
- Built upon by (notable): Sogang/SEND later works (not verified).

## 11. Verification log
- OpenAlex (doi:10.1109/TEMPR.2023.3258409): title; authors in order Jaeik Jeong (ETRI; Sogang), Seung Wan Kim (Chungnam National University), Hongseok Kim (Sogang); 1(2):85-96; published 2023-03-17; closed access.
- Abstract reconstructed from OpenAlex abstract_inverted_index.
- GitHub repository Jaeik-Jeong/DeepBid links to IEEE document 10075530.
- SJR: scimagojr sid 21101343415 - Q1 (2025) in three categories; coverage 2023-2026.
- UNVERIFIED: all architecture, data, split, seeds and numeric results.
