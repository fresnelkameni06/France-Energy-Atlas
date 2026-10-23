
"""Normalize and validate RTE electricity measurements."""

from datetime import datetime, timezone
from math import isfinite

LIVE_SOURCE = "eco2mix-regional-tr"
HISTORICAL_SOURCE = "eco2mix-regional-cons-def"

NUMERIC_FIELDS = {
    "consumption_mw": "consommation",
    "nuclear_mw": "nucleaire",
    "wind_mw": "eolien",
    "solar_mw": "solaire",
    "hydro_mw": "hydraulique",
    "thermal_mw": "thermique",
    "bioenergy_mw": "bioenergies",
    "exchange_mw": "ech_physiques",
}

MISSING_MARKERS = {
    "", "ND", "N/A", "NA", "NULL", "NONE", "NAN", "-"
}


def parse_number(value):
    """Convert values into valid floats or None."""

    if value is None or isinstance(value, bool):
        return None

    if isinstance(value, str):
        value = value.strip()

        if value.upper() in MISSING_MARKERS:
            return None

        value = (
            value.replace("\u202f", "")
            .replace(" ", "")
            .replace(",", ".")
        )

    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        return None

    return result if isfinite(result) else None


# Compatibility with existing scripts
number = parse_number


def clean_records(records, source=LIVE_SOURCE):
    """
    Clean RTE API records.

    Operations:
    - Validate timestamps and regions
    - Normalize timestamps to UTC
    - Convert numerical measurements
    - Handle missing values
    - Detect invalid negative measurements
    - Remove duplicates within the batch
    - Assign data quality flags

    Returns:
        cleaned_records, rejected_count
    """

    if source not in (LIVE_SOURCE, HISTORICAL_SOURCE):
        raise ValueError(f"Unknown data source: {source}")

    cleaned = []
    rejected = 0
    seen = set()

    retrieved = datetime.now(timezone.utc).isoformat()

    for raw in records:

        if not isinstance(raw, dict):
            rejected += 1
            continue

        try:
            timestamp = datetime.fromisoformat(
                str(raw["date_heure"]).replace("Z", "+00:00")
            )

            if timestamp.tzinfo is None:
                raise ValueError("Missing timezone")

            timestamp = (
                timestamp.astimezone(timezone.utc).isoformat()
            )

            region_code = str(
                raw["code_insee_region"]
            ).strip()

            region = str(
                raw["libelle_region"]
            ).strip()

            if (
                not region_code
                or region_code.lower() in {"none", "nan"}
                or not region
                or region.lower() in {"none", "nan"}
            ):
                raise ValueError("Invalid region")

        except (
            KeyError,
            TypeError,
            ValueError,
            AttributeError,
        ):
            rejected += 1
            continue

        key = (source, region_code, timestamp)

        if key in seen:
            continue

        seen.add(key)

        row = {
            "source": source,
            "region_code": region_code,
            "region": region,
            "observation_utc": timestamp,
            "retrieved_utc": retrieved,
        }

        negative_detected = False

        for column, api_column in NUMERIC_FIELDS.items():

            value = parse_number(
                raw.get(api_column)
            )

            # Negative exchanges are legitimate.
            # Negative demand or generation is invalid.
            if (
                value is not None
                and value < 0
                and column != "exchange_mw"
            ):
                value = None
                negative_detected = True

            row[column] = value

        if row["consumption_mw"] is None:
            row["quality_flag"] = "missing_consumption"

        elif negative_detected:
            row["quality_flag"] = "negative_measurement"

        elif any(
            row[column] is None
            for column in NUMERIC_FIELDS
        ):
            row["quality_flag"] = "partially_missing"

        else:
            row["quality_flag"] = "ok"

        cleaned.append(row)

    return cleaned, rejected
