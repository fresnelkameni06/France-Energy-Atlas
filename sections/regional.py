import streamlit as st
from sections.common import empty, limitations
from utils.viz import bar
from sections.deep_dives import regional_summary


def render(ctx):
    st.subheader("04 / Regional Rankings")
    d = ctx.daily
    if empty(d): return
    st.markdown("#### Which regions report the highest average power demand?")
    g = regional_summary(d).dropna(subset=["avg_mw"]).sort_values("avg_mw")
    fig = bar(g, "region", "avg_mw", title="Average Demand by Region (MW)")
    fig.update_xaxes(title="Mean reported demand (MW)"); fig.update_yaxes(title="Region")
    st.plotly_chart(fig, use_container_width=True, key="region_bar")
    winner = g.iloc[-1]
    st.write(f"**Evidence:** {winner.region} records the highest mean demand in the selection (**{winner.avg_mw:,.0f} MW**).")
    limitations("Regional demand is not population-adjusted; absolute power does not measure per-capita consumption.")
