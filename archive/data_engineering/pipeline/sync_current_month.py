
"""Fetch, clean and store monthly RTE electricity data."""

import sys
import gzip
import json
import time

from datetime import date, timedelta
from pathlib import Path

import requests

from pipeline.clean import clean_records
from pipeline.store import save_records


API = (
    "https://odre.opendatasoft.com/api/explore/v2.1/"
    "catalog/datasets/eco2mix-regional-tr/records"
)


def fetch_day(day, session):
    """Retrieve all electricity records for one day."""

    next_day = day + timedelta(days=1)
    all_records = []
    offset = 0

    while True:
        params = {
            "where": (
                f"date_heure >= date'{day.isoformat()}' "
                f"AND date_heure < date'{next_day.isoformat()}'"
            ),
            "limit": 100,
            "offset": offset,
            "timezone": "UTC",
        }

        for attempt in range(3):
            try:
                response = session.get(
                    API,
                    params=params,
                    timeout=45,
                )

                response.raise_for_status()
                payload = response.json()
                batch = payload["results"]

                if not isinstance(batch, list):
                    raise ValueError("Invalid API response")

                break

            except (
                requests.RequestException,
                ValueError,
                KeyError,
            ):
                if attempt == 2:
                    raise

                time.sleep(2 ** attempt)

        all_records.extend(batch)
        offset += len(batch)

        if not batch or offset >= int(
            payload.get("total_count", 0)
        ):
            break

        if offset > 9000:
            raise RuntimeError(
                f"Unexpected pagination for {day}"
            )

    return all_records


def main():
    """Synchronize current month or a selected month."""

    today = date.today()
    first_day = today.replace(day=1)

    # Optional argument: YYYY-MM
    if len(sys.argv) > 1:
        try:
            first_day = date.fromisoformat(
                sys.argv[1] + "-01"
            )
        except ValueError:
            raise SystemExit(
                "Invalid month. Use YYYY-MM, e.g. 2026-09"
            )

        next_month = (
            first_day.replace(day=28)
            + timedelta(days=4)
        ).replace(day=1)

        last_day = next_month - timedelta(days=1)
        today = min(last_day, date.today())

    if first_day > today:
        raise SystemExit("Selected month is in the future.")

    folder = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "raw"
    )

    folder.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    day = first_day

    while day <= today:
        records = fetch_day(day, session)

        if records:
            path = folder / f"live_{day}.json.gz"

            # Save original API response
            with gzip.open(
                path, "wt", encoding="utf-8"
            ) as file:
                json.dump(
                    records,
                    file,
                    ensure_ascii=False,
                )

            # Clean and validate
            cleaned, rejected = clean_records(records)

            # Insert into SQLite
            total = save_records(cleaned)

            print(
                f"{day}: "
                f"fetched={len(records)}, "
                f"cleaned={len(cleaned)}, "
                f"rejected={rejected}, "
                f"database={total}"
            )

        else:
            print(f"{day}: no observations available")

        day += timedelta(days=1)

    print("\nSynchronization completed.")


if __name__ == "__main__":
    main()
