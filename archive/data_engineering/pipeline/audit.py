
"""Read-only audit of the France Energy Live SQLite database."""

import csv
import sqlite3
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "energy.db"
DOCS = ROOT / "docs"

METRICS = [
    "consumption_mw",
    "nuclear_mw",
    "wind_mw",
    "solar_mw",
    "hydro_mw",
    "thermal_mw",
    "bioenergy_mw",
    "exchange_mw",
]

FREQUENCY = {
    "eco2mix-regional-cons-def": 30,
    "eco2mix-regional-tr": 15,
}


def audit():
    if not DB.is_file():
        raise SystemExit(f"Database not found: {DB}")

    DOCS.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(f"{DB.as_uri()}?mode=ro", uri=True)

    try:
        columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(measurements)")
        }

        required = {
            "source", "region_code", "region",
            "observation_utc", "quality_flag", *METRICS,
        }

        if not required <= columns:
            raise SystemExit(
                f"Missing columns: {sorted(required - columns)}"
            )

        total = conn.execute(
            "SELECT COUNT(*) FROM measurements"
        ).fetchone()[0]

        integrity = conn.execute(
            "PRAGMA quick_check"
        ).fetchone()[0]

        sources = conn.execute("""
            SELECT source, COUNT(*),
                   COUNT(DISTINCT region_code),
                   MIN(observation_utc),
                   MAX(observation_utc)
            FROM measurements
            GROUP BY source
            ORDER BY source
        """).fetchall()

        years = conn.execute("""
            SELECT substr(observation_utc, 1, 4), COUNT(*)
            FROM measurements
            GROUP BY 1
            ORDER BY 1
        """).fetchall()

        regions = conn.execute("""
            SELECT region_code, MAX(region),
                   COUNT(*), COUNT(DISTINCT region)
            FROM measurements
            GROUP BY region_code
            ORDER BY region_code
        """).fetchall()

        months = conn.execute("""
            SELECT source, substr(observation_utc, 1, 7),
                   COUNT(*), COUNT(DISTINCT region_code),
                   MIN(observation_utc), MAX(observation_utc)
            FROM measurements
            GROUP BY source, substr(observation_utc, 1, 7)
            ORDER BY 2, 1
        """).fetchall()

        duplicates = conn.execute("""
            SELECT COUNT(*) FROM (
                SELECT 1 FROM measurements
                GROUP BY source, region_code, observation_utc
                HAVING COUNT(*) > 1
            )
        """).fetchone()[0]

        expressions = ", ".join(
            f"SUM(CASE WHEN {c} IS NULL THEN 1 ELSE 0 END)"
            for c in METRICS
        )

        missing = conn.execute(
            f"SELECT {expressions} FROM measurements"
        ).fetchone()

        negatives = conn.execute("""
            SELECT COUNT(*) FROM measurements
            WHERE consumption_mw < 0
               OR nuclear_mw < 0
               OR wind_mw < 0
               OR solar_mw < 0
               OR hydro_mw < 0
               OR thermal_mw < 0
               OR bioenergy_mw < 0
        """).fetchone()[0]

        flags = conn.execute("""
            SELECT quality_flag, COUNT(*)
            FROM measurements
            GROUP BY quality_flag
            ORDER BY 2 DESC
        """).fetchall()

        series = conn.execute("""
            SELECT source, region_code, COUNT(*),
                   MIN(observation_utc),
                   MAX(observation_utc)
            FROM measurements
            GROUP BY source, region_code
        """).fetchall()

        # Estimate missing timestamps within each source/region.
        gaps = defaultdict(int)

        for source, region, count, first, last in series:
            if source not in FREQUENCY:
                continue

            start = datetime.fromisoformat(first)
            end = datetime.fromisoformat(last)

            expected = int(round(
                (end - start).total_seconds()
                / (60 * FREQUENCY[source])
            )) + 1

            gaps[source] += max(0, expected - count)

        off_grid = conn.execute("""
            SELECT COUNT(*) FROM measurements
            WHERE (
                source = 'eco2mix-regional-cons-def'
                AND substr(observation_utc, 15, 2)
                    NOT IN ('00', '30')
            )
            OR (
                source = 'eco2mix-regional-tr'
                AND substr(observation_utc, 15, 2)
                    NOT IN ('00', '15', '30', '45')
            )
        """).fetchone()[0]

        invalid_utc = conn.execute("""
            SELECT COUNT(*) FROM measurements
            WHERE observation_utc NOT LIKE '%+00:00'
        """).fetchone()[0]

    finally:
        conn.close()

    # Export monthly coverage.
    with (DOCS / "monthly_coverage.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "source", "month", "rows",
            "region_count", "first_utc", "last_utc",
        ])

        writer.writerows(months)

    # Build documentation report.
    lines = [
        "# France Energy Live — Database Audit",
        "",
        f"- Total observations: {total:,}",
        f"- SQLite integrity: {integrity}",
        f"- Duplicate keys: {duplicates}",
        f"- Regions: {len(regions)}",
        f"- Negative demand/generation values: {negatives}",
        f"- Unexpected time intervals: {off_grid}",
        f"- Timestamps without UTC offset: {invalid_utc}",
        "",
        "## Sources",
    ]

    for source, count, n_regions, first, last in sources:
        lines.append(
            f"- {source}: {count:,} rows, "
            f"{n_regions} regions, "
            f"{FREQUENCY.get(source, 'unknown')} min, "
            f"{first} to {last}"
        )

    lines += ["", "## Annual Coverage"]

    for year, count in years:
        lines.append(f"- {year}: {count:,} observations")

    lines += ["", "## Regions"]

    for code, name, count, variants in regions:
        lines.append(
            f"- {code} — {name}: {count:,} observations "
            f"(name variants: {variants})"
        )

    lines += ["", "## Missing Values"]

    for field, count in zip(METRICS, missing):
        percentage = 100 * count / total if total else 0

        lines.append(
            f"- {field}: {count:,} ({percentage:.2f}%)"
        )

    lines += ["", "## Data Quality Flags"]

    for flag, count in flags:
        lines.append(f"- {flag}: {count:,}")

    lines += ["", "## Estimated Missing Time Slots"]

    for source, count in gaps.items():
        lines.append(f"- {source}: approximately {count:,}")

    lines += [
        "",
        "Gap estimates concern each source and region separately.",
        "They do not include missing periods outside the observed "
        "date range or between the two data sources.",
        "",
        "Monthly details are available in monthly_coverage.csv.",
    ]

    (DOCS / "database_audit.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    # Short terminal summary.
    print("\n===== DATABASE AUDIT =====")
    print(f"Total observations: {total:,}")
    print(f"SQLite integrity: {integrity}")
    print(f"Regions: {len(regions)}")
    print(f"Duplicate keys: {duplicates}")
    print(f"Negative measurements: {negatives}")
    print(f"Invalid time intervals: {off_grid}")
    print(f"Invalid UTC timestamps: {invalid_utc}")

    print("\nAnnual coverage:")
    for year, count in years:
        print(f"  {year}: {count:,}")

    print("\nEstimated missing time slots:")
    for source, count in gaps.items():
        print(f"  {source}: {count:,}")

    print("\nReports saved:")
    print("  docs/database_audit.md")
    print("  docs/monthly_coverage.csv")


if __name__ == "__main__":
    audit()
