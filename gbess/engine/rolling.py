"""
예측 기반 롤링 운전 (정보 수준 2). 완전예측(정보 수준 1)과의 차이가 "앞을 아는 것의 가치"다.

하루(D)마다:
  1. D 00:00 UTC 이전의 가격만 써서 앞으로 horizon_days일의 가격을 예측한다 (예측 방법은 07 문서 T3: 단순·투명한 것만).
  2. 예측 가격으로 horizon_days일을 최적화한다. 끝에 남은 에너지는 water value(예측 가격 중앙값 × 방전효율)로 평가한다.
  3. 첫날(48구간) 계획만 실행하고, 실제 가격으로 수익을 계산한다. 끝 저장량을 다음 날 시작 저장량으로 넘긴다.
정보 시점 가정: D의 계획을 D 00:00에 정하고 그 전 가격은 모두 안다(일중 거래자 기준). 이 가정은 결과에 함께 기록한다.
장주기 자산은 며칠 앞을 보는 능력의 값이 크므로 horizon_days(1·3·7일)를 실험 축으로 둔다.
"""
import numpy as np
import pandas as pd

from .dispatch import DT, solve

SP_DAY = 48


def forecast(history: np.ndarray, horizon_sp: int, method: str):
    """history: 결정 시점 이전 가격(30분, 시간순). 반환: 앞으로 horizon_sp구간의 예측."""
    if len(history) < 7 * SP_DAY:
        method = "d1"
    d1 = np.resize(history[-SP_DAY:], horizon_sp)
    if method == "d1":
        return d1
    week = history[-7 * SP_DAY:]
    d7 = np.resize(week, horizon_sp)   # 앞으로 h일째 = 7일 전 같은 요일 (7일보다 길면 반복)
    if method == "d7":
        return d7
    if method == "avg":
        return (d1 + d7) / 2
    raise ValueError(f"예측 방법은 d1, d7, avg: {method}")


def run(price: pd.Series, asset, horizon_days=3, method="avg", warmup: pd.Series = None):
    """price: 실행 기간의 실제 가격(하루 단위로 나뉘어야 함). warmup: 그 전 가격(예측용 과거). 없으면 첫 주는 d1."""
    if len(price) % SP_DAY:
        raise ValueError("기간은 하루(48구간) 단위여야 합니다 (UTC 날짜 기준)")
    hist = (warmup.to_numpy(float) if warmup is not None else np.array([]))
    actual = price.to_numpy(float)
    H = horizon_days * SP_DAY
    s = asset.soc_init * asset.e_mwh
    rows, solves = [], []
    for k in range(len(actual) // SP_DAY):
        past = np.r_[hist, actual[:k * SP_DAY]]
        if len(past) < SP_DAY:
            fc = np.r_[actual[:0], np.full(H, np.nan)]
            fc[:] = np.nanmedian(actual[:SP_DAY])  # 과거가 하루도 없으면 첫날 실제 중앙값으로 평평하게 (첫날만)
        else:
            fc = forecast(past, H, method)
        idx = price.index[k * SP_DAY:k * SP_DAY + H]
        if len(idx) < H:   # 기간 끝: 예측 인덱스를 늘려 붙인다
            idx = pd.date_range(price.index[k * SP_DAY], periods=H, freq="30min")
        wv = float(np.median(fc)) * asset.eta_dis
        plan, info = solve(pd.Series(fc, index=idx), asset, terminal="value", water_value=wv, s_start=s)
        day = plan.iloc[:SP_DAY].copy()
        day["price"] = actual[k * SP_DAY:(k + 1) * SP_DAY]
        day["forecast"] = fc[:SP_DAY]
        s = float(day["soc_mwh"].iat[-1])
        rows.append(day)
        solves.append(info["seconds"])
    out = pd.concat(rows)
    out.index = price.index
    meta = {"horizon_days": horizon_days, "method": method, "solve_seconds": round(sum(solves), 1),
            "end_soc_mwh": s, "start_soc_mwh": asset.soc_init * asset.e_mwh,
            "information": "D의 계획을 D 00:00 UTC에 정함, 그 전 가격은 모두 앎"}
    return out, meta
