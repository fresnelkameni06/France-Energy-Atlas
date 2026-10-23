"""Run Phase 1 ingestion once. Schedule hourly later with Windows Task Scheduler."""
import gzip
import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline.fetch import fetch_recent
from pipeline.clean import clean_records
from pipeline.store import save_records


def run():
    print("Fetching official RTE regional measurements...")
    raw = fetch_recent(days=17)
    if not raw:
        print("No recent records returned. Existing database (if any) is untouched.")
        return
    folder = Path(__file__).resolve().parents[1] / "data" / "raw"
    folder.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw_path = folder / f"rte_regional_{now}.json.gz"
    with gzip.open(raw_path, "wt", encoding="utf-8") as file:
        json.dump(raw, file, ensure_ascii=False)
    clean, rejected = clean_records(raw)
    count = save_records(clean)
    print(f"Fetched: {len(raw)} | Valid: {len(clean)} | Rejected: {rejected} | Total stored: {count}")
    print("Saved raw snapshot:", raw_path)


if __name__ == "__main__":
    run()
