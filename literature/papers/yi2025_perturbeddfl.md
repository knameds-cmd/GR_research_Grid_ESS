---
id: yi2025_perturbeddfl
title: "Perturbed Decision-Focused Learning for Modeling Strategic Energy Storage"
authors: ["Yi, M.", "Alghumayjan, S.", "Xu, B."]
year: 2025
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "16(3):2574-2586"
doi: "10.1109/TSG.2025.3548009"
quartile: "Q1 (SJR 2025, Computer Science (miscellaneous); SJR 2025 = 4.363)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Bolun Xu (Columbia University, Earth & Environmental Engineering / Data Science Institute)"
lineage: "Columbia Xu group: Ming Yi = postdoc (Data Science Institute, alumni 2026), Saud Alghumayjan = current PhD student - both verified on bolunxu.github.io/group. Xu = UW PhD 2018 (Kirschen group)."
streams: [S5_rl_learning]
market_context: "NYISO hourly DA/RT prices (arbitrage); Queensland Tesla Powerpack (real dispatch data, 30-min) for behaviour prediction; price-taker"
method_class: "LP"
evidence_read: "full text (arXiv 2406.17085)"
oa_link: "https://arxiv.org/abs/2406.17085"
---

## 1. Research question
Can a neural predictor of a "hidden reward" (price-like signal) be trained end-to-end through a storage arbitrage optimisation - using perturbation-based (Fenchel-Young) decision-focused learning - to (a) arbitrage better than predict-then-optimise and RL, and (b) predict the dispatch behaviour of strategic storage from observed data (inverse modelling)?

## 2. Setting & assumptions
- Price-taker; optimisation layer = deterministic storage arbitrage over T=24 h (or 96 half-hours) with linear or linear+quadratic charge/discharge cost, SoC dynamics, no simultaneous charge/discharge when price < 0.
- Arbitrage: P=0.5 MW, E=2 MWh, eta 0.9 (varied), e0 = 0.5 MWh; rolling 1-h step.
- Behaviour modelling: synthetic dispatch generated from the optimisation with true prices; plus real Tesla Powerpack data (P 1.11 MW, E 2.2 MWh).
- Historical prices only; no clearing simulation (price-maker extension listed as future work).

## 3. Constraints that drove the model choice
The arbitrage argmax is piecewise constant in prices -> zero/undefined gradients. Additive Gaussian perturbation of the predicted reward smooths the solution map, giving the Fenchel-Young gradient y*_eps(lambda_hat) - y_bar without KKT differentiation. Authors argue RL "relies on trial-and-error exploration ... time-consuming and inefficient for tasks with well-defined objectives", handles constraints poorly and needs SoC discretisation.

## 4. Model
- Loss: perturbed Fenchel-Young loss + beta * MSE to a prior price (beta 0.001 synthetic, 0.01 real).
- Gradient: y*_eps(lambda_hat) - y_bar with Gaussian noise, eps in [1,10], K=1 Monte-Carlo sample.
- Predictors: LSTM (1 layer + 2 FC, hidden 64) or MLP (3 x 96); Adam lr 0.01; input T x 24 x 3 (DA price, RT price, load).

## 5. Data & processing
- Arbitrage: NYISO, **train 2017-2020, test 2021 (chronological)**, 35,017 / 8,713 rolling samples.
- Synthetic behaviour: 2 y train / 1 y test; real Powerpack: 6 months train / 3 months test.
- Single split, **no seeds or confidence intervals reported**.

## 6. Justification (why the authors argue the approach is valid)
Benchmarks: LSTM-MPC and MLP-MPC (predict-then-optimise with MSE predictors), a tabular RL arbitrage baseline (efficiency set to 0.9 for fairness), LSTM-only behaviour prediction and two-stage approaches; sensitivity to efficiency and to unknown cost parameters; transfer across storage specifications.

## 7. Key results
- 2021 NYISO cumulative arbitrage profit (read from figure): linear cost - proposed ~9.1k USD vs LSTM-MPC ~6.2k, MLP-MPC ~5.3k, **RL ~6.1k** (+47%, +71%, +50%); linear+quadratic - ~6.5k vs ~5.0k, ~4.7k, **RL ~3.8k** (+30%, +38%, +72%).
- At eta = 0.85, proposed > 2x benchmarks.
- Behaviour prediction (synthetic, event-based) F1 67.7% vs LSTM 60.6% and two-stage 51.5%; real Powerpack F1 68.9% vs 58.8% (LSTM) and 61.1% (MLP).
- No perfect-foresight percentage given for the arbitrage test.

## 8. Limitations (stated + your critical reading)
- Stated: real-data issues (unknown parameters, missing days, SoC inconsistencies); quadratic costs partially captured; convergence analysis only for the optimisation layer; price-maker setting is future work.
- No multi-seed variance; RL baseline is a simple tabular method, so "+50-72% over RL" is not evidence against modern DRL.
- Profits read from figure (approximate).

## 9. Relevance to my study
Two uses: (i) the inverse/behaviour-modelling idea gives an optimisation-consistent way to estimate how real storage fleets bid, which can be fed into counterfactual clearing under different product rules; (ii) explicit statement from a leading group of why RL is ill-suited for well-defined storage objectives.

## 10. Lineage links
- Builds on: Berthet et al. (2020) perturbed optimizers / Fenchel-Young losses (NeurIPS, conference); sang2022_dfpricearbitrage; baker2024_transferablebidder.
- Built upon by (notable): Xu group's decision-focused predict-then-bid framework (arXiv 2505.01551 - preprint, not archived).

## 11. Verification log
- OpenAlex autocomplete -> W4408182128; OpenAlex (doi:10.1109/TSG.2025.3548009): 16(3):2574-2586, online 2025-03-06, Columbia affiliations.
- Full text: arXiv 2406.17085.
- Group roles: bolunxu.github.io/group.
- SJR: scimagojr sid 19700170610 - Q1 2025.
