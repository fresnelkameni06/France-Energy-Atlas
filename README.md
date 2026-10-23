# France Energy Atlas | 2020–2026

### Interactive Electricity Data Storytelling Dashboard

**EFREI Paris — Individual Student Project**  
**Course:** Data Visualization & Data Storytelling  
**Supervisor:** Prof. Mano Joseph Mathew  
**Technology:** Python · Streamlit · Pandas · Plotly · SQLite · Excel · Parquet

## Overview

France Energy Atlas is an interactive data storytelling dashboard exploring electricity consumption and generation across **12 metropolitan French regions from 2020 to 2026**.

Using official open data from **RTE / ODRÉ**, the project transforms complex regional electricity measurements into accessible insights about historical trends, geographical disparities, energy generation, seasonal patterns and data quality.

**Research question:** How have electricity consumption and generation patterns evolved across French regions, and what regional and temporal differences can we identify?

## Live Dashboard & Demo

- **Streamlit Application:** [Add deployed application URL]
- **GitHub Repository:** [Add repository URL]
- **Video Demonstration (2–4 minutes):** [Add video URL]
- **Student Portfolio:** [Add portfolio URL]

## Key Features

The dashboard provides:

- 14 interactive storytelling chapters.
- 8 visualization types: line chart, bar chart, map, stacked area chart, heatmap, box plot, scatter plot and histogram.
- Interactive year, region and date selections.
- Dynamic KPIs and analytical insights.
- Regional electricity consumption and generation comparisons.
- Data quality, missingness and duplicate checks.
- Methodological explanations and responsible interpretation.

### Dashboard Chapters

| # | Chapter | Purpose |
|---|---|---|
| 01 | Introduction | Research context and problem |
| 02 | Overview | Electricity demand trends |
| 03 | Historical Evolution | Annual comparisons |
| 04 | Regional Ranking | Regional demand differences |
| 05 | Regional Map | Geographical exploration |
| 06 | Generation Mix | Electricity production by source |
| 07 | Hourly Patterns | Daily and weekly demand |
| 08 | Seasonal Variability | Monthly demand distributions |
| 09 | Correlations | Demand–generation relationships |
| 10 | Distribution & Peaks | Extreme-value exploration |
| 11 | Data Quality & EDA | Data reliability |
| 12 | Conclusions & Actions | Key findings and implications |
| 13 | Methodology | Data pipeline and limitations |
| 14 | Student & Credits | Academic and author information |

## Data Source

**Provider:** RTE — Réseau de Transport d'Électricité  
**Platform:** ODRÉ — Open Data Réseaux Énergies  
**Website:** https://odre.opendatasoft.com/

Original datasets:

- `eco2mix-regional-cons-def` — Historical regional electricity data.
- `eco2mix-regional-tr` — Provisional regional electricity data.

The prepared snapshot contains **1,463,328 observations**, covering 12 regions and seven calendar years.

**Note:** 2026 is incomplete. Historical and provisional data may have different sampling intervals.

## Data Engineering Pipeline

The project was developed through two complementary pipelines.

**Original collection and consolidation:**

`RTE API → Python Extraction → Cleaning → SQLite → Excel`

**Current dashboard preparation:**

`Excel → Pandas Validation → Parquet → Streamlit`

The original API extraction, cleaning and SQLite scripts are preserved in `archive/data_engineering/`.

The dashboard operates on prepared local datasets and does not fetch new RTE measurements whenever a user opens the application.

## Project Structure

```text
France-Energy-Atlas/
├── app.py                  # Main Streamlit application
├── sections/               # 14 storytelling chapters
├── utils/                  # Data loading and visualization
├── scripts/                # Preparation and validation
├── pipeline/               # Excel processing
├── archive/data_engineering/ # Original API and SQLite workflow
├── data/
│   └── processed/          # Prepared analytical datasets
├── docs/                   # Reports and documentation
├── tests/                  # Automated tests
├── assets/                 # EFREI logo
├── config/                 # Project and student metadata
├── .streamlit/             # Application theme
├── requirements.txt
└── README.md
```

## Installation and Local Execution

**Requirements:** Python 3.12 and an internet connection for initial package installation.

Clone or download the repository, then open a terminal in the project folder.

**1. Create and activate a virtual environment (Windows PowerShell):**

```powershell
python -m venv venv_viz
.\venv_viz\Scripts\Activate.ps1
```

**2. Install dependencies:**

```powershell
python -m pip install -r requirements.txt
```

**3. Prepare the analytical data (if not already provided):**

Place `france_energy_2020_2026.xlsx` inside `data/`, then execute:

```powershell
python -m scripts.prepare_data
python -m scripts.validate_data
```

**4. Launch the dashboard:**

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

**Important:** The Excel workbook is needed to rebuild the analytical data. If the prepared Parquet datasets are already included, the dashboard can read them directly.

## Data Quality and Reproducibility

The project includes:

- Duplicate and invalid-value checks.
- Explicit handling of missing measurements.
- UTC timestamp normalization and French local-time conversion.
- MW-to-MWh conversion using observation durations.
- Definitive-source prioritization when historical and provisional records overlap.
- Automated preprocessing tests.

Run the tests with:

```powershell
python -m unittest discover -s tests -v
```

## Deployment

The application is designed for **Streamlit Community Cloud**, connected to this GitHub repository.

The deployment must have access to the prepared analytical datasets under `data/processed/`. Large raw datasets and the original SQLite database are not required for normal dashboard execution.

A GitHub Actions configuration is included for dataset preparation. New electricity observations require an updated external source workbook; the dashboard does not perform automatic live RTE collection.

## Documentation

Detailed documentation is available in `docs/`:

- `project_brief.md` — Introduction, problem and objectives.
- `analysis_plan.md` — Research questions and analytical strategy.
- `methodology.md` — Data engineering and transformations.
- `eda_report.md` — Exploratory data analysis.
- `database_audit.md` — Quality and validation.
- `storyboard.md` — Detailed explanation of the 14 chapters.
- `data_dictionary.md` — Dataset variables.
- `sources_and_licenses.md` — Data sources and attribution.
- `demo_script.md` — Video demonstration script.
- `submission_checklist.md` — Final submission requirements.

## Limitations

The dashboard is descriptive, not predictive. Regional values are not adjusted for population, weather or economic activity. Correlations do not imply causation, and incomplete-year comparisons require particular care.

## Author and Acknowledgements

**Developed by:** [Student Full Name]  
**Institution:** EFREI Paris  
**Program:** [Academic Program]  
**Academic Year:** [Academic Year]  
**Supervisor:** Prof. Mano Joseph Mathew

Thanks to RTE / ODRÉ for making regional electricity data publicly available.

---

**France Energy Atlas — Turning electricity data into meaningful stories.**