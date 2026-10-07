---
id: linn2019_storagecostemissions
title: "Do lower electricity storage costs reduce greenhouse gas emissions?"
authors: ["Linn, J.", "Shih, J.-S."]
year: 2019
journal: "Journal of Environmental Economics and Management"
volume_issue_pages: "96:130-158"
doi: "10.1016/j.jeem.2019.05.003"
quartile: "Q1 (SJR 2019, Economics and Econometrics; Management, Monitoring, Policy and Law)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Resources for the Future (Linn, Shih) — RFF electricity modelling group"
lineage: "Not verified."
streams: [S8_empirical_econ]
market_context: "ERCOT, 2030 counterfactual calibrated to 2004-2008 hourly data; generic storage cost scenarios"
method_class: "econometric (reduced-form wind investment elasticity) + NLP equilibrium simulation (GAMS)"
evidence_read: "full text (RFF working-paper version, 2017 https://sites.ualberta.ca/~ipe/IPE/PDF/JoshLinn.pdf)"
oa_link: "https://sites.ualberta.ca/~ipe/IPE/PDF/JoshLinn.pdf"
---

## 1. Research question
In the medium run (10-20 years), do falling storage costs reduce CO2 once fossil fuel switching AND endogenous renewable investment responses are accounted for?

## 2. Setting & assumptions
- Competitive equilibrium (cost minimisation) with endogenous hourly storage charge/discharge; 28 representative days (first week of each quarter).
- Coal/gas supply from heat rates and capacities; nuclear and fossil capacity exogenous; no ramping constraints.
- Wind investment responds to prices with an econometrically estimated elasticity; solar fixed in baseline.

## 3. Constraints that drove the model choice
Short-run studies (carson2013) ignore that storage raises the value of variable renewables; the sign of the emissions effect depends on fossil vs renewable supply responsiveness -> a stylised analytical model plus a calibrated equilibrium simulation with an estimated renewable-investment response.

## 4. Model
- Stylised two-period model: sign of d(Emissions)/d(storage cost) depends on supply elasticities of fossil and wind.
- Simulation: NLP, min total generation cost s.t. hourly balance, storage SoC dynamics, capacity limits; wind capacity from estimated investment equation.
- Reduced-form panel (1996-2015, regional annual): MW wind investment on fuel prices, demand, PTC availability.

## 5. Data & processing
ERCOT hourly load/wind 2004-2008; unit heat rates/capacities; fuel prices; regional wind investment panel; validation vs 2004/2008/2010 outcomes.

## 6. Justification
Model validated against observed generation shares/prices; sensitivity to wind and solar investment elasticities, fuel-price forecasts, carbon price.

## 7. Key results
- Without renewable response: halving storage cost ($280 -> $140/kWh) raises CO2 ~2% (coal charging, gas displaced).
- With endogenous wind: increase mitigated; with high wind price-responsiveness, lower storage cost can reduce emissions.
- A $30/tCO2 carbon price makes emission reductions from cheaper storage more likely.

## 8. Limitations (stated + critical reading)
- ERCOT-specific, coal-heavy merit order (now largely outdated); no ramping; exogenous fossil capacity; representative days limit storage cycling realism; competitive storage (no market power).

## 9. Relevance to my study
Structural complement to carson2013 and butters2025: shows that storage's market impact depends on which supply margins respond. For GB, the relevant margins are gas CCGT/OCGT, interconnectors and wind curtailment in the BM — an argument for including BM constraint actions when evaluating battery market impact.

## 10. Lineage links
- Builds on: carson2013_bulkstorageexternality (short-run emissions effect of storage).
- Built upon by: not checked.

## 11. Verification log
- RePEc IDEAS: JEEM 96:130-158 (2019), DOI 10.1016/j.jeem.2019.05.003.
- SJR JEEM: Q1 2019.
- Full text: 2017 RFF WP version (numbers may differ from published).
- Borderline for S8 (mostly simulation); included as the structural/equilibrium-emissions node.
