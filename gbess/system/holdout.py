"""
V5 보류 표본 (spec validation.V5_holdout): 얼린 모형이 평가 창(2026-11-06~2027-05-05)의 B4·B6 제약을 얼마나 맞히나.
절차는 창의 관측 조류를 보기 전에 정해 spec changelog(2026-11-06)에 적었다. 연습 판("dry")은 한 해 앞 같은 창
(2025-11-06~2026-05-05, 모두 2026-10-25 전 자료)으로 코드를 시험한다.

    .venv/bin/python -m gbess.system.holdout dry      # results/system/m2/v5_dry/
    .venv/bin/python -m gbess.system.holdout v5       # 창이 끝난 뒤(2027-05-06 이후)에만. 그 전에는 멈춤

입력 (2025 재현 gbess.system.backcast와 같은 방법, 입력 수정 ② 포함)
- 관측으로 넣는 것: 기상(ERA5, NSF NCAR 미러), 수요·배전망 풍력·태양광·인터커넥터 조류(NESO Historic Demand Data),
  원자력·수력 가용률(Elexon FUELHH), 경계 한도(NESO 하루 전 한도, 결측은 그달 중앙값).
- FES 2025에서 미리 정한 것: 설비(BB Holistic Transition), 연료·탄소(Economics CP.01), 배터리 지속시간 비율(E.01).
  열은 "창 가운데 날짜 바로 앞 연말": 연습 판 2025, 본 판 2026. W1 사업은 없음(2030년 이후 운전).
- 1단계(전국 시장)만 푼다. V5 지표(제약 발생 비율, B4·B6 큰 쪽 초과량)는 1단계 조류와 관측 한도로 정해진다.
- 비교 기준(보고만): 지난해 같은 창의 관측값을 그대로 예측으로 쓰는 단순 예측(04 보고서 V5).
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from gbess.system import backcast as bc
from gbess.system import observed as obs

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "system"
OUT = ROOT / "results" / "system" / "m2"
NO_PEEK_FROM = pd.Timestamp("2026-10-25", tz="UTC")        # spec V5 no_peek: 이 뒤의 하루 전 조류는 창이 끝나기 전에 보지 않음

# FES 2025 Economics Inputs (literature/sources/tech/neso_fes2025_econ_inputs.xlsx)
# CP.01 행 13 경유 £/GJ × 3.6, 행 19 가스 £/MWh LHV, 행 20 바이오매스 p/kWh × 10, 행 57 탄소 £/t (모두 해당 연도 열)
# E.01 HT 배터리 용량 GW 행 131~145 (배전·송전·마이크로 합): 1시간 / 2시간 / 4시간 이상(4·6·9시간)
_BAT_2026 = (5.5894 + 3.87593 + 0.37828, 0.92064 + 3.70062 + 0.00786, 0.02806 + 0.001 + 0.087 + 0.00044 + 0.00003)
FES_INPUTS = {
    "2025": {"fuel": bc.FUEL_2025, "battery_shares": bc.BATTERY_SHARES_2025},
    "2026": {"fuel": {"gas_gbp_mwh_lhv": 27.72, "oil_light_gbp_mwh_lhv": 11.14 * 3.6, "biomass_gbp_mwh": 36.0,
                      "carbon_gbp_t": 87.33299157265505},
             "battery_shares": [x / sum(_BAT_2026) for x in _BAT_2026]},
}
WINDOWS = {
    # 이름: (시작, 끝(이 시각 전까지), FES 열, 수요 파일, ERA5 파일)
    "dry": ("2025-11-06", "2026-05-06", "2025", ["demanddata_2025.csv", "demanddata_2026.csv"],
            ["era5/uk-2025-ncar.nc", "era5/uk-2026-ncar-m1-2-3-4-5.nc"]),
    "v5": ("2026-11-06", "2027-05-06", "2026", ["demanddata_2026.csv", "demanddata_2027.csv"],
           ["era5/uk-2026-ncar-m11-12.nc", "era5/uk-2027-ncar-m1-2-3-4-5.nc"]),
}


def window_hours(start, end):
    """[start, end) UTC 1시간 색인. 날짜는 UTC 0시 기준."""
    return pd.date_range(pd.Timestamp(start, tz="UTC"), pd.Timestamp(end, tz="UTC"), freq="h", inclusive="left")


def shift_year(start, end, years=-1):
    """지난해 같은 창 (비교 기준 '지난해 같은 달')."""
    off = pd.DateOffset(years=years)
    return (pd.Timestamp(start) + off).strftime("%Y-%m-%d"), (pd.Timestamp(end) + off).strftime("%Y-%m-%d")


def guard(start, end, today=None):
    """창의 하루 전 조류가 no-peek 날짜 뒤에 있으면, 창이 끝나기 전에는 읽지 못하게 막는다."""
    today = pd.Timestamp.now(tz="UTC") if today is None else pd.Timestamp(today, tz="UTC")
    if pd.Timestamp(end, tz="UTC") > NO_PEEK_FROM and today < pd.Timestamp(end, tz="UTC"):
        raise RuntimeError(f"V5 창({start}~{end})이 끝나기 전에는 {NO_PEEK_FROM.date()} 이후 하루 전 조류를 읽지 않음 (spec no_peek)")


def era5_window(paths, hours):
    """여러 ERA5 파일을 이어 붙여 창의 시간만 고른다 (시각은 tz 없는 UTC)."""
    import xarray as xr
    parts = [xr.open_dataset(RAW / p) for p in paths]
    ds = xr.concat([d.drop_vars("height") for d in parts], dim="time")
    ds = ds.sel(time=~ds.get_index("time").duplicated())
    ds = ds.sel(time=hours.tz_convert(None))
    ds["height"] = parts[0]["height"]
    if ds.sizes["time"] != len(hours):
        raise ValueError(f"ERA5 시간 {ds.sizes['time']} ≠ 창 {len(hours)}")
    return ds.load()


def build_network_window(name):
    """창 이름(WINDOWS)의 3구역망과 기록. backcast.build_network_2025(corrected=True)와 같은 방법."""
    from gbess.system.fleet import BB, build_fleet, load_bb, load_cfg
    from gbess.system.inputs import EMB_SCOT_WIND_SHARE, renewable_cf, scale_scot_onshore
    from gbess.system.network import Gen, Network
    start, end, fy, dem_files, era5_files = WINDOWS[name]
    hours = window_hours(start, end)
    f = build_fleet(year=fy, window1=False, **FES_INPUTS[fy])
    zones = f["zones"]
    fc, zc = load_cfg()
    bb = load_bb(zc, BB)
    d = bb[bb["Building Block ID Number"] == fc["demand"]["bb"]].groupby("zone")[fy].sum()
    scot_ns = {"N": d["N"] / (d["N"] + d["S"]), "S": d["S"] / (d["N"] + d["S"])}
    h = bc.demand_hourly([RAW / p for p in dem_files], hours)
    dem = bc.zone_demand_embedded_split(h, zones, scot_ns, EMB_SCOT_WIND_SHARE) - bc.interconnector_injection(h, zones)
    cf, diag = renewable_cf(era5_window(era5_files, hours), zones, sites=bc.OFFSHORE_SITES_2025)
    scale_scot_onshore(cf, zones)
    cf["solar"] = np.tile(bc.solar_cf(h), (len(zones), 1))
    nuc_cap = sum(g.cap for g in f["gens"] if g.name.startswith("nuclear_"))
    nuc = (bc.fuelhh_hourly("NUCLEAR", hours=hours) / nuc_cap).clip(0, 1)
    hyd = bc.fuelhh_hourly("NPSHYD", hours=hours)
    hyd = (hyd / hyd.max()).clip(0, 1)
    gens = []
    for g in f["gens"]:
        if g.name.startswith("nuclear_"):
            av = nuc.to_numpy()
        elif g.name.startswith("hydro_"):
            av = hyd.to_numpy()
        else:
            av = None if g.avail is None else np.full(len(hours), float(np.ravel(g.avail)[0]))
        gens.append(Gen(g.name, g.zone, g.cap, g.cost, av))
    for k, caps in f["renewable_mw"].items():
        for i, z in enumerate(zones):
            if caps[z] > 0:
                gens.append(Gen(f"{k}_{z}", i, caps[z], 0.0, cf[k][i], renewable=True))
    lim, filled = bc.observed_limits(hours=hours)
    net = Network(zones, dem, lim, gens, f["stores"])
    meta = {"window": [start, end], "fes_year": fy, "hours": len(hours), "scot_ns": scot_ns,
            "limits_filled_hours": filled, "cf_mean": {k: [float(x) for x in np.asarray(v).mean(axis=1)] for k, v in cf.items()},
            "nuclear_twh": float((nuc * nuc_cap).sum() / 1e6), "interconnector_net_import_twh":
            float(bc.interconnector_injection(h, zones).sum() / 1e6), "inputs": [str(RAW / p) for p in dem_files + era5_files]}
    return net, hours, meta


def metrics(flows_limits):
    """{'B4': 표, 'B6': 표} (열 flow, limit, 1시간) → 제약 발생 비율과 B4·B6 큰 쪽 초과량 TWh."""
    row = {f"{b}_binding": obs.binding_stats(t)["binding"] for b, t in flows_limits.items()}
    row["exceed_twh"] = float(obs.joint_exceedance(flows_limits["B4"], flows_limits["B6"]).sum() / 1e6)
    return row


def observed_window(start, end, today=None):
    guard(start, end, today)
    s, e = pd.Timestamp(start, tz="UTC"), pd.Timestamp(end, tz="UTC")
    hb = {}
    for b in ("B4", "B6"):
        x = obs.hourly(obs.da_flows(b))
        hb[b] = x[(x.index >= s) & (x.index < e)]
    return metrics(hb), {b: len(t) for b, t in hb.items()}


def v5_table(model, observed, persistence, spec_v5):
    """규칙 결과(제약 발생 비율 ±tol, 초과량 비율 띠)와 지난해 같은 창 단순 예측의 오차(보고만)."""
    tol, (lo, hi) = spec_v5["binding_tol_abs"], spec_v5["exceedance_ratio_band"]
    rows = []
    for b in ("B6", "B4"):
        k = f"{b}_binding"
        m, o, p = model[k], observed[k], persistence[k]
        rows.append({"metric": f"V5 {b} 제약 발생 비율", "model": m, "observed": o, "criterion": f"±{tol:.2f}",
                     "pass": abs(m - o) <= tol, "persistence": p, "model_abs_err": abs(m - o),
                     "persistence_abs_err": abs(p - o)})
    m, o, p = model["exceed_twh"], observed["exceed_twh"], persistence["exceed_twh"]
    rows.append({"metric": "V5 B4·B6 큰 쪽 초과량 TWh", "model": m, "observed": o, "criterion": f"비율 {lo}~{hi}",
                 "ratio": m / o, "pass": lo <= m / o <= hi, "persistence": p, "persistence_ratio": p / o,
                 "model_abs_err": abs(m - o), "persistence_abs_err": abs(p - o)})
    return pd.DataFrame(rows)


def run(name="dry", out=None, log=print, today=None):
    from gbess.system.run_m1 import SPEC, file_sha256, git_commit, load_spec
    from gbess.system.stage1 import solve_stage1
    start, end = WINDOWS[name][:2]
    o_row, o_hours = observed_window(start, end, today)          # 막혀 있으면 모형을 풀기 전에 멈춤
    p_row, p_hours = observed_window(*shift_year(start, end), today)
    t0 = time.perf_counter()
    net, hours, meta = build_network_window(name)
    log(f"입력 {time.perf_counter() - t0:.0f}s: {json.dumps(meta, ensure_ascii=False)}")
    plan = solve_stage1(net)
    log(f"1단계 {plan.status} {time.perf_counter() - t0:.0f}s")
    fl = {b: pd.DataFrame({"flow": plan.flows[i], "limit": net.limits[i]}, index=hours) for i, b in enumerate(("B4", "B6"))}
    m_row = metrics(fl)
    spec = load_spec()
    t = v5_table(m_row, o_row, p_row, spec["validation"]["V5_holdout"])
    out = Path(out or OUT / f"v5_{name}")
    out.mkdir(parents=True, exist_ok=True)
    t.to_csv(out / "v5.csv", index=False)
    pd.DataFrame({"t": hours, "flow_B4": plan.flows[0], "flow_B6": plan.flows[1], "limit_B4": net.limits[0],
                  "limit_B6": net.limits[1], "lambda": plan.prices}).to_csv(out / "hourly.csv", index=False)
    rec = {"git_commit": git_commit(), "spec_sha256": file_sha256(SPEC),
           "input_sha256": {p: file_sha256(p) for p in meta["inputs"]}, "solver_status": plan.status,
           "solve_seconds": time.perf_counter() - t0, "meta": meta, "model": m_row, "observed": o_row,
           "observed_hours": o_hours, "persistence_window": shift_year(start, end), "persistence": p_row,
           "persistence_hours": p_hours}
    (out / "run.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return t, rec


if __name__ == "__main__":
    t, _ = run(sys.argv[1] if len(sys.argv) > 1 else "dry")
    print(t.to_string(index=False))
