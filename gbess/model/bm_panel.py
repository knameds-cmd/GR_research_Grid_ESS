"""
BM 채택 모형의 자료: 유닛 × 결제구간 패널. 한 행 = "이 유닛이 이 구간에 이 단가로 이만큼 여유를 내놓았고, NESO가 그중 얼마를 받았나".

    from gbess.model.bm_panel import panel
    p = panel(2019)     # 양수 16기. data/processed/bm_panel/bm_panel_2019.parquet에 저장해 두고 다시 쓴다

열
  t, bmUnit, site(DINO 등), scotland
  fpn_mw          PN의 구간 평균 (발전 +, 양수 −)
  mel_mw, mil_mw  가용 최대 출력, 최대 입력(음수 그대로)
  head_up_mw      max(MEL − FPN, 0): offer로 올릴 수 있는 폭 (양수 중이면 양수를 멈추는 것도 포함)
  head_dn_mw      max(FPN − MIL, 0): bid로 내릴 수 있는 폭 (발전을 줄이거나 양수를 늘리는 것)
  offer_price     BOD pair +1의 offer 단가 = 출력을 올리는 첫 단가
  bid_price       BOD pair −1의 bid 단가 = 출력을 내리는 첫 단가 (pair −1이 없으면 pair +1의 bid)
  offer_mwh, bid_mwh   그 구간에 받은 Tagged 물량(정산과 짝, bid는 양수). 목표 변수
  offer_paid, bid_paid 받은 물량의 평균 단가 (현금흐름 ÷ 물량). 입찰 단가와 맞는지 검산용
  + gbess.data.bm_state의 계통 상태 열. 지역 물량 열(ew_offer_mwh 등)에서는 이 유닛이 속한 발전소 몫을 뺀다
"""
from pathlib import Path

import numpy as np
import pandas as pd

from gbess.data.availability import _unit_sp_mean
from gbess.data.bm_state import _monthly, state, unit_bm
from gbess.data.prices import _utc, index
from gbess.data.units import storage_units
from gbess.realized.physical import sp_energy

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "processed" / "bm_panel"


def _bod_first_pairs(bod, idx):
    b = bod.assign(t=pd.to_datetime(bod["timeFrom"], utc=True))
    b = b[(b["t"] >= idx[0]) & (b["t"] <= idx[-1])]
    up = b[b["pairId"] == 1].drop_duplicates(["bmUnit", "t"], keep="last").set_index(["bmUnit", "t"])
    dn = b[b["pairId"] == -1].drop_duplicates(["bmUnit", "t"], keep="last").set_index(["bmUnit", "t"])
    out = pd.DataFrame({"offer_price": up["offer"]})
    out = out.join(dn["bid"].rename("bid_price"), how="outer")
    out["bid_price"] = out["bid_price"].fillna(up["bid"].reindex(out.index))
    return out


def _build(year, units):
    start, end = f"{year}-01-01", f"{year + 1}-01-01"
    idx = index(start, end)
    pn = _monthly("pn_psh", start, end)
    mel, mil = _monthly("mels_psh", start, end), _monthly("mils_psh", start, end)
    bod = _monthly("bod_psh", start, end)
    e = sp_energy(pn[pn["bmUnit"].isin(units["bmUnit"])], pn.iloc[:0].assign(acceptanceTime=[], acceptanceNumber=[]),
                  _utc(start), _utc(end))
    rows = []
    for _, u in units.iterrows():
        a, _m1 = _unit_sp_mean(mel[mel["bmUnit"] == u["bmUnit"]], start, end)
        b, _m2 = _unit_sp_mean(mil[mil["bmUnit"] == u["bmUnit"]], start, end)
        f = e[e["bmUnit"] == u["bmUnit"]].set_index("start_utc")["pn_mwh"].reindex(idx).fillna(0.0) * 2
        rows.append(pd.DataFrame({"t": idx, "bmUnit": u["bmUnit"], "fpn_mw": f.to_numpy(),
                                  "mel_mw": np.clip(a, 0, None), "mil_mw": np.clip(b, None, 0)}))
    p = pd.concat(rows, ignore_index=True)
    p["head_up_mw"] = np.clip(p["mel_mw"] - p["fpn_mw"], 0, None)
    p["head_dn_mw"] = np.clip(p["fpn_mw"] - p["mil_mw"], 0, None)
    p = p.join(_bod_first_pairs(bod, idx), on=["bmUnit", "t"])

    acc = unit_bm(start, end)
    acc = acc[acc["bmUnit"].isin(units["bmUnit"])]
    for side in ("offer", "bid"):
        a = acc[acc["side"] == side].set_index(["bmUnit", "t"])
        p = p.join(a["mwh"].rename(f"{side}_mwh"), on=["bmUnit", "t"]).join(a["price"].rename(f"{side}_paid"),
                                                                           on=["bmUnit", "t"])
        p[f"{side}_mwh"] = p[f"{side}_mwh"].fillna(0.0)
    p["site"] = p["bmUnit"].str.extract(r"_([A-Z]+)-")[0]
    p["scotland"] = p["bmUnit"].map(units.set_index("bmUnit")["scotland"])

    st = state(year)
    p = p.join(st, on="t")
    # 지역 물량에서 같은 발전소 몫을 뺀다 (자기 결과로 자기를 설명하지 않게)
    site_tot = p.groupby(["site", "t"])[["offer_mwh", "bid_mwh"]].transform("sum")
    for side in ("offer", "bid"):
        own_region = np.where(p["scotland"], f"sc_{side}_mwh", f"ew_{side}_mwh")
        for r in ("ew", "sc"):
            col = f"{r}_{side}_mwh"
            p[col] = p[col] - np.where(own_region == col, site_tot[f"{side}_mwh"], 0.0)
    return p


def panel(year, force=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"bm_panel_{year}.parquet"
    if path.exists() and not force:
        return pd.read_parquet(path)
    u = storage_units()
    p = _build(year, u[u["tech"] == "psh"])
    p.to_parquet(path, index=False)
    return p


def _one(year):
    state(year, force=True)
    return year, len(panel(year, force=True))


def main(argv=None):
    """.venv/bin/python -m gbess.model.bm_panel 2017 2026   (상태표와 패널을 그 해들에 대해 다시 만든다)"""
    import sys
    from concurrent.futures import ProcessPoolExecutor
    a = sys.argv[1:] if argv is None else argv
    years = range(int(a[0]), int(a[1]) + 1)
    with ProcessPoolExecutor(6) as ex:
        for y, n in ex.map(_one, years):
            print(y, f"{n:,}행", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
