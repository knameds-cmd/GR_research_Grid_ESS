# 논문 아카이브 인덱스

총 110편 (2026-10-06 기준). 한 논문이 여러 갈래에 걸치면 각 갈래 표에 모두 나옵니다.

- 각 논문 파일: `papers/<id>.md` (YAML 메타데이터 + 11개 섹션: 질문, 가정, 제약, 모델, 데이터·가공, 정당화, 결과, 한계, 관련성, 계보, 검증기록)
- 갈래별 종합: `streams/S*.md` (개관, 계보, 그룹, 요약표, 공백)
- 연구 그룹·사제 계보: `GROUPS.md` / 교과서·랜드마크 리뷰: `CANON.md` / 내 연구의 위치: `LINEAGE.md`

**표기**: `Q1*` = 현재 Q1이지만 Q2 이하였던 연도가 있거나 발행연도에 SJR 순위가 없던 경우(각 파일의 quartile 필드에 연도별 근거). 2026-10-06 독립 검증에서 표본 24편 서지·12개 저널 등급 재확인. `근거`: full = 전문 읽음, full (pre/WP) = 프리프린트·워킹페이퍼·저자본 전문, abstract = 초록만(심층 필드는 "(from abstract)" 표시), partial = 일부.

근거 수준 분포: full 69편, abstract 41편

## S1 저장장치 가치·경제성 기초 (20편)

