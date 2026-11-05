"""
ERA5 기상 자료를 NSF NCAR 공개 미러(AWS, 열쇠 없음)에서 영국 영역만 받아 Atlite 컷아웃과 같은 변수로 바꾼다.
Zenodo 18325225 컷아웃이 2010~2024년만 있어서, 2025년(T8·V1)에 쓴다.

    .venv/bin/python -m gbess.system.era5_ncar 2025            # data/raw/system/era5/uk-2025-ncar.nc
    .venv/bin/python -m gbess.system.era5_ncar 2020 --months 1 # Zenodo 컷아웃과 대조하는 시험용

- 출처: NSF NCAR RDA ds633.0 "ERA5 Reanalysis" 미러 https://nsf-ncar-era5.s3.amazonaws.com (ECMWF ERA5, Copernicus 라이선스).
  파일은 변수·달마다 전 지구 0.25° netCDF4(HDF5)이고 (시간 27, 위도 139, 경도 277) 단위로 압축 저장돼 있어서, HTTP 범위 요청으로
  영국 영역이 들어 있는 조각만 읽는다.
- 영역: Zenodo 컷아웃과 같은 경도 −13.5~1.75°, 위도 50~60.75° (0.25°, 62 × 44칸).
- 변수 변환 (Atlite era5 모듈과 같은 정의): wnd100m = √(u100² + v100²), roughness = fsr(예보 거칠기), height = z / 9.80665.
- 받는 변수는 풍력에 필요한 u100·v100·fsr뿐이다. 일사(ssrd) 같은 누적 변수는 시간마다 지구 전체가 한 조각(약 11 MB)이라
  영국만 골라 읽을 수 없고, 1년에 약 9 GB가 더 든다. 2025년 태양광은 NESO 수요 자료의 배전망 태양광 실측으로 대신한다
  (gbess.system.backcast). 받기 속도는 이 노트북에서 병렬로 초당 약 3.5 MB(2026-11-05 측정).
"""
import argparse
import io
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

BASE = "https://nsf-ncar-era5.s3.amazonaws.com"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "raw" / "system" / "era5"
LAT = np.arange(60.75, 49.999, -0.25)          # 44칸, 북→남 (원자료 순서)
LON = np.arange(-13.5, 1.751, 0.25)            # 62칸
AN = {"u100": "228_246_100u", "v100": "228_247_100v", "fsr": "128_244_fsr"}
G = 9.80665


class HTTPFile(io.RawIOBase):
    """HTTP 범위 요청으로 읽는 파일 객체 (h5py가 읽을 수 있음). 블록 단위로 캐시한다."""

    def __init__(self, url, block=1 << 19, session=None):
        import requests
        self.s = session or requests.Session()
        self.url, self.pos, self.block, self.cache = url, 0, block, {}
        r = self.s.head(url, timeout=60)
        r.raise_for_status()
        self.size = int(r.headers["Content-Length"])

    def readable(self):
        return True

    def seekable(self):
        return True

    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else self.pos + off if whence == 1 else self.size + off
        return self.pos

    def tell(self):
        return self.pos

    def _blk(self, i):
        if i not in self.cache:
            a = i * self.block
            b = min(a + self.block, self.size) - 1
            for k in range(5):
                try:
                    r = self.s.get(self.url, headers={"Range": f"bytes={a}-{b}"}, timeout=120)
                    r.raise_for_status()
                    if len(r.content) == b - a + 1:
                        break
                except Exception:
                    if k == 4:
                        raise
            self.cache[i] = r.content
        return self.cache[i]

    def readinto(self, buf):
        n = min(len(buf), self.size - self.pos)
        if n <= 0:
            return 0
        out, p = bytearray(), self.pos
        while len(out) < n:
            i = p // self.block
            o = p - i * self.block
            c = self._blk(i)[o:o + n - len(out)]
            out += c
            p += len(c)
        buf[:n] = out
        self.pos += n
        return n


def lon_index(lon_grid):
    """원자료 경도(0~359.75)에서 영역 경도(−13.5~1.75) 칸 번호."""
    want = np.mod(LON, 360.0)
    return np.array([int(np.argmin(np.abs(lon_grid - w))) for w in want])


def lat_index(lat_grid):
    return np.array([int(np.argmin(np.abs(lat_grid - w))) for w in LAT])


def _read_box(ds, lat_i, lon_i):
    """ds[..., lat, lon]에서 영역만. 경도가 0°를 넘어 이어지므로 두 덩어리로 읽어 붙인다."""
    la = slice(lat_i.min(), lat_i.max() + 1)
    west = lon_i[lon_i > 700]
    east = lon_i[lon_i < 700]
    parts = []
    if len(west):
        parts.append(ds[..., la, west.min():west.max() + 1])
    if len(east):
        parts.append(ds[..., la, east.min():east.max() + 1])
    return np.concatenate(parts, axis=-1)


