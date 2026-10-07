# CANON — textbooks, landmark reviews and convention-setting articles

Compiled 2026-10-06. Each anchor gives a full citation, what it standardised, and the **modelling convention** it set (bold). Use the convention tag in `papers/*.md → method_class` to trace a paper's formulation back to its anchor.

**How metadata was checked**
- **[✓OA]** means the DOI was resolved with `api.openalex.org/works/doi:<DOI>` on 2026-10-06, and the title, authors and venue matched.
- **[DOI unverified]** means rate limits blocked the lookup. The citation is given from standard publisher data and should be re-checked before formal use.
- **Years** are the print or issue year. OpenAlex sometimes reports the online-first year.
- **Quartile** was not re-checked in this pass, because SJR and JCR were unreachable.

---

## A. Textbooks and monographs

### A1. Market foundations and design

1. **Schweppe, F.C., Caramanis, M.C., Tabors, R.D., Bohn, R.E. (1988).** *Spot Pricing of Electricity.* Kluwer / Springer. doi:10.1007/978-1-4613-1683-1 [✓OA]
   - The theoretical origin of time- and location-varying marginal-cost pricing.
   - It set out how spot prices act as the coordination signal for generation, demand and network.
   - **Convention:** nodal (LMP-type) spot prices, with prices treated as exogenous signals that flexible resources respond to. This is the logic behind the "price-taker storage" assumption.

2. **Hogan, W.W. (1992).** Contract networks for electric power transmission. *Journal of Regulatory Economics* 4(3):211–242. doi:10.1007/BF00133621 [✓OA]
   - The design paper for LMP plus financial transmission rights (FTRs) as practised in PJM, NYISO and ISO-NE.
   - **Convention:** security-constrained, bid-based LMP markets with financial rights for congestion hedging.
   - A companion piece is Hogan (2013), *Economics of Energy & Environmental Policy* 2(2), doi:10.5547/2160-5890.2.2.4 [✓OA]. It is the operating-reserve demand curve (ORDC) and scarcity-pricing reference behind ERCOT's ORDC, and the reason the reserve-price adder enters storage revenue models.

3. **Stoft, S. (2002).** *Power System Economics: Designing Markets for Electricity.* IEEE Press / Wiley-Interscience. ISBN 978-0-471-15040-4. [DOI unverified — rate-limited]
   - The engineer-economist's design manual: the reliability externality, price caps, the "missing money" problem, capacity mechanisms and market power.
   - **Convention:** the energy-only vs. capacity-market framing and the screening-curve logic for long-run equilibrium. Storage revenue-adequacy arguments (scarcity rents) usually start here.

4. **Kirschen, D.S., Strbac, G. (2004; 2nd ed. 2019).** *Fundamentals of Power System Economics.* Wiley. 1st ed. doi:10.1002/0470020598 [✓OA]. 2nd ed. 2019 [DOI unverified].
   - The standard teaching text: market structures, bilateral vs. pool trading, merit-order dispatch, ancillary services and network pricing.
   - **Convention:** merit-order/economic-dispatch LP and the producer's profit-maximisation viewpoint used in most storage-arbitrage introductions.

5. **Shahidehpour, M., Yamin, H., Li, Z. (2002).** *Market Operations in Electric Power Systems: Forecasting, Scheduling, and Risk Management.* Wiley-IEEE. [DOI 10.1002/047122412X — lookup rate-limited, unverified]
   - Popularised price-based unit commitment (PBUC) and the generation company (GENCO) bidding viewpoint, alongside the ISO's security-constrained unit commitment (SCUC).
   - **Convention:** the self-scheduling MILP of a price-taking GENCO. Storage self-scheduling models inherit its structure.

6. **Biggar, D.R., Hesamzadeh, M.R. (2014).** *The Economics of Electricity Markets.* Wiley(-IEEE). doi:10.1002/9781118775745 [✓OA; OpenAlex lists no authors — check]
   - Economics-first treatment of nodal pricing, hedging, market power and the role of storage as an intertemporal arbitrageur.
   - **Convention:** welfare-maximising dispatch with storage as intertemporal trade.

