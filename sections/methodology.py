import streamlit as st


def render(ctx):
    st.subheader("13 / Methods, Sources & Caveats")
    st.markdown("""**Data provenance:** Public RTE / ODRÉ regional electricity exports, initially collected via the provider's API and exported from a local SQLite database into a seven-sheet Excel workbook (2020–2026).

**Current architecture:** Excel → offline validation & transformation → per-year Parquet + daily aggregates → Streamlit. **There are no RTE API requests, web scrapers, or cloud SQL dependencies in this version.**

**Processing:**
1. Validate source, timestamp and region identifiers; normalize timestamps to UTC.
2. Preserve missing data as missing, reject invalid negative generation/demand values.
3. Deduplicate by source, region and observation timestamp.
4. Prefer definitive observations when provisional intervals overlap.
5. Convert MW to MWh using the observation's 30-minute or 15-minute interval.
6. Create repeatable daily aggregations, coverage reports and plots.

**Statistical rules:** Pearson correlation is descriptive, not causal; no artificial data imputation; no unsupported forecast; comparisons of a partial year with full years are explicitly warned against.

**Update policy:** The dashboard reads prepared files. A GitHub Action can rebuild them every three days **only when an updated Excel workbook is available remotely**. It does not create new measurements by itself.

**Reproducibility:** requirements, preprocessing script, validation, documentation, tests and GitHub Actions are versioned with the repository. The source workbook and local SQLite are deliberately excluded from the code ZIP.
""")
