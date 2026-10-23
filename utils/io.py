"""Read prepared analytical data; never query RTE from the Streamlit app."""
from pathlib import Path
import json
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

@st.cache_data(show_spinner=False, ttl=3600, max_entries=6)
def load_facts(years: tuple[int, ...]):
    frames = []
    for year in years:
        path = PROCESSED / f"facts_{year}.parquet"
        if path.exists():
            frames.append(pd.read_parquet(path))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

@st.cache_data(show_spinner=False, ttl=3600)
def load_daily():
    path = PROCESSED / "daily_summary.parquet"
    return pd.read_parquet(path) if path.exists() else pd.DataFrame()

@st.cache_data(show_spinner=False, ttl=3600)
def load_quality():
    path = PROCESSED / "quality_summary.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def available_years():
    return sorted(int(p.stem.split("_")[1]) for p in PROCESSED.glob("facts_*.parquet") if p.stem.split("_")[-1].isdigit())
