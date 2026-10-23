"""Import historical RTE data into SQLite."""

import argparse
import gzip
import time

from pathlib import Path
from io import BytesIO

import pandas as pd
import requests

from pipeline.clean import clean_records
from pipeline.store import save_records


URL = (
    "https://odre.opendatasoft.com/api/explore/v2.1/"
    "catalog/datasets/eco2mix-regional-cons-def/exports/csv"
)


def month_bounds(year, month):
    start = f"{year}-{month:02d}-01"

    if month == 12:
        end = f"{year + 1}-01-01"
    else:
        end = f"{year}-{month + 1:02d}-01"

    return start, end


def run(years):
    session = requests.Session()

    raw_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    for year in years:
        for month in range(1, 13):
            start, end = month_bounds(year, month)

            if start > pd.Timestamp.today().strftime("%Y-%m-%d"):
                continue

            where = (
                f"date_heure >= date'{start}' "
                f"AND date_heure < date'{end}'"
            )

            for attempt in range(3):
                try:
                    response = session.get(
                        URL,
                        params={"where": where, "delimiter": ";"},
                        timeout=120,
                    )
                    response.raise_for_status()

                    csv = pd.read_csv(
                        BytesIO(response.content),
                        sep=";",
                        dtype=str,
                        encoding="utf-8-sig",
                        low_memory=False,
                    )

                    if csv.empty:
                        print(f"{start}: no published data")
                        break

                    required = {
                        "date_heure",
                        "code_insee_region",
                        "libelle_region",
                    }

                    if not required.issubset(csv.columns):
                        raise ValueError(
                            f"Unexpected API columns: {list(csv.columns)}"
                        )

                    # Preserve the original API export for reproducibility.
                    raw_path = raw_dir / f"history_{year}_{month:02d}.csv.gz"

                    with gzip.open(raw_path, "wb") as file:
                        file.write(response.content)

                    rows, rejected = clean_records(
                        csv.to_dict("records"),
                        "eco2mix-regional-cons-def",
                    )

                    count = save_records(rows)

                    print(
                        f"{start}: imported {len(rows)} | "
                        f"rejected {rejected} | "
                        f"database rows {count}"
                    )
                    break

                except (requests.RequestException, pd.errors.ParserError):
                    if attempt == 2:
                        raise

                    time.sleep(2 ** attempt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("years", type=int, nargs="+")
    run(parser.parse_args().years)