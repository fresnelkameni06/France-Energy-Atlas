"""Excel normalization, quality controls and non-causal feature engineering."""
import pandas as pd
import numpy as np
from utils.schema import NUMERIC, GENERATION, RENEWABLES, SOURCE_HIST, SOURCE_LIVE

KEY = ["source", "region_code", "observation_utc"]


def normalize_sheet(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Keep valid rows and flag, rather than impute, missing measurements."""
    initial = len(raw)
    d = raw.copy()
    d.columns = d.columns.astype(str).str.strip().str.lower()
    required = {"source", "region_code", "region", "observation_utc"}
    missing = required - set(d.columns)
    if missing:
        raise ValueError(f"Excel missing required fields: {sorted(missing)}")
    d["source"] = d["source"].astype("string").str.strip()
    d["region_code"] = d["region_code"].astype("string").str.replace(r"\.0$", "", regex=True).str.strip()
    d["region"] = d["region"].astype("string").str.strip()
    # Support both the real XlsxWriter ISO timestamp strings and native
    # Excel date serial numbers (as used by some spreadsheet exporters).
    serial = pd.to_numeric(d["observation_utc"], errors="coerce")
    from_text = pd.to_datetime(
        d["observation_utc"].where(serial.isna()),
        utc=True, errors="coerce", format="mixed",
    )
    from_excel = pd.to_datetime(
        serial.where(serial.between(20000, 100000)),
        unit="D", origin="1899-12-30", utc=True, errors="coerce",
    )
    d["observation_utc"] = from_text.fillna(from_excel)
    d = d.dropna(subset=["observation_utc", "region_code", "region", "source"])
    d = d[(d.region_code.str.len() > 0) & (d.region.str.len() > 0)]
    d = d[d.source.isin([SOURCE_HIST, SOURCE_LIVE])]
    for c in NUMERIC:
        if c not in d:
            d[c] = np.nan
        d[c] = pd.to_numeric(d[c], errors="coerce")
        if c != "exchange_mw":
            d.loc[d[c] < 0, c] = np.nan
    if "quality_flag" not in d:
        d["quality_flag"] = "not_recorded"
    d["quality_flag"] = d["quality_flag"].fillna("not_recorded").astype(str)
    d = d.drop_duplicates(KEY, keep="last")
    d["interval_hours"] = np.where(d.source.eq(SOURCE_HIST), 0.5, 0.25)
    # If definitive data exist for a 30-minute interval, discard provisional
    # 15-minute observations for this region and that 30-minute bucket.
    bucket = d.observation_utc.dt.floor("30min")
    d["half_hour"] = bucket
    has_hist = d[d.source.eq(SOURCE_HIST)][["region_code", "half_hour"]].drop_duplicates()
    has_hist["historical_present"] = True
    d = d.merge(has_hist, on=["region_code", "half_hour"], how="left")
    superseded = d.source.eq(SOURCE_LIVE) & d.historical_present.eq(True)
    removed_superseded = int(superseded.sum())
    d = d.loc[~superseded].drop(columns=["historical_present", "half_hour"])
    # In the presence of an unrecognized date we do not assign invented time.
    d["local_time"] = d.observation_utc.dt.tz_convert("Europe/Paris")
    d["year"] = d.local_time.dt.year.astype("int16")
    d["month"] = d.local_time.dt.month.astype("int8")
    d["hour"] = d.local_time.dt.hour.astype("int8")
    d["weekday"] = d.local_time.dt.dayofweek.astype("int8")
    d["date"] = d.local_time.dt.date.astype(str)
    for col in NUMERIC:
        d[col.replace("_mw", "_mwh")] = d[col] * d.interval_hours
    d["generation_mw"] = d[GENERATION].sum(axis=1, min_count=len(GENERATION))
    d["renewable_mw"] = d[RENEWABLES].sum(axis=1, min_count=len(RENEWABLES))
    d["renewable_share_pct"] = (100 * d.renewable_mw / d.generation_mw).where(d.generation_mw > 0)
    d["missing_measurements"] = d[NUMERIC].isna().sum(axis=1).astype("int8")
    d["generation_mwh"] = d.generation_mw * d.interval_hours
    d["renewable_mwh"] = d.renewable_mw * d.interval_hours
    d = d.sort_values(["observation_utc", "region_code"])
    return d.reset_index(drop=True), {
        "input_rows": int(initial), "output_rows": int(len(d)),
        "invalid_or_duplicate_or_superseded": int(initial-len(d)),
        "superseded_live_rows": removed_superseded,
        "null_consumption_rows": int(d.consumption_mw.isna().sum()),
    }


def aggregate_daily(d: pd.DataFrame) -> pd.DataFrame:
    if d.empty:
        return pd.DataFrame()
    energy_fields = [c.replace("_mw", "_mwh") for c in NUMERIC]
    grp = d.groupby(["date", "region", "region_code"], observed=True, as_index=False)
    sums = grp[energy_fields + ["generation_mwh", "renewable_mwh", "interval_hours"]].sum(min_count=1)
    counts = grp.agg(readings=("source", "size"), valid_demand=("consumption_mw", "count"),
                     peak_demand_mw=("consumption_mw", "max"),
                     mean_demand_mw=("consumption_mw", "mean"),
                     average_renewable_share_pct=("renewable_share_pct", "mean"))
    daily = sums.merge(counts, on=["date", "region", "region_code"], validate="1:1")
    daily["date"] = pd.to_datetime(daily.date)
    daily["year"] = daily.date.dt.year
    daily["month"] = daily.date.dt.month
    return daily


def stats_for_years(d: pd.DataFrame) -> pd.DataFrame:
    """Useful for period-matched annual comparisons, not crude YTD/full-year claims."""
    if d.empty:
        return d
    return d.groupby("year", as_index=False).agg(
        demand_mwh=("consumption_mwh", "sum"),
        mean_demand_mw=("mean_demand_mw", "mean"),
        observations=("readings", "sum"),
    )
