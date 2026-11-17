"""Download the raw data the notebook uses into data/raw.

    python3 scripts/download_data.py

- NOAA GHCN-Daily file for Madrid Retiro (station SP000003195)
- ERA5 daily minimum temperature for the grid square around Retiro, from Open-Meteo
- AEMET's daily values for Madrid, Retiro (station 3195) from August 1, 2026, if AEMET_API_KEY is set.
  A free key is available at https://opendata.aemet.es
"""
import json
import os
import time
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
GHCN = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/SP000003195.csv"
ERA5 = ("https://archive-api.open-meteo.com/v1/archive?latitude=40.4117&longitude=-3.6781"
        "&start_date=1940-01-01&end_date={end}&daily=temperature_2m_min&timezone=Europe%2FMadrid&models=era5")
AEMET = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/"
         "fechaini/{start}T00:00:00UTC/fechafin/{end}T23:59:59UTC/estacion/3195")


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "madrid-autumn-cold-onset", **(headers or {})})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    (RAW / "SP000003195.csv").write_bytes(get(GHCN))
    (RAW / "download.json").write_text(json.dumps(
        {"url": GHCN, "downloaded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}, indent=2))
    print("NOAA GHCN-Daily: data/raw/SP000003195.csv")

    (RAW / "era5_madrid.json").write_bytes(get(ERA5.format(end=today)))
    print("ERA5: data/raw/era5_madrid.json")

    key = os.environ.get("AEMET_API_KEY")
    if not key:
        print("AEMET: skipped, set AEMET_API_KEY to download it")
        return
    for _ in range(3):
        meta = json.loads(get(AEMET.format(start="2026-08-01", end=today), {"api_key": key}).decode("latin-1"))
        if meta.get("estado") == 200:
            break
        time.sleep(20)  # AEMET answers 429 when asked too often
    else:
        raise SystemExit(f"AEMET returned {meta.get('estado')}: {meta.get('descripcion')}")
    rows = json.loads(get(meta["datos"]).decode("latin-1"))
    (RAW / "aemet_3195_2026.json").write_text(json.dumps({
        "source": "AEMET OpenData, valores climatologicos diarios, station 3195 (Madrid, Retiro)",
        "fetched": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "range": ["2026-08-01", today],
        "rows": rows,
    }, ensure_ascii=False, indent=1))
    print(f"AEMET: data/raw/aemet_3195_2026.json, {len(rows)} days")


if __name__ == "__main__":
    main()
