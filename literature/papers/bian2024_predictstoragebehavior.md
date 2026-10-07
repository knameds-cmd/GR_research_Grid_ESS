---
id: bian2024_predictstoragebehavior
title: "Predicting Strategic Energy Storage Behaviors"
authors: ["Bian, Y.", "Zheng, N.", "Zheng, Y.", "Xu, B.", "Shi, Y."]
year: 2024
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "15(2):1608-1619 (online 2023-08-09)"
doi: "10.1109/TSG.2023.3303469"
quartile: "Q1 (SJR 2024, Computer Science (miscellaneous); SJR 2024 = 4.608)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Yuanyuan Shi (UC San Diego ECE) and Bolun Xu (Columbia EEE)"
lineage: "UCSD Shi group x Columbia Xu group. N. Zheng = Xu PhD 2024 (verified on bolunxu.github.io/group). Bian = UCSD ECE student member, first author with Shi as senior author (advisor relation consistent, not independently verified). Shi and Xu both UW Seattle PhDs in the Kirschen/B. Zhang power-systems cluster (not independently checked here)."
streams: [S5_rl_learning]
market_context: "NYISO NYC RT prices (synthetic agents); real UQ Tesla Powerpack 1.1 MW/2.22 MWh in NEM Queensland (Jan-Jun 2020); price-taker storage"
method_class: "NLP"
evidence_read: "full text (arXiv 2306.11872)"
oa_link: "https://arxiv.org/abs/2306.11872"
---

## 1. Research question
Can the price-response behaviour (and hidden cost/constraint parameters) of a strategic storage participant be identified from observed prices and dispatch by embedding a differentiable storage-optimisation layer in an end-to-end learner, outperforming black-box ML predictors?

## 2. Setting & assumptions
- Storage agent solves min sum lambda_t (p_t - d_t) + u_theta(p, d) s.t. power, energy, SoC dynamics with efficiencies; price-taker.
- Learned: disutility u_theta (quadratic c1, c2 or ICNN), power/energy limits, efficiencies, constraint matrices.
- Synthetic agents driven by NYISO NYC 2019 RT prices (hourly, T=24); real data: UQ Powerpack, 5-min downsampled to 30-min, 40-h sequences.

## 3. Constraints that drove the model choice
Black-box ML needs many samples and ignores physical constraints; classical inverse optimisation (bilevel MIP via Gurobi) scales poorly and is fragile to noise. Differentiating through KKT conditions (quadratic case) or using sequential convex programming with an ICNN (generic case) gives a data-efficient, constraint-consistent model.

## 4. Model
- Loss: MSE between predicted optimal dispatch y* and observed dispatch y.
- Algorithm 1: gradient descent through KKT (matrix inversion), Adam lr 0.01.
- Algorithm 2: SCP with 2nd-order Taylor approximation of ICNN disutility (2 x 24 softplus), converges in < 20 SCP iterations.
- Baselines: MLP (4 x 64), LSTM-RNN (4 layers + FC), threshold rule (real data), Gurobi-based inverse optimisation.

## 5. Data & processing
- Synthetic: **10 independent runs with median and 20/80% quantile bands**; N = 20-40 training samples vs 200 for ML baselines.
- Real: 42 cleaned sequences (contingency events/manual interventions removed); 22 train / 20 test.

## 6. Justification (why the authors argue the approach is valid)
Parameter recovery on synthetic data with known ground truth; model-mismatch test (SoC-dependent cost); noise-robustness test; runtime vs Gurobi inverse optimisation; real-battery validation.

## 7. Key results
- Synthetic quadratic: test MSE 8.74e-5 (exact-structure) vs 0.018 MLP and 0.017 RNN (with 10x more data).
- SoC-dependent mismatch: generic ICNN 0.016 vs MLP/RNN 0.039.
- Real UQ battery: test MSE 0.042 (corr 0.74) vs threshold 0.070 (0.57), MLP 0.096 (0.34), RNN 0.109 (0.27).
- Gradient method 28.7 s vs Gurobi 600 s (N=1); Gurobi times out (>3600 s) at N=20; gradient method robust to N(0, 0.05) noise where optimisation approach fails.

## 8. Limitations (stated + your critical reading)
- Stated: convergence only proved for equality-constrained quadratic case; local minima; price-maker multi-unit extension and tariff design as future work; real price vs simulated price mismatch.
- Real-data sample is small (20 test sequences); one battery.

## 9. Relevance to my study
Not RL, but the most relevant "learning" alternative for market-rule attribution: identify an optimisation-consistent behaviour model of storage from data, then re-solve it under counterfactual rules. Authors explicitly frame it for market monitoring and tariff/market design.

## 10. Lineage links
- Builds on: Amos & Kolter OptNet (ICML 2017, conference); Amos et al. ICNN; inverse optimisation of generator offers.
- Built upon by (notable): yi2025_perturbeddfl (perturbed DFL for strategic storage).

## 11. Verification log
- OpenAlex autocomplete -> W4385695890; OpenAlex (doi:10.1109/TSG.2023.3303469): 15(2):1608-1619, online 2023-08-09; UCSD/Columbia affiliations; arXiv 2306.11872 listed as OA location (read in full). A PESGM 2024 derivative exists (conference, excluded).
- SJR: scimagojr sid 19700170610 - Q1 2019-2025.
