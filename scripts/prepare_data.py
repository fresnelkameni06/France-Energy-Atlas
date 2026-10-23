"""Build small, fast analytical Parquet datasets from the existing Excel.

No network requests and no modification of the source workbook or SQLite DB.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from utils.prep import normalize_sheet, aggregate_daily
from utils.schema import NUMERIC

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = DATA / "processed"
EXCEL = DATA / "france_energy_2020_2026.xlsx"


def build(excel: Path = EXCEL, output: Path = OUTPUT, verbose: bool = True):
    if not excel.is_file():
        raise FileNotFoundError(
            f"Missing Excel workbook: {excel}. Keep the existing workbook in data/."
        )
    output.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    with excel.open("rb") as stream:
        for chunk in iter(lambda: stream.read(2 ** 20), b""):
            digest.update(chunk)
    source_hash = digest.hexdigest()
    info_path = output / "quality_summary.json"
    if info_path.exists():
        previous = json.loads(info_path.read_text(encoding="utf-8"))
        if previous.get("sha256") == source_hash and all((output / f"facts_{y}.parquet").exists() for y in previous.get("years", [])):
            if verbose:
                print("Excel unchanged. Prepared data are already current.")
            return previous

    year_rows = []
    daily_frames = []
    observed_years = []
    valid_sources = {}
    for year in range(2020, 2027):
        if verbose:
            print(f"Reading sheet {year}...", flush=True)
        try:
            raw = pd.read_excel(excel, sheet_name=str(year), engine="openpyxl")
        except ValueError as exc:
            raise ValueError(f"Sheet {year} is missing from {excel.name}") from exc
        normalized, report = normalize_sheet(raw)
        del raw
        # The workbook is split by UTC year; local dates can straddle the boundary.
        normalized.to_parquet(output / f"facts_{year}.parquet", index=False, compression="zstd")
        daily_frames.append(aggregate_daily(normalized))
        observed_years.append(year)
        report.update({"sheet": year, "observation_start_utc": normalized.observation_utc.min().isoformat() if len(normalized) else None,
                       "observation_end_utc": normalized.observation_utc.max().isoformat() if len(normalized) else None})
        for src, count in normalized.source.value_counts().items():
            valid_sources[src] = valid_sources.get(src, 0) + int(count)
        if verbose:
            print(f"  {len(normalized):,} validated rows | {report['null_consumption_rows']:,} missing demand")
        year_rows.append(report)
        del normalized

    daily = pd.concat(daily_frames, ignore_index=True)
    # Ensure uniqueness if the UTC/local date boundary creates cross-sheet overlap.
    daily = daily.groupby(["date", "region", "region_code"], as_index=False).agg({
        **{f"{c.replace('_mw', '_mwh')}": "sum" for c in NUMERIC},
        "generation_mwh": "sum", "renewable_mwh": "sum", "interval_hours": "sum",
        "readings": "sum", "valid_demand": "sum", "peak_demand_mw": "max",
        "mean_demand_mw": "mean", "average_renewable_share_pct": "mean",
        "year": "first", "month": "first",
    })
    daily.to_parquet(output / "daily_summary.parquet", compression="zstd", index=False)
    summary = {
        "sha256": source_hash,
        "prepared_utc": datetime.now(timezone.utc).isoformat(),
        "workbook_name": excel.name,
        "source_size_mb": round(excel.stat().st_size / 2**20, 2),
        "years": observed_years,
        "sheet_reports": year_rows,
        "total_input_rows": sum(r["input_rows"] for r in year_rows),
        "total_prepared_rows": sum(r["output_rows"] for r in year_rows),
        "source_counts": valid_sources,
        "date_min": daily.date.min().strftime("%Y-%m-%d"),
        "date_max": daily.date.max().strftime("%Y-%m-%d"),
        "unique_regions": int(daily.region_code.nunique()),
        "daily_rows": int(len(daily)),
    }
    info_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    if verbose:
        print(f"Prepared {summary['total_prepared_rows']:,} observations, {summary['daily_rows']:,} daily rows.")
        print(f"Data ready in: {output}")
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--excel", type=Path, default=EXCEL)
    p.add_argument("--output", type=Path, default=OUTPUT)
    args = p.parse_args()
    build(args.excel, args.output)
