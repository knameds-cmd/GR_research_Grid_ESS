"""
유닛별 가용 출력: MEL(최대 출력 한도)·MIL(최대 입력 한도, 음수)을 결제구간 평균 MW로 만든다.

    from gbess.data.availability import site_availability
    av = site_availability("DINO", "2025-01-01", "2026-01-01")   # 열: mel_mw, mil_mw(양수), units_pump

- 같은 구간을 여러 번 고쳐 내므로 notificationTime 순서대로 덮어써 마지막 통보값을 쓴다 (gbess.realized.physical._paint 재사용).
- 통보가 없는 분은 0 MW로 본다(그 유닛을 쓸 수 없음). 통보가 한 번도 없는 달이면 오류를 낸다.
- units_pump: 그 구간에 양수가 가능한 유닛 수 = |MIL|이 유닛 정격 양수 출력의 절반을 넘는 유닛 수.
  양수형 엔진의 정수 펌프 제약 상한으로 쓴다.
- 운영자는 계획 정지를 미리 알므로, 롤링 운전에서도 이 값은 "미리 아는 정보"로 둔다.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from gbess.data.prices import _months, _utc
from gbess.realized.physical import MIN, _paint

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "elexon"


def _load(ds, start, end):
    ms = _months(start, end)
    files = [RAW / f"{ds}_psh" / f"{ds}_psh_{m:%Y%m}.parquet" for m in [ms[0] - 1, *ms, ms[-1] + 1]]
    return pd.concat([pd.read_parquet(f) for f in files if f.exists()], ignore_index=True)


def _unit_sp_mean(df, start, end):
    t0 = np.datetime64(_utc(start).tz_localize(None), "m")
    n = int((np.datetime64(_utc(end).tz_localize(None), "m") - t0) // MIN)
    vals = np.full(n, np.nan)
    if len(df):
        d = df.sort_values(["notificationTime", "notificationSequence", "timeFrom"])

        def tm(s):
            return pd.to_datetime(s, utc=True).dt.tz_localize(None).to_numpy().astype("datetime64[m]")
        _paint(vals, t0, tm(d["timeFrom"]), tm(d["timeTo"]), d["levelFrom"].to_numpy(float), d["levelTo"].to_numpy(float))
    missing = int(np.isnan(vals).sum())
    vals = np.nan_to_num(vals)
    return vals.reshape(-1, 30).mean(axis=1), missing


def site_availability(site, start, end, pump_unit_mw=None):
    idx = pd.date_range(_utc(start), _utc(end), freq="30min", inclusive="left")
    mel, mil = _load("mels", start, end), _load("mils", start, end)
    units = sorted(u for u in set(mel["bmUnit"]) | set(mil["bmUnit"]) if f"_{site}-" in u)
    if not units:
        raise ValueError(f"{site}: MEL/MIL 자료 없음 ({start}~{end})")
    tot_mel, tot_mil, n_pump, miss = np.zeros(len(idx)), np.zeros(len(idx)), np.zeros(len(idx)), 0
    for u in units:
        a, m1 = _unit_sp_mean(mel[mel["bmUnit"] == u], start, end)
        b, m2 = _unit_sp_mean(mil[mil["bmUnit"] == u], start, end)
        miss += m1 + m2
        tot_mel += np.clip(a, 0, None)
        tot_mil += np.clip(-b, 0, None)
        ref = pump_unit_mw if pump_unit_mw else max(np.percentile(-b, 95), 1.0)
        n_pump += (-b > 0.5 * ref)
    out = pd.DataFrame({"mel_mw": tot_mel, "mil_mw": tot_mil, "units_pump": n_pump}, index=idx)
    out.attrs = {"units": units, "missing_unit_minutes": miss}
    return out
