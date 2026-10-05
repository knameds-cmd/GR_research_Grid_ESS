---
id: bertrand2020_intradaystorage
title: "Adaptive Trading in Continuous Intraday Electricity Markets for a Storage Unit"
authors: ["Bertrand, G.", "Papavasiliou, A."]
year: 2020
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "35(3):2339-2350"
doi: "10.1109/TPWRS.2019.2957246"
quartile: "Q1 (SJR 2019-2025, Electrical & Electronic Eng. and Energy Eng. & Power Technology; SJR 2024 = 3.629)"
group: "Anthony Papavasiliou (CORE, UCLouvain; ENGIE Chair on Energy Economics and Energy Risk Management)"
lineage: "Papavasiliou group (UCLouvain CORE; Papavasiliou = UC Berkeley PhD under S. Oren). Bertrand listed as IEEE Student Member at CORE, sole co-author with Papavasiliou (PhD-student relation consistent but not independently verified)."
streams: [S5_rl_learning]
market_context: "German continuous intraday market (EPEX, hourly products), price-taker liquidity taker"
method_class: "RL/DRL"
evidence_read: "full text (author-hosted PDF: https://ap-rg.eu/wp-content/uploads/2020/07/J19.pdf)"
oa_link: "https://ap-rg.eu/wp-content/uploads/2020/07/J19.pdf"
---

## 1. Research question
How should a storage unit trade in the continuous intraday market (CIM), where it can hit standing order-book offers at any time before gate closure, and can a learned, interpretable threshold policy beat the industry-standard rolling-intrinsic (RI) policy?

## 2. Setting & assumptions
- Price-taker and liquidity taker: the agent only accepts existing orders, does not place limit orders; it does not influence later orders of others (validity discussed in an e-supplement).
- **Historical order-book replay** (EPEX open/cancel/accept events processed chronologically) - a data-driven market simulator, not a price series.
- Generic 200 MWh storage (battery / pumped hydro), round-trip efficiency 1.0 or 0.81; no end-of-horizon residual value; risk neutral; position must be balanced at gate closure.
- Hourly products only; test trading frequency 1 s (captures 98.3% of offers).

## 3. Constraints that drove the model choice
The transition dynamics of the order book are unknown and non-parametric; a full SDP over order-book states is intractable. Authors therefore choose a low-dimensional parametrised (threshold) policy trained by policy-gradient on replayed data, keeping interpretability.

## 4. Model
- MDP: state = current order book (delivery time, side, price, quantity), stored-energy trajectory v_{t-1,d} per delivery hour, time to closure, day-ahead/intraday auction price; action = discrete buy/sell quantity per delivery hour; reward = integral of the order-book curve over accepted quantity.
- Policy: Gaussian buy/sell price thresholds per delivery hour; means adapted by 10 parameters alpha (auction-price range, inventory, exponential time-to-closure urgency, deviation from RI recommendation, efficiency scaling).
- Algorithm: REINFORCE (Monte-Carlo policy gradient), learning frequency increased gradually hourly -> 15 min -> 5 min; 1 iteration = 4 x 200 training days = 800 episodes, 8 CPUs, ~40 h.

## 5. Data & processing
- EPEX German CIM order books 2015-2016.
- **Chronological split**: train first 200 days of 2015; out-of-sample test = remaining 165 days of 2015 + all of 2016 (531 days).

## 6. Justification (why the authors argue the approach is valid)
Benchmarks against Rolling Intrinsic (re-optimised myopic trading, an optimisation baseline used in industry) and against their earlier threshold policy (GM). In- vs out-of-sample comparison, ablation of each alpha group, and 6 independent REINFORCE runs (hourly) reported as "very similar" (details in e-supplement).

## 7. Key results
- 1-s trading, eta=1.0, out-of-sample: 6,405 EUR/day vs RI 5,438 EUR/day (**+17.8%**); better than RI on 77.4% of days.
- eta=0.81: 3,762 vs 3,311 EUR/day (+13.6%).
- In-sample vs out-of-sample profit differs by only a few % -> limited overfitting.
- Removing the time-to-closure urgency parameters (alpha_3, alpha_4) cuts profit by ~13%, collapsing toward RI.
- **No perfect-foresight bound reported.**

## 8. Limitations (stated + your critical reading)
- Stated: no limit-order placement, no block/iceberg orders, hourly products only, no price impact, risk neutral.
- Seed variance acknowledged with 6 runs (good practice relative to the field), but statistics are only in the e-supplement.
- No PF bound, so absolute efficiency is unknown; order-book replay ignores reaction of other traders to the agent's liquidity taking.

## 9. Relevance to my study
Best-in-class example of RL for a market whose clearing mechanism (continuous pay-as-bid order book) is itself the object: the environment is a replay of the actual market mechanism. Shows that low-dimensional, interpretable parametrised policies reduce RL variance - a design principle if any learning is used in attribution. Also a clear benchmark (Rolling Intrinsic) for CIM studies.

## 10. Lineage links
- Builds on: Bertrand & Papavasiliou threshold policy (earlier conference work "GM"); Williams REINFORCE (1992); rolling-intrinsic literature (Löhndorf & Wozabal style).
- Built upon by (notable): boukas2021_intradaydrl (DRL for CIM, Liège); Bertrand & Papavasiliou follow-ups on intraday RL for renewable sources.

## 11. Verification log
- OpenAlex (doi:10.1109/TPWRS.2019.2957246): title, authors (CORE UCLouvain), 35(3):2339-2350, online 2019-12-02.
- Full text: author/group-hosted PDF (ap-rg.eu J19).
- SJR: scimagojr sid 28825 - Q1 2019-2025 in two categories.
- Unverified: the 6-run variance statistics (in electronic supplement, not read).
