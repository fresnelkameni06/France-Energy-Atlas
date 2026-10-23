import streamlit as st
from sections.common import empty, limitations
from utils.viz import box

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def render(ctx):
    st.subheader("08 / Seasonal Variability")
    d = ctx.daily
    if empty(d): return
    st.markdown("#### How much does daily demand vary from month to month?")
    # Limit memory and chart latency; sampling is deterministic and documented.
    a = d.dropna(subset=["mean_demand_mw"]).copy()
    if len(a) > 12000:
        a = a.sample(n=12000, random_state=42)
        st.caption("Visualization uses a reproducible sample of 12,000 region-day records.")
    a["month_name"] = a.month.map(dict(enumerate(MONTHS, 1)))
    fig = box(a, "month_name", "mean_demand_mw", title="Variation in Daily Average Demand by Month")
    fig.update_xaxes(categoryorder="array", categoryarray=MONTHS, title="Month")
    fig.update_yaxes(title="Regional average demand (MW)")
    st.plotly_chart(fig, use_container_width=True, key="season_box")
    limitations("Visible values are regional observations; unequal region sizes and missing readings affect comparisons.")
