"""
2030년 3구역 모형의 입력 (T4, M1-3): 시간별 수요, 풍력·태양광 이용률, 경계 한도를 만들고 network.Network로 조립한다.

    .venv/bin/python -m gbess.system.inputs              # data/processed/system/에 시계열을 만들고 점검표를 출력
    from gbess.system.inputs import build_network_2030
    net, meta = build_network_2030()                    # meta: w1_north, w1_all, levels, bind_boundaries, inputs(파일 목록)

다른 해 기상을 2030년 설비에 입히는 방법: 2013년 ERA5 기상으로 만든 시간별 이용률(0~1)에 FES 2030년 설비 용량을 곱한다.
수요는 2013년 NESO 수요의 시간별 모양에 FES 2030년 구역별 연간 합을 맞춘다. 2013년과 2030년은 윤년이 아니어서 8,760시간이다.
ERA5는 UTC, 수요는 GMT/BST 정산 구간 순서 그대로 8,760시간으로 맞춘다(서머타임 한 시간 차는 무시).

풍력·태양광 이용률 (ERA5 2013, data/raw/system/era5/uk-2013.nc = Zenodo 18325225 "Atlite Cutouts for GB", CC-BY-4.0)
  - 풍속: 100 m 풍속(wnd100m)을 대수 법칙(거칠기 roughness)으로 허브 높이(육상 100 m, 해상 120 m)에 옮긴다.
  - 출력 곡선: 일반화한 곡선. 시동 vi, 정격 vr, 정지 vo에서 P = (v³ − vi³)/(vr³ − vi³) (vi ≤ v < vr), 1 (vr ≤ v < vo).
    육상 3 / 12.5 / 25 m/s, 해상 3.5 / 13 / 30 m/s. 후류·가용률 손실 계수 육상 0.90, 해상 0.88.  (status: placeholder)
  - 태양광: 수평면 일사(influx_direct + influx_diffuse) ÷ 1,000 W/m², 온도 보정 −0.4 %/°C (25 °C 초과). 연간 이용률이
    FES E.08 신규 태양광 가정 11.7%가 되도록 성능 비율을 정한다(경사각 이득을 따로 모형화하지 않으므로).  (status: derived)
  - 구역 배정(근사): 영국 본토 육지 칸을 위도·경도로 나눈다. 스코틀랜드 = 솔웨이(−3.1°, 54.95°)~베릭(−2.0°, 55.8°)을 잇는
    선의 북쪽. N = 스코틀랜드 중 위도 56.25° 이상, 또는 킨타이어·서부 섬(경도 −4.8° 서쪽, 위도 55.3° 이상). 아일랜드 섬은 뺌.
  - 해상풍력: 구역마다 2030년 운전 단지 위치 몇 곳의 가장 가까운 칸을 같은 가중치로 평균한다 (OFFSHORE_SITES). 자료 동쪽 끝이
    경도 1.75°라 Dogger Bank·East Anglia·Norfolk는 동쪽 끝 칸으로 대신한다.
  - 해상풍력 보정: 2013년 터빈 수준의 곡선(정격 13 m/s)으로는 연간 이용률이 약 38%다. 2030년 발전소군에 맞추려고, 설비 가중
    연간 이용률이 목표 = (FES 2025년 설비 × 정격 13 m/s일 때 이용률 + 2025→2030 증가분 × 51%) ÷ 2030년 설비가 되도록
    정격 풍속을 이분법으로 정한다. 51%는 FES E.08 행 18 "Fixed offshore wind" 2025년 착공 가정 이용률.  (status: derived)
"""
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from gbess.system.fleet import CFG, ROOT, build_fleet, v
from gbess.system.network import Gen, Network

RAW = ROOT / "data" / "raw" / "system"
ERA5 = RAW / "era5" / "uk-2013.nc"
DEMAND = RAW / "demanddata_2013.csv"
CALIBRATION = "calibration_2013.json"   # 2013년에 정한 해상 정격 풍속·태양광 성능 비율. 다른 기상연도에 그대로 씀


def era5_path(year):
    return RAW / "era5" / f"uk-{year}.nc"


def demand_path(year):
    return RAW / f"demanddata_{year}.csv"
OUT = ROOT / "data" / "processed" / "system"
T = 8760
WIND = {"onshore": dict(hub=100.0, vi=3.0, vr=12.5, vo=25.0, loss=0.90),
        "offshore": dict(hub=120.0, vi=3.5, vr=13.0, vo=30.0, loss=0.88)}
