import pandas as pd
import streamlit as st
from sections.common import empty, limitations
from utils.viz import heatmap

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def render(ctx):
    st.subheader("07 / When Do Peaks Occur?")
    d = ctx.raw
    if empty(d): return
    st.markdown("#### Which days and hours show the highest demand?")
    a = d.dropna(subset=["consumption_mw"]).copy()
    g = a.groupby(["weekday", "hour"], as_index=False).consumption_mw.mean()
    pivot = g.pivot(index="weekday", columns="hour", values="consumption_mw").reindex(range(7))
    pivot.index = DAYS
    fig = heatmap(pivot, "Average Electricity Demand by Hour and Weekday")
    st.plotly_chart(fig, use_container_width=True, key="temporal_heatmap")
    row = g.loc[g.consumption_mw.idxmax()]
    st.write(f"**Evidence:** The strongest mean selected station-equivalent regional demand occurs on **{DAYS[int(row.weekday)]} around {int(row.hour):02d}:00**.")
    limitations("Clock times use Europe/Paris. Daylight-saving transitions can produce repeated or absent local hours.")