6a. **Schmidt, O., Staffell, I. (2023).** *Monetizing Energy Storage: A Toolkit to Assess Future Cost and Value.* Oxford University Press. doi:10.1093/oso/9780192888174.001.0001 [added 2026-10-07; DOI from OUP/doi.org search results, not resolved via OpenAlex]
   - Imperial CEP toolkit: experience-curve investment cost, LCOS, market value of storage services ("Market value: Making money"), system value, with the companion tool EnergyStorage.ninja.
   - Likely methodological base (not verified — full texts not read) of the 2026 Imperial GB papers (gale2026_balancingbatteries, landy2026_hybridstacking; see `WATCHLIST.md`).
   - **Convention:** cost side (experience rates, LCOS) and value side (revenue stacking) assessed with one transparent, reproducible toolkit — the Staffell-line template for GB storage economics.

### A2. Decision-making under uncertainty for market agents

7. **Conejo, A.J., Carrión, M., Morales, J.M. (2010).** *Decision Making Under Uncertainty in Electricity Markets.* Springer, Int. Series in OR & MS vol. 153. doi:10.1007/978-1-4419-7421-1 [✓OA]
   - The template for producer, retailer and consumer trading problems: scenario trees, two- and multi-stage SP, non-anticipativity, scenario reduction.
   - Risk is handled with CVaR in the objective, giving an efficient frontier of expected profit vs. CVaR.
   - **Convention:** "two-stage SP with scenarios + CVaR (β-weighted)" (the CVaR linearisation is due to Rockafellar–Uryasev). It is also the canonical stepwise offer-curve construction from scenario-dependent quantities with non-decreasing constraints.

8. **Gabriel, S.A., Conejo, A.J., Fuller, J.D., Hobbs, B.F., Ruiz, C. (2013).** *Complementarity Modeling in Energy Markets.* Springer ISOR vol. 180. doi:10.1007/978-1-4419-6123-5 [✓OA; OpenAlex year 2012]
   - Standardised the MCP/LCP, MPEC, EPEC and bilevel toolbox for strategic agents.
   - It covers KKT reformulation with big-M or SOS1, strong duality linearisation, and Nash–Cournot equilibria.
   - **Convention:** "price-maker storage as an MPEC (upper level = storage profit, lower level = market clearing)". Pair it with Pineda & Morales (2019, TPWRS) for the big-M caveat.

9. **Morales, J.M., Conejo, A.J., Madsen, H., Pinson, P., Zugno, M. (2014).** *Integrating Renewables in Electricity Markets: Operational Problems.* Springer ISOR vol. 205. doi:10.1007/978-1-4614-9411-9 [✓OA; OpenAlex year 2013]
   - Covers probabilistic forecasts as inputs, renewable trading under dual-price imbalance settlement, stochastic market clearing and balancing-market design.
   - **Convention:** the "newsvendor/quantile bid from a predictive distribution" for imbalance-exposed agents, and scenario-based stochastic clearing as the welfare benchmark for sequential markets.

10. **Conejo, A.J., Baringo, L., Kazempour, S.J., Siddiqui, A.S. (2016).** *Investment in Electricity Generation and Transmission: Decision Making under Uncertainty.* Springer. doi:10.1007/978-3-319-29501-5 [✓OA]
    - **Convention:** bilevel and stochastic or robust investment models. This is the template for strategic storage *sizing*, e.g., Nasrolahpour et al. 2016.

11. **Baringo, L., Rahimiyan, M. (2020).** *Virtual Power Plants and Electricity Markets: Decision Making Under Uncertainty.* Springer. doi:10.1007/978-3-030-47602-1 [✓OA]
    - Covers DA, RT and futures scheduling of virtual power plants (VPPs) with storage, using SP, RO and ARO side by side.
    - **Convention:** VPP/aggregator self-scheduling, with storage as a VPP component and SP vs. RO compared on the same case.

### A3. Optimisation, dynamic programming and RL foundations

12. **Sioshansi, R., Conejo, A.J. (2017).** *Optimization in Engineering: Models and Algorithms.* Springer Optimization and Its Applications vol. 120. doi:10.1007/978-3-319-56769-3 [✓OA]
    - A modelling-first OR text whose running examples are energy problems (LP, MILP, NLP, DP).
    - **Convention:** the energy-storage LP/DP formulation (SoC balance, charge/discharge efficiencies, binaries for mutual exclusivity) as taught to engineers.

13. **Birge, J.R., Louveaux, F. (2011, 2nd ed.).** *Introduction to Stochastic Programming.* Springer Series in OR & FE. doi:10.1007/978-1-4614-0237-4 [✓OA]
    - **Convention:** recourse models, value of the stochastic solution (VSS) and expected value of perfect information (EVPI), and L-shaped/Benders decomposition. VSS/EVPI are the standard metrics for reporting the "value of stochastic bidding" for storage.

