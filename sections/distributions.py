import streamlit as st
from sections.common import empty, limitations
from utils.viz import histogram
from utils.schema import LABELS
from sections.deep_dives import extremes


def render(ctx):
    st.subheader("10 / Distributions & Anomalies")
    d = ctx.raw
    if empty(d): return
    st.markdown("#### Are high-demand events unusual or part of a wider pattern?")
    c = ctx.metric
    g = d.dropna(subset=[c])
    if g.empty:
        st.warning("No measurements available for the selected indicator."); return
    result = extremes(g[c])
    threshold = result["threshold"]
    n = result["above"]
    st.metric(f"99th percentile — {LABELS.get(c, c)} (MW)", f"{threshold:,.0f}")
    st.caption(f"{n:,} readings exceed this within-selection percentile. They are flagged for analysis, not automatically discarded.")
    if len(g) > 25000:
        g = g.sample(25000, random_state=42)
        st.caption("Histogram uses a reproducible 25,000-record sample.")
    fig = histogram(g, c, title=f"Distribution of {LABELS.get(c, c)} (MW)")
    fig.update_xaxes(title=f"{LABELS.get(c, c)} (MW)")
    st.plotly_chart(fig, use_container_width=True, key="distribution_hist")
    limitations("Outliers can be genuine demand peaks or data issues. Extreme values are not removed without documented checks.")
