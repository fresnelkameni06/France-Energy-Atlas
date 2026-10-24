ACADEMIC PROJECT REPORT
France Energy Atlas | 2020–2026
Exploring regional electricity consumption and generation through interactive data storytelling
1. Background, problem and objectives
Electricity is essential to daily life, industry and digital infrastructure, yet demand and generation vary by season, time of day, location and technology. National averages can conceal important regional differences. Open electricity measurements offer a valuable basis for investigation, provided that their temporal resolution, units and completeness are handled correctly.
Research question. How have electricity consumption and generation patterns evolved across metropolitan French regions from 2020 to 2026, and what geographical and temporal differences deserve closer investigation?
The project aims to construct a reproducible dataset, compare regional demand, examine the generation mix, detect recurring temporal patterns and high-value observations, and communicate defensible findings with clear data-quality warnings. The result is an explanatory, descriptive dashboard not a forecasting or causal model.
2. Data provenance and analytical scope
The underlying measurements come from RTE / ODRÉ regional éCO2mix open data: the historical/definitive dataset (eco2mix-regional-cons-def) and the provisional dataset (eco2mix-regional-tr). The project covers 12 metropolitan French regions. The 2026 series is incomplete, so full-year comparisons with earlier years require aligned observation windows.
Validated preparation snapshot	Result
Period	2020–2026 (2026 partial)
Prepared observations	1,463,328
Region-day aggregates	29,856
Missing consumption measurements	108
Reporting regions	12
Quality tests	3 unit tests passed; prepared-data validation passed
3. Data Engineering: from official API to dashboard
Historical processing followed: RTE/ODRÉ API → Python extraction and cleaning → SQLite consolidation → seven-sheet Excel export. Current dashboard preparation follows: existing Excel workbook → Pandas validation and transformation → yearly Parquet files and daily aggregates → Streamlit/Plotly.
Key controls include required region/timestamp identifiers, deduplication by source–region–UTC time, preference for definitive records in overlapping time intervals, treatment of invalid or missing values, and timezone conversion (UTC to Europe/Paris). Power is converted into energy using E (MWh) = P (MW) × interval duration (hours); 15- and 30-minute observations must not be summed as if they represented equal durations. Missing demand is kept missing, not replaced with zero.

DATA STORYTELLING & RESULTS
4. Narrative design: fourteen connected chapters
The interface follows Hook → Context → Analysis → Insights → Implications. Filters let readers change the region, period and applicable measures; conclusions are recalculated rather than fixed in advance. The sequence deliberately advances from broad context to targeted exploration and transparent interpretation.
Chapter	Purpose and contribution
01  Introduction	Defines the energy question, audience and RTE/ODRÉ provenance.
02  Overview	Time-series line chart of demand energy; identifies selected-period peaks.
03  Historical Evolution	Annual summary table; distinguishes complete from partial years.
04  Regional Ranking	Horizontal bars compare average reported regional demand.
05  Regional Map	Interactive markers locate regions and provide spatial context.
06  Generation Mix	Stacked area chart compares nuclear, wind, solar, hydro, thermal and bioenergy.
07  Hourly Patterns	Weekday × hour heatmap reveals recurring demand rhythms.
08  Seasonal Variability	Monthly box plots show medians, dispersion and outliers.
09  Correlations	Scatter plot and Pearson r explore demand–generation associations.
10  Distribution & Peaks	Histogram and 99th percentile contextualize high readings.
11  Data Quality & EDA	Displays coverage, missingness, duplicate checks and caveats.
12  Conclusions & Actions	Synthesizes selection-dependent findings and next questions.
13  Methodology	Documents extraction, transformations, assumptions and limitations.
14  Student & Credits	Attributes academic work and links to professional profiles.
5. Analytical interpretation and findings
The application combines eight principal chart types: line, bar, map, stacked area, heatmap, box plot, scatter plot and histogram. These complementary views highlight temporal evolution, regional variation, production composition, weekly and seasonal rhythms, linear associations and measurement distributions.
The verified project-level findings concern data readiness and coverage: 1.46 million prepared observations, 12 regions and a transparent incomplete-year warning. Regional leaders, peak dates, renewable shares and correlation coefficients depend on the user’s filters; they are intentionally calculated in the app rather than invented as universal results. Regional electricity generation is not necessarily consumed in the same region, and a statistical correlation does not imply causation.