14. **Ben-Tal, A., El Ghaoui, L., Nemirovski, A. (2009).** *Robust Optimization.* Princeton University Press. doi:10.1515/9781400831050 [✓OA]
    - **Convention:** uncertainty sets and tractable robust counterparts. The basis for robust offering (Baringo & Conejo 2011) and adaptive RO (Bertsimas et al. 2013).

15. **Powell, W.B. (2011, 2nd ed.).** *Approximate Dynamic Programming: Solving the Curses of Dimensionality.* Wiley. doi:10.1002/9781118029176 [✓OA]
    - **Convention:** post-decision states and value-function approximation (VFA). Storage is a recurring example; this is the framework behind Jiang & Powell (2015) and Salas & Powell (2018).

16. **Powell, W.B. (2022).** *Reinforcement Learning and Stochastic Optimization: A Unified Framework for Sequential Decisions.* Wiley. doi:10.1002/9781119815068 [✓OA]
    - Set the "four classes of policies" taxonomy: policy function approximation (PFA), cost function approximation (CFA), VFA, and direct lookahead (DLA).
    - **Convention:** benchmark any DRL storage bidder against a parametric CFA (e.g., deterministic lookahead with tuned buffers) and a DLA. This is the vocabulary to use when positioning a DRL storage bidder against MPC and SP.

17. **Sutton, R.S., Barto, A.G. (2018, 2nd ed.).** *Reinforcement Learning: An Introduction.* MIT Press. [No DOI; not checked via OpenAlex]
    - **Convention:** MDP notation, TD learning and policy-gradient basics, as cited by DRL-bidding papers.

---

## B. Landmark reviews

18. **Sioshansi, R., Denholm, P., Arteaga, J., Awara, S., Bhattacharjee, S., Botterud, A., et al. (2022).** Energy-storage modeling: State-of-the-art and future research directions. *IEEE Trans. Power Systems* 37(2):860–875. doi:10.1109/TPWRS.2021.3104768 [✓OA]
    - Written by a 23-author team (OSU, NREL, MIT, UW/NYU, Zagreb, Calgary, Imperial and others).
    - Catalogues how storage is represented in production-cost, capacity-expansion and market models: chronology, SoC coupling, representative days, degradation, and storage bidding/offer formats in ISO markets.
    - **Convention:** the reference checklist of storage-modelling simplifications, and the source for the "SoC-aware offer / state-of-charge management in market clearing" agenda.

19. **Collath, N., Tepe, B., Englberger, S., Jossen, A., Hesse, H.C. (2022).** Aging aware operation of lithium-ion battery energy storage systems: A review. *J. Energy Storage* 55:105634. doi:10.1016/j.est.2022.105634 [✓OA]
    - Classifies how aging is embedded in operation: throughput or energy cost, cycle-depth (rainflow) cost, semi-empirical calendar + cycle models, and physics-based models. It also covers where the cost of degradation enters (objective vs. constraint).
    - **Convention:** the taxonomy for degradation modelling in dispatch. Cite it when justifying the choice of a degradation term in a DRL reward.

20. **Weitzel, T., Glock, C.H. (2018).** Energy management for stationary electric energy storage systems: A systematic literature review. *European J. Operational Research* 264(2):582–606. doi:10.1016/j.ejor.2017.06.052 [✓OA]
    - An OR-side taxonomy of storage energy-management problems: application, decision level, uncertainty treatment and solution method.
    - **Convention:** the classification scheme for method_class across the storage-scheduling literature.

21. **Zakeri, B., Syri, S. (2015).** Electrical energy storage systems: A comparative life cycle cost analysis. *Renewable & Sustainable Energy Reviews* 42:569–596. doi:10.1016/j.rser.2014.10.011 [✓OA]
    - **Convention:** the life-cycle-cost / levelised-cost comparison across storage technologies and applications. Widely used as a source of cost parameters.

22. **Dunn, B., Kamath, H., Tarascon, J.-M. (2011).** Electrical energy storage for the grid: A battery of choices. *Science* 334(6058):928–935. doi:10.1126/science.1212741 [✓OA]
    - **Convention:** the technology landscape (Li-ion, flow, NaS, etc.) and the grid-service framing ("power vs. energy applications"). It is the standard opening citation for grid batteries.

