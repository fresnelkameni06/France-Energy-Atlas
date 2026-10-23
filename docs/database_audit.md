# Database Audit and Data Quality Report
## France Energy Atlas (2020–2026)

## 1. Audit Objective

The objective of this audit is to document the reliability, consistency and traceability of the electricity dataset used by France Energy Atlas.

A data-storytelling dashboard must not rely solely on the visual appearance of charts. It must also demonstrate that the underlying measurements were processed with appropriate quality controls.

This report covers:

- Data provenance.
- Observation counts.
- Temporal and geographical coverage.
- Missing values.
- Duplicate records.
- Measurement validity.
- Temporal resolution.
- Definitive/provisional source overlap.
- Validation procedures.
- Residual limitations.

The audit distinguishes the original SQLite storage process from the validation of the final analytical datasets.

---

## 2. Data Lineage

The historical data-engineering workflow followed the sequence:

**RTE / ODRÉ API → Python cleaning → SQLite → Excel**

The current analytical workflow follows:

**Excel → Pandas preprocessing → Parquet → Streamlit**

The original SQLite database remains available locally in:

`data/energy.db`

The consolidated Excel workbook is:

`data/france_energy_2020_2026.xlsx`

The prepared analytical data are stored in:

`data/processed/`

The application does not require a live SQLite connection.

## 3. Audit Scope

The audit concerns the successfully prepared project snapshot.

The study includes 12 metropolitan French regions and seven represented calendar years, from 2020 through 2026.

The 2026 period is incomplete.

### Summary of validated preprocessing output

| Audit indicator | Reported result |
|---|---:|
| Total prepared observation records | 1,463,328 |
| Regional entities | 12 |
| Years represented | 7 |
| Annual analytical files | 7 |
| Daily region-level records | 29,856 |
| Missing demand measurements | 108 |
| Automated preprocessing tests | 3 passed |
| Prepared-data integrity validation | Passed |

These results were reported by the preprocessing and validation commands.

They should not be misrepresented as an independent, comprehensive audit of every possible issue in the original SQLite database.

## 4. Annual Observation Counts

The preparation process produced the following counts:

| Year | Prepared rows | Missing consumption |
|---|---:|---:|
| 2020 | 210,792 | 0 |
| 2021 | 210,216 | 0 |
| 2022 | 210,216 | 0 |
| 2023 | 210,216 | 0 |
| 2024 | 210,792 | 0 |
| 2025 | 210,216 | 12 |
| 2026 | 200,880 | 96 |
| **Total** | **1,463,328** | **108** |

The differences between annual counts must be interpreted in light of calendar duration, reporting coverage and the mixture of historical and provisional datasets.

In particular, the incomplete 2026 period cannot be interpreted as equivalent to a full calendar year.

## 5. Structural Validation

The preprocessing pipeline verifies the presence of mandatory identifying variables.

The required fields include:

- Source identifier.
- Region code.
- Region name.
- Observation timestamp.

Records lacking valid mandatory identifiers are unsuitable for reliable regional or temporal attribution.

The pipeline normalizes field names and data types before performing analytical calculations.

## 6. Duplicate Record Control

### 6.1 Duplicate definition

An observation is identified using the following key:

`source + region_code + observation_utc`

Two records sharing this combination are considered duplicates under the implemented source-level uniqueness definition.

### 6.2 Cleaning procedure

Duplicate records are removed during normalization.

When historical and provisional datasets overlap, a separate rule prioritizes definitive measurements for the affected region and half-hour interval.

This distinction is important:

- Duplicate elimination operates on repeated observation keys.
- Source-overlap resolution operates on different source records representing overlapping physical time coverage.

### 6.3 Validation result

The prepared-data validation passed its duplicate-key checks.

This indicates that the checked annual Parquet datasets did not contain duplicate observation keys after preprocessing.

It does not establish that the original API extracts contained no duplicates before cleaning.

## 7. Missing-Value Assessment

### 7.1 Missing consumption measurements

The prepared snapshot contained 108 missing consumption measurements.

Of these:

- 12 occurred in the 2025 worksheet.
- 96 occurred in the 2026 worksheet.

No missing consumption measurements were reported for the prepared 2020–2024 worksheets.

### 7.2 Interpretation

The missing-value count indicates that some consumption measurements could not be used as valid numeric demand readings.

However, it does not by itself measure gaps where no observation record exists at all.

Missing values within recorded rows and entirely absent time intervals are different quality problems and should be assessed separately.

### 7.3 Treatment

Missing quantitative values are preserved as missing.

They are not replaced with zero or artificially estimated.

This prevents unobserved electricity measurements from being interpreted as genuine zero consumption or zero generation.

### 7.4 Other variables

The missingness of nuclear, solar, wind, hydro, thermal, bioenergy and exchange fields should be assessed separately.

The dashboard's Data Quality chapter computes indicator-specific missing percentages for the selected data.

The 108 missing consumption records must not be presented as the total missing-value count across every field.

## 8. Measurement Validity

The preprocessing rules ensure that numeric measurements are converted consistently.

Invalid non-numeric or non-finite values are treated as missing.

Negative consumption and negative generation values are not retained as valid numerical measurements under the implemented cleaning rules.

