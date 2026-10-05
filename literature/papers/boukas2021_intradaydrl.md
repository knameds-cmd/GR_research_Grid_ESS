---
id: boukas2021_intradaydrl
title: "A deep reinforcement learning framework for continuous intraday market bidding"
authors: ["Boukas, I.", "Ernst, D.", "Théate, T.", "Bolland, A.", "Huynen, A.", "Buchwald, M.", "Wynants, C.", "Cornélusse, B."]
year: 2021
journal: "Machine Learning"
volume_issue_pages: "110(9):2335-2387"
doi: "10.1007/s10994-021-06020-8"
quartile: "Q1 (SJR 2021: Artificial Intelligence and Software, SJR 1.640; also Q1 2024/2025)"
group: "Damien Ernst and Bertrand Cornélusse (Montefiore Institute, University of Liège), with ENGIE Market Modeling (Brussels)"
lineage: "Liège Ernst group - originators of fitted Q iteration (Ernst, Geurts & Wehenkel, JMLR 2005); Boukas, Théate, Bolland were Liège PhD students in the Ernst/Cornélusse group (co-authorship and affiliation; formal supervision not checked)."
streams: [S5_rl_learning]
market_context: "German EPEX continuous intraday (quarter-hourly products), pumped-hydro storage, price-taker liquidity taker"
method_class: "RL/DRL"
evidence_read: "full text partially (arXiv 2004.05940: sections 1-4 incl. MDP, algorithm, case-study setup); quantitative results section not retrieved -> results (from abstract)"
oa_link: "https://arxiv.org/abs/2004.05940"
---

## 1. Research question
Can a batch-mode deep RL agent learn when to trade in the continuous intraday order book for a storage asset, improving on the rolling-intrinsic (RI) policy used in industry?

## 2. Setting & assumptions
- Price-taker / no price impact: other participants' orders follow the historical order-book record ("depend strictly on the history of order book states").
- **Historical order-book replay** of EPEX German CID, 96 quarter-hourly products, trading window 17:00-03:00 discretised into K=40 steps of 15 min.
- Asset: PHES 200 MWh, 200 MW charge/discharge, eta = 100%, initial = terminal SoC 100 MWh.
- Imbalance penalties at settlement included in reward; restrictive assumption that positions can always be covered without imbalance.

## 3. Constraints that drove the model choice
The full order-book state is extremely high-dimensional and partially observable; exact SDP is impossible. The authors reduce the action space to two high-level actions ("Trade" = solve a bid-acceptance optimisation maximising immediate revenue; "Idle"), compress the state into hand-crafted order-book depth features and a 10-step history pseudo-state, and use batch RL (fitted Q) on replayed data.

## 4. Model
- State: 10 order-book depth/distance features, market position and SoC per delivery period, DA prices (24), recent imbalance prices/volumes, calendar features; history window of 10 steps (263-d input per step).
- Action: {Trade, Idle}; "Trade" embeds an optimisation (RI-like bid acceptance) - i.e. hybrid RL-over-optimisation.
- Reward: trading revenue + imbalance settlement terms.
- Algorithm: Fitted Q Iteration with LSTM function approximator (1 LSTM layer 128 units + 5 FC layers x 36 ReLU), asynchronous distributed actors (epsilon in [0.1,0.5] annealed to 0), single learner, 2,000 episodes per training day.

## 5. Data & processing
- 362 days of German CID order-book data.
- Split: 252 training days and 110 test days **sampled uniformly without replacement (not a chronological split)** - seasonal leakage possible.
- Results averaged over **10 learned policies** (independent runs).

## 6. Justification (why the authors argue the approach is valid)
Backtest on held-out days against RI; averaging over 10 runs to account for training stochasticity; discussion of assumptions (no price impact, pseudo-state sufficiency, discretisation suboptimality).

## 7. Key results
- (from abstract) The learned policy "achieves in average higher total revenues than the benchmark strategy" (rolling intrinsic). Exact numeric gains, run-to-run dispersion and number of days beaten were not retrieved in this reading -> to be filled from the published version.
- No perfect-foresight bound.

## 8. Limitations (stated + your critical reading)
- Stated: restrictive no-imbalance assumption; discretisation suboptimality; pseudo-state sufficiency unvalidated; no price impact; "only way to evaluate exact viability is to deploy it".
- Random-day split rather than walk-forward; eta = 100% removes a key arbitrage friction.
- Action space so coarse that the RL contribution is a timing rule on top of an optimisation step - the gain over RI is a "when to trade" gain.

## 9. Relevance to my study
Shows the hybrid design (RL selects among optimisation-based actions) and the practice of reporting averages over 10 runs. Highlights that even in strong ML groups, environment = historical replay with no reaction of others, which is incompatible with counterfactual market-rule analysis.

## 10. Lineage links
- Builds on: Ernst, Geurts & Wehenkel 2005 (fitted Q iteration); Löhndorf & Wozabal rolling intrinsic; bertrand2020_intradaystorage.
- Built upon by (notable): later CID RL / DRL papers (not archived here).

## 11. Verification log
- Springer article page: Machine Learning 110(9):2335-2387, online 2021-07-12, DOI 10.1007/s10994-021-06020-8, author list (8 authors) verified.
- ORBi (Liège repository) record exists (handle 2268/232846).
- SJR: scimagojr sid 24775 - Q1 in Artificial Intelligence and Software for 2021, 2024, 2025.
- NOT verified: quantitative results (results section of arXiv/published text not retrieved by the fetch tool).
