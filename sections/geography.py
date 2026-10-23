import pandas as pd
import streamlit as st
from sections.common import empty, limitations
from utils.viz import map_markers
from utils.schema import REGION_POINTS


def render(ctx):
    st.subheader("05 / Map of the Electricity Landscape")
    d = ctx.daily
    if empty(d): return
    st.markdown("#### Where are the main regional demand concentrations?")
    g = d.groupby("region", as_index=False).agg(demand=("consumption_mwh", "sum"), hours=("interval_hours", "sum"))
    g["value"] = g.demand / g.hours.where(g.hours > 0)
    g["lat"] = g.region.map(lambda x: REGION_POINTS.get(x, (None, None))[0])
    g["lon"] = g.region.map(lambda x: REGION_POINTS.get(x, (None, None))[1])
    g = g.dropna(subset=["lat", "lon", "value"])
    if g.empty:
        st.warning("No mapped regions match the selection."); return
    g["size"] = g.value.clip(lower=1)
    fig = map_markers(g, "Regional Electricity Demand — Representative City Markers")
    st.plotly_chart(fig, use_container_width=True, key="map_scatter")
    limitations("Markers represent administrative city positions, not measurement sites or regional centroids.")
