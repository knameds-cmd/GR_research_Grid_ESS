"""
2025년 과거 재현 (T8 = M1-9 기본 점검, M2 검증 V1·V2·V4·V6). 같은 3구역망을 2025년 설비·기상·수요와 NESO 관측 한도로 푼다.

    .venv/bin/python -m gbess.system.backcast            # results/system/m2/backcast_2025/ 에 결과와 V1·V2·V4 표

입력 (모두 2025년, 시각은 UTC 1시간. 정의를 정한 근거는 docs/notes/m2_backcast_KO.md)
- 설비: FES 2025 Building Blocks Holistic Transition의 "2025" 열(fleet.build_fleet(year="2025")). W1 사업은 없음(2025년 운전 0).
  배터리 지속시간 비율: FES 2025 Economics Inputs E.01 2025년 HT 1h 6.486 / 2h 3.784 / 4h 이상 0.117 GW (행 131~145).
- 연료·탄소 (CP.01 2025 열): 가스 £33.63/MWh LHV(행 19), 경유 £11.51/GJ × 3.6(행 13), 바이오매스 3.7 p/kWh(행 20),
  탄소 £78.70/t(행 57). 효율·가변 운영비는 fleet_2030.yaml 그대로.
- 수요: NESO Historic Demand Data 2025. 실제 소비(underlying) = ND + 배전망 풍력 + 배전망 태양광. 스코틀랜드 몫 = (ND − 잉글랜드·
  웨일스 수요) ÷ ND를 실제 소비에 곱한다. 스코틀랜드 안의 N:S는 FES BB Dem_BB003 2025 구역 비율.
- 인터커넥터: 같은 파일의 링크별 조류(+ = 수입)를 고정 주입으로 넣는다. Moyle은 S(오흐렌크로시, SPT), 나머지는 EW.
- 풍력: ERA5 2025(gbess.system.era5_ncar, NSF NCAR 미러) → inputs.renewable_cf. 해상 곡선은 정격 13 m/s(2025년 발전소군 수준,
  2030년 목표 이용률 계산에서 2025년 설비에 쓴 곡선과 같음). 해상 단지는 2025년에 운전한 곳만(OFFSHORE_SITES_2025).
- 태양광: NESO 배전망 태양광 발전 ÷ 배전망 태양광 용량(같은 파일)을 모든 구역에 같은 이용률로 쓴다.
- 원자력·수력: Elexon FUELHH 2025 실측(NUCLEAR, NPSHYD)으로 시간별 가용률을 만든다. 원자력 = 실측 ÷ FES 2025 용량 6,076 MW,
  수력 = 실측 ÷ 그해 실측 최대값. 모든 구역에 같은 비율.
- 경계 한도: NESO 하루 전 한도(B4 = SSE_SP2, B6 = SCOTEX)를 1시간 평균한 시계열(spec V1 limits_input = observed_da_hourly).
  자료가 없거나 자리채움 값인 시간은 그달 중앙값으로 채운다.
"""
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from gbess.system import observed as obs
from gbess.system.fleet import BB, build_fleet, load_bb, load_cfg
from gbess.system.inputs import RAW, renewable_cf
from gbess.system.network import Gen, Network

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "system" / "m2" / "backcast_2025"
YEAR = 2025
T0 = pd.Timestamp(f"{YEAR}-01-01", tz="UTC")
HOURS = pd.date_range(T0, T0 + pd.DateOffset(years=1), freq="h", inclusive="left")
DEMAND_2025 = RAW / "demanddata_2025.csv"
ERA5_2025 = RAW / "era5" / "uk-2025-ncar.nc"
FUEL_2025 = {"gas_gbp_mwh_lhv": 33.63, "oil_light_gbp_mwh_lhv": 11.51 * 3.6, "biomass_gbp_mwh": 37.0,
             "carbon_gbp_t": 78.697}