def _open(url):
    import h5py
    f = HTTPFile(url)
    return f, h5py.File(f, "r")


def an_url(code, m):
    m = pd.Period(m, freq="M")
    end = (m + 1).start_time - pd.Timedelta(hours=1)
    return f"{BASE}/e5.oper.an.sfc/{m:%Y%m}/e5.oper.an.sfc.{code}.ll025sc.{m:%Y%m}0100_{end:%Y%m%d%H}.nc"


def _data_var(h):
    return [k for k in h if getattr(h[k], "ndim", 0) >= 3][0]


def read_an(name, m):
    """분석 변수 한 달: (시각 UTC, 배열 (T, 44, 62))."""
    f, h = _open(an_url(AN[name], m))
    try:
        li, lo = lat_index(h["latitude"][:]), lon_index(h["longitude"][:])
        x = _read_box(h[_data_var(h)], li, lo).astype(np.float32)
        t = pd.Timestamp("1900-01-01") + pd.to_timedelta(h["time"][:].astype(np.int64), unit="h")
    finally:
        h.close()
        f.cache.clear()
    return pd.DatetimeIndex(t), x


def read_height():
    url = f"{BASE}/e5.oper.invariant/197901/e5.oper.invariant.128_129_z.ll025sc.1979010100_1979010100.nc"
    f, h = _open(url)
    try:
        li, lo = lat_index(h["latitude"][:]), lon_index(h["longitude"][:])
        z = _read_box(h[_data_var(h)], li, lo)
    finally:
        h.close()
    return np.asarray(z, np.float64).reshape(len(LAT), len(LON)) / G


def convert(u100, v100, fsr):
    """원자료 → Atlite 변수 (같은 모양의 배열)."""
    return {"wnd100m": np.sqrt(u100.astype(np.float64) ** 2 + v100.astype(np.float64) ** 2).astype(np.float32),
            "roughness": fsr.astype(np.float32)}


def _job(j):
    n, m = j
    t, x = read_an(n, m)
    print(f"  {n} {m} 받음", flush=True)
    return n, t, x


def fetch(year, months=None, workers=8, out=None):
    """year의 시간별 영역 자료를 netCDF로 쓴다. months를 주면 그 달만(대조 시험용)."""
    import xarray as xr
    months = months or list(range(1, 13))
    per = [pd.Period(f"{year}-{m:02d}", freq="M") for m in months]
    times = pd.date_range(per[0].start_time, (per[-1] + 1).start_time, freq="h", inclusive="left")
    jobs = [(n, m) for n in AN for m in per]
    data = {n: [] for n in AN}
    with ProcessPoolExecutor(workers) as ex:          # h5py는 전역 잠금이 있어 스레드로는 동시에 받지 못함
        for n, t, x in ex.map(_job, jobs):
            data[n].append(pd.Series(list(x), index=t))
    arr = {}
    for n, parts in data.items():
        s = pd.concat(parts)
        s = s[~s.index.duplicated(keep="first")].reindex(times)
        if s.isna().any():
            raise ValueError(f"{n}: {int(s.isna().sum())} 시간 없음")
        arr[n] = np.stack(s.to_list())
    v = convert(arr["u100"], arr["v100"], arr["fsr"])
    ds = xr.Dataset({k: (("time", "y", "x"), x) for k, x in v.items()},
                    coords={"time": times, "y": LAT, "x": LON})
    ds["height"] = (("y", "x"), read_height())
    ds = ds.sortby("y")                                        # Zenodo 컷아웃처럼 남→북
    ds.attrs.update(source=f"ERA5 via NSF NCAR RDA ds633.0 AWS mirror ({BASE}), converted by gbess.system.era5_ncar",
                    licence="Copernicus licence (ERA5)")
    out = out or OUT / (f"uk-{year}-ncar.nc" if months == list(range(1, 13)) else
                        f"uk-{year}-ncar-m{'-'.join(map(str, months))}.nc")
    out.parent.mkdir(parents=True, exist_ok=True)
    enc = {k: {"zlib": True, "complevel": 4} for k in v}
    ds.to_netcdf(out, encoding=enc)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("year", type=int)
    ap.add_argument("--months", type=int, nargs="*")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args(argv)
    p = fetch(a.year, a.months, a.workers)
    print(p, os.path.getsize(p) // 1_000_000, "MB", flush=True)
    os._exit(0)                                                 # h5py + 파일 객체 종료 순서 문제(세그폴트)를 피함


if __name__ == "__main__":
    main()