23. **Luo, X., Wang, J., Dooner, M., Clarke, J.C. (2015).** Overview of current development in electrical energy storage technologies and the application potential in power system operation. *Applied Energy* 137:511–536. doi:10.1016/j.apenergy.2014.09.081 [✓OA]
    - **Convention:** a technology-parameter table (efficiency, lifetime, power/energy density, cost) reused as default inputs.

24. **Chen, X., Qu, G., Tang, Y., Low, S.H., Li, N. (2022).** Reinforcement learning for selective key applications in power systems: Recent advances and future challenges. *IEEE Trans. Smart Grid* 13(4):2935–2958. doi:10.1109/TSG.2022.3154718 [✓OA]
    - Covers frequency regulation, voltage control and energy management. It stresses safety, stability guarantees, sample efficiency and the gap between simulators and real systems.
    - **Convention:** the critical-RL review, used for "limitations of DRL" sections and the safety/certification argument. This matches the researcher's "certifiable" agenda.

25. **Zhang, Z., Zhang, D., Qiu, R.C. (2020).** Deep reinforcement learning for power system: An overview. *CSEE J. Power and Energy Systems* 6(1):213–225. doi:10.17775/CSEEJPES.2019.00920 [✓OA]
    - **Convention:** the DRL algorithm taxonomy (DQN, DDPG, A3C, PPO…) mapped to power-system tasks, including bidding.

26. **Perera, A.T.D., Kamalaruban, P. (2021).** Applications of reinforcement learning in energy systems. *Renewable & Sustainable Energy Reviews* 137:110618. doi:10.1016/j.rser.2020.110618 [✓OA]
    - **Convention:** a broad RL-in-energy survey, useful for counting how often model-free RL is benchmarked against MPC or optimisation (rarely).

27. **Weron, R. (2014).** Electricity price forecasting: A review of the state-of-the-art with a look into the future. *Int. J. Forecasting* 30(4):1030–1081. doi:10.1016/j.ijforecast.2014.08.008 [✓OA]
    - **Convention:** the electricity price forecasting (EPF) model taxonomy (multi-agent, fundamental, reduced-form, statistical, computational-intelligence models). It is the price-input side of any storage bidder.

28. **Lago, J., Marcjasz, G., De Schutter, B., Weron, R. (2021).** Forecasting day-ahead electricity prices: A review of state-of-the-art algorithms, best practices and an open-access benchmark. *Applied Energy* 293:116983. doi:10.1016/j.apenergy.2021.116983 [✓OA]
    - **Convention:** the open benchmark (LEAR and DNN baselines, epftoolbox) and the Diebold–Mariano / GW testing practice. Use it to make the forecast layer of a bidding study reproducible.

29. **Hong, T., Pinson, P., Fan, S., Zareipour, H., Troccoli, A., Hyndman, R.J. (2016).** Probabilistic energy forecasting: GEFCom2014 and beyond. *Int. J. Forecasting* 32(3):896–913. doi:10.1016/j.ijforecast.2016.02.001 [✓OA]
    - **Convention:** pinball-loss evaluation of quantile price and load forecasts, which feed the newsvendor- or scenario-based bids.

---

## C. Convention-setting research articles (frequently treated as canon)

30. **Walawalkar, R., Apt, J., Mancini, R. (2007).** Economics of electric energy storage for energy arbitrage and regulation in New York. *Energy Policy* 35(4):2558–2568. doi:10.1016/j.enpol.2006.09.005 [✓OA]
    - **Convention:** "price-taker, perfect-foresight arbitrage + regulation revenue on historical ISO prices" (NYISO) as an upper bound on revenue.

31. **Sioshansi, R., Denholm, P., Jenkin, T., Weiss, J. (2009).** Estimating the value of electricity storage in PJM: Arbitrage and some welfare effects. *Energy Economics* 31(2):269–277. doi:10.1016/j.eneco.2008.10.005 [✓OA]
    - **Convention:** the "price-taker LP arbitrage with perfect foresight" benchmark. It also quantifies the price-suppression effect of large storage and the welfare split, the first step toward price-maker models.

32. **Hittinger, E., Whitacre, J.F., Apt, J. (2012).** What properties of grid energy storage are most valuable? *J. Power Sources* 206:436–449. doi:10.1016/j.jpowsour.2011.12.003 [✓OA]
    - **Convention:** sensitivity of storage value to efficiency, power/energy cost, lifetime and degradation. It is the basis for parameter-ranking arguments.

