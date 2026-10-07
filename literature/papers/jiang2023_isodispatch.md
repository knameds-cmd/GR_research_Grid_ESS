---
id: jiang2023_isodispatch
title: "What Duality Theory Tells Us About Giving Market Operators the Authority to Dispatch Energy Storage"
authors: ["Jiang, Y.", "Sioshansi, R."]
year: 2023
journal: "The Energy Journal"
volume_issue_pages: "44(3):89-110"
doi: "10.5547/01956574.44.2.yjia"
quartile: "Q1 (SJR 2024 and 2022, Economics & Econometrics; Energy (misc.)) - NOTE: SJR 2023 (publication year) = Q2"
quartile_basis: "pub-year; rule=FAIL; SJR 2023 (publication year) = Q2 in Economics & Econometrics"
group: "Sioshansi (Ohio State ISE; now CMU)"
lineage: "Jiang at OSU ISE with Sioshansi at time of writing; formal advisor tie NOT verified. Extends Hogan (1992) transmission-rent duality to intertemporal storage."
streams: [S7_market_design]
market_context: "Generic nodal (DC-OPF) market; case study ISO New England (283 buses, Aug 2005); policy context FERC LEAPS ruling / Order 841"
method_class: "LP (multi-period DC-OPF) + duality theory"
evidence_read: "full text (author PDF https://www.cmu.edu/ceic/people/rsioshan/docs/storage_opf.pdf)"
oa_link: "https://www.cmu.edu/ceic/people/rsioshan/docs/storage_opf.pdf"
---

## 1. Research question
Does letting the market operator (MO) dispatch storage inside the clearing problem (as it does for generators and transmission) threaten market independence or price formation, or does it yield efficient, incentive-compatible prices and correct long-run investment signals?

## 2. Setting & assumptions
- Price-taking agents, perfect competition, perfect foresight (deterministic), convex costs, lossless DC network, hourly multi-period horizon.
- Storage: power and energy capacity, constant round-trip efficiency, no operating/degradation cost, zero start/end SoE.

## 3. Constraints that drove the model choice
To make a general statement about MO-dispatched storage the problem must be convex so that strong duality holds; the dual then gives rents for each asset class (generators, lines, storage), mirroring Hogan's transmission argument.

## 4. Model
- Primal: max sum (willingness-to-pay - generation cost) s.t. nodal balance, generator limits, PTDF line limits, storage charge/discharge limits, SoE dynamics and bounds.
- Dual: min total rents; lambda_{n,t} = LMP, tau/phi/nu = per-unit rents on discharge, charge and energy capacity; omega_{i,t} = marginal value of stored energy.
- Lemma 1: storage rents = LMP-based net-discharge revenue. Theorem 1: if marginal rents equal marginal investment cost, a profit-maximising investor builds the socially optimal capacity.

## 5. Data & processing
- Stylised: 4 buses, 5 lines, 5 h, two generators ($4 and $8/MWh), three 5 MW/1.5 h storage units at 80% efficiency (GAMS/Gurobi via NEOS).
- ISO-NE: 283 buses, 276 generators, 31 days of Aug 2005; eight storage units in load zones, P_max and duration varied.

## 6. Justification
Duality proofs (dispatch-supporting prices, incentive compatibility, rent minimisation); numerical illustration that results hold on a realistic network; explicit mapping to transmission precedent.

## 7. Key results
- MO dispatch of storage raises no novel design issues relative to dispatching generators/lines: prices support the optimal dispatch, no agent gains by bypassing the MO, storage is paid LMP differences net of losses.
- ISO-NE: adding storage (up to ~2000 MW at 1.5 h, ~1000 MW at 3 h) raises total welfare; generator rents fall, load rents rise, congestion falls; daily morning-charge/afternoon-discharge pattern.
- Cost-recovery example (Connecticut, P_max ~1646 MW, 4.25 h): marginal rent equals marginal investment cost ($100/MWh-equivalent) at the optimum; lumpy investment can break this alignment.
- Conclusion: concerns behind FERC's denial of CAISO operational control of LEAPS are "misplaced".

## 8. Limitations (stated + critical reading)
Convexity, no degradation cost, perfect foresight, perfect competition, lossless network, no unit commitment. Critical: the practical problem in markets (MISO/CAISO SoC management, bhattacharjee2022_soemanagement) is exactly the non-convex/uncertain/strategic case this paper abstracts from; the result is a first-best benchmark, not evidence that ISO-managed SoC works under uncertainty.

## 9. Relevance to my study
Provides the theoretical yardstick for "ISO-optimised" vs "self-scheduled" participation: in a rule-switchable simulator, the ISO-dispatch case with perfect foresight is the welfare upper bound, and revenue gaps of other rule sets can be decomposed relative to it. The rent decomposition (power vs energy capacity rents) is reusable for attributing battery revenue to power- vs energy-limited constraints.

## 10. Lineage links
- Builds on: Hogan 1992 (contract networks / FTRs), sioshansi2017_capacityrights.
- Built upon by (notable): Gu & Sioshansi 2022 IEEE OAJPE (market equilibria with storage as flexibility resource); bhattacharjee2022_soemanagement.

## 11. Verification log
- SAGE article page (doi 10.5547/01956574.44.2.yjia): Vol 44, Issue 3, pp 89-110, May 2023. Note: DOI string encodes "44.2" while issue is 3; RePEc IDEAS (aen/journl/ej44-3-sioshansi) also lists vol 44 no 3; CMU list gives pp 89-109 (SAGE page used).
- SJR: scimagojr sourceid 29391; Q1 2022 and 2024, Q2 in 2023 -> flagged as borderline under the Q1 rule.
- Full text read (author PDF); funding NSF 1548015, 1808169.