SOLAR_TARGET_CF = 0.117          # FES 2025 Economics Inputs E.08 행 14 Solar PV assumed load factor
OFFSHORE_SITES = {               # (위도, 경도). 2030년 운전 단지, 연결 송전망으로 구역 배정
    "N": [(58.25, -3.00), (58.18, -2.72), (58.10, -3.10), (56.60, -1.75), (57.22, -1.98), (57.00, -1.87)],
    # Beatrice, Moray East, Moray West, Seagreen(Tealing, SSEN), Aberdeen EOWDC, Kincardine
    "S": [(56.27, -2.30), (56.47, -2.25), (56.10, -2.20)],
    # Neart na Gaoithe, Inch Cape, Berwick Bank (SPT 연결)
    "EW": [(54.85, 1.90), (53.90, 1.80), (52.20, 2.50), (52.90, 2.30), (51.63, 1.50), (54.05, -3.60), (53.50, 0.85),
           (50.67, -0.27)],
    # Dogger Bank, Hornsea, East Anglia, Norfolk, London Array, 아일랜드해(Walney), Triton Knoll, Rampion
}


# ---------------------------------------------------------------------------------------------------------------
def demand_shapes(path=DEMAND, underlying=False):
    """(EW, 스코틀랜드) 1시간 평균 MW 모양, 길이 8,760 (윤년은 12월 31일을 뺌).
    underlying=False: EW = ENGLAND_WALES_DEMAND, 스코틀랜드 = ND − EW (2013년 주 결과).
    underlying=True: 배전망 풍력·태양광이 줄여 준 몫을 되돌린 실제 소비 GB = ND + EMBEDDED_WIND + EMBEDDED_SOLAR를
    시간마다 EW/ND 비율로 나눔. 배전망 태양광이 큰 해(2020년 13 GW)에는 모형의 태양광 발전기와 두 번 세지 않으려고 쓴다."""
    d = pd.read_csv(path)
    ew = d["ENGLAND_WALES_DEMAND"].to_numpy(float)
    sc = d["ND"].to_numpy(float) - ew
    if underlying:
        nd = d["ND"].to_numpy(float)
        gb = nd + d["EMBEDDED_WIND_GENERATION"].to_numpy(float) + d["EMBEDDED_SOLAR_GENERATION"].to_numpy(float)
        ew, sc = gb * ew / nd, gb * (1 - ew / nd)
    n = len(d) // 2 * 2
    ew, sc = ew[:n].reshape(-1, 2).mean(1), sc[:n].reshape(-1, 2).mean(1)
    if len(ew) < T:
        raise ValueError(f"수요 시간 수 {len(ew)} < {T}")
    return ew[:T], sc[:T]


def zone_demand(annual_gwh, zones, path=DEMAND, underlying=False):
    ew, sc = demand_shapes(path, underlying)
    rows = []
    for z in zones:
        shape = ew if z == "EW" else sc
        rows.append(shape / shape.sum() * annual_gwh[z] * 1e3)
    return np.vstack(rows)


def zone_of(lat, lon):
    """근사 구역: 'N', 'S', 'EW' 또는 None(영국 본토 밖)."""
    if lon < -5.8 and lat < 55.45:                       # 북아일랜드·아일랜드
        return None
    if lon < -8.0:
        return None
    border = 54.95 + (lon + 3.1) * (55.8 - 54.95) / (-2.0 + 3.1)
    scot = lat > border if lon < -1.8 else lat > 55.8
    if not scot:
        return "EW"
    if lat >= 56.25 or (lon < -4.8 and lat >= 55.3):
        return "N"
    return "S"


def power_curve(v, vi, vr, vo):
    p = np.clip((v ** 3 - vi ** 3) / (vr ** 3 - vi ** 3), 0.0, 1.0)
    return np.where((v < vi) | (v >= vo), 0.0, p)


def wind_cf(wnd100, z0, kind, vr=None):
    w = WIND[kind]
    z0 = np.maximum(z0, 1e-4)
    vh = wnd100 * np.log(w["hub"] / z0) / np.log(100.0 / z0)
    return power_curve(vh, w["vi"], w["vr"] if vr is None else vr, w["vo"]) * w["loss"]