33. **Bradbury, K., Pratson, L., Patiño-Echeverri, D. (2014).** Economic viability of energy storage systems based on price arbitrage potential in real-time U.S. electricity markets. *Applied Energy* 114:512–519. doi:10.1016/j.apenergy.2013.10.010 [✓OA]
    - **Convention:** a multi-ISO, technology-parameterised RT arbitrage LP producing IRR maps. The "optimal energy/power ratio" result comes from here.

34. **Hirth, L. (2013).** The market value of variable renewables. *Energy Economics* 38:218–236. doi:10.1016/j.eneco.2013.02.004 [✓OA]
    - **Convention:** "value factor / cannibalisation". It is the reason storage arbitrage spreads are expected to widen with VRE penetration and then compress as storage enters.

35. **Hittinger, E.S., Azevedo, I.M.L. (2015).** Bulk energy storage increases United States electricity system emissions. *Environmental Science & Technology* 49(5):3203–3210. doi:10.1021/es505027p [✓OA]
    - **Convention:** marginal-emissions accounting for storage, i.e., arbitrage can raise emissions. Pair it with Schmidt et al. 2019 (ES&T) and Beuse et al. 2021 (Joule).

36. **Conejo, A.J., Nogales, F.J., Arroyo, J.M. (2002).** Price-taker bidding strategy under price uncertainty. *IEEE TPWRS* 17(4):1081–1088. doi:10.1109/TPWRS.2002.804948 [✓OA]
    - **Convention:** constructing price-taker offer curves from forecast price distributions (the self-scheduling-to-bid-curve mapping).

37. **Pinson, P., Chevallier, C., Kariniotakis, G. (2007).** Trading wind generation from short-term probabilistic forecasts of wind power. *IEEE TPWRS* 22(3):1148–1156. doi:10.1109/TPWRS.2007.901117 [✓OA]
    - **Convention:** the "quantile bid = f(imbalance price ratio)" newsvendor rule under two-price imbalance settlement.

38. **Xu, B., Zhao, J., Zheng, T., Litvinov, E., Kirschen, D.S. (2018).** Factoring the cycle aging cost of batteries participating in electricity markets. *IEEE TPWRS* 33(2):2248–2259. doi:10.1109/TPWRS.2017.2733339 [✓OA]
    - Translates a cycle-depth stress function into a piecewise-linear marginal cost that can be submitted inside an ISO bid. This makes degradation compatible with market clearing.
    - **Convention:** the "rainflow cycle cost → piecewise-linear segment bids" convention. The underlying cell model is Xu, Oudalov, Ulbig, Andersson & Kirschen (2018), *IEEE TSG* 9(2):1131–1140, doi:10.1109/TSG.2016.2578950 [✓OA].

39. **Shi, Y., Xu, B., Tan, Y., Kirschen, D.S., Zhang, B. (2019).** Optimal battery control under cycle aging mechanisms in pay for performance settings. *IEEE Trans. Automatic Control* 64(6):2324–2339. doi:10.1109/TAC.2018.2867507 [✓OA]
    - **Convention:** proves the convexity of the rainflow-based cycle-aging cost. Cite it to justify convex or online-convex treatment of degradation.

40. **Schmalstieg, J., Käbitz, S., Ecker, M., Sauer, D.U. (2014).** A holistic aging model for Li(NiMnCo)O2 based 18650 lithium-ion batteries. *J. Power Sources* 257:325–334. doi:10.1016/j.jpowsour.2014.02.012 [✓OA]
    - **Convention:** the "semi-empirical calendar (√t, SoC, T) + cycle (Ah throughput, DoD) aging model" used in SimSES-type simulators and many techno-economic studies.

41. **Krishnamurthy, D., Uçkun, C., Zhou, Z., Thimmapuram, P., Botterud, A. (2018).** Energy storage arbitrage under day-ahead and real-time price uncertainty. *IEEE TPWRS* 33(1):84–93. doi:10.1109/TPWRS.2017.2685347 [✓OA]
    - **Convention:** two-stage SP with DA commitment and RT recourse for storage, with VSS reported against deterministic bidding.

42. **Jiang, D.R., Powell, W.B. (2015).** Optimal hour-ahead bidding in the real-time electricity market with battery storage using approximate dynamic programming. *INFORMS J. Computing* 27(3):525–543. doi:10.1287/ijoc.2015.0640 [✓OA]
    - **Convention:** an "ADP with monotone value functions" storage bidder. This is the most direct pre-DRL learning-based benchmark.

