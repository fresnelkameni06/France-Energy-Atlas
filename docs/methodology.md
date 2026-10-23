# Methodology — Data Collection, Engineering and Analytical Processing

## 1. Purpose of This Document

This document describes the technical and methodological process used to construct France Energy Atlas.

It explains how public electricity observations were initially collected, cleaned, stored in SQLite, exported to Excel, transformed into optimized analytical datasets and finally visualized in Streamlit.

The workflow was designed around four principles:

1. **Traceability:** every analytical observation must originate from an identifiable source.
2. **Data integrity:** invalid and missing measurements must be handled explicitly.
3. **Reproducibility:** transformations should be repeatable using documented Python scripts.
4. **Interpretability:** statistical indicators must preserve their physical meaning and limitations.

The project distinguishes its original historical data-engineering pipeline from the current dashboard execution pipeline.

---

## 2. Overall System Architecture

The project evolved through several technical stages.

### Stage A — Historical data acquisition

RTE / ODRÉ API → Python extraction → Cleaning and validation → SQLite database

### Stage B — Dataset consolidation

SQLite database → Structured export → Excel workbook with seven annual worksheets

### Stage C — Analytical preparation

Excel workbook → Data normalization → Quality checks → Feature engineering → Annual Parquet files and daily aggregates

### Stage D — Data storytelling

Prepared Parquet datasets → Streamlit application → Interactive charts, KPIs and narrative insights

The SQLite database and Excel workbook serve as historical and analytical artifacts. The deployed dashboard is designed to read prepared Parquet files rather than query SQLite or the remote API at runtime.

## 3. Data Source Identification

### 3.1 Official provider

The original electricity observations were obtained from public datasets published by RTE and distributed through the ODRÉ open-data platform.

RTE is France's electricity transmission system operator. The regional Eco2mix datasets provide measurements concerning electricity consumption, electricity generation by technology and physical electricity exchanges.

### 3.2 Source datasets

Two source identifiers are relevant to this project:

| Dataset identifier | Role | Typical interval |
|---|---|---|
| `eco2mix-regional-cons-def` | Historical/definitive regional measurements | 30 minutes |
| `eco2mix-regional-tr` | More recent provisional regional measurements | 15 minutes |

The distinction matters because provisional values can subsequently be revised or replaced by definitive records.

It also matters because the time interval affects the calculation of electrical energy.

### 3.3 Collection method

The original extraction was performed programmatically using official data API endpoints.

This approach is more precise than describing the process as conventional website scraping. The extraction scripts retrieved structured records from the provider's API rather than reading information from rendered HTML pages.

The historical extraction code is retained in `archive/data_engineering/pipeline/` for documentation and reproducibility.

The current Streamlit application does not execute this acquisition stage.

## 4. Original API Extraction Process

The first data-engineering challenge was to obtain observations covering several years while preserving regional and temporal detail.

The historical workflow involved:

1. Identifying the relevant regional electricity datasets.
2. Requesting records from the official API.
3. Handling historical backfill and more recent observations as distinct collection activities.
4. Preserving the source identifier of every observation.
5. Retrieving electricity measurements and their regional metadata.
6. Converting the downloaded records into a consistent Python structure.
7. Cleaning the records before database insertion.
8. Storing validated information in SQLite.

The archived extraction, backfill and synchronization scripts provide the historical implementation of this process.

**Important distinction:** historical data extraction is a documented stage of the project, but it is not automatically performed when the current Streamlit dashboard starts.

## 5. Data Cleaning and Normalization

Raw API records cannot be assumed to be immediately suitable for visualization.

The cleaning process addresses both structural problems and measurement problems.

### 5.1 Mandatory identifiers

Each observation must contain sufficient information to identify:

- Its source dataset.
- Its region code.
- Its region name.
- Its observation timestamp.

Records with missing or invalid mandatory identifiers are excluded from the normalized dataset because they cannot be reliably associated with a geographical location or observation time.

### 5.2 Data type normalization

The pipeline converts measurement fields into numeric values.

Non-numeric strings, recognized missing-value markers and non-finite values are treated as missing observations.

The original cleaning process also handles numerical representations such as decimal commas.

### 5.3 Negative values

Negative electricity consumption and negative generation measurements are treated as invalid in the implemented normalization rules and converted to missing values.

However, physical electricity exchanges may legitimately be negative, depending on the measurement convention. Consequently, negative exchange values are preserved.

This distinction prevents the pipeline from incorrectly removing meaningful exchange information.

### 5.4 Missing values

Unknown values are preserved as missing rather than replaced with zero.

This is important because:

**Missing measurement ≠ Zero electricity consumption or production**

A zero represents an observed numerical value, whereas a missing measurement means that the value is unavailable or invalid.

Replacing missing observations with zero could artificially reduce demand averages, generation totals or renewable shares.

### 5.5 Duplicate observations

The principal observation key is:

`source + region_code + observation_utc`

Duplicate records sharing this key are removed during preprocessing.

The historical SQLite workflow also used uniqueness controls to protect against duplicate insertion across repeated data-acquisition operations.