Negative physical electricity exchange values are preserved, because they may represent legitimate exchange directions under the source convention.

The prepared-data validator checks that usable consumption measurements are not negative.

## 9. Temporal Resolution Audit

The dataset combines observations with different durations.

| Observation type | Interval duration |
|---|---:|
| Historical/definitive | 0.5 hours |
| Recent/provisional | 0.25 hours |

The validation process checks that the prepared observation duration belongs to the accepted interval set.

### Why this matters

The duration of each record affects energy aggregation.

A power measurement of 1,000 MW sustained over 30 minutes represents 500 MWh under the interval-average power interpretation.

The same power level over 15 minutes represents 250 MWh.

Therefore, raw MW values must not be indiscriminately summed to estimate energy across time.

The preparation pipeline creates interval-adjusted MWh variables to support meaningful temporal aggregation.

## 10. Timezone and Calendar Consistency

Observation timestamps are normalized to UTC.

Local analytical variables are derived using the `Europe/Paris` timezone.

These variables include local date, month, weekday and hour.

Timezone handling matters because daylight-saving changes can introduce repeated or absent local clock hours.

It also matters near calendar-year boundaries, where an observation's UTC date and local date may differ.

The preprocessing pipeline accounts for the distinction between UTC observation times and local analytical dates.

## 11. Geographical Integrity

The dataset identifies observations using regional labels and region codes.

The preparation summary reported 12 unique reporting regions.

Regional identifiers are validated before observations are included in analytical output.

However, the audit does not claim full coverage of every French territory.

The geographical visualization is also based on representative regional city coordinates rather than actual measurement-site locations.

## 12. Automated Testing

The preprocessing test suite includes checks for:

**Daily energy aggregation:** verifying that numerical power observations are appropriately transformed into energy and aggregated.

**Duplicate handling and source precedence:** verifying that duplicated or overlapping source records are treated according to the implemented rules.

**Negative demand handling:** verifying that invalid negative demand values remain missing rather than being silently accepted as valid consumption.

The reported test execution completed successfully:

**3 tests passed.**

### Validation command

`python -m unittest discover -s tests -v`

### Prepared-data verification

`python -m scripts.validate_data`

The separate prepared-data validation also passed its implemented integrity checks.

## 13. Data Provenance and Integrity Tracking

The preparation process calculates a SHA-256 hash of the source Excel workbook.

This fingerprint allows the pipeline to identify whether the input workbook has changed between preparation runs.

The quality metadata also record information such as:

- Workbook name.
- Annual preparation results.
- Prepared observation counts.
- Available years.
- Source-date coverage.
- Region count.
- Preparation timestamp.
- Dataset source counts.

These metadata are saved in:

`data/processed/quality_summary.json`

This file provides a reproducible reference for the prepared analytical snapshot.

## 14. Quality Controls in the Dashboard

The Streamlit application's Data Quality & EDA chapter provides a user-facing summary of quality information.

It displays:

- The number of observations in the selected data.
- The number of reporting regions.
- The number of duplicate observation keys found in the selected prepared records.
- Missing-value percentages by numerical indicator.
- Preparation reports associated with the Excel worksheets.
- Warnings concerning incomplete periods and temporal resolutions.

The purpose is to make data reliability part of the analytical narrative rather than hide it in technical documentation.

## 15. Residual Risks and Limitations

The successful execution of the quality checks does not eliminate all uncertainty.

### Incomplete year

The 2026 data do not represent a complete calendar year.

### Missing temporal intervals

Checking null values within rows does not necessarily establish that every expected timestamp is present.

### Provisional revisions

More recent source values may be revised in later definitive releases.

### Regional comparability

Regions differ in size, economic activity and electricity-use characteristics.

### Aggregation bias

Observed totals depend on source completeness and selected reporting periods.

### Unmeasured variables

Weather, population, detailed economic activity and electricity prices are not controlled for in the current analysis.

### Static data snapshot

The dashboard is not a continuous live electricity-monitoring system.

Its contents remain based on the prepared data snapshot until updated source data are supplied and the analytical files are rebuilt.

## 16. Audit Conclusion

The documented preprocessing run successfully prepared 1,463,328 electricity observations covering 12 metropolitan regions and the years 2020–2026.

Automated tests and integrity validation passed.

The pipeline explicitly addresses duplicate observation keys, invalid measurement values, source overlap, timezone normalization and the conversion of power into interval-adjusted energy.

Missing consumption values were identified and preserved rather than artificially filled.

These checks provide a credible technical foundation for descriptive electricity analysis.

However, the audit does not establish that the original source is complete in every possible respect or that descriptive statistical patterns have causal explanations.

**Overall conclusion:** the prepared dataset passed the implemented validation controls and is suitable for the dashboard's intended descriptive analyses, provided that missingness, incomplete-year coverage and other documented limitations remain visible to users.

---

**Audit artifacts:** `quality_summary.json`, annual Parquet files, original Excel workbook, local SQLite database.  
**Verification scripts:** `scripts/prepare_data.py`, `scripts/validate_data.py`, `tests/test_preprocessing.py`.  
**Related documents:** `methodology.md`, `eda_report.md`, `data_dictionary.md`.