def renewable_cf(path=ERA5, zones=("N", "S", "EW"), offshore_vr=None, solar_pr=None, sites=None):
    """{'onshore_wind': (Z, T), 'offshore_wind': (Z, T), 'solar': (Z, T)} 이용률과 칸 수 진단.
    sites: 해상 단지 위치(기본 OFFSHORE_SITES). 일사 변수가 없는 파일(gbess.system.era5_ncar)이면 'solar'를 빼고 돌려준다."""
    sites = OFFSHORE_SITES if sites is None else sites
    import xarray as xr
    ds = xr.open_dataset(path)
    ds = ds.isel(time=slice(0, T))
    lat, lon = ds["y"].values, ds["x"].values
    height = ds["height"].values if "height" in ds else None
    LON, LAT = np.meshgrid(lon, lat)
    land = height > 1.0 if height is not None else np.ones_like(LAT, bool)
    zone_grid = np.vectorize(zone_of)(LAT, LON)
    w100 = ds["wnd100m"].values                          # (T, y, x)
    z0 = ds["roughness"].values
    z0 = z0 if z0.ndim == 3 else np.broadcast_to(z0, w100.shape)
    cf_on = wind_cf(w100, z0, "onshore")
    has_solar = "influx_direct" in ds
    if has_solar:
        ghi = (ds["influx_direct"].values + ds["influx_diffuse"].values) / 1000.0
        tc = ds["temperature"].values - 273.15 if "temperature" in ds else np.full_like(ghi, 15.0)
        pv_raw = np.clip(ghi * (1 - 0.004 * np.maximum(tc - 25.0, 0.0)), 0, None)
    out = {k: np.zeros((len(zones), T)) for k in ("onshore_wind", "offshore_wind", "solar")}
    diag = {}
    for i, z in enumerate(zones):
        m = land & (zone_grid == z)
        diag[z] = int(m.sum())
        out["onshore_wind"][i] = cf_on[:, m].mean(axis=1)
        if has_solar:
            out["solar"][i] = pv_raw[:, m].mean(axis=1)
        cells = []
        for la, lo in sites[z]:
            iy, ix = int(np.abs(lat - la).argmin()), int(np.abs(lon - lo).argmin())
            cells.append(wind_cf(w100[:, iy, ix], z0[:, iy, ix], "offshore", offshore_vr))
        out["offshore_wind"][i] = np.mean(cells, axis=0) if cells else 0.0
    if not has_solar:
        del out["solar"]
        ds.close()
        return out, diag
    pr = SOLAR_TARGET_CF / out["solar"].mean() if solar_pr is None else solar_pr
    out["solar"] = np.clip(out["solar"] * pr, 0, 1)
    diag["solar_performance_ratio"] = float(pr)
    ds.close()
    return out, diag


OFFSHORE_NEW_CF = 0.51           # FES 2025 Economics Inputs E.08 행 18 Fixed offshore wind, 2025년 착공 가정 이용률


def offshore_target_cf(cf_2013_level, path=None):
    from gbess.system.fleet import BB, PATHWAY
    b = pd.read_csv(path or BB)
    h = b[(b["FES Pathway"] == PATHWAY) & (b["Building Block ID Number"] == "Gen_BB014")]
    c25, c30 = h["2025"].sum(), h["2030"].sum()
    return (c25 * cf_2013_level + (c30 - c25) * OFFSHORE_NEW_CF) / c30


def write_processed(zones=("N", "S", "EW"), year=2013):
    """2013년은 해상 정격 풍속·태양광 성능 비율을 정해 calibration_2013.json에 남긴다. 다른 해는 그 값을 그대로 쓰고,
    수요 모양은 배전망 발전을 되돌린 실제 소비(underlying)로 만든다."""
    import json
    f = build_fleet()
    if year != 2013:
        cal = json.loads((OUT / CALIBRATION).read_text())
        dem = zone_demand(f["demand_gwh"], zones, demand_path(year), underlying=True)
        cf, diag = renewable_cf(era5_path(year), zones, offshore_vr=cal["offshore_vr"], solar_pr=cal["solar_performance_ratio"])
        diag.update(calibration=cal)
        _save(zones, year, dem, cf)
        return dem, cf, diag
    dem = zone_demand(f["demand_gwh"], zones)
    w = np.array([f["renewable_mw"]["offshore_wind"][z] for z in zones])
    cf, diag = renewable_cf(zones=zones)
    level = float(w @ cf["offshore_wind"].mean(axis=1) / w.sum())
    target = offshore_target_cf(level)
    lo, hi = 8.0, WIND["offshore"]["vr"]
    for _ in range(25):                 # 정격 풍속이 낮을수록 이용률이 높다
        mid = (lo + hi) / 2
        c, _d = renewable_cf(zones=zones, offshore_vr=mid)
        if float(w @ c["offshore_wind"].mean(axis=1) / w.sum()) > target:
            lo = mid
        else:
            hi = mid
    cf["offshore_wind"] = c["offshore_wind"]
    diag.update(offshore_cf_2013_level=level, offshore_target=target, offshore_vr=mid,
                offshore_cf=float(w @ c["offshore_wind"].mean(axis=1) / w.sum()))
    _save(zones, 2013, dem, cf)
    (OUT / CALIBRATION).write_text(json.dumps({"offshore_vr": mid, "solar_performance_ratio": diag["solar_performance_ratio"],
                                               "offshore_target": target, "offshore_cf_2013_level": level}, indent=1))
    return dem, cf, diag