The final Parquet validation explicitly checks uniqueness of the prepared observation keys.

## 6. SQLite Database Construction

### 6.1 Why SQLite was used

SQLite was selected as the local structured storage layer for the original extraction pipeline.

Its advantages for this academic project included:

- Integration with Python.
- Structured storage of large numbers of observations.
- Support for SQL queries.
- Efficient filtering and aggregation.
- Persistent local storage.
- No requirement for a separate database server.

This made it possible to separate acquisition from later analytical processing.

### 6.2 Database role

The SQLite database acted as the consolidated historical repository.

It preserved cleaned electricity records with their source, timestamp, region and quantitative measurements.

Database audit and extraction scripts were used during the historical workflow to inspect stored observations and prepare their export.

The database file is retained locally as `data/energy.db`.

### 6.3 Why the current dashboard does not query SQLite

Although SQLite was useful for acquisition and consolidation, the interactive dashboard was intentionally simplified.

Instead of reading the original database whenever users navigate between chapters, the current application uses preprocessed analytical files.

This reduces unnecessary runtime processing and allows the dashboard to operate without an active database connection.

SQLite remains important evidence of the project's data-engineering process even though it is not a runtime dependency.

## 7. Exporting SQLite Data to Excel

Following historical consolidation, the cleaned records were exported into:

`data/france_energy_2020_2026.xlsx`

The workbook contains seven worksheets, corresponding to the years 2020 through 2026.

This format provides a readable intermediate artifact and allows the current preparation pipeline to process each annual partition separately.

The original Excel export script is preserved at:

`archive/data_engineering/export_excel.py`

### Reasons for using Excel as an intermediate source

- It preserves a consolidated snapshot of the historical data.
- It offers an easily recognizable format for inspection.
- It separates the original database-building workflow from dashboard preprocessing.
- Its annual worksheets support partition-based processing.
- It avoids requiring a database connection during deployment preparation.

Excel is not used as the main analytical computation engine; Python performs the validation and transformations.

## 8. Preparing the Data for Streamlit

The current application relies on the script:

`scripts/prepare_data.py`

This script reads the existing Excel workbook and creates optimized datasets.

### 8.1 Loading annual worksheets

Pandas reads each worksheet using the Excel-reading engine.

The pipeline processes years separately to avoid unnecessarily holding the complete workbook in memory as a single unprocessed DataFrame.

### 8.2 Timestamp processing

Observation timestamps are normalized to UTC.

Local calendar features are then derived using the `Europe/Paris` timezone:

- Local date.
- Calendar year.
- Month.
- Hour.
- Day of the week.

This distinction is essential around daylight-saving transitions, when certain local hours may occur twice or not occur at all.

### 8.3 Managing definitive and provisional overlap

Definitive and provisional datasets may contain measurements covering the same region and time interval.

To prevent duplicate physical coverage, the preprocessing pipeline prioritizes definitive measurements when provisional data overlap with them.

Specifically, definitive observations take precedence within matching regional 30-minute time buckets.

This prevents provisional and definitive records from being counted simultaneously for the same interval.

## 9. Converting Power into Energy

One of the most important methodological decisions concerns measurement units.

### 9.1 Power versus energy

Power is measured in megawatts (MW).

Energy is measured in megawatt-hours (MWh).

They are related through time:

**Energy (MWh) = Power (MW) × Duration (hours)**

For a 30-minute record:

`Energy (MWh) = Power (MW) × 0.5`

For a 15-minute record:

`Energy (MWh) = Power (MW) × 0.25`

### 9.2 Why this transformation is necessary

Historical and provisional observations have different sampling intervals.

Simply summing MW values across records would incorrectly treat measurements from 15-minute and 30-minute periods as equivalent contributions of energy.

Applying interval duration allows temporal energy totals to be constructed consistently under the dataset's interval-average power interpretation.

### 9.3 Derived indicators

The normalized dataset includes derived measures such as:

- `consumption_mwh`
- `generation_mwh`
- `renewable_mwh`
- `generation_mw`
- `renewable_mw`
- `renewable_share_pct`
- `interval_hours`
- `missing_measurements`

The renewable category includes wind, solar, hydropower and bioenergy.

The renewable share is computed relative to recorded electricity generation, not regional household consumption.

## 10. Daily Aggregation and Analytical Storage

After normalization, the pipeline creates a region-day analytical dataset.

This reduces the number of records needed for frequently used visualizations such as:

- Historical trends.
- Regional rankings.
- Seasonal comparisons.
- Daily consumption and generation relationships.
- Narrative conclusions.

The prepared files include:

| Output | Description |
|---|---|
| `facts_2020.parquet` through `facts_2026.parquet` | Normalized annual observation files |
| `daily_summary.parquet` | Daily regional aggregates |
| `quality_summary.json` | Data preparation and quality metadata |

Parquet was chosen because it supports efficient columnar storage, compression and selective loading.

The original Excel and SQLite files are not overwritten during this process.

## 11. Data Validation and Quality Assurance

The project applies automated checks before prepared data are used.

