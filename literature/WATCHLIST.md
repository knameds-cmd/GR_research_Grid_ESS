# WATCHLIST — competitor and preprint tracking

Created 2026-10-07. This list is **separate from the Q1 citation archive** (`papers/`, `INDEX.md`).

- `papers/` + `INDEX.md` = evidence we cite to justify modelling choices. Q1 rule applies.
- `WATCHLIST.md` = everything that could pre-empt or overlap our contribution, **including preprints and working papers**. The Q1 rule does not apply here. Leaving preprints out would hide scooping risk.

When a watchlist item is published in a Q1 journal, create a `papers/<id>.md` entry and mark it `in archive` below.

Status codes: `in archive` = has a `papers/` file. `preprint` = not peer-reviewed yet. `check` = publication status unknown.

## 1. Direct competitors (GB battery revenue / market rules)

| # | Item | Status | Group | What it does | Overlap with our RQs | Our remaining edge |
|---|---|---|---|---|---|---|
| C1 | Gale E, Schmidt O, O'Cinneide A, Johnson N, Staffell I (2026). *Balancing with batteries: The impact of revenue stacking and skip rates on battery energy storage profitability in Great Britain.* J. Energy Storage 166:122328. doi:10.1016/j.est.2026.122328 | **in archive** (`gale2026_balancingbatteries`, abstract-level) | Imperial CEP (Staffell) | DA + BM co-optimisation, 3 yrs half-hourly data; BM adds up to +250% vs DA alone; each +10 pp skip rate = −7% profit (~£12k/MW/yr) | RQ2 skip-rate switch; wholesale+BM layer | EAC ancillary products; rule-level counterfactual + Shapley; regime comparison; estimated BM acceptance model |
| C2 | Landy M, Schmidt O, Johnson N, Staffell I (2026). *Maximising the economic value of renewable and battery storage hybrids with revenue stacking.* Energy Environ. Sci. 19(13):4469–4494. doi:10.1039/d6ee00776g | **in archive** (`landy2026_hybridstacking`, abstract-level) | Imperial CEP (Staffell) | One revenue-stacking model across UK + world regions; "profitability depends more on market access and operating constraints than on location" | Cross-country one-model comparison (professor's country framing); "rules > location" | Rule-by-rule (not bundle) attribution for stand-alone BESS; regime dependence; GB product-level detail |
| C3 | Xia Y, Schiele F, Zhou Y, Kumtepeli V, Howey D, Savelli I, Morstyn T (2026). *Lifetime Profit-Maximising Co-optimisation of Multi-Service Stacking for Battery Storage.* arXiv:2609.03767 | **preprint** (Sept 2026) | Oxford (Morstyn, Howey) + Bocconi (Savelli) | Ageing-aware receding-horizon co-optimisation of GB EAC dynamic frequency services + trading with SoE compliance rules; ageing-aware = up to +32% lifetime revenue | Layer 1–2 engine (EAC + SoE + rolling horizon) | Rules as experimental variables; BM layer; CM; attribution |
| C4 | Dalton R, O'Sullivan A (2026). *Decarbonising price formation: unit-level evidence on battery storage and the imbalance price in the GB Balancing Mechanism.* arXiv:2608.29818 | **preprint** (Aug 2026) | UCL (O'Sullivan; affiliation believed, not verified) | Reconstructs the marginal BM bid/offer stack for 50,684 SPs (2023–2025); batteries' marginal share rose to 36.2% (bid) / 26.9% (offer); "individual batteries price-takers, fleet endogenous" | Price-taker assumption (M3); BM acceptance (O4) | We study profitability and rule attribution; cite C4 to bound the price-taker assumption |
| C5 | Nosratabadi SM, Savelli I, Kumtepeli V, Grunewald P, Aunedi M, Howey DA, Morstyn T (2024). *The Impact of Grid Storage on Balancing Costs and Carbon Emissions in Great Britain.* arXiv:2410.07740 | **preprint**; journal version not found by search on 2026-10-07 | Oxford (Morstyn) + Imperial (Aunedi) | Several storage technologies in the GB BM; financially optimal balancing operation can raise emissions | BM modelling of storage (system view) | Private profitability and market-rule attribution |

## 2. Adjacent items found while checking (lower priority)

| Item | Status | Why listed |
|---|---|---|
| Casella V, La Fata A, Suzzi S, Barbero G, Barilli R (2024). *The United Kingdom electricity market mechanism: A tool for a battery energy storage system optimal dispatching.* Renewable Energy 231:120957. doi:10.1016/j.renene.2024.120957 | **in archive** (`casella2024_ukbessmilp`, abstract-level) | Q1 MILP encoding GB DA/ID/DFR/imbalance rules — closest published analogue of our Layer 1 |
| Schmidt O, Staffell I (2023). *Monetizing Energy Storage: A Toolkit to Assess Future Cost and Value.* Oxford University Press. doi:10.1093/oso/9780192888174.001.0001 | book (in `CANON.md`) | Methodological base of C1/C2 |
| Hendrickx C, Pavirani F, Develder C (2026). *Multi-market value-stacking: Battery control for combined imbalance participation and non-uniform FCR bidding.* arXiv:2605.23964 (ACM Sustainability Week 2026 companion, 5 pp.) | conference/preprint | Not GB (FCR + imbalance, Ghent group); stacking + DRL. Not a competitor; listed so it is not re-checked |

## 3. Searches still to run (next update)

- Google Scholar "cited by" for C1 and C2 once indexed.
- arXiv listings (econ.GN, eess.SY) for "Enduring Auction Capability", "Dynamic Containment", "Balancing Reserve", "Quick Reserve", "skip rate".
- Energy Policy / Applied Energy / Energy Economics 2025–2026 issues for GB battery market-design papers.
- Modo Energy, Aurora and Cornwall Insight research notes are grey literature: useful for numbers, not citable as Q1 evidence.

## 4. Verification note

All bibliographic details above came from search-engine results on 2026-10-07. Publisher sites (ScienceDirect, RSC) and arXiv were blocked in the session, so no DOI was resolved through a resolver and no full text was read. Re-check when the PDFs are downloaded (see `DOWNLOAD_LIST.md`).
