"""
BM 채택 모형: "이 자산이 이 구간에 이 단가로 여유를 내놓으면 NESO가 그중 몇 %를 받아 주나".

    .venv/bin/python -m gbess.model.bm_accept          # 검증 A·B를 돌리고 results/validation/bm_accept_*.csv를 쓴다

왜 필요한가 (09 문서 5.6): 기준 무리의 MW당 지시량 × κ로는 실제 Dinorwig의 BM 물량 증가(2017→2024 세 배)를 설명하지
못했다. 패널(gbess.model.bm_panel)을 보면 그 사이 Dinorwig의 offer 단가는 "그 구간 잉글랜드·웨일스에서 받아 준 offer
단가의 90% 분위수"보다 £85 높던 것이 £0 안팎으로 내려왔다. 즉 지시량은 자산 자신의 단가 경쟁력에 달려 있고, 이 경쟁력은
자산마다 다르다. 기준 무리의 평균 지시량은 이것을 담지 못한다.

모형 (방향 s = offer, bid 각각)
    y = 받은 물량 ÷ (여유 MW × 0.5h), 0~1         여유 = offer는 MEL − FPN, bid는 FPN − MIL
    E[y | x] = 1 / (1 + exp(−x·β))                  분수 로짓 (Papke–Wooldridge). 여유 MW로 가중해 물량 오차를 줄인다
  x (모두 그 구간에 관측되는 값)
    경쟁력  offer: 자기 단가 − 잉글랜드·웨일스 받아 준 offer 90% 분위수 (낮을수록 유리)
            bid:   자기 단가 − 받아 준 bid 10% 분위수 (높을수록 유리). 스코틀랜드 유닛은 스코틀랜드 분위수도 함께
            조각선형(꺾는 점 −100, −30, 0, 30, 100 £/MWh)으로 넣어 "한계 근처에서 급히 변하는" 모양을 허용한다
    도매 대비 단가 (자기 단가 − MID), 순불균형량, 같은 지역의 다른 유닛이 받은 물량(자기 발전소 몫 제외),
    풍력·풍력 변화·총발전 변화, 스코틀랜드 풍력 bid 물량(제약 대용) × 스코틀랜드 여부, 시각(조화항), 주말
  설명변수 선택 기록 (2026-10-25, 결과를 보고 고친 것이므로 그대로 남긴다)
    v1 위 x + 유닛 정격(로그): 양수 발전소가 넷뿐이라 정격이 지역과 겹쳐, 표본 밖 정격(Dinorwig 288 MW)에서 검증 A의
       bid 예측이 실제의 10배가 됐다 → 정격 제외
    v2 v1 − 정격 + 배터리가 받은 물량: 보정 기간(2017~2020)에 배터리가 거의 없어 계수를 알 수 없는데, 검증 기간에는 값이
       수십 배라 외삽으로 크게 빗나갔다(검증 B Dinorwig offer 오차 101~124%) → 제외. 배터리 경쟁은 이 실증 모형으로는
       보정할 수 없는 변화이며, 검증 B의 오차가 그 크기를 보여 준다
    v3 (현재) v1 − 정격
  변형 둘
    engine: 위 x만. FPN에 따라 달라지는 값이 없으므로 운전 최적화에서 지시 상한 = α·여유 가 FPN에 선형이다
    full:   위 x + 운전 상태(발전·양수·정지) + 여유 ÷ 정격. 엔진 변형이 이것보다 얼마나 덜 맞는지를 기록한다
  비교 모형: 같은 x로 기울기 부스팅(경쟁력에 단조 제약). 로짓이 놓치는 비선형이 얼마나 되는지 본다

검증 (07 문서 T13: 보정 2017~2020, 검증 2021 이후)
    A. 다른 발전소 → Dinorwig: Dinorwig를 뺀 양수 유닛의 2017~2020년으로 맞추고, Dinorwig의 실제 FPN·가용·입찰
       단가를 넣어 2017~2026년 연간 지시 물량을 예측. 유닛도 기간도 표본 밖이다
    B. 같은 발전소, 다른 기간: 양수 16기 전부의 2017~2020년으로 맞추고 2021~2026년을 발전소별로 예측
    C. 발전소 하나 빼기: 나머지 세 발전소의 전 기간으로 맞추고 뺀 발전소를 예측. 새 위치의 가상 자산에 쓰는 상황과 같다
  주 모형은 engine 변형의 기울기 부스팅이다: 단조 제약이 있고 보정 범위 밖에서 평평하게 멈춰 외삽이 덜 위험하다.
  로짓은 계수를 읽을 수 있어 해석용으로 함께 둔다. full 변형은 진단용(부스팅만)
한계 (결과에 기록)
    - 기존 유닛이 받던 지시를 기준으로 한 모형이다. 새 자산이 들어와 지시를 나눠 가지는 효과는 담지 않는다(구조층에서 다룸)
    - 단가는 자산이 정하는 값이다. 검증에서는 실제 입찰 단가를 넣고, 가상 자산에는 입찰 규칙을 따로 정해야 한다
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "validation"
KNOTS = (-100, -30, 0, 30, 100)
KNOTS_SC = (-30, 0, 30)   # 스코틀랜드 유닛은 넷뿐이라 꺾는 점을 줄인다 (첫 시험에서 계수가 ±30으로 불안정)
MIN_HEAD = 5.0
CLIP = 500.0
YEARS = range(2017, 2027)
TRAIN = (2017, 2020)


def _hinges(c, name, knots=KNOTS):
    c = np.clip(c, -CLIP, CLIP)
    out = {f"{name}": c / 100}
    for k in knots:
        out[f"{name}_h{k}"] = np.maximum(c - k, 0) / 100
    return out


def design(p: pd.DataFrame, side: str, variant="engine"):
    """패널 → (X, y, 가중치, 유효 행 마스크). side = "offer" | "bid"."""
    head = p["head_up_mw"] if side == "offer" else p["head_dn_mw"]
    own = p["offer_price"] if side == "offer" else p["bid_price"]
    ok = (head >= MIN_HEAD) & own.notna() & p["mid"].notna() & p["niv_mwh"].notna() & p["wind_mw"].notna()
    q = p[ok]
    head, own = head[ok], own[ok]
    sc = q["scotland"].astype(float).to_numpy()
    x = {}
    if side == "offer":
        ref = q["ew_offer_p90"].fillna(q["mid"] + 100)   # 받아 준 offer가 하나도 없던 구간: 한계가 매우 높다고 본다(희귀)
        x.update(_hinges((own - ref).to_numpy(), "comp"))
        x["no_ref"] = q["ew_offer_p90"].isna().astype(float).to_numpy()
        x["markup"] = np.clip((own - q["mid"]).to_numpy(), -CLIP, CLIP) / 100
        x["niv"] = q["niv_mwh"].to_numpy() / 1000
        x["need_ew"] = q["ew_offer_mwh"].to_numpy() / 1000
        x["need_sc"] = q["sc_offer_mwh"].to_numpy() / 1000
    else:
        ref = q["ew_bid_p10"].fillna(q["mid"] - 100)
        x.update(_hinges((own - ref).to_numpy(), "comp"))
        x["no_ref"] = q["ew_bid_p10"].isna().astype(float).to_numpy()
        ref_sc = q["sc_bid_p10"]
        x.update({k: v * sc for k, v in _hinges((own - ref_sc.fillna(ref)).to_numpy(), "comp_sc", KNOTS_SC).items()})
        x["markup"] = np.clip((q["mid"] - own).to_numpy(), -CLIP, CLIP) / 100
        x["niv"] = -q["niv_mwh"].to_numpy() / 1000
        x["need_ew"] = q["ew_bid_mwh"].to_numpy() / 1000
        x["need_sc"] = q["sc_bid_mwh"].to_numpy() / 1000
    x["wind"] = q["wind_mw"].to_numpy() / 10000
    x["wind_ramp"] = q["wind_ramp_mw"].fillna(0).to_numpy() / 1000
    x["gen_ramp"] = q["gen_ramp_mw"].fillna(0).clip(-5000, 5000).to_numpy() / 1000
    x["sc_wind_bid"] = q["sc_wind_bid_mwh"].to_numpy() / 1000 * sc
    x["scotland"] = sc
    hr = (q["t"].dt.hour + q["t"].dt.minute / 60).to_numpy()
    for k in (1, 2):
        x[f"sin{k}"] = np.sin(2 * np.pi * k * hr / 24)
        x[f"cos{k}"] = np.cos(2 * np.pi * k * hr / 24)
    x["weekend"] = (q["t"].dt.dayofweek >= 5).astype(float).to_numpy()
    if variant == "full":
        x["gen"] = (q["fpn_mw"] > 5).astype(float).to_numpy()
        x["pump"] = (q["fpn_mw"] < -5).astype(float).to_numpy()
        x["head_rel"] = (head / q["unit_mw"]).clip(0, 3).to_numpy()
    X = pd.DataFrame(x, index=q.index)
    mwh = q[f"{side}_mwh"].to_numpy()
    y = np.clip(mwh / (head.to_numpy() * 0.5), 0, 1)
    return X, y, head.to_numpy(), ok


class FracLogit:
    """분수 로짓. 한 행을 (y=1, 가중 w·y)와 (y=0, 가중 w·(1−y)) 두 행으로 나눠 로지스틱 회귀로 푼다."""

    def __init__(self, C=10.0):
        self.C = C

    def fit(self, X, y, w):
        from sklearn.linear_model import LogisticRegression
        self.mu, self.sd = X.mean(), X.std().replace(0, 1)
        Z = ((X - self.mu) / self.sd).to_numpy()
        ZZ = np.vstack([Z, Z])
        yy = np.r_[np.ones(len(y)), np.zeros(len(y))]
        ww = np.r_[w * y, w * (1 - y)]
        self.m = LogisticRegression(C=self.C, max_iter=2000).fit(ZZ, yy, sample_weight=ww / ww.mean())
        self.cols = list(X.columns)
        return self

    def predict(self, X):
        return self.m.predict_proba(((X[self.cols] - self.mu) / self.sd).to_numpy())[:, 1]

    def coefs(self):
        return pd.Series(self.m.coef_[0] / self.sd.to_numpy(), index=self.cols)   # 원래 단위로 되돌린 계수


class FracGBM:
    """같은 분할 요령의 기울기 부스팅. 경쟁력 열에는 단조 제약(offer는 비쌀수록, bid는 쌀수록 덜 받음)."""

    def __init__(self, side):
        self.side = side

    def fit(self, X, y, w):
        from sklearn.ensemble import HistGradientBoostingClassifier
        sign = -1 if self.side == "offer" else 1
        cst = [sign if c.startswith("comp") else 0 for c in X.columns]
        XX = pd.concat([X, X]).to_numpy()
        yy = np.r_[np.ones(len(y)), np.zeros(len(y))]
        ww = np.r_[w * y, w * (1 - y)]
        keep = ww > 0
        self.m = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.08, max_leaf_nodes=31,
                                                monotonic_cst=cst, random_state=0)
        self.m.fit(XX[keep], yy[keep], sample_weight=ww[keep] / ww[keep].mean())
        self.cols = list(X.columns)
        return self

    def predict(self, X):
        return self.m.predict_proba(X[self.cols].to_numpy())[:, 1]


def load_panel(years=YEARS):
    from gbess.data.units import storage_units
    from gbess.model.bm_panel import panel
    P = pd.concat([panel(y) for y in years], ignore_index=True)
    P = P[P["niv_mwh"].notna()]          # 자료 끝(2026-10 이후) 제외
    u = storage_units().set_index("bmUnit")["mw"]
    P["unit_mw"] = P["bmUnit"].map(u)
    P["year"] = P["t"].dt.year
    return P


def fit(P, side, variant="engine", kind="logit"):
    X, y, w, _ = design(P, side, variant)
    m = FracLogit() if kind == "logit" else FracGBM(side)
    return m.fit(X, y, w)


def predict_mwh(m, P, side, variant="engine"):
    """예측 물량(MWh) = α × 여유 × 0.5h. 유효하지 않은 행(여유 < 5 MW 등)은 0."""
    X, y, w, ok = design(P, side, variant)
    out = pd.DataFrame({"pred_mwh": 0.0, "real_mwh": P[f"{side}_mwh"].to_numpy()}, index=P.index)
    out.loc[ok[ok].index, "pred_mwh"] = m.predict(X) * w * 0.5
    return out


def _annual(P, m, side, variant):
    r = predict_mwh(m, P, side, variant)
    r["site"], r["year"] = P["site"], P["year"]
    g = r.groupby(["site", "year"])[["pred_mwh", "real_mwh"]].sum() / 1e3
    g.columns = [f"{side}_pred_gwh", f"{side}_real_gwh"]
    return g


def _sp_metrics(P, m, side, variant):
    """구간 단위: 받았는지(>0.5 MWh)를 α로 얼마나 가려내나(AUC)와 물량 상관."""
    from sklearn.metrics import roc_auc_score
    X, y, w, ok = design(P, side, variant)
    a = m.predict(X)
    hit = (y * w * 0.5) > 0.5
    return {"auc": float(roc_auc_score(hit, a)) if 0 < hit.mean() < 1 else np.nan,
            "corr_mwh": float(np.corrcoef(a * w, y * w)[0, 1]), "rows": int(len(y))}


def validate():
    P = load_panel()
    tr = P["year"].between(*TRAIN)
    rows, coefs, sp = [], {}, []
    tests = [("A", tr & (P["site"] != "DINO"), P["site"] == "DINO"), ("B", tr, ~tr)]
    tests += [(f"C-{s}", P["site"] != s, P["site"] == s) for s in sorted(P["site"].unique())]
    for test, train_mask, pred_mask in tests:
        for variant, kind in (("engine", "gbm"), ("engine", "logit"), ("full", "gbm")):
            if test.startswith("C") and variant == "full":
                continue
            if True:
                g = []
                for side in ("offer", "bid"):
                    m = fit(P[train_mask], side, variant, kind)
                    g.append(_annual(P[pred_mask], m, side, variant))
                    sp.append({"test": test, "variant": variant, "kind": kind, "side": side,
                               **_sp_metrics(P[pred_mask], m, side, variant)})
                    if kind == "logit" and variant == "engine":
                        coefs[(test, side)] = m.coefs()
                    print(f"  {test} {variant} {kind} {side} 완료", flush=True)
                g = pd.concat(g, axis=1).reset_index().assign(test=test, variant=variant, kind=kind)
                rows.append(g)
    a = pd.concat(rows, ignore_index=True)
    a["bm_pred_gwh"] = a["offer_pred_gwh"] + a["bid_pred_gwh"]
    a["bm_real_gwh"] = a["offer_real_gwh"] + a["bid_real_gwh"]
    OUT.mkdir(parents=True, exist_ok=True)
    a.to_csv(OUT / "bm_accept_annual.csv", index=False)
    pd.DataFrame(sp).to_csv(OUT / "bm_accept_sp.csv", index=False)
    pd.DataFrame(coefs).to_csv(OUT / "bm_accept_coefs.csv")
    return a, pd.DataFrame(sp), pd.DataFrame(coefs)


def main():
    a, sp, coefs = validate()
    cols = ["year", "offer_pred_gwh", "offer_real_gwh", "bid_pred_gwh", "bid_real_gwh", "bm_pred_gwh", "bm_real_gwh"]
    summ = []
    for (test, variant, kind, site), h in a.groupby(["test", "variant", "kind", "site"]):
        h = h.sort_values("year")
        err = {f"{c}_mape": float((h[f"{c}_pred_gwh"] / h[f"{c}_real_gwh"] - 1).abs().mean() * 100)
               for c in ("bm", "offer", "bid")}
        summ.append({"test": test, "variant": variant, "kind": kind, "site": site, **err,
                     "total_ratio": float(h["bm_pred_gwh"].sum() / h["bm_real_gwh"].sum())})
        if kind == "gbm" and variant == "engine" and site in ("DINO", "CRUA"):
            print(f"\n== 검증 {test}, {site} (engine, gbm)")
            print(h[cols].round(1).to_string(index=False))
    summ = pd.DataFrame(summ)
    summ.to_csv(OUT / "bm_accept_summary.csv", index=False)
    print("\n연간 물량 평균 절대 오차 %(MAPE)와 전 기간 합계 비(예측 ÷ 실제)")
    print(summ.round(2).to_string(index=False))
    print("\n구간 단위 지표"), print(sp.round(3).to_string(index=False))
    print("\n로짓 계수 (engine)"), print(coefs.round(3).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# ---- 엔진에 넣는 α 계열 -------------------------------------------------------------------------------------------
MODELS = ROOT / "data" / "processed" / "bm_accept"
SETTINGS = {"others_all": lambda P, site: P["site"] != site,                                  # 검증 C와 같은 조건
            "others_train": lambda P, site: (P["site"] != site) & P["year"].between(*TRAIN)}   # 검증 A와 같은 조건


def trained(site, setting="others_all", kind="logit", force=False):
    """site를 뺀 자료로 맞춘 (offer, bid) 모형. 여러 프로세스에서 다시 쓰도록 pickle로 저장한다."""
    import pickle
    MODELS.mkdir(parents=True, exist_ok=True)
    path = MODELS / f"{site}_{setting}_{kind}.pkl"
    if path.exists() and not force:
        return pickle.loads(path.read_bytes())
    P = load_panel()
    T = P[SETTINGS[setting](P, site)]
    m = {side: fit(T, side, "engine", kind) for side in ("offer", "bid")}
    path.write_bytes(pickle.dumps(m))
    return m


def site_frame(site, years):
    """발전소의 구간별 자기 단가(가용 유닛의 중앙값)와 계통 상태. 지역 물량은 패널에서 이미 자기 몫을 뺀 값이다."""
    P = load_panel(years)
    P = P[P["site"] == site]
    avail = P[P["mel_mw"] > 10]
    pr = avail.groupby("t")[["offer_price", "bid_price"]].median()
    first = P.drop_duplicates("t").set_index("t")
    f = first.drop(columns=["offer_price", "bid_price"]).join(pr)
    return f.reset_index()


def alphas(models, frame):
    """α 계열. 여유는 FPN과 무관하게 정해야 하므로 설계 행렬은 여유를 충분히 크게 두고 만든다."""
    f = frame.copy()
    f["head_up_mw"] = f["head_dn_mw"] = 100.0
    f["offer_mwh"] = f["bid_mwh"] = 0.0
    f["unit_mw"] = 100.0
    out = pd.DataFrame(index=pd.DatetimeIndex(f["t"]))
    for side in ("offer", "bid"):
        X, _, _, ok = design(f, side, "engine")
        a = np.zeros(len(f))
        a[ok.to_numpy()] = models[side].predict(X)
        out[f"alpha_{side}"] = a
        out[f"{side}_price"] = f[f"{side}_price"].to_numpy()
    return out
