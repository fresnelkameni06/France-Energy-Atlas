import pandas as pd
import streamlit as st
from sections.common import empty
from utils.schema import NUMERIC


def render(ctx):
    st.subheader("11 / Can We Trust These Results?")
    st.markdown("#### Reproducibility and data limitations")
    q = ctx.quality
    reports = pd.DataFrame(q.get("sheet_reports", []))
    if not reports.empty:
        st.dataframe(reports, use_container_width=True, hide_index=True)
    d = ctx.raw
    if not d.empty:
        missing = (d[NUMERIC].isna().mean().mul(100).round(2)).rename("Missing (%)").reset_index().rename(columns={"index": "Indicator"})
        st.markdown("**Missing measurements in the current selection:**")
        st.dataframe(missing, use_container_width=True, hide_index=True)
        a, b, c = st.columns(3)
        a.metric("Selected observations", f"{len(d):,}")
        b.metric("Regions", str(d.region_code.nunique()))
        c.metric("Duplicate source-region-time keys", str(int(d.duplicated(["source", "region_code", "observation_utc"]).sum())))
    st.caption("The original workbook remains unchanged. The preprocessing records source hash, counts, missingness and date coverage.")
    st.warning("2026 is partial. Historical data are generally 30-minute intervals; provisional observations are 15-minute intervals. Aggregated MWh use each record's interval length.")