BATTERY_SHARES_2025 = [6.486 / 10.387, 3.784 / 10.387, 0.117 / 10.387]
OFFSHORE_SITES_2025 = {
    "N": [(58.25, -3.00), (58.18, -2.72), (58.10, -3.10), (56.60, -1.75), (57.22, -1.98), (57.00, -1.87)],
    # Beatrice, Moray East, Moray West(2025 운전), Seagreen, Aberdeen EOWDC, Kincardine
    "S": [(56.27, -2.30)],
    # Neart na Gaoithe (2024~). Inch Cape·Berwick Bank는 2025년에 운전하지 않음
    "EW": [(54.85, 1.90), (53.90, 1.80), (52.20, 2.50), (51.63, 1.50), (54.05, -3.60), (53.50, 0.85), (50.67, -0.27)],
    # Dogger Bank(A 일부), Hornsea 1·2, East Anglia One·Three, London Array, Walney 등 아일랜드해, Triton Knoll, Rampion
}
IC_COLUMNS = ["IFA_FLOW", "IFA2_FLOW", "BRITNED_FLOW", "MOYLE_FLOW", "EAST_WEST_FLOW", "NEMO_FLOW", "NSL_FLOW",
              "ELECLINK_FLOW", "VIKING_FLOW", "GREENLINK_FLOW"]
IC_ZONE = {"MOYLE_FLOW": "S"}        # 나머지는 EW


def sp_to_utc(dates, periods):
    """정산일(현지) + 정산 구간(1~46/48/50) → 구간 시작 UTC."""
    d = pd.to_datetime(dates).dt.tz_localize("Europe/London").dt.tz_convert("UTC")
    return d + pd.to_timedelta((np.asarray(periods) - 1) * 30, unit="min")


def demand_hourly(path=DEMAND_2025):
    df = pd.read_csv(path)
    df.index = pd.DatetimeIndex(sp_to_utc(df["SETTLEMENT_DATE"], df["SETTLEMENT_PERIOD"]))
    num = df.drop(columns=["SETTLEMENT_DATE", "SETTLEMENT_PERIOD"]).apply(pd.to_numeric, errors="coerce")
    h = num.groupby(num.index.floor("h")).mean()
    return h.reindex(HOURS).interpolate(limit_direction="both")


def zone_demand_2025(h, zones, scot_ns):
    """(Z, T) 실제 소비 MW. scot_ns = {'N': 몫, 'S': 몫} (합 1)."""
    under = h["ND"] + h["EMBEDDED_WIND_GENERATION"] + h["EMBEDDED_SOLAR_GENERATION"]
    scot = ((h["ND"] - h["ENGLAND_WALES_DEMAND"]) / h["ND"]).clip(0, 1)
    out = {"EW": under * (1 - scot), "N": under * scot * scot_ns["N"], "S": under * scot * scot_ns["S"]}
    return np.array([out[z].to_numpy() for z in zones])


def interconnector_injection(h, zones):
    """(Z, T) 순수입 MW (+ = 수입)."""
    inj = np.zeros((len(zones), len(h)))
    for c in IC_COLUMNS:
        z = zones.index(IC_ZONE.get(c, "EW"))
        inj[z] += h[c].fillna(0).to_numpy()
    return inj


def solar_cf(h):
    return (h["EMBEDDED_SOLAR_GENERATION"] / h["EMBEDDED_SOLAR_CAPACITY"]).clip(0, 1).to_numpy()


def fuelhh_hourly(fuel, year=YEAR):
    from gbess.system.observed import ELEXON
    parts = [pd.read_parquet(ELEXON / "fuelhh" / f"fuelhh_{m:%Y%m}.parquet")
             for m in pd.period_range(f"{year}-01", f"{year}-12", freq="M")]
    f = pd.concat(parts)
    f = f[f["fuelType"] == fuel]
    s = f.assign(t=pd.to_datetime(f["startTime"], utc=True)).drop_duplicates("t").set_index("t")["generation"].astype(float)
    return s.groupby(s.index.floor("h")).mean().reindex(HOURS).interpolate(limit_direction="both")


def observed_limits(year=YEAR):
    """(2, T) [B4, B6] 1시간 한도 MW와 채운 시간 수."""
    rows, filled = [], {}
    for b in ("B4", "B6"):
        lim = obs.hourly(obs.da_flows(b))["limit"].reindex(HOURS)
        filled[b] = int(lim.isna().sum())
        med = lim.groupby(lim.index.month).transform("median")
        rows.append(lim.fillna(med).to_numpy())
    return np.array(rows), filled