| id | 연도 | 저널 | Q | 방법 | 맥락 | 근거 |
|---|---|---|---|---|---|---|
| [walawalkar2007_nyisoarbitrage](papers/walawalkar2007_nyisoarbitrage.md) | 2007 | Energy Policy | Q1 | heuristic revenue screening + Monte Carl | NYISO (2001-2005), zonal DA energy (NYC / NY East  | full |
| [sioshansi2009_pjmvalue](papers/sioshansi2009_pjmvalue.md) | 2009 | Energy Economics | Q1 | LP (price-taker) / QP (price-responsive) | PJM 2002-2007, hourly LMP (system-average and noda | full |
| [sioshansi2010_ownership](papers/sioshansi2010_ownership.md) | 2010 | The Energy Journal | Q1* | analytical Nash equilibrium + MCP (compl | ERCOT 2005 (calibration), stylised two-period (off | full |
| [he2011_aggregatingvalues](papers/he2011_aggregatingvalues.md) | 2011 | Energy Policy | Q1 | MILP | Belgium 2007 (one week): week-ahead generation-cos | full |
| [bradbury2014_rtarbitrage](papers/bradbury2014_rtarbitrage.md) | 2014 | Applied Energy | Q1 | LP | 7 U.S. real-time markets (2008 prices), 14 storage | abstract |
| [sioshansi2014_welfareloss](papers/sioshansi2014_welfareloss.md) | 2014 | Energy Economics | Q1 | analytical game theory (Nash-Cournot equ | stylised two-period wholesale market (no specific  | full |
| [mcconnell2015_energyonly](papers/mcconnell2015_energyonly.md) | 2015 | Applied Energy | Q1 | LP | Australian NEM (South Australia focus), energy-onl | full |
| [braff2016_windsolarvalue](papers/braff2016_windsolarvalue.md) | 2016 | Nature Climate Change | Q1 | LP (revenue-maximising hybrid-plant disp | U.S. locations (incl. Texas wind), hybrid wind/sol | abstract |
| [desisternes2016_decarbvalue](papers/desisternes2016_decarbvalue.md) | 2016 | Applied Energy | Q1 | MILP (capacity expansion with clustered  | ERCOT-like (Texas) system, long-run capacity expan | abstract |
| [staffell2016_maxvalue](papers/staffell2016_maxvalue.md) | 2016 | Journal of Energy Storage | Q1* | heuristic (greedy price-pairing) validat | GB 2013/14 half-hourly wholesale prices + STOR res | full |
| [dowling2017_multiscalemarkets](papers/dowling2017_multiscalemarkets.md) | 2017 | Applied Energy | Q1 | MILP | CAISO 2015: day-ahead IFM (1 h), FMM (15 min), RTD | full |
| [schmidt2017_experiencerates](papers/schmidt2017_experiencerates.md) | 2017 | Nature Energy | Q1 | econometric (experience-curve regression | global technology cost data (no market); 11 storag | full |
| [wankmuller2017_degradationarbitrage](papers/wankmuller2017_degradationarbitrage.md) | 2017 | Journal of Energy Storage | Q1 | LP/MILP arbitrage with degradation penal | MISO historical energy prices; price-taker arbitra | abstract |
| [he2018_intertemporal](papers/he2018_intertemporal.md) | 2018 | Nature Energy | Q1 | Lagrangian decomposition (life-cycle pro | CAISO 2016: day-ahead energy arbitrage and frequen | full |
| [schmidt2019_lcos](papers/schmidt2019_lcos.md) | 2019 | Joule | Q1 | techno-economic LCOS + Monte Carlo | generic application archetypes (12 applications: a | full |
| [mallapragada2020_longrunvalue](papers/mallapragada2020_longrunvalue.md) | 2020 | Applied Energy | Q1 | LP (GenX capacity expansion, hourly, per | stylised U.S. Northeast and Texas systems, long-ru | abstract |
| [junge2022_efficientstorage](papers/junge2022_efficientstorage.md) | 2022 | The Energy Journal | Q1* | LP (welfare-maximising capacity expansio | theory + 'Texas-like' (ERCOT) deeply decarbonised  | full |
| [xu2022_dynamicvaluation](papers/xu2022_dynamicvaluation.md) | 2022 | IEEE Transactions on Power Systems | Q1 | SDP/DP over state of health with piecewi | NYISO real-time arbitrage 2010-2020 (WEST, NORTH,  | full |
| [mercier2023_eudaarbitrage](papers/mercier2023_eudaarbitrage.md) | 2023 | Energy Economics | Q1 | MILP | EU-28 + NO, CH, TR day-ahead hourly prices 2000-20 | abstract |
| [antweiler2025_newmeritorder](papers/antweiler2025_newmeritorder.md) | 2025 | Energy Economics | Q1 | analytical long-run equilibrium + NLP nu | greenfield 100% wind+solar+storage (Li-ion battery | full |

## S2 다중서비스 공동최적화(수익 스택) (14편)

| id | 연도 | 저널 | Q | 방법 | 맥락 | 근거 |
|---|---|---|---|---|---|---|
| [he2011_aggregatingvalues](papers/he2011_aggregatingvalues.md) | 2011 | Energy Policy | Q1 | MILP | Belgium 2007 (one week): week-ahead generation-cos | full |
| [moreno2015_multiservicemilp](papers/moreno2015_multiservicemilp.md) | 2015 | Applied Energy | Q1 | MILP | Great Britain: distribution-network congestion man | abstract |
| [perez2016_degradationmultiservice](papers/perez2016_degradationmultiservice.md) | 2016 | IEEE Transactions on Sustainable Energy | Q1 | MILP | Great Britain: balancing-market services + DNO (di | abstract |
| [staffell2016_maxvalue](papers/staffell2016_maxvalue.md) | 2016 | Journal of Energy Storage | Q1* | heuristic (greedy price-pairing) validat | GB 2013/14 half-hourly wholesale prices + STOR res | full |
| [dowling2017_multiscalemarkets](papers/dowling2017_multiscalemarkets.md) | 2017 | Applied Energy | Q1 | MILP | CAISO 2015: day-ahead IFM (1 h), FMM (15 min), RTD | full |
| [kazemi2017_jointenergyancillary](papers/kazemi2017_jointenergyancillary.md) | 2017 | IEEE Transactions on Sustainable Energy | Q1 | RO | Day-ahead energy + spinning reserve + regulation ( | abstract |
| [cheng2018_multiscaledp](papers/cheng2018_multiscaledp.md) | 2018 | IEEE Transactions on Smart Grid | Q1 | SDP/DP | US (PJM-style) frequency regulation + energy arbit | abstract |
| [shi2018_superlineargains](papers/shi2018_superlineargains.md) | 2018 | IEEE Transactions on Power Systems | Q1 | SP | PJM RegD capacity payment + US C&I tariff (energy  | full |
| [braeuer2019_parallelrevenue](papers/braeuer2019_parallelrevenue.md) | 2019 | Applied Energy | Q1 | LP | Germany: behind-the-meter industrial BESS: peak sh | abstract |
| [namor2019_multiservicecontrol](papers/namor2019_multiservicecontrol.md) | 2019 | IEEE Transactions on Smart Grid | Q1 | MPC | Swiss/ENTSO-E CE primary frequency regulation (dro | full |
| [engels2020_fcrpeakshaving](papers/engels2020_fcrpeakshaving.md) | 2020 | IEEE Transactions on Smart Grid | Q1 | SDP/DP | Continental Europe FCR (symmetric, ±200 mHz, daily | full |
| [englberger2020_dynamicstacking](papers/englberger2020_dynamicstacking.md) | 2020 | Cell Reports Physical Science | Q1* | MILP | Germany: FCR (PCR) + peak shaving + self-consumpti | abstract |
| [biggins2022_tradeornot](papers/biggins2022_tradeornot.md) | 2022 | Journal of Energy Storage | Q1 | MILP | GB: monthly Firm Frequency Response (dynamic FFR)  | full |
| [mirzaeialavijeh2025_swedenfcrstacking](papers/mirzaeialavijeh2025_swedenfcrstacking.md) | 2025 | Applied Energy | Q1 | MILP | Sweden SE3: Nord Pool day-ahead + FCR-N, FCR-D up, | full |

## S3 불확실성 하 입찰(SP/RO/SDP/가격결정자) (16편)

| id | 연도 | 저널 | Q | 방법 | 맥락 | 근거 |
|---|---|---|---|---|---|---|
| [conejo2002_pricetaker](papers/conejo2002_pricetaker.md) | 2002 | IEEE Transactions on Power Systems | Q1 | SP | Generic pool, next-day hourly clearing prices; pri | abstract |
| [ruiz2009_mpecoffer](papers/ruiz2009_mpecoffer.md) | 2009 | IEEE Transactions on Power Systems | Q1 | MILP (bilevel → MPEC → MILP via KKT + du | Generic pool, multiperiod network-constrained (DC) | abstract |
| [baringo2011_robustoffer](papers/baringo2011_robustoffer.md) | 2011 | IEEE Transactions on Power Systems | Q1 | RO (sequence of robust MILPs) | Generic pool, hourly offering curves; price-taker  | abstract |
| [lohndorf2013_addp](papers/lohndorf2013_addp.md) | 2013 | Operations Research | Q1 | SDP/DP (ADDP = SDDP cuts in reservoir st | EEX (German) day-ahead hourly auction with intrada | full |
| [pandzic2013_vppoffer](papers/pandzic2013_vppoffer.md) | 2013 | Applied Energy | Q1 | SP | Day-ahead + balancing market; VPP = wind + pumped- | abstract |
| [jiang2015_hourahead](papers/jiang2015_hourahead.md) | 2015 | INFORMS Journal on Computing | Q1 | SDP/DP (Monotone-ADP) | NYISO real-time market (NYC zone), 5-min settlemen | full |
| [mohsenianrad2016_pricemaker](papers/mohsenianrad2016_pricemaker.md) | 2016 | IEEE Transactions on Power Systems | Q1 | MILP (bilevel → KKT + big-M + strong dua | Nodal (LMP) day-ahead energy market, DC-OPF cleari | full |
| [kazemi2017_jointenergyancillary](papers/kazemi2017_jointenergyancillary.md) | 2017 | IEEE Transactions on Sustainable Energy | Q1 | RO | Day-ahead energy + spinning reserve + regulation ( | abstract |
| [wang2017_lookahead](papers/wang2017_lookahead.md) | 2017 | IEEE Transactions on Sustainable Energy | Q1 | MILP (bilevel → KKT + linearisation) | Day-ahead, ramp-constrained multiperiod nodal mark | abstract |
| [krishnamurthy2018_dart](papers/krishnamurthy2018_dart.md) | 2018 | IEEE Transactions on Power Systems | Q1 | SP | US two-settlement (DA + RT) energy market; price-t | abstract |
| [nasrolahpour2018_bilevel](papers/nasrolahpour2018_bilevel.md) | 2018 | IEEE Transactions on Sustainable Energy | Q1 | MILP (stochastic bilevel → MPEC → MILP;  | Pool with DA joint energy + up/down reserve cleari | full |
| [tomasson2020_offerbid](papers/tomasson2020_offerbid.md) | 2020 | Applied Energy | Q1 | MILP (stochastic bilevel → KKT → stochas | Nodal pool with merchant storage portfolio exercis | abstract |
| [kim2021_vss](papers/kim2021_vss.md) | 2021 | Journal of Modern Power Systems and Clean Energy | Q1 | SP (two-stage, NLP with quadratic object | PJM DA + RT energy, APCO zone, 2012; 100 MW / 1,00 | full |
| [finnah2022_dpid](papers/finnah2022_dpid.md) | 2022 | European Journal of Operational Research | Q1 | SDP/DP (ADP) | German day-ahead auction (60-min slots, 15-min sub | abstract |
| [zheng2022_asdp](papers/zheng2022_asdp.md) | 2022 | IEEE Transactions on Power Systems | Q1 | SDP/DP (analytical SDP with piecewise-li | NYISO real-time 5-min energy, zones NYC, LONGIL, N | full |
| [lohndorf2023_coordination](papers/lohndorf2023_coordination.md) | 2023 | Operations Research | Q1 | SP (multistage SP with scenario tree + r | Auction-based day-ahead + continuous intraday mark | abstract |

## S4 열화·물리 모델링 (17편)

| id | 연도 | 저널 | Q | 방법 | 맥락 | 근거 |
|---|---|---|---|---|---|---|
| [he2016_pbrcyclelife](papers/he2016_pbrcyclelife.md) | 2016 | IEEE Transactions on Smart Grid | Q1 | MINLP (life-cycle income objective with  | PJM-style joint day-ahead energy, spinning reserve | full |
| [perez2016_degradationmultiservice](papers/perez2016_degradationmultiservice.md) | 2016 | IEEE Transactions on Sustainable Energy | Q1 | MILP | Great Britain: balancing-market services + DNO (di | abstract |
| [wankmuller2017_degradationarbitrage](papers/wankmuller2017_degradationarbitrage.md) | 2017 | Journal of Energy Storage | Q1 | LP/MILP arbitrage with degradation penal | MISO historical energy prices; price-taker arbitra | abstract |
| [he2018_intertemporal](papers/he2018_intertemporal.md) | 2018 | Nature Energy | Q1 | Lagrangian decomposition (life-cycle pro | CAISO 2016: day-ahead energy arbitrage and frequen | full |
| [schimpe2018_efficiency](papers/schimpe2018_efficiency.md) | 2018 | Applied Energy | Q1 | electro-thermal system simulation (compo | German Primary Control Reserve (FCR), Secondary Co | abstract |
| [shi2018_superlineargains](papers/shi2018_superlineargains.md) | 2018 | IEEE Transactions on Power Systems | Q1 | SP | PJM RegD capacity payment + US C&I tariff (energy  | full |
| [xu2018_cycleagingcost](papers/xu2018_cycleagingcost.md) | 2018 | IEEE Transactions on Power Systems | Q1 | MILP (piecewise-linear cycle-depth cost, | ISO-NE (SE-MASS zone) 2015, day-ahead hourly, real | full |
| [xu2018_degradationmodel](papers/xu2018_degradationmodel.md) | 2018 | IEEE Transactions on Smart Grid | Q1 | semi-empirical aging model + rainflow cy | PJM frequency regulation (RegA/RegD-type signal) c | full |
| [pandzic2019_chargingmodel](papers/pandzic2019_chargingmodel.md) | 2019 | IEEE Transactions on Power Systems | Q1 | LP (piecewise-linear SoE-dependent charg | EPEX spot day-ahead (15 Jan 2018 prices), 10 MWh p | full |
| [shi2019_cycleagingpfp](papers/shi2019_cycleagingpfp.md) | 2019 | IEEE Transactions on Automatic Control | Q1 | convex optimisation (subgradient, offlin | PJM pay-for-performance frequency regulation (RegD | full |
| [maheshwari2020_nonlineardeg](papers/maheshwari2020_nonlineardeg.md) | 2020 | Applied Energy | Q1 | MILP with linearised non-linear degradat | Wholesale market scheduling (market time constrain | abstract |
| [padmanabhan2020_energyreserve](papers/padmanabhan2020_energyreserve.md) | 2020 | IEEE Transactions on Power Systems | Q1 | MILP market clearing with BESS degradati | ISO-level LMP-based co-optimised day-ahead energy  | full |
| [reniers2021_advancedmodels](papers/reniers2021_advancedmodels.md) | 2021 | Journal of Power Sources | Q1 | NLP (physics-based SPM + SEI model as co | Belgian day-ahead market 2014, hourly; energy arbi | full |
| [collath2022_agingreview](papers/collath2022_agingreview.md) | 2022 | Journal of Energy Storage | Q1 | review | Review; case studies on FCR, self-consumption incr | full |
| [xu2022_dynamicvaluation](papers/xu2022_dynamicvaluation.md) | 2022 | IEEE Transactions on Power Systems | Q1 | SDP/DP over state of health with piecewi | NYISO real-time arbitrage 2010-2020 (WEST, NORTH,  | full |
| [collath2023_lifetimeprofit](papers/collath2023_lifetimeprofit.md) | 2023 | Applied Energy | Q1 | MPC with MILP (linearised calendar + cyc | EPEX SPOT intraday (Germany) arbitrage, price data | abstract |
| [mirzaeialavijeh2025_swedenfcrstacking](papers/mirzaeialavijeh2025_swedenfcrstacking.md) | 2025 | Applied Energy | Q1 | MILP | Sweden SE3: Nord Pool day-ahead + FCR-N, FCR-D up, | full |

## S5 강화학습·학습 기반 입찰 (15편)

| id | 연도 | 저널 | Q | 방법 | 맥락 | 근거 |
|---|---|---|---|---|---|---|
| [bertrand2020_intradaystorage](papers/bertrand2020_intradaystorage.md) | 2020 | IEEE Transactions on Power Systems | Q1 | RL/DRL | German continuous intraday market (EPEX, hourly pr | full |
| [cao2020_drlarbitragedegradation](papers/cao2020_drlarbitragedegradation.md) | 2020 | IEEE Transactions on Smart Grid | Q1 | RL/DRL | GB wholesale (hourly) energy arbitrage, price-take | full |
| [ye2020_drlstrategicbidding](papers/ye2020_drlstrategicbidding.md) | 2020 | IEEE Transactions on Smart Grid | Q1 | RL/DRL | Stylised single-bus pool-based day-ahead energy ma | full |
| [boukas2021_intradaydrl](papers/boukas2021_intradaydrl.md) | 2021 | Machine Learning | Q1 | RL/DRL | German EPEX continuous intraday (quarter-hourly pr | full |
| [harrold2022_rainbowarbitrage](papers/harrold2022_rainbowarbitrage.md) | 2022 | Energy | Q1 | RL/DRL | GB day-ahead wholesale prices as tariff for a camp | full |
| [kwon2022_rlcycledegradation](papers/kwon2022_rlcycledegradation.md) | 2022 | IEEE Transactions on Smart Grid | Q1 | RL/DRL | ERCOT 5-min energy prices + PJM regulation signal  | full |
| [sang2022_dfpricearbitrage](papers/sang2022_dfpricearbitrage.md) | 2022 | IEEE Transactions on Smart Grid | Q1 | MILP | PJM day-ahead hourly prices, price-taker ESS arbit | full |
| [jeong2023_deepbid](papers/jeong2023_deepbid.md) | 2023 | IEEE Transactions on Energy Markets, Policy and Regulation | Q1* | RL/DRL | Real-time energy market bidding of a renewable pro | abstract |
| [ye2023_marllocalmarket](papers/ye2023_marllocalmarket.md) | 2023 | IEEE Transactions on Smart Grid | Q1 | RL/DRL | Local electricity market (P2P/local trading) + fle | abstract |
| [baker2024_transferablebidder](papers/baker2024_transferablebidder.md) | 2024 | IEEE Transactions on Power Systems | Q1 | SDP/DP | Real-time wholesale arbitrage: NYISO 5-min RT pric | full |
| [bian2024_predictstoragebehavior](papers/bian2024_predictstoragebehavior.md) | 2024 | IEEE Transactions on Smart Grid | Q1 | NLP | NYISO NYC RT prices (synthetic agents); real UQ Te | full |
| [karimimadahi2024_distrlimbalance](papers/karimimadahi2024_distrlimbalance.md) | 2024 | Journal of Energy Storage | Q1 | RL/DRL | Belgian (Elia) single-price imbalance settlement,  | full |
| [li2024_temporalawaredrl](papers/li2024_temporalawaredrl.md) | 2024 | IEEE Transactions on Energy Markets, Policy and Regulation | Q1 | RL/DRL | Australian NEM, 5-min spot + 6 contingency FCAS (f | full |
| [sage2025_drlbatterybenchmark](papers/sage2025_drlbatterybenchmark.md) | 2025 | Journal of Energy Storage | Q1 | RL/DRL | Battery arbitrage and load-following/renewable-uti | abstract |
| [yi2025_perturbeddfl](papers/yi2025_perturbeddfl.md) | 2025 | IEEE Transactions on Smart Grid | Q1 | LP | NYISO hourly DA/RT prices (arbitrage); Queensland  | full |

## S6 보조서비스 상품 설계와 배터리 (18편)

| id | 연도 | 저널 | Q | 방법 | 맥락 | 근거 |
|---|---|---|---|---|---|---|
| [oudalov2007_pfcsizing](papers/oudalov2007_pfcsizing.md) | 2007 | IEEE Transactions on Power Systems | Q1 | simulation-based sizing (time-series sim | UCTE/Swiss primary frequency control (today's FCR) | abstract |
| [he2016_pbrcyclelife](papers/he2016_pbrcyclelife.md) | 2016 | IEEE Transactions on Smart Grid | Q1 | MINLP (life-cycle income objective with  | PJM-style joint day-ahead energy, spinning reserve | full |
| [greenwood2017_efrservicedesign](papers/greenwood2017_efrservicedesign.md) | 2017 | Applied Energy | Q1 | real-time simulation + power-hardware-in | GB Enhanced Frequency Response (EFR, 2016 tender)  | abstract |
| [thien2017_fcrgermanystrategy](papers/thien2017_fcrgermanystrategy.md) | 2017 | Journal of Energy Storage | Q1* | simulation + sensitivity analysis of a r | German FCR (Primärregelleistung), 2015 TSO rules w | abstract |
| [gundogdu2018_efrtriad](papers/gundogdu2018_efrtriad.md) | 2018 | IEEE Transactions on Industrial Electronics | Q1 | rule-based EMS + simulation + field expe | GB EFR (Service-2, narrow deadband) + TNUoS Triad  | full |
| [xu2018_regdparticipation](papers/xu2018_regdparticipation.md) | 2018 | IEEE Transactions on Power Systems | Q1 | online threshold control policy with reg | PJM RegD performance-based regulation (capability  | full |
| [engels2019_fcrgermanytechnoeco](papers/engels2019_fcrgermanytechnoeco.md) | 2019 | Applied Energy | Q1 | stochastic SAA + chance constraint, solv | German FCR (Regelleistung.net weekly auction, pay- | full |
| [lee2019_closedloopgb](papers/lee2019_closedloopgb.md) | 2019 | Applied Energy | Q1 | closed-loop swing-equation simulation (n | GB EFR (Service 2) and STOR reserve, 2015 vs 2025  | full |
| [shi2019_cycleagingpfp](papers/shi2019_cycleagingpfp.md) | 2019 | IEEE Transactions on Automatic Control | Q1 | convex optimisation (subgradient, offlin | PJM pay-for-performance frequency regulation (RegD | full |
| [engels2020_fcrpeakshaving](papers/engels2020_fcrpeakshaving.md) | 2020 | IEEE Transactions on Smart Grid | Q1 | SDP/DP | Continental Europe FCR (symmetric, ±200 mHz, daily | full |
| [biggins2022_tradeornot](papers/biggins2022_tradeornot.md) | 2022 | Journal of Energy Storage | Q1 | MILP | GB: monthly Firm Frequency Response (dynamic FFR)  | full |
| [engelhardt2022_fcrnrecovery](papers/engelhardt2022_fcrnrecovery.md) | 2022 | Sustainable Energy, Grids and Networks | Q1 | multi-year time-series simulation of ene | Nordic FCR-N (and FCR-D context), DK2 / Energinet  | abstract |
| [koltermann2022_fcrbalancinggroup](papers/koltermann2022_fcrbalancinggroup.md) | 2022 | International Journal of Electrical Power & Energy Systems | Q1 | simulation model validated with field da | German FCR + balancing-group settlement (reBAP imb | abstract |
| [cao2024_dcvsefr](papers/cao2024_dcvsefr.md) | 2024 | International Journal of Electrical Power & Energy Systems | Q1 | closed-loop simulation + root-locus stab | GB Dynamic Containment (DC/DCFR) vs Enhanced Frequ | abstract |
| [gilmore2024_lcofcas](papers/gilmore2024_lcofcas.md) | 2024 | The Energy Journal | Q1* | levelised-cost (LCoFCAS) equilibrium-pri | Australia NEM FCAS: regulation raise/lower, 6 s /  | full |
| [celicortes2025_deterministicfreq](papers/celicortes2025_deterministicfreq.md) | 2025 | Energy Reports | Q1* | time-series decomposition (statistical)  | Continental Europe FCR (Germany); frequency data 2 | abstract |
| [fan2025_dccolocatedreforms](papers/fan2025_dccolocatedreforms.md) | 2025 | CSEE Journal of Power and Energy Systems | Q1* | multi-year techno-economic simulation +  | GB Dynamic Containment LF/HF (EFA-block day-ahead  | full |
| [mirzaeialavijeh2025_swedenfcrstacking](papers/mirzaeialavijeh2025_swedenfcrstacking.md) | 2025 | Applied Energy | Q1 | MILP | Sweden SE3: Nord Pool day-ahead + FCR-N, FCR-D up, | full |

## S7 저장장치 시장설계·규제 (22편)

| id | 연도 | 저널 | Q | 방법 | 맥락 | 근거 |
|---|---|---|---|---|---|---|
| [sioshansi2010_ownership](papers/sioshansi2010_ownership.md) | 2010 | The Energy Journal | Q1* | analytical Nash equilibrium + MCP (compl | ERCOT 2005 (calibration), stylised two-period (off | full |
| [he2011_aggregatingvalues](papers/he2011_aggregatingvalues.md) | 2011 | Energy Policy | Q1 | MILP | Belgium 2007 (one week): week-ahead generation-cos | full |
| [sioshansi2014_capacityvalue](papers/sioshansi2014_capacityvalue.md) | 2014 | IEEE Transactions on Power Systems | Q1 | SDP/DP + probabilistic reliability (LOLP | Five US utility systems (PG&E, SCE, NV Energy, PNM | full |
| [sioshansi2014_welfareloss](papers/sioshansi2014_welfareloss.md) | 2014 | Energy Economics | Q1 | analytical game theory (Nash-Cournot equ | stylised two-period wholesale market (no specific  | full |
| [mcconnell2015_energyonly](papers/mcconnell2015_energyonly.md) | 2015 | Applied Energy | Q1 | LP | Australian NEM (South Australia focus), energy-onl | full |
| [papavasiliou2017_ordcbelgium](papers/papavasiliou2017_ordcbelgium.md) | 2017 | The Energy Journal | Q1 | counterfactual simulation (market model  | Belgian electricity market (Elia), real-time energ | abstract |
| [sioshansi2017_capacityrights](papers/sioshansi2017_capacityrights.md) | 2017 | IEEE Transactions on Power Systems | Q1 | LP (auction clearing) + duality-based pr | Generic; motivated by FERC rulings on LEAPS (marke | full |
| [grubb2018_ukemr](papers/grubb2018_ukemr.md) | 2018 | The Energy Journal | Q1 | review / ex-post policy evaluation | GB Electricity Market Reform (2013): Carbon Price  | abstract |
| [sakti2018_usparticipation](papers/sakti2018_usparticipation.md) | 2018 | Energy Policy | Q1 | review | US federal (FERC), ISO/RTO (CAISO, ERCOT, ISO-NE,  | abstract |
| [xu2018_cycleagingcost](papers/xu2018_cycleagingcost.md) | 2018 | IEEE Transactions on Power Systems | Q1 | MILP (piecewise-linear cycle-depth cost, | ISO-NE (SE-MASS zone) 2015, day-ahead hourly, real | full |
| [siddiqui2019_merchantinvestment](papers/siddiqui2019_merchantinvestment.md) | 2019 | The Energy Journal | Q1 | bilevel (MPEC) analytical model + numeri | Stylised imperfectly competitive (Cournot) energy  | abstract |
| [denholm2020_peakingcapacity](papers/denholm2020_peakingcapacity.md) | 2020 | Renewable Energy | Q1 | chronological peak-shaving simulation (d | 18 US regions (NERC assessment areas incl. CAISO,  | full |
| [padmanabhan2020_energyreserve](papers/padmanabhan2020_energyreserve.md) | 2020 | IEEE Transactions on Power Systems | Q1 | MILP market clearing with BESS degradati | ISO-level LMP-based co-optimised day-ahead energy  | full |
| [bhattacharjee2022_soemanagement](papers/bhattacharjee2022_soemanagement.md) | 2022 | IEEE Open Access Journal of Power and Energy | Q1 | bilevel stochastic MPEC -> MILP (KKT + b | Alberta single-bus energy-only market (2015 data); | full |
| [chen2022_misobatteryscuc](papers/chen2022_misobatteryscuc.md) | 2022 | IEEE Transactions on Power Systems | Q1 | MILP (SCUC) - convex relaxation vs binar | MISO day-ahead SCUC, storage participation model u | abstract |
| [junge2022_efficientstorage](papers/junge2022_efficientstorage.md) | 2022 | The Energy Journal | Q1* | LP (welfare-maximising capacity expansio | theory + 'Texas-like' (ERCOT) deeply decarbonised  | full |
| [williams2022_marketpower](papers/williams2022_marketpower.md) | 2022 | Energy Policy | Q1 | welfare-maximisation LP / Cournot equili | GB wholesale energy market, near-future 2020s syst | full |
| [andrescerezo2023_marketstructure](papers/andrescerezo2023_marketstructure.md) | 2023 | The RAND Journal of Economics | Q1 | analytical IO (two-stage investment + op | Theory with Spanish wholesale market simulation (2 | full |
| [jiang2023_isodispatch](papers/jiang2023_isodispatch.md) | 2023 | The Energy Journal | Q1* | LP (multi-period DC-OPF) + duality theor | Generic nodal (DC-OPF) market; case study ISO New  | full |
| [mercier2023_eudaarbitrage](papers/mercier2023_eudaarbitrage.md) | 2023 | Energy Economics | Q1 | MILP | EU-28 + NO, CH, TR day-ahead hourly prices 2000-20 | abstract |
| [antweiler2025_newmeritorder](papers/antweiler2025_newmeritorder.md) | 2025 | Energy Economics | Q1 | analytical long-run equilibrium + NLP nu | greenfield 100% wind+solar+storage (Li-ion battery | full |
| [bhattacharjee2025_hybridparticipation](papers/bhattacharjee2025_hybridparticipation.md) | 2025 | IEEE Transactions on Power Systems | Q1 | bilevel stochastic MPEC -> MILP | Alberta energy-only market (2015 data); US hybrid- | full |

## S8 실증·계량경제 (12편)

| id | 연도 | 저널 | Q | 방법 | 맥락 | 근거 |
|---|---|---|---|---|---|---|
| [green2012_storingwind](papers/green2012_storingwind.md) | 2012 | The Energy Journal | Q1 | econometric (correlations, GLS with Coch | Denmark (DK1/DK2) wind and trade with Nordic hydro | full |
| [carson2013_bulkstorageexternality](papers/carson2013_bulkstorageexternality.md) | 2013 | Journal of Environmental Economics and Management | Q1 | econometric (reduced-form marginal emiss | ERCOT 2007-2009, hourly balancing-market prices, C | full |
| [mauritzen2013_deadbattery](papers/mauritzen2013_deadbattery.md) | 2013 | The Energy Journal | Q1 | econometric (distributed-lag ARMA time s | Nord Pool: West/East Denmark wind vs southern-Norw | full |
| [tangeras2018_hydrodarealtime](papers/tangeras2018_hydrodarealtime.md) | 2018 | The Journal of Industrial Economics | Q1 | econometric (theory-derived test of comp | Nord Pool Sweden SE1-SE4, Elspot (DA) vs Elbas (in | full |
| [hortacsu2019_strategicability](papers/hortacsu2019_strategicability.md) | 2019 | American Economic Review | Q1 | econometric (structural: ex-post best re | ERCOT balancing energy market, unit/firm-level bid | full |
| [linn2019_storagecostemissions](papers/linn2019_storagecostemissions.md) | 2019 | Journal of Environmental Economics and Management | Q1 | econometric (reduced-form wind investmen | ERCOT, 2030 counterfactual calibrated to 2004-2008 | full |
| [tabari2020_payforperformance](papers/tabari2020_payforperformance.md) | 2020 | Energy Economics | Q1 | econometric (difference-in-differences o | US ISOs/RTOs; FERC Order 755 (2011) pay-for-perfor | abstract |
| [lamp2022_caisobatteryarbitrage](papers/lamp2022_caisobatteryarbitrage.md) | 2022 | Energy Economics | Q1 | econometric (quantile regression, event  | CAISO fleet of utility batteries (aggregate output | full |
| [rangarajan2023_batteryfcasdid](papers/rangarajan2023_batteryfcasdid.md) | 2023 | Energy Economics | Q1 | econometric (staggered difference-in-dif | Australia NEM, FCAS (regulation + contingency rais | abstract |
| [brown2024_reliabilitybattery](papers/brown2024_reliabilitybattery.md) | 2024 | Journal of Public Economics | Q1 | econometric (event-study DiD + dynamic d | California residential solar and solar-plus-storag | full |
| [butters2025_soakingsun](papers/butters2025_soakingsun.md) | 2025 | Econometrica | Q1 | econometric + SDP/DP (structural dynamic | CAISO (SP-15 hub), 5-min real-time + hourly day-ah | full |
| [kirkpatrick2026_batterycongestion](papers/kirkpatrick2026_batterycongestion.md) | 2026 | The Energy Journal | Q1* | econometric (high-dimensional FE DiD + d | CAISO day-ahead nodal LMPs, 757 nodes, 2009-2016;  | full |
