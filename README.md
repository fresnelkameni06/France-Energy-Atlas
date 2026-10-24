# ⚡ France Energy Atlas (2020–2026)

**An interactive data-storytelling dashboard exploring regional electricity demand and generation in France.**

[**🌐 Explore the live dashboard**](https://france-energy-atlas-fk.streamlit.app/) · [**📊 Open data: RTE / ODRÉ**](https://odre.opendatasoft.com/) · **EFREI Paris — Individual Student Project**

> **Project question:** How have electricity consumption and generation patterns evolved across 12 metropolitan French regions between 2020 and 2026, and which temporal and geographical differences deserve closer investigation?

**Course:** Data Visualization & Data Storytelling  
**Academic supervisor:** Prof. Mano Joseph Mathew (EFREI Paris)  
**Stack:** Python 3.12 · Streamlit · Pandas · NumPy · Plotly · SQLite · Excel · Parquet · GitHub Actions

## Project at a glance

| Dataset snapshot | Value |
|---|---:|
| Validated interval observations | **1,463,328** |
| Metropolitan regions | **12** |
| Years represented | **2020–2026** |
| Region-day aggregate records | **29,856** |
| Missing demand measurements | **108** |
| Storytelling chapters | **14** |
| Primary interactive chart families | **8** |

*These figures refer to the locally validated analytical snapshot; they are **not** live counters. The 2026 data cover only part of the year. The exact latest reporting date is shown within the application.*

## The story: 14 connected chapters

Rather than presenting isolated charts, France Energy Atlas follows **Hook → Context → Analysis → Insights → Implications**.

| Chapter | What it answers | Presentation |
|---|---|---|
| 01 · Introduction | Why are French regional electricity patterns worth studying? | Motivation, scope, central question |
| 02 · Overview | When does recorded demand rise or fall? | **Interactive line chart** and dynamic KPIs |
| 03 · Historical Evolution | How can 2020–2026 be compared fairly? | Annual summaries and coverage caveats |
| 04 · Regional Ranking | Which regions report higher average demand? | **Horizontal bar chart** |
| 05 · Regional Map | Where are those regions located? | **Interactive geographical map** |
| 06 · Generation Mix | How do generation technologies contribute over time? | **Stacked area chart** |
| 07 · Hourly Patterns | When during the week is demand relatively high? | **Weekday × hour heatmap** |
| 08 · Seasonal Variability | How does demand variability differ by month? | **Monthly box plots** |
| 09 · Correlations | Are regional demand and generation associated? | **Scatter plot** and Pearson's *r* |
| 10 · Distribution & Peaks | How unusual are high measurements? | **Histogram** and 99th percentile |
| 11 · Data Quality & EDA | How complete and consistent are the data? | Missingness and validation indicators |
| 12 · Conclusions & Actions | What can we conclude from the current selection? | Filter-aware findings and next steps |
| 13 · Methodology | Where do the data come from, and what assumptions were made? | Provenance, transformations, limitations |
| 14 · Student & Credits | Who developed the work? | EFREI identification, GitHub, LinkedIn, portfolio |

The interface provides left-side chapter navigation and purposeful selections of years, regions, dates and relevant indicators. Charts include contextual interpretation rather than unsupported causal explanations.

## Official data sources and licensing

The original observations were obtained from official **RTE / ODRÉ éCO2mix regional electricity datasets**:

- [Consolidated and definitive regional measurements — `eco2mix-regional-cons-def`](https://odre.opendatasoft.com/explore/dataset/eco2mix-regional-cons-def/) (generally 30-minute intervals).
- [Provisional regional measurements — `eco2mix-regional-tr`](https://odre.opendatasoft.com/explore/dataset/eco2mix-regional-tr/) (15-minute intervals).
- [French government open-data catalogue](https://www.data.gouv.fr/datasets/donnees-eco2mix-regionales-consolidees-et-definitives).

**Attribution:** Data © RTE / ODRÉ, made available under **Licence Ouverte / Open Licence 2.0 (Etalab)**. This project is an independent academic analysis, not an official RTE publication. Source details and the associated reuse requirements are discussed in [`docs/sources_and_licenses.md`](docs/sources_and_licenses.md).

## Data Engineering and reproducibility

The project was built in **two distinct stages**:

```text
HISTORICAL ACQUISITION & STORAGE
Official RTE / ODRÉ API
          ↓
Python extraction and cleaning
          ↓
SQLite database (data/energy.db, local)
          ↓
Excel export (2020–2026 annual worksheets, local)

DASHBOARD PREPARATION & EXECUTION
Existing Excel workbook
          ↓
Pandas normalization + automated validation
          ↓
Compressed Parquet facts + region-day aggregates
          ↓
Streamlit + Plotly interactive chapters
```

The historical acquisition and SQL scripts are retained under `archive/data_engineering/`. The current deployed application reads **prepared Parquet**, not the SQLite database or RTE API directly. An unrefreshed Excel workbook will not create new observations.

**Important methodological decisions:**

- Preserve missing measurements; do not replace unknown data with zero.
- Deduplicate observations and give definitive data priority when source periods overlap.
- Normalize timestamps to UTC; derive local calendar fields in `Europe/Paris`.
- Convert **power (MW)** into **energy (MWh)** using interval duration: `MWh = MW × hours` (0.5 h historical; 0.25 h provisional).
- Document unequal temporal coverage, especially incomplete 2026.
- Treat correlations as descriptive relationships, **not causal effects**.
- Use deterministic sampling where needed for interactive chart performance.

## Repository layout

```text
France-Energy-Atlas/
├── app.py                      # Streamlit entry point and filters
├── sections/                   # Fourteen analytical and narrative chapters
├── utils/                      # Data loading, schemas, preparation, plotting
├── scripts/                    # Offline preparation and data validation
├── pipeline/                   # Excel data-processing module
├── archive/data_engineering/   # Historical RTE API, cleaning, SQLite, export
├── data/processed/             # Optimized Parquet files + quality metadata
├── config/                     # Student and application metadata (no secrets)
├── assets/                     # Institutional branding
├── docs/                       # Report, EDA, storyboard, sources, demo script
├── tests/                      # Unit tests
├── .github/workflows/          # CI and optional data-refresh workflow
├── .streamlit/config.toml      # Visual theme
├── requirements.txt
└── README.md
```

The original database `data/energy.db`, Excel workbook and virtual environment are intentionally **not required in the published application repository**. A dataset-source link is provided as an alternative to bundling large original files.

## Run locally

Requires **Python 3.12**. In PowerShell, from the repository root:

```powershell
python -m venv venv_viz
.\venv_viz\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m scripts.validate_data
python -m streamlit run app.py --server.port 8502
```

If `data/processed/` is absent, first obtain the **consolidated project Excel workbook** (`data/france_energy_2020_2026.xlsx`) and run:

```powershell
python -m scripts.prepare_data
python -m scripts.validate_data
```

The official RTE dataset links above provide the original public source, **not an automatically identical copy of this seven-worksheet consolidated workbook**. Rebuilding the exact workbook from scratch requires the historical Data Engineering workflow.

## Continuous integration and planned refresh automation

**Already demonstrated:** the GitHub Actions workflow **France Energy Atlas – Quality Checks** completed successfully after a push. It installs dependencies, runs unit tests and validates the prepared analytical data. A green CI check does **not** mean that new RTE measurements have been downloaded.

**Planned, not yet verified end-to-end:** an Excel-based refresh workflow (`refresh_excel.yml`) can be enabled after a maintained, updated workbook is made available via a configured URL or GitHub Release asset. The intended sequence is:

1. Acquire an **updated** Excel workbook from the configured source.
2. Validate and regenerate the Parquet analytical datasets.
3. Commit the changed Parquet data to GitHub.
4. Let Streamlit Community Cloud synchronize with the updated repository.

If the Excel source has not changed, **no new electricity readings can appear**. Future work may connect the archived RTE API extraction pipeline to a scheduled, tested ingestion job, with source-rate limits, validation and failure notifications.

## Deployment and project deliverables

- **Live dashboard:** https://france-energy-atlas-fk.streamlit.app/
- **GitHub repository:** https://github.com/fresnelkameni06/France-Energy-Atlas/
- **Academic report:** [`docs/France_Energy_Atlas_Report.pdf`](docs/France_Energy_Atlas_Report.pdf)
- **Detailed storyboard:** [`docs/storyboard.md`](docs/storyboard.md)
- **Student portfolio:** https://fresnelkameni06.github.io/fresnelk.github.io/



## Limitations and ethical interpretation

This is an exploratory, descriptive academic project—not a forecast, operational monitoring service or proof of policy impact. Regional demand is not adjusted for population, weather or industrial structure. The map uses representative locations rather than power-plant coordinates. Regionally generated power is not necessarily consumed locally. Missing records, provisional revisions and incomplete-year data may influence totals.

## Acknowledgements

Developed at **EFREI Paris** for an individual Data Visualization & Data Storytelling assignment proposed by **Prof. Mano Joseph Mathew**. We thank **RTE / ODRÉ** for providing reusable official electricity data.

*France Energy Atlas — turning official electricity measurements into an interpretable, interactive regional story.*