def build_network_2025(era5=ERA5_2025, limits="observed"):
    f = build_fleet(year=str(YEAR), fuel=FUEL_2025, battery_shares=BATTERY_SHARES_2025, window1=False)
    zones = f["zones"]
    fc, zc = load_cfg()
    bb = load_bb(zc, BB)
    d = bb[bb["Building Block ID Number"] == fc["demand"]["bb"]].groupby("zone")[str(YEAR)].sum()
    scot_ns = {"N": d["N"] / (d["N"] + d["S"]), "S": d["S"] / (d["N"] + d["S"])}
    h = demand_hourly()
    dem = zone_demand_2025(h, zones, scot_ns) - interconnector_injection(h, zones)
    cf, diag = renewable_cf(era5, zones, sites=OFFSHORE_SITES_2025)
    cf["solar"] = np.tile(solar_cf(h), (len(zones), 1))
    nuc = (fuelhh_hourly("NUCLEAR") / sum(g.cap for g in f["gens"] if g.name.startswith("nuclear_"))).clip(0, 1)
    hyd = fuelhh_hourly("NPSHYD")
    hyd = (hyd / hyd.max()).clip(0, 1)
    gens = []
    for g in f["gens"]:
        if g.name.startswith("nuclear_"):
            av = nuc.to_numpy()
        elif g.name.startswith("hydro_"):
            av = hyd.to_numpy()
        else:
            av = None if g.avail is None else np.full(len(HOURS), float(np.ravel(g.avail)[0]))
        gens.append(Gen(g.name, g.zone, g.cap, g.cost, av))
    for k, caps in f["renewable_mw"].items():
        for i, z in enumerate(zones):
            if caps[z] > 0:
                gens.append(Gen(f"{k}_{z}", i, caps[z], 0.0, cf[k][i], renewable=True))
    if limits == "observed":
        lim, filled = observed_limits()
    else:
        raise ValueError(limits)
    net = Network(zones, dem, lim, gens, f["stores"])
    meta = {"scot_ns": scot_ns, "limits_filled_hours": filled, "cf_diag": diag,
            "cf_mean": {k: [float(x) for x in np.asarray(v).mean(axis=1)] for k, v in cf.items()},
            "nuclear_twh": float((nuc * 6076).sum() / 1e6), "hydro_avail_mean": float(hyd.mean()),
            "interconnector_net_import_twh": float(interconnector_injection(h, zones).sum() / 1e6),
            "underlying_demand_twh": float(zone_demand_2025(h, zones, scot_ns).sum() / 1e6),
            "inputs": [str(DEMAND_2025), str(era5), str(BB)]}
    return net, meta


# ---------------------------------------------------------------------------------------------------- 비교
def v1_model(net, plan, redis_i=None):
    """모형 1단계 경계 조류 → V1 지표. plan.flows (2, T) [B4, B6], 한도는 net.limits."""
    fr = {}
    for i, b in enumerate(("B4", "B6")):
        fr[b] = pd.DataFrame({"flow": plan.flows[i], "limit": net.limits[i]}, index=HOURS)
    row = {f"{b}_{k}": v for b in fr for k, v in obs.binding_stats(fr[b]).items()}
    j = obs.joint_exceedance(fr["B4"], fr["B6"])
    row["exceed_max_B4_B6_twh"] = float(j.sum() / 1e6)
    monthly = j.groupby(j.index.tz_convert(None).to_period("M")).sum() / 1e6
    if redis_i is not None:
        row["redispatch_cost_i_gbp_m"] = float((redis_i.cost - plan.cost) / 1e6)
    return row, monthly


def v1_table(model, obs_row, model_monthly, obs_monthly, spec_v1):
    r = []
    tol = spec_v1["binding_freq"]["tol_abs"]
    for b, key in (("B6", "B6_obs"), ("B4", "B4_obs")):
        m, o = model[f"{b}_binding"], obs_row[f"{b}_binding"]
        r.append({"metric": f"V1a {b} 제약 발생 비율", "model": m, "observed": o, "criterion": f"±{tol:.2f}",
                  "pass": abs(m - o) <= tol})
    ratio = model["exceed_max_B4_B6_twh"] / obs_row["exceed_max_B4_B6_twh"]
    lo, hi = spec_v1["exceedance_TWh"]["ratio_band"]
    r.append({"metric": "V1b B4·B6 큰 쪽 초과량 TWh", "model": model["exceed_max_B4_B6_twh"],
              "observed": obs_row["exceed_max_B4_B6_twh"], "criterion": f"비율 {lo}~{hi}", "ratio": ratio,
              "pass": lo <= ratio <= hi})
    c = float(np.corrcoef(model_monthly.to_numpy(), obs_monthly.to_numpy())[0, 1])
    r.append({"metric": "V1c 월별 초과량 상관", "model": c, "criterion": f"≥ {spec_v1['monthly_corr_min']}",
              "pass": c >= spec_v1["monthly_corr_min"]})
    if "redispatch_cost_i_gbp_m" in model:
        ref = spec_v1["cost"]["scot_share"] * spec_v1["cost"]["obs_thermal_gbp_m"]
        rr = model["redispatch_cost_i_gbp_m"] / ref
        lo, hi = spec_v1["cost"]["ratio_band"]
        r.append({"metric": "V1d 재급전 비용 (i) £m ÷ (0.60 × 열적 비용)", "model": model["redispatch_cost_i_gbp_m"],
                  "observed": ref, "criterion": f"비율 {lo}~{hi}", "ratio": rr, "pass": lo <= rr <= hi})
    lo, hi = spec_v1["order_check_band"]
    r.append({"metric": "M1-9 자릿수 점검 (초과량 비율)", "model": ratio, "criterion": f"{lo:.3f}~{hi}",
              "pass": lo <= ratio <= hi})
    return pd.DataFrame(r)


