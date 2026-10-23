import pandas as pd
import streamlit as st
from sections.common import empty


def render(ctx):
    st.subheader("12 / Findings & Implications")
    d = ctx.daily
    if empty(d): return
    st.markdown("#### What does the evidence say, and what remains uncertain?")
    g = d.groupby("region", as_index=False).agg(total_mwh=("consumption_mwh", "sum"), hours=("interval_hours", "sum"))
    g["avg_mw"] = g.total_mwh / g.hours.where(g.hours > 0)
    g = g.dropna(subset=["avg_mw"]).sort_values("avg_mw", ascending=False)
    if not g.empty:
        st.success(f"**Regional contrast:** {g.iloc[0].region} reports the highest average regional demand in this selection: {g.iloc[0].avg_mw:,.0f} MW.")
    p = d.groupby("date", as_index=False).consumption_mwh.sum()
    if not p.empty:
        top = p.loc[p.consumption_mwh.idxmax()]
        st.write(f"**Period of greatest recorded demand:** {top.date:%d %B %Y} with {top.consumption_mwh:,.0f} MWh across the selected reporting regions.")
    total_production = d.generation_mwh.sum(min_count=1)
    renewable = d.renewable_mwh.sum(min_count=1)
    if pd.notna(total_production) and total_production > 0:
        st.write(f"**Renewable generation share:** {100 * renewable / total_production:.1f}% of selected recorded generation, subject to missing-data coverage.")
    st.markdown("""**Recommendations for decision support**
    - Investigate persistent regional differences before treating them as policy performance.
    - Examine peak periods and seasonal variability when planning further monitoring.
    - Track generation-source trends using matched time windows.
    - Prioritize completeness and year-to-date warnings in public communication.

    **Next steps:** include population-normalized demand and weather data in future work before proposing explanations for regional differences.
    """)