43. **Ye, Y., Qiu, D., Sun, M., Papadaskalopoulos, D., Strbac, G. (2020).** Deep reinforcement learning for strategic bidding in electricity markets. *IEEE Trans. Smart Grid* 11(2):1343–1355. doi:10.1109/TSG.2019.2936142 [✓OA]
    - **Convention:** "DRL agent with a market-clearing simulator in the loop" for strategic, price-making bidding. It is the reference for MPEC vs. DRL comparisons.

44. **Bertrand, G., Papavasiliou, A. (2020).** Adaptive trading in continuous intraday electricity markets for a storage unit. *IEEE TPWRS* 35(3):2339–2350. doi:10.1109/TPWRS.2019.2957246 [✓OA]
    - **Convention:** RL-tuned threshold policies for storage in the continuous intraday market (CID, the European continuous market). This is the policy-search alternative to DQN/PPO in continuous markets.

45. **Mohajerin Esfahani, P., Kuhn, D. (2018).** Data-driven distributionally robust optimization using the Wasserstein metric: Performance guarantees and tractable reformulations. *Mathematical Programming* 171(1–2):115–166. doi:10.1007/s10107-017-1172-1 [✓OA]
    - **Convention:** "Wasserstein-ball DRO with finite-sample guarantees and convex reformulations". This is the backbone of the researcher's DRO sizing work.

46. **Rockafellar, R.T., Uryasev, S. (2000).** Optimization of conditional value-at-risk. *Journal of Risk* 2(3):21–41. doi:10.21314/JOR.2000.038 [✓OA]
    - **Convention:** the LP linearisation of CVaR used in every risk-averse SP bidding model (Conejo et al. 2010). Quartile flag: this is a finance journal; it is cited for the method, not the venue.

---

## D. Convention quick-map: modelling convention → anchors

| Modelling convention | Anchors |
|---|---|
| Price-taker LP arbitrage, perfect foresight | Walawalkar 2007; Sioshansi 2009; Bradbury 2014; Sioshansi & Conejo 2017 |
| Price-taker offer curves from price scenarios | Conejo, Nogales & Arroyo 2002; Conejo, Carrión & Morales 2010 |
| Two-stage SP + CVaR | Conejo, Carrión & Morales 2010; Rockafellar & Uryasev 2000; Birge & Louveaux 2011; Krishnamurthy 2018 |
| Quantile / newsvendor bids under imbalance pricing | Pinson 2007; Morales et al. 2014 (book) |
| RO / ARO | Ben-Tal et al. 2009; Baringo & Conejo 2011; Bertsimas et al. 2013 |
| Wasserstein DRO | Mohajerin Esfahani & Kuhn 2018 |
| Price-maker storage, MPEC / bilevel | Gabriel et al. 2013; Mohsenian-Rad 2016; Nasrolahpour 2016/2018; Pineda & Morales 2019 (caveat) |
| Rainflow cycle cost in bids | Xu et al. 2018 TPWRS; Shi et al. 2019 TAC; Collath et al. 2022 (taxonomy) |
| Semi-empirical aging | Schmalstieg 2014; Ecker 2014 (see GROUPS §17) |
| ADP / VFA | Powell 2011; Jiang & Powell 2015; Salas & Powell 2018 |
| DRL bidding | Ye et al. 2020; Bertrand & Papavasiliou 2020; Chen et al. 2022 (critical review); Powell 2022 (policy classes) |
| LMP / FTR / ORDC market design | Schweppe 1988; Hogan 1992, 2013; Stoft 2002; Papavasiliou & Smeers 2017 |
| Market value / cannibalisation | Hirth 2013 |
| System value of storage | de Sisternes 2016; Mallapragada 2020; Sepulveda 2021; Braff 2016 |
| GB storage revenue stacking (cost + value toolkit) | Staffell & Rustomji 2016; Schmidt & Staffell 2023 (book); Gale et al. 2026; Landy et al. 2026 |

## Items not verified (to re-check)

- **Stoft (2002) and Shahidehpour, Yamin & Li (2002):** the DOI lookups were rate-limited.
- **Kirschen & Strbac, 2nd ed. (2019):** the DOI was not found in this pass.
- **Sutton & Barto (2018):** the book has no DOI.
- **SJR/JCR quartiles:** not re-checked for any item.
- **Not included because they could not be verified:** a "Hittinger/Ciez" review, and an LCOS review beyond Schmidt et al. 2019 (*Joule*). Schmidt et al. 2019 is listed in GROUPS §11, doi:10.1016/j.joule.2018.12.008 [✓OA].