def store_energy(dispatch, net, name):
    i = [s.name for s in net.stores].index(name)
    return dispatch.d[i], dispatch.ch[i]


def v2_model(net, plan, redis_ii, spec_v2, obs_pn_gen, obs_pn_pump, obs_bid):
    d1, c1 = store_energy(plan, net, "cruachan")
    d2, c2 = store_energy(redis_ii, net, "cruachan")
    net1, net2 = d1 - c1, d2 - c2
    down = float(np.clip(net1 - net2, 0, None).sum() / 1e3)
    lo, hi = spec_v2["pn_volume_ratio_band"]
    blo, bhi = spec_v2["variant_ii_bid_ratio_band"]
    rows = [{"metric": "V2a 1단계 발전 GWh ÷ PN", "model": d1.sum() / 1e3, "observed": obs_pn_gen,
             "ratio": d1.sum() / 1e3 / obs_pn_gen, "criterion": f"{lo}~{hi}"},
            {"metric": "V2a 1단계 양수 GWh ÷ PN", "model": c1.sum() / 1e3, "observed": obs_pn_pump,
             "ratio": c1.sum() / 1e3 / obs_pn_pump, "criterion": f"{lo}~{hi}"},
            {"metric": "V2c 변형 (ii) 하향 조정 GWh ÷ 관측 BOA 하향", "model": down, "observed": obs_bid,
             "ratio": down / obs_bid, "criterion": f"{blo}~{bhi}"}]
    df = pd.DataFrame(rows)
    df["pass"] = [lo <= r <= hi for r in df["ratio"][:2]] + [blo <= df["ratio"][2] <= bhi]
    f_obs = obs_bid / down if down > 0 else float("nan")
    return df, f_obs


def within_day_spearman(model_p, obs_p):
    """현지 날짜마다 두 가격의 순위상관(Spearman), 그 중앙값."""
    a = pd.Series(model_p, index=HOURS).tz_convert("Europe/London")
    b = obs_p.reindex(HOURS).tz_convert("Europe/London")
    df = pd.DataFrame({"m": a, "o": b}).dropna()
    r = df.groupby(df.index.date).apply(lambda x: x["m"].rank().corr(x["o"].rank()) if len(x) >= 12 else np.nan)
    return float(r.median())


def v4_table(model_p, spec_v4):
    o_h = obs.mid_hourly(T0, T0 + pd.DateOffset(years=1)).reindex(HOURS)
    mo = obs.price_metrics(pd.Series(model_p, index=HOURS))
    ob = obs.price_metrics(o_h)
    rho = within_day_spearman(model_p, o_h)
    r1, r2 = mo["spread_median"] / ob["spread_median"], mo["spread_p90"] / ob["spread_p90"]
    lo1, hi1 = spec_v4["top8_minus_bottom8_median_ratio"]
    lo2, hi2 = spec_v4["top8_minus_bottom8_p90_ratio"]
    tol = spec_v4["nonpositive_hours_tol_abs"]
    rows = [{"metric": "V4 상위8 − 하위8 중앙값 £/MWh", "model": mo["spread_median"], "observed": ob["spread_median"],
             "ratio": r1, "criterion": f"{lo1}~{hi1}", "pass": lo1 <= r1 <= hi1},
            {"metric": "V4 상위8 − 하위8 P90 £/MWh", "model": mo["spread_p90"], "observed": ob["spread_p90"],
             "ratio": r2, "criterion": f"{lo2}~{hi2}", "pass": lo2 <= r2 <= hi2},
            {"metric": "V4 가격 ≤ 0 시간 비율", "model": mo["nonpositive_share"], "observed": ob["nonpositive_share"],
             "criterion": f"±{tol}", "pass": abs(mo["nonpositive_share"] - ob["nonpositive_share"]) <= tol},
            {"metric": "V4 하루 안 순위상관 중앙값", "model": rho, "criterion": f"≥ {spec_v4['within_day_spearman_median_min']}",
             "pass": rho >= spec_v4["within_day_spearman_median_min"]},
            {"metric": "참고: 연평균 가격 £/MWh", "model": float(np.mean(model_p)), "observed": float(o_h.mean())}]
    return pd.DataFrame(rows)


