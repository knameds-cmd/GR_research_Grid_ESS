---
id: sioshansi2014_welfareloss
title: "When energy storage reduces social welfare"
authors: ["Sioshansi, R."]
year: 2014
journal: "Energy Economics"
volume_issue_pages: "41:106-116"
doi: "10.1016/j.eneco.2013.09.027"
quartile: "Q1 (SJR 2014 and 2023-2025, Economics & Econometrics; Energy (misc.))"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Ramteen Sioshansi — The Ohio State University"
lineage: "Generalises sioshansi2010_ownership to elastic demand and strategic (Cournot) generation."
streams: [S1_foundations_value, S7_market_design]
market_context: "stylised two-period wholesale market (no specific ISO); competitive vs Nash-Cournot generation"
method_class: "analytical game theory (Nash-Cournot equilibrium, lemmas/corollaries)"
evidence_read: "full text (preprint submitted to Energy Economics, Nov 2013, https://www.cmu.edu/ceic/people/rsioshan/docs/sto_mkt_power.pdf)"
oa_link: "https://www.cmu.edu/ceic/people/rsioshan/docs/sto_mkt_power.pdf"
---

## 1. Research question
Under which market structures (competitive vs strategic generation; standalone vs generator-owned storage; competitive vs strategic storage) can storage use reduce social welfare relative to having no storage?

## 2. Setting & assumptions
- Two periods (off-peak, on-peak); linear demand D_t(p_t) = N_t − γ_t p_t; quadratic aggregate generation cost c(g) = b g + ½ c g² (per firm ĉ(g) = b g + ½ G c g² for G symmetric firms).
- Storage: round-trip efficiency ε ∈ (0,1), power cap δ̄; charges off-peak, discharges on-peak only; no multi-period energy constraint.
- Perfect information; Nash-Cournot for strategic agents.

## 3. Constraints that drove the model choice
The goal is a sign result (can ΔW < 0?) requiring closed-form equilibria → minimal two-period linear–quadratic model.

## 4. Model
- Welfare W(δ) = CW(δ) + PW(δ) + Π_S(δ).
- Lemma 1: competitive generation + competitive standalone storage → unique global welfare maximiser.
- Corollary 2: with competitive generation, standalone storage never yields a net welfare loss.
- Lemma 3: with strategic generators, storage use can reduce welfare.
- Lemma 6: generator-owned storage with competitive generation but strategic storage → loss only for a monopolist (G = 1).
- Lemma 7: when generators strategically choose both generation and storage, storage can reduce welfare for any number of firms.
- Solution: first-order conditions of each agent's problem; numerical illustration.

## 5. Data & processing
Stylised parameters only (no market data set).

## 6. Justification (why the authors argue the approach is valid)
Proofs hold under stated functional forms; counter-intuitive result (adding a participant reduces welfare) is shown to be driven by interaction with existing generator market power.

## 7. Key results
- Storage is welfare-improving under perfect competition, but with Cournot generators its price-smoothing can raise off-peak and alter on-peak markups such that total welfare falls.
- "Perfectly competitive storage" can deliver larger welfare losses than strategic storage when generators are strategic (strategic storage partially internalises the externality).
- Generator-owned storage in concentrated markets warrants scrutiny.

## 8. Limitations (stated + your critical reading)
- Stated: stylised two-period framework; competitive-generation/strategic-storage case may be unrealistic; investment incentives left for future work.
- Critical: no network, uncertainty or multi-product markets; quadratic costs miss merit-order steps; results are possibility (existence) results, not magnitudes.

## 9. Relevance to my study
Theoretical warning that battery **profits** and **social value** can diverge in concentrated markets; relevant when interpreting profitability differences across markets with different concentration/mitigation rules (e.g., GB vs Nordic).

## 10. Lineage links
- Builds on: sioshansi2010_ownership; sioshansi2009_pjmvalue.
- Built upon by (notable): storage market-power papers (e.g., EJOR/Energy Policy strategic-storage literature; see S7 stream).

## 11. Verification log
- OpenAlex (doi:10.1016/j.eneco.2013.09.027): single author Sioshansi (OSU), Energy Economics 41:106–116 ✔; IDEAS handle v41y2014 confirms 2014 volume year ✔.
- Crossref direct call rate-limited (HTTP 429) — fields cross-checked via OpenAlex + RePEc only.
- SJR Energy Economics Q1 2014 ✔.
- Full text: preprint version (Nov 2013); final published wording not checked.
