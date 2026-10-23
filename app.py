"""France Energy Atlas | EFREI Data Storytelling Project."""
from dataclasses import dataclass
from datetime import date

import pandas as pd
import streamlit as st

from utils.io import ROOT, load_facts, load_daily, load_quality, available_years
from utils.schema import NUMERIC, GENERATION, LABELS
from sections import (
    intro, overview, historical, regional, geography, energy_mix, temporal,
    seasonality, correlations, distributions, data_quality, conclusions,
    methodology, profile,
)

st.set_page_config(
    page_title="France Energy Atlas | EFREI",
    page_icon="⚡", layout="wide", initial_sidebar_state="expanded",
)

# Soft, readable UI. Plotly's palette is configured in utils/viz.py.
st.markdown("""<style>
.block-container {padding-top:1.3rem;max-width:1470px;padding-bottom:2rem;}
[data-testid="stSidebar"] {background:#EEF4F8;border-right:1px solid #D7E3EC;}
[data-testid="stSidebar"] * {color:#25384A;}
[data-testid="stSidebar"] .stCaption {color:#627789;}
h1,h2,h3 {letter-spacing:-0.025em;}
[data-testid="stMetric"] {background:#FFFFFF;border:1px solid #DFE8EF;border-radius:12px;padding:13px;}
[data-testid="stMetricValue"] {color:#376F8A;font-size:1.55rem;}
[data-testid="stExpander"] {border:1px solid #DCE7EE;border-radius:10px;}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {background-color:#DCEBF3 !important;}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {color:#22465D !important;}
</style>""", unsafe_allow_html=True)


@dataclass
class Context:
    raw: pd.DataFrame
    daily: pd.DataFrame
    quality: dict
    years: list[int]
    regions: list[str]
    metric: str
    energy_sources: list[str]
    aggregation: str
    top_n: int


pages = {
    "01 · Introduction": intro.render,
    "02 · Overview": overview.render,
    "03 · Historical Evolution": historical.render,
    "04 · Regional Ranking": regional.render,
    "05 · Regional Map": geography.render,
    "06 · Generation Mix": energy_mix.render,
    "07 · Hourly Patterns": temporal.render,
    "08 · Seasonal Variability": seasonality.render,
    "09 · Correlations": correlations.render,
    "10 · Distribution & Peaks": distributions.render,
    "11 · Data Quality & EDA": data_quality.render,
    "12 · Conclusions & Actions": conclusions.render,
    "13 · Methodology": methodology.render,
    "14 · Student & Credits": profile.render,
}

st.markdown("""<style>
/* Soft vertical navigation tabs */
[data-testid="stSidebar"] div.stButton > button {
    text-align: left;
    justify-content: flex-start;
    border-radius: 8px;
    min-height: 2.1rem;
    font-size: .85rem;
}
</style>""", unsafe_allow_html=True)

st.sidebar.image(str(ROOT / "assets" / "efrei.webp"), width=185)
st.sidebar.markdown("### France Energy Atlas")
st.sidebar.caption("RTE / ODRÉ  ·  Electricity, 2020–2026")

quality = load_quality()
years_available = available_years()
if not years_available:
    st.error("Prepared data not found. Run `python -m scripts.prepare_data` using the Excel workbook in data/.")
    st.stop()

# Left sidebar: navigation + a single compact year-range slider.

# Navigation — Radio buttons in the left sidebar
st.sidebar.markdown("### Dashboard Navigation")

page = st.sidebar.radio(
    "Choose a chapter",
    options=list(pages.keys()),
    index=0,
    key="dashboard_navigation",
    label_visibility="collapsed",
)


st.sidebar.divider()
st.sidebar.caption("Regional and advanced filters are above the charts.")
st.sidebar.caption(f"Workbook: {quality.get('workbook_name', 'not found')}")
st.sidebar.caption(f"Source updated through: {quality.get('date_max', 'unknown')}")


# Year selection — Sidebar
st.sidebar.markdown("### Select Study Period")

if len(years_available) == 1:
    years = list(years_available)
else:
    default_year = 2025 if 2025 in years_available else max(years_available)

    start_year, end_year = st.sidebar.select_slider(
        "Year range",
        options=years_available,
        value=(default_year, default_year),
    )

    years = [
        year for year in years_available
        if start_year <= year <= end_year
    ]

