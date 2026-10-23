"""Read-only validation of the prepared yearly Parquet and Excel lineage."""
from pathlib import Path
import json
import pandas as pd
from utils.schema import NUMERIC
PROCESSED = Path(__file__).resolve().parents[1] / "data" / "processed"


def validate(root=PROCESSED):
    manifest = root / "quality_summary.json"
    if not manifest.exists():
        raise SystemExit("No prepared data found. Run python -m scripts.prepare_data first.")
    report = json.loads(manifest.read_text(encoding="utf-8"))
    for year in report["years"]:
        f = root / f"facts_{year}.parquet"
        if not f.exists():
            raise AssertionError(f"Missing {f}")
        df = pd.read_parquet(f, columns=["source", "region_code", "observation_utc", "interval_hours", "consumption_mw"])
        if df.duplicated(["source", "region_code", "observation_utc"]).any():
            raise AssertionError(f"Duplicated keys in {f}")
        if not df.interval_hours.isin([0.25, 0.5]).all():
            raise AssertionError(f"Invalid intervals in {f}")
        if (df.consumption_mw.dropna() < 0).any():
            raise AssertionError(f"Negative demand in {f}")
    print("PASS: prepared data integrity, unique observation keys, interval lengths and measurement bounds")
    print(f"Rows: {report['total_prepared_rows']:,}; Regions: {report['unique_regions']}; Years: {report['years']}")

if __name__ == "__main__":
    validate()
