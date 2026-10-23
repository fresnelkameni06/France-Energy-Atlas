import streamlit as st
from sections.common import empty, limitations


def render(ctx):
    st.subheader("03 / Comparing Years")
    d = ctx.daily
    if empty(d): return
    st.markdown("#### What changed between comparable years?")
    by = d.groupby("year", as_index=False).agg(total_mwh=("consumption_mwh", "sum"),
                                                observed_hours=("interval_hours", "sum"),
                                                peak_mw=("peak_demand_mw", "max"),
                                                recorded_readings=("readings", "sum"))
    by["avg_reported_mw"] = by.total_mwh / by.observed_hours.where(by.observed_hours > 0)
    st.dataframe(by.rename(columns={"year": "Year", "total_mwh": "Reported demand (MWh)",
                                     "observed_hours": "Reporting region-hours",
                                     "peak_mw": "Max regional demand (MW)"}), hide_index=True, use_container_width=True)
    st.markdown("**Analytical takeaway:** Compare the same calendar months and regions before interpreting year-over-year changes. The latest year is incomplete.")
    limitations("The dataset begins in 2020 and includes a partial 2026. Total MWh can only be compared over equivalent coverage windows.")
