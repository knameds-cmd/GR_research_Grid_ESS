"""
2030년 설비 구성 (T4, M1-2). gbess/config/fleet_2030.yaml과 zones.yaml을 읽어 FES 2025 Building Blocks(Holistic Transition,
2030)의 기술별 설비를 3구역으로 나누고, Window 1 잠정 16건과 기존 양수 4곳을 실제 사양으로 더한다.

    from gbess.system.fleet import build_fleet
    f = build_fleet()            # f["gens"]: [network.Gen(재생은 avail=None)], f["stores"], f["demand_gwh"], f["renewable_mw"]

한계비용(£/MWh) = 연료가 ÷ 효율 + 탄소가 × 배출계수 ÷ 효율 + 가변 운영비 (marginal_cost).
"""
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from gbess.engine.asset import load_technologies
from gbess.system.network import Gen, Store

ROOT = Path(__file__).resolve().parents[2]
CFG = ROOT / "gbess" / "config"
BB = ROOT / "data" / "raw" / "system" / "fes2025_bb1_v006.csv"
W1 = ROOT / "literature" / "sources" / "ldes" / "window1_projects.csv"
PATHWAY, YEAR = "Holistic Transition", "2030"


def load_cfg():
    fleet = yaml.safe_load((CFG / "fleet_2030.yaml").read_text(encoding="utf-8"))
    zones = yaml.safe_load((CFG / "zones.yaml").read_text(encoding="utf-8"))
    return fleet, zones


def v(x):
    return x["value"] if isinstance(x, dict) else x


def zone_ids(zones):
    return [z["id"] for z in zones["zones"]]


def load_bb(zones, path=BB):
    b = pd.read_csv(path)
    b = b[b["FES Pathway"] == PATHWAY]
    area_zone = {a: z["id"] for z in zones["zones"] for a in z["fes_areas"]}
    b = b.assign(zone=b["DNO License Area"].map(area_zone))
    unknown = set(b.loc[b["zone"].isna(), "DNO License Area"]) - {"Not Connected"}
    if unknown:
        raise ValueError(f"구역에 배정되지 않은 FES 지역: {unknown}")
    return b.dropna(subset=["zone"])


def bb_by_zone(bb, ids, zones_order):
    s = bb[bb["Building Block ID Number"].isin(ids)].groupby("zone")[YEAR].sum()
    return {z: float(s.get(z, 0.0)) for z in zones_order}


def marginal_cost(tech, fuel_cfg):
    vom = v(tech["vom"])
    fuel = tech.get("fuel", "none")
    if fuel == "none":
        return vom
    eta = v(tech["efficiency"])
    price = {"gas": v(fuel_cfg["gas_gbp_mwh_lhv"]), "oil": v(fuel_cfg["oil_light_gbp_mwh_lhv"]),
             "biomass": v(fuel_cfg["biomass_gbp_mwh"])}[fuel]
    ef = {"gas": v(fuel_cfg["ef_gas_t_mwh"]), "oil": v(fuel_cfg["ef_oil_t_mwh"]), "biomass": 0.0}[fuel]
    return price / eta + v(fuel_cfg["carbon_gbp_t"]) * ef / eta + vom


def _store(name, zone, p_mw, hours, rte, var_cost, soc0, tags=()):
    eta = float(np.sqrt(rte))
    return Store(name, zone, p_mw, p_mw, p_mw * hours / eta, eta, eta, soc0, var_cost, frozenset(tags))


def window1_projects(include_post_2030=True, path=W1):
    w = pd.read_csv(path)
    w = w[w["minded_to"] == 1]
    if not include_post_2030:
        w = w[w["first_operation"] <= 2030]
    return w


def build_fleet(include_post_2030=True, bb_path=BB):
    fc, zc = load_cfg()
    Z = zone_ids(zc)
    zi = {z: i for i, z in enumerate(Z)}
    bb = load_bb(zc, bb_path)
    gens, stores = [], []
    for key, t in fc["thermal"].items():
        if not isinstance(t, dict):
            continue
        cap = bb_by_zone(bb, t["bb"], Z)
        mc = marginal_cost(t, fc["fuel"])
        av = v(t["availability"]) if "availability" in t else None
        for z, mw in cap.items():
            if mw > 0:
                gens.append(Gen(f"{key}_{z}", zi[z], mw, mc, None if av is None else np.full(1, av)))
    ren = {k: bb_by_zone(bb, r["bb"], Z) for k, r in fc["renewables"].items()}

    st = fc["storage"]
    soc0 = st["soc0"]
    b = st["batteries"]
    bat = bb_by_zone(bb, b["bb"], Z)
    for z, mw in bat.items():
        for h, sh in zip(b["durations_h"], v(b["shares"])):
            if mw * sh > 0:
                stores.append(_store(f"bess{h}h_{z}", zi[z], mw * sh, h, v(b["rte"]), v(b["var_cost"]), soc0))
    o = st["other_laes"]
    for z, mw in bb_by_zone(bb, o["bb"], Z).items():
        if mw > 0:
            stores.append(_store(f"laes_{z}", zi[z], mw, v(o["duration_h"]), v(o["rte"]), o["var_cost"], soc0))
    tech = load_technologies()
    for name, e in st["existing_psh"].items():
        if "tech_key" in e:
            a = tech[e["tech_key"]]
            stores.append(Store(name, zi[e["zone"]], a.p_ch_mw, a.p_dis_mw, a.e_mwh, a.eta_ch, a.eta_dis,
                                soc0, a.var_cost, frozenset({"existing_psh"})))
        else:
            eta = float(np.sqrt(v(e["rte"])))
            stores.append(Store(name, zi[e["zone"]], v(e["p_mw"]), v(e["p_mw"]), v(e["e_mwh_discharge"]) / eta, eta, eta,
                                soc0, e["var_cost"], frozenset({"existing_psh"})))
    w1 = fc["window1"]
    projects = []
    for _, r in window1_projects(include_post_2030).iterrows():
        z = w1["zone_by_region"].get(r["region"], w1["zone_by_region"]["default"])
        tags = {"w1"} | ({"north"} if z == "N" else set())
        stores.append(_store(r["project"], zi[z], r["mw"], r["duration_h"], r["rte_pct"] / 100,
                             w1["var_cost_by_tech"][r["technology"]], soc0, tags))
        projects.append((r["project"], r["technology"], r["mw"], r["duration_h"]))
    return {"zones": Z, "gens": gens, "stores": stores, "renewable_mw": ren,
            "demand_gwh": bb_by_zone(bb, [fc["demand"]["bb"]], Z), "w1_projects": projects}


def summary(f):
    rows = [{"kind": "gen", "name": g.name, "zone": f["zones"][g.zone], "mw": g.cap, "cost": g.cost} for g in f["gens"]]
    rows += [{"kind": "store", "name": s.name, "zone": f["zones"][s.zone], "mw": s.p_dis, "mwh": s.e_mwh * s.eta_dis,
              "rte": s.eta_ch * s.eta_dis, "tags": ",".join(sorted(s.tags))} for s in f["stores"]]
    for k, d in f["renewable_mw"].items():
        rows += [{"kind": "renewable", "name": f"{k}_{z}", "zone": z, "mw": mw, "cost": 0.0} for z, mw in d.items()]
    return pd.DataFrame(rows)
