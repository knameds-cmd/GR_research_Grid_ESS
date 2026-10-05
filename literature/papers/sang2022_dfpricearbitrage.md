---
id: sang2022_dfpricearbitrage
title: "Electricity Price Prediction for Energy Storage System Arbitrage: A Decision-Focused Approach"
authors: ["Sang, L.", "Xu, Y.", "Long, H.", "Hu, Q.", "Sun, H."]
year: 2022
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "13(4):2822-2832"
doi: "10.1109/TSG.2022.3166791"
quartile: "Q1 (SJR 2022 and 2024/2025, Computer Science (miscellaneous); SJR 2024 = 4.608)"
group: "Yinliang Xu (Tsinghua-Berkeley Shenzhen Institute / Tsinghua SIGS), with Hongbin Sun (Tsinghua EE, State Key Lab of Power Systems) and Qinran Hu (Southeast Univ.)"
lineage: "Tsinghua power-systems lineage (Hongbin Sun). Sang first-authored under corresponding author Y. Xu at Tsinghua SIGS (advisor relation plausible, not independently verified)."
streams: [S5_rl_learning]
market_context: "PJM day-ahead hourly prices, price-taker ESS arbitrage"
method_class: "MILP"
evidence_read: "full text (arXiv 2305.00362, accepted version)"
oa_link: "https://arxiv.org/abs/2305.00362"
---

## 1. Research question
Instead of training a day-ahead price forecaster for accuracy (MSE), can it be trained for the downstream ESS arbitrage decision (regret), and how much arbitrage profit does that recover?

## 2. Setting & assumptions
- Price-taker; day-ahead deterministic arbitrage MILP solved on predicted prices; evaluated on realised prices (no real-time recourse).
- Hourly, 24-h horizon, daily one-shot.
- ESS 500 kWh (normalised to 1 MWh), 250 kW charge/discharge, eta_ch 0.90, eta_dis 0.92, E in [0.2, 0.95] of capacity; no degradation cost.
- No market simulation; exogenous historical PJM prices.

## 3. Constraints that drove the model choice
Regret is piecewise constant/discontinuous in the predicted price (argmin of a MILP), so it has no useful gradient. Authors relax the feasible region to derive a tractable surrogate upper bound of regret with an explicit gradient, and combine it with MSE to stabilise training.

## 4. Model
- Loss: L = L_regret_surrogate + eps * L_MSE (eps = 25 best).
- Explicit surrogate gradient (Lemma 1): dL_regret/d lambda_hat = -2(P*(lambda) + P*(lambda - 2 lambda_hat)), requiring two MILP solves per sample per step; MSE gradient by autograd; combined in one SGD step ("hybrid SGD").
- Predictors: linear regression and a ResNet-style MLP ([50,50], dropout 0.2, Adam lr 1e-6, batch 100, 50 epochs); target = log price.
- Downstream: standard ESS arbitrage MILP (charge/discharge binaries, SoC balance, limits).

## 5. Data & processing
- PJM, six years of hourly data; features: previous-day load, temperature, temperature^2, forecast temperature, calendar/holiday flags.
- Split 60/20/20 train/validation/test; **whether the split is chronological is not clearly stated** in the arXiv text (treat as unclear).

## 6. Justification (why the authors argue the approach is valid)
Compares the same architecture trained on MSE only vs decision-focused loss, plus MLP and Random Forest predictors, and an oracle (perfect-information) arbitrage benchmark; sensitivity to eps.

## 7. Key results
- Test regret 0.952 (DFP) vs 10.470 (same model MSE-trained), 1.595 (MLP), 1.433 (RF); daily benefit 29.86 USD vs 20.33/28.14/28.94.
- **Oracle daily benefit 30.712 USD -> DFP attains about 97.3% of the perfect-foresight bound.**
- DFP has slightly worse RMSE/MAPE than the MSE-trained model but much lower regret - illustrating decision error != prediction error.

## 8. Limitations (stated + your critical reading)
- No degradation, no real-time stage, price-taker, MILP inside the training loop (compute not quantified).
- Linear-model experiments averaged over 100 runs, but **ResNet results are single-run; no confidence intervals or significance tests**.
- 97% of oracle in a smooth PJM DA setting with 2-h duration battery is an easy regime; transfer to spiky/real-time markets untested.

## 9. Relevance to my study
Key reference for the "predict-then-optimise vs decision-focused vs RL" spectrum: keeps the optimisation model explicit (attributable to market rules), while learning only the forecast. A natural middle-ground if pure optimisation baselines are criticised for using naive forecasts.

## 10. Lineage links
- Builds on: Elmachtoub & Grigas "Smart predict-then-optimize" (Management Science 2022); Donti, Amos & Kolter task-based learning (NeurIPS 2017, conference).
- Built upon by (notable): yi2025_dfpredictthenbid (Bolun Xu group, strategic storage); decision-focused forecasting for storage in later TSG/TPWRS work.

## 11. Verification log
- OpenAlex (doi:10.1109/TSG.2022.3166791): title, author order, 13(4):2822-2832, online 2022-04-12.
- Full text: arXiv 2305.00362 (TSG manuscript number TSG-01664-2021).
- SJR: scimagojr sid 19700170610 - Q1 2019-2025.
- Note: Some RMSE values in the arXiv table appear inconsistent across columns (scaling); only regret/benefit figures are relied on here.
