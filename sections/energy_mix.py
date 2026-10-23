import pandas as pd
import streamlit as st
from sections.common import empty, limitations
from utils.viz import area
from utils.schema import GENERATION, LABELS


def render(ctx):
    st.subheader("06 / How Is Electricity Generated?")
    d = ctx.daily
    if empty(d): return
    st.markdown("#### Which generation sources shape the regional electricity mix?")
    fields = [c.replace("_mw", "_mwh") for c in ctx.energy_sources]
    if not fields:
        st.warning("Choose at least one generation source in the sidebar."); return
    if ctx.aggregation == "Monthly":
        d = d.assign(period=pd.to_datetime(d.date).dt.to_period("M").dt.start_time)
    elif ctx.aggregation == "Weekly":
        d = d.assign(period=pd.to_datetime(d.date).dt.to_period("W").dt.start_time)
    else:
        d = d.assign(period=pd.to_datetime(d.date))
    g = d.groupby("period", as_index=False)[fields].sum(min_count=1)
    p = g.melt("period", var_name="source", value_name="mwh")
    p["source"] = p.source.str.replace("_mwh", "_mw").map(LABELS)
    fig = area(p, "period", "mwh", "source", title="Regional Generation Mix Over Time (MWh)")
    fig.update_xaxes(title="Date"); fig.update_yaxes(title="Production over period (MWh)")
    st.plotly_chart(fig, use_container_width=True, key="mix_area")
    st.caption("These are generation values recorded within regions, not the precise mix consumed by local households.")
