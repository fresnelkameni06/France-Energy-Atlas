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

