import pandas as pd
import streamlit as st
from sections.common import heading, empty, limitations
from utils.viz import line


def render(ctx):
    st.subheader("02 / Electricity at a Glance")
    d = ctx.daily
    if empty(d): return
    heading("How does average electricity demand change through the selected period?")
    a = d.groupby("date", as_index=False).agg(demand_mwh=("consumption_mwh", "sum"),
                                               reading_count=("valid_demand", "sum"))
    a["date"] = pd.to_datetime(a.date)
    if ctx.aggregation == "Weekly":
        a["period"] = a.date.dt.to_period("W").dt.start_time
    elif ctx.aggregation == "Monthly":
        a["period"] = a.date.dt.to_period("M").dt.start_time
    else:
        a["period"] = a.date
    plot = a.groupby("period", as_index=False).demand_mwh.sum()
    fig = line(plot, "period", "demand_mwh", title=f"Reported Electricity Demand | {ctx.aggregation} (MWh)")
    fig.update_xaxes(title="Date"); fig.update_yaxes(title="Energy demand (MWh)")
    st.plotly_chart(fig, use_container_width=True, key="overview_line")
    top = a.loc[a.demand_mwh.idxmax()]
    st.markdown(f"**Evidence:** The largest reported daily sum in the selection was **{top.demand_mwh:,.0f} MWh**, on **{top.date:%d %B %Y}**.")
    limitations("Incomplete regions or missing measurements may depress reported totals; this is not a weather-normalized demand model.")
