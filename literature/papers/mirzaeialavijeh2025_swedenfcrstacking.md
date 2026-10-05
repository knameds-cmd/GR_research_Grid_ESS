---
id: mirzaeialavijeh2025_swedenfcrstacking
title: "Profit benchmarking and degradation analysis for revenue stacking of batteries in Sweden's day-ahead electricity and frequency containment reserve markets"
authors: ["Mirzaei Alavijeh, N.", "Khezri, R.", "Mazidi, M.", "Steen, D.", "Le, A. T."]
year: 2025
journal: "Applied Energy"
volume_issue_pages: "381:125151"
doi: "10.1016/j.apenergy.2024.125151"
quartile: "Q1 (SJR 2025, Energy (misc.); Renewable Energy, Sustainability and the Environment; Mechanical Engineering)"
group: "Div. of Electric Power Engineering, Chalmers University of Technology (D. Steen, Le Anh Tuan)"
lineage: "Chalmers Electric Power Engineering group (Steen, Le Anh Tuan as senior authors). Mirzaei Alavijeh's Chalmers record also lists 'Flexibility from local resources: Congestion management..., and frequency containment reserves' (likely his thesis). The advisor tie was not verified."
streams: [S2_stacking_cooptimization, S4_degradation_operation, S6_ancillary_products]
market_context: "Sweden SE3: Nord Pool day-ahead + FCR-N, FCR-D up, FCR-D down (D-1 auctions, pay-as-clear), 2022"
method_class: "MILP"
evidence_read: "full text (Chalmers accepted/published version, https://research.chalmers.se/publication/544875/file/544875_Fulltext.pdf)"
oa_link: "https://research.chalmers.se/en/publication/544875"
---

## 1. Research question
What is the upper-bound annual profit of a BESS that stacks Nordic day-ahead energy with the three Swedish FCR products? How much extra degradation does stacking cause, and can degradation-aware operation reduce it?

## 2. Setting & assumptions
- **Oracle / perfect foresight.** Historical 2022 prices (DA, FCR capacity, regulation) and 1-min frequency are known. The authors say explicitly that it is "not a bidding algorithm".
- Successive daily MILPs over all 365 days. Hourly market decisions; physical simulation at 1 min (1440 steps per day).
- Asset: 1 MW / 1 MWh NMC battery, η = 93% each way, SoE window 10–90%, EOL at 80% capacity, replacement cost €137k.
- Market rules:
  - FCR-N: symmetric, capacity plus energy payment, 1 h endurance.
  - FCR-D up and FCR-D down: capacity only, 20 min endurance each.
  - Minimum bid sizes; ENTSO-E LER/endurance requirements.

## 3. Constraints that drove the model choice
- Minimum bid sizes, charge/discharge exclusivity and participation gates need binaries, hence a MILP.
- Hourly bids need minute-level SoE tracking to capture activation energy.
- The nonlinear calendar and cycle ageing models are piecewise-linearised (Appendix A) so the problem stays a MILP.

## 4. Model
- Objective: max $F = R_{DA} + R_{FCR} - C_{DA} - C_{DEG}$. $C_{DEG}$ is calendar plus cycle ageing, monetised through the battery NPV.
- Decisions: hourly DA baseline $p^{bl}_h$ (charge/discharge), hourly FCR capacities $p^{\Theta,N}_h, p^{\Theta,DU}_h, p^{\Theta,DD}_h$, and 1-min power $p_t$.
- **Capacity split: dynamic, hourly.** Each hour can switch between FCR-N, FCR-D up/down and DA arbitrage. Power headroom around the baseline is shared through rule-derived coefficients. As read in the text, these are of the form $1.34p^{N}+p^{DU}+0.2p^{DD}\le \bar P + p^{bl}$, with the symmetric counterpart for downward headroom. The coefficients encode product overlap in the droop/activation bands.
- **Frequency-signal energy: historical replay.** 1-min Fingrid/Nordic frequency is passed through product droop curves (FCR-N ±0.1 Hz band; FCR-D 49.5–49.9 / 50.1–50.5 Hz) to give per-minute activation energy.
- **Endurance / SoE rule:** worst-case checkpoint constraints. The SoE must stay within limits after simultaneous FCR-N plus FCR-D activation for 20 min, and after a further 40 min of FCR-N, in both directions. This is an explicit encoding of energy-reservation (LER) rules.
- Solver: commercial MILP (solver not named in the text as read).

## 5. Data & processing
- Sources: ENTSO-E Transparency (SE3 DA prices), eSett (regulation prices), SVK/Mimer (FCR prices and rules), Fingrid (1-min frequency), all for 2022.
- Ageing parameters from a published NMC cycling study.
- No train/test split: this is an ex-post benchmark.

## 6. Justification (why the authors argue the approach is valid)
The result is positioned as a profit benchmark (upper bound) for evaluating bidding algorithms. Five modes are compared: DA only, DA+FCR-N, DA+FCR-DU, DA+FCR-DD, and Multi. The model is also run with and without degradation in the objective.

## 7. Key results
- Multi-market stacking: about €708k per year for 1 MW/1 MWh, roughly 22 times DA-only profit (2022 was an extreme price year).
- Dominant strategy: simultaneous FCR-D up plus down, switching hourly to FCR-N when SoE allows.
- Capacity loss: 1.7% per year (Multi) versus 3.0% (FCR-N only). Putting degradation in the objective cuts ageing cost by 5–29% while lowering profit by only 0–3.6%. The abstract reports annual loss falling from 1.7% to 1.2%.

## 8. Limitations (stated + your critical reading)
- Stated: perfect foresight; single year (2022); fixed 1 h sizing; no SoC exceptions; droop simplified; temperature fixed at 20 °C.
- Critical reading:
  - FCR capacity prices in 2022 were exceptionally high, and FCR-D saturation since then means the profit level does not generalise.
  - There is no bid-acceptance risk and no price impact.
  - LER is modelled as a deterministic worst case. This is the right way to encode the rule, but it is not compared with alternative SoE-management rules.

## 9. Relevance to my study
This is directly reusable as a template for encoding product rules (endurance, power-headroom overlap coefficients, SoE checkpoints) in a MILP with frequency replay. It is a good benchmark structure for asking how much each rule costs. One option is to re-run with endurance relaxed or tightened, or with stacking of FCR-D up and down forbidden.

## 10. Lineage links
- Builds on: Nordic FCR battery studies and an NMC ageing model from the literature (reference list not itemised). Related: engels2020_fcrpeakshaving (FCR SoE feasibility, chance-constrained alternative).
- Built upon by (notable): too recent to say.

## 11. Verification log
- Chalmers research portal (research.chalmers.se/en/publication/544875): title, authors, Applied Energy 381, article 125151, 2025, DOI. Confirmed.
- Full text PDF read through the portal. Equations above are transcribed through a text-extraction tool. The 1.34/0.2 coefficients should be checked against the PDF before reuse.
- SJR (scimagojr.com, id 28801): Applied Energy Q1 2025.
- Crossref direct lookup not done (rate-limited); the DOI is consistent with the Elsevier pattern and the portal.