def run(out=OUT, log=print, era5=ERA5_2025):
    from gbess.system.planner import solve_planner
    from gbess.system.redispatch import redispatch
    from gbess.system.run_m1 import file_sha256, git_commit, load_spec, SPEC
    from gbess.system.stage1 import solve_stage1
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    spec = load_spec()
    t0 = time.perf_counter()
    net, meta = build_network_2025(era5)
    log(f"입력 {time.perf_counter() - t0:.0f}s: {json.dumps({k: meta[k] for k in meta if k != 'cf_diag'}, ensure_ascii=False)}")
    plan = solve_stage1(net)
    log(f"1단계 {plan.status} {time.perf_counter() - t0:.0f}s")
    r_i = redispatch(plan, net, "gen_only", infeasible="min_deviation")
    log(f"재급전 (i) {r_i.status} {time.perf_counter() - t0:.0f}s")
    r_ii = redispatch(plan, net, "intertemporal")
    log(f"재급전 (ii) {r_ii.status} {time.perf_counter() - t0:.0f}s")
    s6 = solve_planner(net)
    obs_row, obs_monthly = obs.v1_observed(YEAR)
    model, model_monthly = v1_model(net, plan, r_i)
    t1 = v1_table(model, obs_row, model_monthly, obs_monthly, spec["validation"]["V1_constraints"])
    cr = obs.cruachan_pn(YEAR)
    t2, f_obs = v2_model(net, plan, r_ii, spec["validation"]["V2_cruachan"], cr["pn_gen_gwh"], cr["pn_pump_gwh"],
                         cr["boa_down_gwh"])
    t4 = v4_table(plan.prices, spec["validation"]["V4_prices"])
    v1_vol = float(np.abs(r_i.p - plan.p).sum() / 2 / 1e6)         # 재급전 (i) 물량 TWh (올림 + 내림의 절반)
    kappa_model_unit = model["redispatch_cost_i_gbp_m"] * 1e6 / max(v1_vol * 1e6, 1.0)
    obs_unit = obs_row["thermal_cost_gbp_m"] / obs_row["thermal_volume_twh"]
    extra = {"stage1_cost_gbp_m": plan.cost / 1e6, "redispatch_i_cost_gbp_m": model["redispatch_cost_i_gbp_m"],
             "redispatch_ii_cost_gbp_m": (r_ii.cost - plan.cost) / 1e6, "planner_cost_gbp_m": s6.cost / 1e6,
             "redispatch_i_volume_twh": v1_vol, "model_unit_gbp_mwh": kappa_model_unit,
             "observed_unit_gbp_mwh": obs_unit, "kappa": obs_unit / kappa_model_unit, "f_obs": f_obs,
             "min_deviation_gwh": float(r_i.extra.get("fixed_deviation_mwh", 0.0)) / 1e3}
    for name, t in (("v1", t1), ("v2", t2), ("v4", t4)):
        t.to_csv(out / f"{name}.csv", index=False)
    pd.DataFrame({"model": model_monthly, "observed": obs_monthly}).to_csv(out / "v1_monthly.csv")
    pd.DataFrame({"t": HOURS, "lambda": plan.prices, "flow_B4": plan.flows[0], "flow_B6": plan.flows[1],
                  "limit_B4": net.limits[0], "limit_B6": net.limits[1]}).to_csv(out / "hourly.csv", index=False)
    rec = {"git_commit": git_commit(), "spec_sha256": file_sha256(SPEC),
           "input_sha256": {p: file_sha256(p) for p in meta["inputs"]},
           "solver_status": sorted({plan.status, r_i.status, r_ii.status, s6.status}),
           "solve_seconds": time.perf_counter() - t0, "meta": meta, "summary": extra}
    (out / "run.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return t1, t2, t4, extra


if __name__ == "__main__":
    pd.set_option("display.width", 220)
    t1, t2, t4, extra = run()
    for t in (t1, t2, t4):
        print(t.round(3).to_string(index=False))
    print(json.dumps(extra, indent=1))