QUALITY, DELIVERY & PERSPECTIVES
6. Data quality, validation and engineering
The preprocessing generated compressed Parquet files and a quality summary. Checks cover observation-key uniqueness, valid 0.25/0.5-hour durations, invalid negative demand, overlap handling and the 108 missing consumption measurements. Automated tests passed locally, and the GitHub Actions quality-check workflow was shown passing on the main branch. These checks establish engineering discipline without guaranteeing that every possible source-data issue has been detected.
The code is organized into app.py, sections/, utils/, scripts/, pipeline/, tests/, docs/ and assets/. The original API-to-SQLite/Excel scripts are preserved under archive/data_engineering/ as evidence of the full historical workflow. Streamlit caches prepared analytical files for responsive interaction.
7. Deployment and planned automation
The application has been deployed at https://france-energy-atlas-fk.streamlit.app/. GitHub Actions currently performs automated tests and dataset-integrity checks. A separate refresh workflow is planned: obtain an actually updated Excel source, rebuild Parquet, validate the files, publish the changes and allow the deployed Streamlit app to load the updated snapshot. Successful CI alone does not prove automatic ingestion of new RTE data; that complete refresh chain remains to be implemented and tested.
8. Limitations and implications
The study is descriptive. Comparisons are affected by incomplete 2026 coverage, occasional missing measurements, mixed source resolutions, regional population and economic differences, and absent weather adjustment. Map markers use representative cities, not exact measurement sites. Chart sampling may be used for performance, while key reported statistical measures use eligible data. The project can support further investigation but should not be used as a standalone grid-operation or energy-policy evaluation tool.
Future extensions could include population-normalized indicators, meteorological context, explicit exchange-flow analysis and a verified incremental data-refresh pipeline. The immediate academic value is a transparent example of connecting public-data engineering with interactive evidence-based storytelling.
9. Alignment with the course rubric
Assessment criterion	Evidence in this project
Data Storytelling (25)	Research question; 14-chapter narrative; dynamic implications
Data Cleaning & Analysis (25)	Official extraction, cleaning, SQLite, Excel, Parquet and validation
Visualization & UX (25)	Eight visual families, map, controls, KPI and explanatory context
Engineering Quality (15)	Modular code, caching, tests and successful CI workflow
Communication (10)	README, detailed docs, storyboard, this report and demo script

# France Energy Atlas — Data Storytelling Storyboard

**Project:** France Energy Atlas (2020–2026)  
**Institution:** EFREI Paris  
**Data Source:** RTE / ODRÉ  
**Dashboard:** https://france-energy-atlas-fk.streamlit.app/

## 1. Introduction and Research Question

Electricity consumption and generation vary across French regions and throughout the year. Understanding these differences is essential for exploring electricity demand, regional disparities and the evolution of generation technologies.

**Main research question:**

How have electricity consumption and generation patterns evolved across 12 metropolitan French regions between 2020 and 2026?

The dashboard transforms official electricity data into an interactive narrative structured around:

**Problem → Context → Analysis → Insights → Implications.**

## 2. Dashboard Storyboard — 14 Chapters

| Chapter | Objective and Storytelling Contribution |
|---|---|
| **01 — Introduction** | Introduces the energy context, project objectives, official data sources and central research question. |
| **02 — Overview** | Uses an interactive line chart and KPIs to visualize overall electricity demand trends and identify high-demand periods. |
| **03 — Historical Evolution** | Compares annual electricity indicators from 2020 to 2026, emphasizing fair comparisons and the incomplete coverage of 2026. |
| **04 — Regional Ranking** | Uses a horizontal bar chart to compare regions and identify differences in average electricity demand. |
| **05 — Regional Map** | Displays geographical markers to connect regional electricity indicators with their locations across metropolitan France. |
| **06 — Generation Mix** | Uses a stacked area chart to examine nuclear, wind, solar, hydro, thermal and bioenergy generation over time. |
| **07 — Hourly Patterns** | Uses a heatmap to reveal recurring demand patterns across weekdays and hours. |
| **08 — Seasonal Variability** | Uses monthly box plots to compare demand distributions, variability and seasonal differences. |
| **09 — Correlations** | Uses a scatter plot and Pearson correlation to explore relationships between regional electricity consumption and generation. |
| **10 — Distribution & Peaks** | Uses a histogram and the 99th percentile to examine measurement distributions and unusually high observations. |
| **11 — Data Quality & EDA** | Evaluates missing values, duplicates, coverage and measurement consistency to establish confidence in the analysis. |
| **12 — Conclusions & Actions** | Summarizes dynamic findings from the selected data and suggests further analytical investigations. |
| **13 — Methodology** | Explains the workflow: RTE API → Python cleaning → SQLite → Excel → Parquet → Streamlit. |
| **14 — Student & Credits** | Presents the student, EFREI Paris, academic supervisor, GitHub, LinkedIn and portfolio. |

## 3. Interactive Visualizations

The dashboard combines **eight visualization types**: line chart, bar chart, geographical map, stacked area chart, heatmap, box plot, scatter plot and histogram.

Interactive year, region and date selections allow users to investigate different subsets of the data. KPIs and analytical statements adapt to the selected observations.

Each visualization serves a specific purpose rather than simply displaying additional graphics.

## 4. Key Insights and Interpretation

The dashboard supports several important analytical perspectives:

- Electricity demand changes across time, regions and seasons.
- Regional rankings reveal differences in absolute demand, not necessarily energy efficiency.
- The electricity generation mix varies by source and observation period.
- Hourly and weekly patterns help identify recurring demand rhythms.
- Correlation and extreme-value analysis reveal statistical patterns that require careful interpretation.
- Data quality checks are essential for reliable conclusions.

The year **2026 is incomplete**, and correlations must not be interpreted as causal relationships.

## 5. Final Message and Implications

France Energy Atlas demonstrates how public electricity data can be transformed into meaningful insights through Data Engineering, exploratory analysis and interactive visualization.

Its main contribution is to connect historical trends, regional comparisons, generation technologies and data quality within a coherent analytical story.

Future improvements could include population-adjusted comparisons, weather data integration and automated updates from verified new RTE datasets.

**Final takeaway:** Effective data storytelling does not only show what the data contain; it explains what the evidence means, why it matters and where further investigation is needed.

