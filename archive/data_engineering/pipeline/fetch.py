
"""Reliable data extraction from the official RTE API."""

from datetime import datetime, timedelta, timezone
import time

import requests


API = (
    "https://odre.opendatasoft.com/api/explore/v2.1/"
    "catalog/datasets/eco2mix-regional-tr/records"
)

PAGE_SIZE = 100
MAX_OFFSET = 9900


def fetch_day(day, session):
    """Retrieve one complete UTC day from the API."""

    next_day = day + timedelta(days=1)

    where = (
        f"date_heure >= date'{day.isoformat()}' "
        f"AND date_heure < date'{next_day.isoformat()}'"
    )

    records = []
    offset = 0

    while True:

        params = {
            "where": where,
            "order_by": "date_heure ASC, code_insee_region ASC",
            "timezone": "UTC",
            "limit": PAGE_SIZE,
            "offset": offset,
        }

        for attempt in range(3):
            try:
                response = session.get(
                    API,
                    params=params,
                    timeout=(10, 45),
                )

                response.raise_for_status()
                payload = response.json()

                if (
                    not isinstance(payload, dict)
                    or not isinstance(payload.get("results"), list)
                ):
                    raise ValueError(
                        "Unexpected API response format"
                    )

                break

            except requests.RequestException:
                if attempt == 2:
                    raise

                time.sleep(2 ** attempt)

        batch = payload["results"]
        total = payload.get("total_count")

        if not isinstance(total, int) or total < 0:
            raise ValueError(
                "API returned an invalid record count"
            )

        records.extend(batch)
        offset += len(batch)

        if offset >= total:
            break

        if not batch:
            raise RuntimeError(
                f"Incomplete API results for {day}"
            )

        if offset >= MAX_OFFSET:
            raise RuntimeError(
                "Pagination limit reached"
            )

    if len(records) != total:
        raise RuntimeError(
            f"{day}: expected {total}, "
            f"received {len(records)}"
        )

    return records


def fetch_recent(days=17, session=None):
    """
    Fetch recent RTE observations.

    The 17-day window provides a safety overlap
    for a pipeline scheduled every 14 days.
    """

    if not isinstance(days, int) or not 1 <= days <= 31:
        raise ValueError(
            "days must be an integer between 1 and 31"
        )

    today = datetime.now(timezone.utc).date()
    start = today - timedelta(days=days - 1)

    own_session = session is None

    client = (
        requests.Session()
        if own_session
        else session
    )

    all_records = []

    try:
        for index in range(days):
            day = start + timedelta(days=index)

            records = fetch_day(day, client)

            print(
                f"{day}: fetched {len(records):,} records"
            )

            all_records.extend(records)

    finally:
        if own_session:
            client.close()

    return all_records
