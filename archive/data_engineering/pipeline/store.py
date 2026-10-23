"""Idempotent SQLite storage, one row per source, region, observation timestamp."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "energy.db"
MEASURES = ["consumption_mw", "nuclear_mw", "wind_mw", "solar_mw",
            "hydro_mw", "thermal_mw", "bioenergy_mw", "exchange_mw"]


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=30)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            source TEXT NOT NULL,
            region_code TEXT NOT NULL,
            region TEXT NOT NULL,
            observation_utc TEXT NOT NULL,
            retrieved_utc TEXT NOT NULL,
            consumption_mw REAL,
            nuclear_mw REAL,
            wind_mw REAL,
            solar_mw REAL,
            hydro_mw REAL,
            thermal_mw REAL,
            bioenergy_mw REAL,
            exchange_mw REAL,
            quality_flag TEXT NOT NULL,
            PRIMARY KEY(source, region_code, observation_utc)
        )
    """)
    return connection


def save_records(rows):
    fields = ["source", "region_code", "region", "observation_utc", "retrieved_utc", *MEASURES, "quality_flag"]
    columns = ", ".join(fields)
    placeholders = ", ".join(["?"] * len(fields))
    updates = ", ".join(f"{field}=excluded.{field}" for field in fields if field not in ("source", "region_code", "observation_utc"))
    statement = f"INSERT INTO measurements ({columns}) VALUES ({placeholders}) ON CONFLICT(source, region_code, observation_utc) DO UPDATE SET {updates}"
    with connect() as conn:
        conn.executemany(statement, [[row.get(field) for field in fields] for row in rows])
        n = conn.execute("SELECT COUNT(*) FROM measurements").fetchone()[0]
    return n
