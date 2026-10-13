#!/usr/bin/env python3
"""
층 1 모델 실행. 저장소 루트에서:
    python3 run_layer1.py                                   # 2026-09, 50 MW / 2시간, 시나리오 6개 비교
    python3 run_layer1.py --start 2025-01-01 --end 2025-02-01 --duration 1
    python3 run_layer1.py --scenarios full wholesale        # 고른 시나리오만
필요한 패키지: pandas, pulp, highspy (pip install pandas pulp highspy)
결과: results/layer1/<기간>_<MW>MW_<h>h/ 에 summary.csv(시나리오별 수익)와 <시나리오>_dispatch.csv(30분 운전 계획)
해설: docs/04_layer1_model_KO.md
"""
import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

try:
    import pandas as pd
    import pulp  # noqa: F401
except ImportError:
    sys.exit("pandas와 pulp가 필요합니다: python3 -m pip install pandas pulp highspy")

from model.data import RESERVE, RESPONSE, build_inputs
from model.layer1 import Battery, Rules, build, results, solve, solve_exact

ROOT = Path(__file__).resolve().parent

# 규칙 스위치 조합. 나중에 Shapley 분해는 이 스위치들을 켜고 끈 모든 조합으로 돌린다
SCENARIOS = {
    "wholesale": ("도매만", Rules(services=())),
    "response": ("도매 + DC/DM/DR (SoE 모든 구간)", Rules(services=tuple(RESPONSE))),
    "response_soe_block_start": ("response에서 SoE를 블록 시작만 확인",
                                 Rules(services=tuple(RESPONSE), soe_rule="block_start")),
    "response_no_soe": ("response에서 SoE 확인 없음 (에너지 제한 없는 상한)",
                        Rules(services=tuple(RESPONSE), soe_rule="off")),
    "full": ("도매 + DC/DM/DR + BR/QR/SR (2026년 상품, SoE 모든 구간)", Rules()),
    "full_soe_block_start": ("full에서 SoE를 블록 시작만 확인", Rules(soe_rule="block_start")),
    "full_no_soe": ("full에서 DC/DM/DR SoE 확인 없음 (예비력 에너지는 유지)", Rules(soe_rule="off")),
    "response_no_split": ("response에서 블록·방향당 DC/DM/DR 하나만 (양식화된 제한)",
                          Rules(services=tuple(RESPONSE), splitting=False)),
    "full_no_split": ("full에서 블록·방향당 DC/DM/DR 하나만 (양식화된 제한)", Rules(splitting=False)),
    "response_no_stack": ("response에서 응답 상품 든 블록 도매 금지 (양식화된 제한)",
                          Rules(services=tuple(RESPONSE), wholesale_stacking=False)),
}


def main(argv=None):
    ap = argparse.ArgumentParser(description="층 1 완전예측 MILP (해설: docs/04_layer1_model_KO.md)")
    ap.add_argument("--start", default="2026-09-01", help="시작 EFA일 (포함). 전날 23:00 영국 현지시각에 시작")
    ap.add_argument("--end", default="2026-10-01", help="끝 EFA일 (포함 안 함)")
    ap.add_argument("--power", type=float, default=50.0, help="정격 출력 MW")
    ap.add_argument("--duration", type=float, default=2.0, help="지속시간 h (용량 = 출력 × 지속시간)")
    ap.add_argument("--scenarios", nargs="+", default=list(SCENARIOS), choices=list(SCENARIOS))
    ap.add_argument("--relax", action="store_true", help="이진 변수를 풀어 LP로 풀기 (빠르지만 동시 충방전 허용)")
    ap.add_argument("--freq-sigma", type=float, default=0.06,
                    help="주파수 편차 표준편차 Hz (DC/DM/DR 응답 에너지 계산용, 0이면 무시). 1초 주파수로 보정 전 임시값")
    ap.add_argument("--time-limit", type=float, default=600, help="시나리오당 계산 제한 초 (넘으면 근사해와 gap 표시)")
    ap.add_argument("--out", help="결과 폴더 (기본 results/layer1/...)")
    a = ap.parse_args(argv)

    inp = build_inputs(a.start, a.end)
    bat = replace(Battery(), power_mw=a.power, duration_h=a.duration)
    out = Path(a.out) if a.out else ROOT / "results" / "layer1" / f"{a.start}_{a.end}_{a.power:g}MW_{a.duration:g}h"
    out.mkdir(parents=True, exist_ok=True)
    print(f"기간 EFA일 {a.start} ~ {a.end} (UTC {inp.index[0]:%m-%d %H:%M} 시작), {len(inp.index)}구간, "
          f"배터리 {a.power:g} MW / {bat.energy_mwh:g} MWh")
    for note in inp.notes:
        print("  -", note)

    rows = []
    for key in a.scenarios:
        label, rules = SCENARIOS[key]
        if a.relax:
            b = build(inp, bat, rules, relax=True, freq_sigma_hz=a.freq_sigma or None)
            info = solve(b, time_limit=a.time_limit)
        else:
            b, info = solve_exact(inp, bat, rules, freq_sigma_hz=a.freq_sigma or None, time_limit=a.time_limit)
        if info.get("warning"):
            print(f"  [!] {key}: {info['warning']}")
        if info["status"] != "Optimal":
            print(f"[!] {key}: {info['status']}")
            continue
        df, s = results(inp, bat, b)
        df.to_csv(out / f"{key}_dispatch.csv")
        row = {"scenario": key, "설명": label, "total_gbp_per_mw_yr": s["total_gbp_per_mw_yr"],
               **{f"{k}_gbp_per_mw_yr": x for k, x in s["revenue_gbp_per_mw_yr"].items()},
               "cycles_per_day": s["cycles_per_day"], "solve_seconds": info["seconds"], "solver": info["solver"],
               "binary_periods": info.get("binary_periods", 0), "simultaneous_periods": info.get("simultaneous", 0),
               "solution": info["solution"], "mip_gap": info["mip_gap"]}
        rows.append(row)
        gap = info["mip_gap"]
        warn = "" if info["solution"] == "Optimal Solution Found" else \
            f", 시간 제한에 걸린 근사해 (gap {gap:.1%})" if gap is not None else ", 시간 제한에 걸린 근사해"
        print(f"  {key:15s} {s['total_gbp_per_mw_yr']:>10,.0f} £/MW/yr  (사이클 {s['cycles_per_day']}/일, {info['seconds']}초{warn})")

    if rows:
        summary = pd.DataFrame(rows)
        if (out / "summary.csv").exists():  # 이전에 돌린 다른 시나리오 결과는 남긴다
            old = pd.read_csv(out / "summary.csv")
            summary = pd.concat([old[~old["scenario"].isin(summary["scenario"])], summary], ignore_index=True)
        order = {k: i for i, k in enumerate(SCENARIOS)}
        summary = summary.sort_values("scenario", key=lambda c: c.map(order)).fillna(0)
        summary.to_csv(out / "summary.csv", index=False)
        (out / "run.json").write_text(json.dumps({
            "start": a.start, "end": a.end, "battery": vars(bat), "relax": a.relax, "freq_sigma_hz": a.freq_sigma,
            "notes": inp.notes, "scenarios": {k: str(SCENARIOS[k][1]) for k in summary["scenario"]},
        }, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        print(f"\n결과: {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