Validation includes:

- Existence of expected annual output files.
- Uniqueness of the source-region-timestamp key.
- Valid observation durations of 0.25 or 0.5 hours.
- Absence of negative non-missing electricity consumption values.
- Recording of annual input and output row counts.
- Recording of missing consumption observations.
- Recording of temporal coverage and available regions.

The relevant verification components are:

`python -m scripts.validate_data`

`python -m unittest discover -s tests -v`

The dataset build also creates a SHA-256 fingerprint of the source workbook to identify whether the input has changed between preparation runs.

A validation success means that the implemented checks passed. It does not imply that every possible source-data error has been detected.

## 12. Reproducible Data Preparation

From the project root, the main commands are:

**Prepare the analytical dataset:**

`python -m scripts.prepare_data`

**Validate the output:**

`python -m scripts.validate_data`

**Run automated tests:**

`python -m unittest discover -s tests -v`

**Launch the application:**

`python -m streamlit run app.py --server.port 8502`

These commands use the existing Excel workbook and do not initiate new RTE API extraction.

The Python environment and required packages are documented in `requirements.txt`.

## 13. Performance and Streamlit Architecture

The application uses a modular structure.

`app.py` manages the dashboard's main execution flow, navigation, global selections and context shared with individual chapters.

The `sections/` directory contains the narrative and analytical pages.

The `utils/` directory contains reusable data-loading, preprocessing and visualization functions.

The `scripts/` directory handles offline analytical preparation and validation.

The `archive/data_engineering/` directory preserves the original acquisition, cleaning and database code for methodological documentation.

### 13.1 Caching

The data-loading layer uses Streamlit caching to reduce repeated file-reading operations.

### 13.2 Pre-aggregation

The daily summary avoids repeatedly processing all original observation records for visualizations that require only region-day information.

### 13.3 Visualization sampling

Large visualization datasets are reduced when necessary using deterministic sampling with `random_state=42`.

In the original implementation:

- Seasonal box plots may use up to 12,000 region-day records.
- Correlation scatterplots may display up to 3,500 region-day records, while the reported correlation uses all eligible records.
- Distribution histograms may display up to 25,000 observations, while the percentile threshold is calculated from the full eligible selection.

Sampling supports responsiveness but must be disclosed when interpreting the visual appearance of distributions.

## 14. Statistical Analysis

The dashboard implements descriptive and exploratory analysis.

### 14.1 Temporal aggregation

Reported demand energy is aggregated into daily, weekly or monthly intervals, depending on the selected analytical view.

### 14.2 Regional comparisons

Regions are compared using reported power demand and energy indicators.

Absolute demand is not adjusted for population, climate or economic activity.

### 14.3 Distribution analysis

Histograms and percentiles help identify the shape of measurement distributions and high-value observations.

The 99th percentile is used as a descriptive threshold for unusually high values within the selected dataset.

Observations above that threshold are not automatically classified as measurement errors.

### 14.4 Correlation analysis

Pearson's correlation coefficient is used to summarize the linear association between regional daily demand and generation.

The coefficient ranges from -1 to +1 when defined.

Positive and negative values describe direction, while values closer to zero indicate weaker linear association.

The method does not establish a causal relationship.

## 15. Updating the Dashboard Data

The current architecture does not automatically retrieve new measurements from RTE.

A GitHub Actions workflow has been prepared to rebuild analytical datasets when an updated Excel source is made available.

The proposed mechanism checks on a daily schedule and uses a three-day refresh condition.

Its source workbook may be supplied through a configured direct download URL or a GitHub Release asset.

**The workflow cannot create new electricity readings.** If the externally maintained Excel workbook is not updated, the dashboard's underlying observations remain unchanged.

This process should be described as a configured or proposed refresh mechanism until it has been tested successfully in the deployed repository.

## 16. Methodological Limitations

The principal limitations are:

1. The year 2026 is incomplete.
2. Historical and provisional records have different temporal resolutions.
3. Missing values reduce coverage and are not imputed.
4. Electricity demand is not normalized by population or weather.
5. Regional generation and regional consumption are distinct concepts.
6. Physical electricity exchanges complicate simple local supply-demand interpretations.
7. Correlation should not be interpreted as causation.
8. Deterministic chart sampling may affect the visual density of points or distributions.
9. The geographical map uses representative city locations.
10. The dashboard is descriptive and does not implement causal models or validated forecasts.

## 17. Conclusion

The methodology of France Energy Atlas demonstrates the connection between Data Engineering and Data Storytelling.

The original API extraction and SQLite database establish the historical data foundation. The Excel export preserves a consolidated analytical source. The preprocessing and validation stages produce consistent Parquet datasets, while Streamlit turns those prepared measurements into interactive narratives.

The central methodological achievement is therefore not merely the creation of an interface. It is the construction of a transparent workflow in which **data provenance, quality, measurement units, performance and interpretation are treated as connected responsibilities**.

---

**Related files:** `database_audit.md`, `data_dictionary.md`, `eda_report.md`, `storyboard.md`, `README.md`.