raw = load_facts(tuple(years))
daily = load_daily()
if raw.empty or daily.empty:
    st.warning("No data available for the selected year(s).")
    st.stop()

raw = raw[raw.year.isin(years)]
daily = daily[daily.year.isin(years)]
regions_all = sorted(raw.region.dropna().unique().tolist())

st.title("⚡ France Energy Atlas")
st.caption("DATA STORYTELLING · RTE / ODRÉ · EFREI Paris")


# Above the charts: choose the geographical scope with radio buttons.
with st.container(border=True):
    st.markdown("**Explore the data**")
    geographic_scope = st.radio(
        "Regional coverage",
        ["All regions", "One region", "Compare regions"],
        horizontal=True,
        help="The geographical filter is applied to all analyses.",
    )
    if geographic_scope == "One region":
        default_region = regions_all.index("Île-de-France") if "Île-de-France" in regions_all else 0
        regions = [st.selectbox("Choose a region", regions_all, index=default_region)]
    elif geographic_scope == "Compare regions":
        regions = st.multiselect(
            "Choose regions to compare",
            regions_all,
            default=regions_all[:2],
            help="Only selected regions will appear on the charts.",
        )
    else:
        regions = regions_all
        st.caption(f"All {len(regions_all)} available metropolitan regions are included.")

    # The date range is optional because the year slider already controls time.
    with st.expander("Advanced date filter (optional)", expanded=False):
        custom_date = st.checkbox("Use a custom date range", value=False)
        if custom_date:
            available_dates = pd.to_datetime(daily.loc[daily.year.isin(years), "date"])
            minimum = available_dates.min().date()
            maximum = available_dates.max().date()
            selected = st.date_input(
                "Date range", value=(minimum, maximum),
                min_value=minimum, max_value=maximum,
                key=f"custom_date_{years[0]}_{years[-1]}",
            )
        else:
            selected = None

if not regions:
    st.info("Select at least one region to continue.")
    st.stop()
raw = raw[raw.region.isin(regions)]
daily = daily[daily.region.isin(regions)]

if custom_date:
    if not isinstance(selected, (tuple, list)) or len(selected) != 2:
        st.info("Choose a start and end date.")
        st.stop()
    start, end = selected
    if start > end:
        st.warning("The start date must be before the end date.")
        st.stop()
    raw = raw[(raw.local_time.dt.date >= start) & (raw.local_time.dt.date <= end)]
    dates = pd.to_datetime(daily.date)
    daily = daily[(dates.dt.date >= start) & (dates.dt.date <= end)]

# Context defaults are kept compatible with all existing sections.
metric = "consumption_mw"
energy_sources = list(GENERATION)
aggregation = "Monthly"

# Specialized filters belong on their relevant page, not in the global sidebar.
if page in ("02 · Overview", "06 · Generation Mix"):
    aggregation = st.radio(
        "Time aggregation", ["Daily", "Weekly", "Monthly"],
        index=2, horizontal=True,
    )

if page == "10 · Distribution & Peaks":
    metric = st.selectbox(
        "Indicator to explore", NUMERIC,
        format_func=lambda value: f"{LABELS.get(value, value)} (MW)",
    )

if page == "06 · Generation Mix":
    with st.expander("Choose production sources", expanded=False):
        st.caption("Select the sources displayed in the energy mix chart.")
        cols = st.columns(3)
        energy_sources = [
            source for idx, source in enumerate(GENERATION)
            if cols[idx % 3].checkbox(LABELS.get(source, source), value=True, key=f"src_{source}")
        ]

if 2026 in years:
    st.caption("⚠️ 2026 is incomplete. Compare equivalent dates when interpreting annual changes.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Selected observations", f"{len(raw):,}")
c2.metric("Reporting regions", str(raw.region_code.nunique()))
c3.metric("Demand (MWh)", f"{raw.consumption_mwh.sum():,.0f}")
c4.metric("Source updated through", quality.get("date_max", "N/A"))

ctx = Context(
    raw=raw, daily=daily, quality=quality, years=years, regions=regions,
    metric=metric, energy_sources=energy_sources,
    aggregation=aggregation, top_n=len(regions),
)
pages[page](ctx)

st.divider()
st.caption(
    "Academic project · RTE / ODRÉ · Regional electricity statistics are descriptive, "
    "not causal evidence or a continuously live feed."
)
