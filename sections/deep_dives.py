"""Reusable drill-down statistics; charts remain in the specialized chapters."""
import pandas as pd


def regional_summary(daily: pd.DataFrame) -> pd.DataFrame:
    if daily.empty:
        return pd.DataFrame(columns=["region", "total_mwh", "reporting_hours", "avg_mw"])
    summary = daily.groupby("region", as_index=False).agg(
        total_mwh=("consumption_mwh", "sum"),
        reporting_hours=("interval_hours", "sum"),
    )
    summary["avg_mw"] = summary.total_mwh / summary.reporting_hours.where(summary.reporting_hours > 0)
    return summary


def extremes(series: pd.Series, quantile: float = .99) -> dict:
    valid = series.dropna()
    if valid.empty:
        return {"threshold": None, "above": 0}
    cutoff = valid.quantile(quantile)
    return {"threshold": float(cutoff), "above": int((valid > cutoff).sum())}
