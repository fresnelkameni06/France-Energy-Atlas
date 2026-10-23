import pandas as pd
import streamlit as st
from sections.common import empty, limitations
from utils.viz import scatter
from utils.schema import LABELS


def render(ctx):
    st.subheader("09 / What Moves Together?")
    d = ctx.daily
    if empty(d): return
    st.markdown("#### Is electricity demand associated with electricity generation?")
    # Daily regional aggregates, not arbitrary 15- and 30-minute readings.
    a = d.copy()
    a["generation_avg_mw"] = a.generation_mwh / a.interval_hours.where(a.interval_hours > 0)
    x = "mean_demand_mw"
    y = "generation_avg_mw"
    a = a.dropna(subset=[x, y])
    if len(a) < 30:
        st.warning("At least 30 paired observations are required."); return
    r = a[[x, y]].corr(method="pearson").iloc[0, 1]
    st.metric("Pearson r — Demand vs Generation", f"{r:+.3f}" if pd.notna(r) else "N/A")
    if len(a) > 3500:
        a = a.sample(3500, random_state=42)
        st.caption("Scatterplot sampled to 3,500 region-days for responsiveness; correlation uses all eligible observations.")
    fig = scatter(a, x, y, "region", title="Daily Regional Demand vs Generation (MW)")
    fig.update_xaxes(title="Regional average demand (MW)"); fig.update_yaxes(title="Regional average generation (MW)")
    st.plotly_chart(fig, use_container_width=True, key="corr_scatter")
    limitations("Correlation does not demonstrate a causal link. Shared seasonality and structural regional differences may influence r.")
