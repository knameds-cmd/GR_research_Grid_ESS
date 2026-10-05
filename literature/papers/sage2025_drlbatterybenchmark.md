---
id: sage2025_drlbatterybenchmark
title: "Deep reinforcement learning for economic battery dispatch: A comprehensive comparison of algorithms and experiment design choices"
authors: ["Sage, M.", "Zhao, Y. F."]
year: 2025
journal: "Journal of Energy Storage"
volume_issue_pages: "115:115428"
doi: "10.1016/j.est.2025.115428"
quartile: "Q1 (SJR 2025: Electrical & Electronic Eng.; Energy Eng. & Power Technology; Renewable Energy, Sustainability & Env.; SJR 2025 = 1.795)"
group: "Yaoyao Fiona Zhao (Dept. of Mechanical Engineering, McGill University)"
lineage: "McGill Zhao lab (design/manufacturing & AI). Sage = McGill doctoral researcher, corresponding author Zhao (supervision not independently verified). NOTE: not one of the renowned power-systems groups listed in the archive criteria - included because it is the only Q1 journal benchmark found that systematically studies DRL design choices / reproducibility for battery dispatch."
streams: [S5_rl_learning]
market_context: "Battery arbitrage and load-following/renewable-utilisation tasks; case studies in Canada and Germany; price-taker"
method_class: "RL/DRL"
evidence_read: "abstract + highlights (OpenAlex); full text not accessible (ScienceDirect blocked by robots, SSRN rate-limited) -> deep fields (from abstract)"
oa_link: "https://doi.org/10.1016/j.est.2025.115428 (hybrid OA, CC BY-NC-ND)"
---

## 1. Research question
Which DRL algorithms, experiment set-ups and hyper-parameters are most effective for economic battery dispatch, given contradictory results in the literature and a lack of thorough benchmarks?

## 2. Setting & assumptions
(from abstract) Two battery tasks representing the literature's cross-section: (i) arbitrage, (ii) load following with improved renewable utilisation. Case studies in Canada and Germany. Price-taker implied; data details not verified.

## 3. Constraints that drove the model choice
(from abstract) Motivated by contradictory DRL results and the absence of systematic benchmarks in battery dispatch.

## 4. Model
(from abstract) Four DRL models benchmarked (DQN named as best; the others not verified). Design factors compared: continuous vs discrete action spaces, time counters in state (incl. sine/cosine cyclic encodings), observation stacking, reward-function penalties.

## 5. Data & processing
(from abstract) Canada and Germany case studies; split, seeds and hyper-parameter search: not verified.

## 6. Justification (why the authors argue the approach is valid)
(from abstract) Comparative, factorial-style benchmark across algorithms and design choices; oracle comparison referenced in highlights.

## 7. Key results
(from abstract/highlights)
- Observation stacking reliably improves DRL performance.
- Cyclic (sin/cos) time encodings work best, especially when combining multiple counters.
- Reward penalties barely increase rewards.
- DQN outperformed the other DRL models and benefited most from the features: +51% and +20% reward on the two case studies.
- Highlight: "With the right setup: Reinforcement learning can outperform oracles" (the oracle definition is not verified - as in harrold2022_rainbowarbitrage, "beating an oracle" typically indicates an oracle that is myopic or mis-specified rather than a true perfect-foresight bound).

## 8. Limitations (stated + your critical reading)
- Full text not read: seed counts, variance and statistical tests unverified.
- The headline that design choices change rewards by 20-51% is itself the key finding for attribution: **the result of an RL study depends on implementation choices of the same order as typical market-design effects.**

## 9. Relevance to my study
Direct support for the "RL is risky for attribution" argument: a dedicated benchmark finds large sensitivity to action-space type, state encoding, stacking and algorithm choice. Should be cited when justifying an optimisation-based counterfactual design.

## 10. Lineage links
- Builds on: battery DRL literature incl. cao2020_drlarbitragedegradation, harrold2022_rainbowarbitrage (not verified which are cited).
- Built upon by (notable): 21 citations per OpenAlex (Oct 2026); not reviewed.

## 11. Verification log
- OpenAlex autocomplete -> W4407997333; OpenAlex (doi:10.1016/j.est.2025.115428): J. Energy Storage 115, art. 115428, online 2025-02-27; both authors McGill Mechanical Eng.; hybrid OA CC BY-NC-ND. SSRN preprints exist (10.2139/ssrn.4706893, 10.2139/ssrn.4829677).
- Abstract and highlights reconstructed from OpenAlex abstract_inverted_index.
- SJR: scimagojr sid 21100400826 - Q1 2024 and 2025.
- UNVERIFIED: everything beyond the abstract.
