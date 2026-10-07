---
id: ye2023_marllocalmarket
title: "Multi-Agent Deep Reinforcement Learning for Coordinated Energy Trading and Flexibility Services Provision in Local Electricity Markets"
authors: ["Ye, Y.", "Papadaskalopoulos, D.", "Yuan, Q.", "Tang, Y.", "Strbac, G."]
year: 2023
journal: "IEEE Transactions on Smart Grid"
volume_issue_pages: "14(2):1541-1554 (online 2022-02-07)"
doi: "10.1109/TSG.2022.3149266"
quartile: "Q1 (SJR 2023 and 2024/2025, Computer Science (miscellaneous); SJR 2024 = 4.608)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Goran Strbac and Dimitrios Papadaskalopoulos (Imperial College London) with Yujian Ye's group at Southeast University (Nanjing)"
lineage: "Continuation of ye2020_drlstrategicbidding: Ye (formerly Imperial, now Southeast University) + Imperial Strbac/Papadaskalopoulos. Yuan and Tang at Southeast University."
streams: [S5_rl_learning]
market_context: "Local electricity market (P2P/local trading) + flexibility services to system operators; prosumers with flexible DERs (incl. storage); stylised large-scale real-world-based case"
method_class: "RL/DRL"
evidence_read: "abstract only (OpenAlex); closed access, no OA copy located -> deep fields (from abstract)"
oa_link: ""
---

## 1. Research question
How to coordinate a local electricity market that jointly performs local energy trading and flexibility-service provision to wider system operators, comparing a model-based, system-centric optimal formulation (benchmark) with a model-free, prosumer-centric multi-agent DRL approach?

## 2. Setting & assumptions
(from abstract) Prosumers with time-coupled flexible DERs; LEM with two functions (local trading + FS provision); market outcome produced by the LEM mechanism (endogenous, multi-agent), not historical prices. Price-maker interactions among agents implied. Details not verified.

## 3. Constraints that drove the model choice
(from abstract) Model-based approaches have "practical limitations" (information/privacy, model knowledge of each prosumer); hence model-free MARL. The system-centric optimisation is retained as the "theoretical optimality benchmark".

## 4. Model
(from abstract) New system-centric optimisation for LEM coordination accounting for DER time coupling; MARL combining multi-actor-attention-critic (MAAC) with prioritized experience replay. MDP details, rewards, hyper-parameters: not verified.

## 5. Data & processing
(from abstract) "real-world, large-scale setting"; data, split and seeds not verified.

## 6. Justification (why the authors argue the approach is valid)
(from abstract) Comparison with the optimal system-centric benchmark and with previous MARL methods.

## 7. Key results
(from abstract) The LEM design captures benefits of both functions; the proposed MARL "outperforms previous methods". **Gap to the optimality benchmark not verified** (key quantity to extract from full text).

## 8. Limitations (stated + your critical reading)
- Full text not read.
- Multi-agent learning is non-stationary from each agent's view; equilibrium selection and seed dependence are central reproducibility issues for MARL-based market studies (to be checked whether the paper reports multi-seed results).

## 9. Relevance to my study
Represents the stream's market-simulator / multi-agent branch from a top group, and importantly retains an optimisation benchmark for the RL outcome - the methodological pattern to cite: if RL is used for market design questions, its outcome must be compared to a model-based optimum.

## 10. Lineage links
- Builds on: ye2020_drlstrategicbidding; Iqbal & Sha MAAC (ICML 2019, conference).
- Built upon by (notable): 122 citations per OpenAlex (Oct 2026); not reviewed.

## 11. Verification log
- OpenAlex autocomplete -> W4210939496; OpenAlex (doi:10.1109/TSG.2022.3149266): authors/affiliations (Southeast Univ.; Imperial; Decentralized Energy Solutions), 14(2):1541-1554, online 2022-02-07; no OA location.
- Abstract reconstructed from OpenAlex.
- SJR: scimagojr sid 19700170610 - Q1 2019-2025.
- UNVERIFIED: all deep fields.