def processed_files(year):
    return [OUT / f"demand_2030_mw_{year}.csv"] + [OUT / f"cf_{k}_{year}.csv" for k in ("onshore_wind", "offshore_wind", "solar")]


def _save(zones, year, dem, cf):
    OUT.mkdir(parents=True, exist_ok=True)
    idx = pd.RangeIndex(T, name="hour")
    pd.DataFrame(dem.T, index=idx, columns=zones).to_csv(OUT / f"demand_2030_mw_{year}.csv")
    for k, a in cf.items():
        pd.DataFrame(a.T, index=idx, columns=zones).to_csv(OUT / f"cf_{k}_{year}.csv")


def load_processed(zones=("N", "S", "EW"), year=2013):
    dem = pd.read_csv(OUT / f"demand_2030_mw_{year}.csv", index_col=0)[list(zones)].to_numpy().T
    cf = {k: pd.read_csv(OUT / f"cf_{k}_{year}.csv", index_col=0)[list(zones)].to_numpy().T
          for k in ("onshore_wind", "offshore_wind", "solar")}
    return dem, cf


def boundary_limits(mult=1.0, nominal=False):
    zc = yaml.safe_load((CFG / "zones.yaml").read_text(encoding="utf-8"))
    key = "etys_2030_mw" if nominal else "limit_2030_mw"
    return np.array([v(b[key]) for b in zc["boundaries"]]) * mult


def build_network_2030(limit_mult=1.0, include_post_2030=True, nominal_limits=False, weather_year=2013):
    f = build_fleet(include_post_2030=include_post_2030)
    zones = f["zones"]
    dem, cf = load_processed(zones, weather_year)
    gens = []
    for g in f["gens"]:
        av = None if g.avail is None else np.full(T, float(np.ravel(g.avail)[0]))
        gens.append(Gen(g.name, g.zone, g.cap, g.cost, av))
    for k, caps in f["renewable_mw"].items():
        for i, z in enumerate(zones):
            if caps[z] > 0:
                gens.append(Gen(f"{k}_{z}", i, caps[z], 0.0, cf[k][i], renewable=True))
    net = Network(zones, dem, boundary_limits(limit_mult, nominal_limits), gens, f["stores"])
    from gbess.system.run_m1 import floor_cap_levels
    meta = {"w1_north": net.store_names("north"), "w1_all": net.store_names("w1"),
            "levels": floor_cap_levels(f["w1_projects"]), "bind_boundaries": [0, 1],
            "inputs": processed_files(weather_year) + [CFG / "zones.yaml", CFG / "fleet_2030.yaml",
                                                      RAW / "fes2025_bb1_v006.csv"]}
    return net, meta


def checklist(net, f=None):
    """입력 점검표: 구역별 수요·설비·이용률."""
    rows = []
    for i, z in enumerate(net.zones):
        rows.append({"zone": z, "demand_twh": net.demand[i].sum() / 1e6, "peak_gw": net.demand[i].max() / 1e3})
    df = pd.DataFrame(rows)
    ren = {}
    for g in net.gens:
        if g.renewable:
            ren[g.name] = {"mw": g.cap, "cf": float(np.mean(g.avail))}
    return df, pd.DataFrame(ren).T


if __name__ == "__main__":
    import sys
    pd.set_option("display.width", 200)
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2013
    dem, cf, diag = write_processed(year=year)
    print("칸 수·보정", diag)
    net, meta = build_network_2030(weather_year=year)
    d, r = checklist(net)
    print(d.round(2).to_string(index=False))
    print(r.round(3).to_string())
