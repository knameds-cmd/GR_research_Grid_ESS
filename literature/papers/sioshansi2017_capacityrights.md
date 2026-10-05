---
id: sioshansi2017_capacityrights
title: "Using Storage-Capacity Rights to Overcome the Cost-Recovery Hurdle for Energy Storage"
authors: ["Sioshansi, R."]
year: 2017
journal: "IEEE Transactions on Power Systems"
volume_issue_pages: "32(3):2028-2040"
doi: "10.1109/TPWRS.2016.2607153"
quartile: "Q1 (SJR 2017, Electrical & Electronic Engineering; Energy Engineering & Power Technology)"
group: "Sioshansi (Ohio State ISE; now CMU)"
lineage: "Sioshansi = Oren (Berkeley) PhD 2007 (CV). Single author. Conceptual sibling of financial transmission rights (Hogan 1992) and of Munoz-Alvarez & Bitar's financial storage rights (J Regul Econ 2017)."
streams: [S7_market_design]
market_context: "Generic; motivated by FERC rulings on LEAPS (market-based) vs Western Grid (rate-based) storage"
method_class: "LP (auction clearing) + duality-based pricing"
evidence_read: "full text (author PDF https://www.cmu.edu/ceic/people/rsioshan/docs/mkt_design_storage.pdf)"
oa_link: "https://www.cmu.edu/ceic/people/rsioshan/docs/mkt_design_storage.pdf"
---

## 1. Research question
How can a storage asset recover its investment cost when its value is split between market-priced services (arbitrage, regulation) and unpriced/regulated services (transmission deferral, backup), given that US regulation forces a choice between market-based and rate-based recovery?

## 2. Setting & assumptions
- Storage owner auctions rights to use its capacity to third parties (merchants, utilities, TSOs, customers) instead of operating it.
- Perfect competition (truthful bids), perfect foresight, hourly resolution, linear charging/carrying efficiencies, rights are obligations (not options), no network.

## 3. Constraints that drove the model choice
Cost recovery fails under the "hybrid" regime because no single party can monetise both priced and unpriced value; a rights auction lets each user reveal its value. Obligation-type rights keep the clearing problem an LP whose duals give uniform clearing prices.

## 4. Model
- Rights: power-capacity charging q^c_{t,n}, discharging q^d_{t,n} (MW in hour t), energy-capacity q^e_{t,t',m} (inject at t, withdraw at t').
- Objective: max total accepted bid value sum pi^d q^d - pi^c q^c + pi^e q^e.
- Constraints: SoC balance with self-discharge eta^s and energy-capacity obligations; SoC between minimum implied by energy rights and H*R; net power within +/- R; bid quantity limits.
- Prices from duals (Props. 1-2): e.g., discharging right price = -lambda_t - (gamma^-_t - gamma^+_t); energy-capacity right price built from SoC-constraint duals between t and t'.

## 5. Data & processing
Illustrative: 1 MW battery, H = 1-4 h, eta^c = 0.8, 24-h double-peak price profile, stepped bids around a forecast; second case adds a backup-energy bidder (1.0-1.5 MW over hours 5-19 at $1000-$500/MW).

## 6. Justification
LP duality guarantees that rights prices equal marginal value of storage capacity (revenue adequacy analogous to FTRs); numerical examples demonstrate.

## 7. Key results
- Arbitrage-only: auction revenue peaks at H = 3 h ($78/day) and falls at H = 4 h; charge/discharge price spread narrows with duration ($27.5 -> $14.7).
- With backup-energy bidder: total auction revenue $538.8 vs $93.8 from direct arbitrage participation; energy-capacity right clears at $39.9/MW.
- Mechanism lets the asset be cost-recovered through market or regulated channels depending on the end user, sidestepping the market-vs-rate-base dichotomy.

## 8. Limitations (stated + critical reading)
Deterministic, hourly, no network, obligation rights only (options require stochastic extension), uncoupled charge/discharge bids may need reconfiguration auctions, scalability untested. Critical: assumes truthful bidding — strategic bidding for rights not analysed.

## 9. Relevance to my study
Formalises "who controls the SoC and who gets paid" as a design dimension distinct from product definitions. In GB, a battery under a capacity-market agreement plus DC/DM contracts is effectively selling time-sliced capacity rights to several buyers; this LP is a direct template for allocating power/energy headroom across products in a rule-switchable simulator.

## 10. Lineage links
- Builds on: Hogan 1992 (FTRs), sioshansi2010_ownership.
- Built upon by (notable): jiang2023_isodispatch (duality of ISO-dispatched storage), Munoz-Alvarez & Bitar 2017 J Regul Econ "Financial storage rights in electric power networks" (parallel line; title seen in Springer listing, not read).

## 11. Verification log
- DOI resolved via doi.org -> IEEE Xplore document 7563410; vol/issue/pages from Sioshansi CMU publication list (Vol 32, No 3, pp 2028-2040, May 2017).
- SJR: scimagojr sourceid 28825, Q1 2017.
- Full text (author accepted manuscript) read; funding NSF 1029337.
