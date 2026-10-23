# France Energy Atlas (2020–2026)
## Project Brief — Introduction, Context and Research Objectives

**Project:** Individual Student Project — Data Storytelling Dashboard with Streamlit  
**Institution:** EFREI Paris  
**Course:** Data Visualization / Data Storytelling  
**Project supervisor:** Prof. Mano Joseph Mathew  
**Data provider:** RTE / ODRÉ — French Regional Electricity Data  
**Technologies:** Python, Pandas, SQLite, Microsoft Excel, Parquet, Plotly, Streamlit  
**Study period:** 2020–2026 (2026 is a partial year)

---

## 1. Introduction

Electricity is a fundamental component of modern society. It powers residential buildings, industries, transport infrastructure, public services, healthcare systems, communication networks and an increasing number of digital technologies.

However, electricity consumption and electricity generation do not follow identical patterns everywhere. Demand changes throughout the day, from one season to another and from one geographical area to another. Similarly, electricity production depends on the location and operation of different generation technologies, including nuclear power, hydropower, wind, solar, thermal generation and bioenergy.

France provides an especially interesting environment for studying these differences. Its electricity system combines several generation technologies, while its regions differ substantially in their economic activities, population concentrations, climate conditions, industrial infrastructure and electricity-producing facilities.

A national electricity indicator can describe the overall situation but often hides important territorial variations. Two regions may experience different demand patterns even during the same period. A region with substantial electricity generation may also have a consumption profile very different from another region.

Understanding these differences requires more than displaying isolated figures. Electricity data must be collected, prepared, compared and interpreted within a coherent analytical framework.

This observation motivated the development of **France Energy Atlas**, an interactive data-storytelling application designed to investigate the evolution of electricity consumption and generation across 12 metropolitan French regions between 2020 and 2026.

Rather than presenting a collection of unrelated charts, the application guides readers through a progressive analytical investigation: understanding the problem, examining historical changes, identifying territorial differences, studying temporal patterns, evaluating data quality and formulating evidence-based conclusions.

The ultimate objective is to transform complex electricity measurements into accessible, interactive and interpretable information.

## 2. Project Motivation

The motivation behind this project is based on three complementary challenges.

### 2.1 The complexity of electricity data

Electricity datasets contain numerous variables, timestamps, regional identifiers and production measurements.

Raw records can be difficult to interpret because they may use different temporal resolutions, contain missing values and represent different physical concepts.

For example, a measurement expressed in megawatts (MW) describes power, whereas a value expressed in megawatt-hours (MWh) represents energy over a defined time interval.

Confusing these quantities can lead to misleading comparisons. Consequently, meaningful electricity analysis requires careful preprocessing and documented analytical choices.

### 2.2 The importance of regional comparisons

National summaries do not always reveal regional patterns.

A ranking of regional electricity demand can identify territories with higher reported demand, but such a ranking must be interpreted carefully. A region with higher absolute demand is not necessarily less energy-efficient; it may simply have a larger population or a more energy-intensive economic structure.

Regional comparisons are therefore useful as a starting point for investigation, rather than as direct measures of performance.

### 2.3 The need for accessible data storytelling

Open data can support research and decision-making, but its value depends on the ability to communicate results clearly.

A dashboard should not require users to understand the underlying database structure or execute Python code.

France Energy Atlas addresses this challenge by providing interactive controls, understandable visualizations, contextual explanations and explicit methodological limitations.

## 3. Problem Statement

Although official regional electricity datasets are publicly available, interpreting several years of regional power measurements remains challenging.

Three difficulties are particularly important:

1. **Temporal complexity:** electricity demand changes at several time scales, from hourly fluctuations to annual trends.
2. **Geographical heterogeneity:** regions differ in electricity demand and generation characteristics.
3. **Data reliability:** historical and provisional measurements may have different temporal resolutions, completeness levels and revision statuses.

A useful analytical application must address these challenges together instead of treating them independently.

### Central research question

**How have electricity consumption and generation patterns evolved across metropolitan French regions between 2020 and 2026, and which temporal and geographical differences should be investigated more closely?**

This question is descriptive and exploratory. The project does not claim to establish causal relationships between regional characteristics and electricity outcomes.

## 4. Research Objectives

### 4.1 General objective

To design and develop a reproducible, interactive Streamlit application that transforms official regional electricity data into a coherent and accessible data story.

### 4.2 Specific objectives

The project aims to:

1. Collect and preserve official historical and provisional electricity measurements from RTE / ODRÉ.
2. Develop a documented data-engineering workflow for extracting, cleaning, validating and storing records.
3. Build a structured analytical dataset covering the period 2020–2026.
4. Analyze changes in reported electricity demand over time.
5. Compare demand levels across the 12 reporting regions.
6. Explore the geographical distribution of regional electricity indicators.
7. Study the evolution of recorded electricity generation by source.
8. Identify recurring hourly, weekly and seasonal demand patterns.
9. Explore statistical associations between electricity consumption and generation.
10. Identify unusually high observations without automatically classifying them as errors.
11. Evaluate missing data, duplicate records, temporal coverage and other quality issues.
12. Communicate findings through interactive visualizations and an evidence-based narrative.
13. Document the application's assumptions, limitations and reproducibility procedures.

## 5. Supporting Research Questions

The central question is divided into several analytical questions.

**Historical evolution:** How does reported electricity demand vary between 2020 and 2026? Which comparisons remain valid when the latest year is incomplete?

**Regional disparities:** Which regions report the highest average electricity demand? How large are the differences across selected regions and periods?

**Geographical interpretation:** Where are the selected regions located, and how can their electricity indicators be compared spatially?

**Electricity generation:** What are the respective contributions of nuclear, wind, solar, hydropower, thermal generation and bioenergy?

**Daily and weekly patterns:** At what hours and on which weekdays does reported electricity demand tend to be highest?

**Seasonality:** How does the distribution of daily demand differ between months?

**Statistical relationships:** How are recorded electricity consumption and generation associated across regional daily observations?

**Extreme values:** What does the distribution of measurements reveal about unusually high electricity demand?

**Data quality:** How complete and reliable are the observations used to produce these results?

## 6. Target Audience

The application is intended for several audiences.

**Students and researchers:** To practice exploratory data analysis, statistical interpretation, data engineering and interactive visualization using authentic public data.

**Energy analysts:** To explore regional demand patterns, generation categories and temporal differences.

**Public decision-makers:** To identify descriptive patterns that may motivate further investigation, without treating the dashboard as a forecasting or policy-evaluation system.

**Citizens and non-specialist users:** To better understand how electricity demand and generation vary across France through accessible visual explanations.

The interface is designed to remain understandable without advanced knowledge of databases or programming.

## 7. Dataset and Study Scope

The project uses public regional electricity measurements published by RTE through the ODRÉ open-data ecosystem.

Two source categories were involved in the historical data-engineering process:

- **Definitive or historical regional measurements:** `eco2mix-regional-cons-def`, generally recorded at 30-minute intervals.
- **Provisional regional measurements:** `eco2mix-regional-tr`, recorded at 15-minute intervals in the recent portion of the dataset.

The prepared project dataset covers 12 metropolitan French regions and the calendar years 2020 through 2026.

### Dataset preparation snapshot

The successful preprocessing run reported:

| Characteristic | Result |
|---|---|
| Study period | 2020–2026 |
| Reporting regions | 12 |
| Prepared observations | 1,463,328 |
| Aggregated region-day records | 29,856 |
| Annual Excel worksheets | 7 |
| Missing consumption measurements | 108 |
| Main original storage | SQLite |
| Source transferred to the current application | Excel workbook |
| Optimized application storage | Parquet |
| Dashboard framework | Streamlit |

These figures describe the validated project snapshot, not a continuously updated live feed.

### Geographical scope

The analysis concerns the metropolitan regions represented in the dataset. It does not claim complete coverage of every French territory or overseas region.

### Temporal scope

The historical comparison includes full past years and an incomplete 2026 period.

Consequently, total demand for 2026 should not be compared directly with complete annual totals from earlier years without aligning the observed calendar periods.

## 8. Project Approach

The project combines two related but separate workflows.

### 8.1 Original Data Engineering Workflow

The initial data collection and storage process followed this sequence:

**Official RTE / ODRÉ API → Automated extraction → Data cleaning → Validation → SQLite database → Excel export**

This workflow preserved the origin of the observations and provided a structured foundation for later analysis.

The collection method used official data APIs rather than extracting information from website HTML pages.

### 8.2 Current Analytical and Visualization Workflow

The current Streamlit application follows a second workflow:

**Existing Excel workbook → Python preprocessing → Validation → Parquet analytical files → Streamlit Dashboard**

This separation improves clarity and reproducibility.

The interactive application does not need to contact the RTE API or query the original SQLite database every time a user changes a filter.

## 9. The Data Storytelling Approach

The project follows a narrative structure inspired by the course requirements:

**Hook → Context → Analysis → Key Insights → Implications**

The application is organized into 14 chapters.

The first chapters introduce the main problem and provide a general overview. Subsequent chapters progressively examine historical trends, regional rankings, geographical differences, generation technologies, temporal patterns, correlations and distributions.

A dedicated chapter examines data quality and methodological uncertainty.

The final analytical chapters synthesize the evidence, explain how the data were processed and document the project's academic authorship.

This structure allows users to move beyond simply observing charts toward understanding why each visualization matters.

The detailed explanation of all 14 chapters is provided in `docs/storyboard.md`.

## 10. Expected Contribution

France Energy Atlas contributes in three main ways.

**Technical contribution:** It demonstrates an end-to-end data workflow involving official API data, data cleaning, relational storage, Excel export, analytical transformation and deployment-oriented Streamlit development.

**Analytical contribution:** It enables interactive exploration of regional and temporal electricity measurements across multiple years.

**Communication contribution:** It organizes eight interactive visualization types within a 14-chapter narrative, while explaining findings and methodological limitations.

The application is intended as a descriptive decision-support and educational tool, not as an operational electricity-grid management platform.

## 11. Limitations and Responsible Interpretation

Several important limitations must be acknowledged:

- The 2026 dataset is incomplete.
- Regional demand totals depend on selected periods and available records.
- Regions differ in population, economic activity and geographical size.
- Population-adjusted and weather-adjusted indicators are not included.
- The geographic visualization uses representative city coordinates rather than precise observation sites or region centroids.
- Historical and provisional measurements have different time resolutions.
- Missing values are preserved rather than replaced with fabricated measurements.
- Correlation is not evidence of causation.
- Regional electricity production is not necessarily consumed in the same region.
- The application is based on a prepared data snapshot; it does not provide a continuously refreshed real-time electricity feed.

These limitations are not secondary details. They are necessary for interpreting the charts correctly.

## 12. Conclusion

France Energy Atlas demonstrates how official open data can be transformed into a structured and meaningful analytical narrative.

Its value does not lie only in the number of observations, charts or filters. It lies in connecting reliable data preparation, appropriate statistical exploration, interactive visualization and transparent interpretation.

By combining regional comparisons, historical analysis, generation-source exploration, temporal patterns, statistical associations and data-quality checks, the project provides a coherent framework for understanding recorded electricity activity in metropolitan France.

**The guiding principle of the project is simple: visualizations should not merely display data; they should help users ask better questions, interpret evidence and recognize the limits of what the data can establish.**

---

**Primary data provider:** RTE / ODRÉ  
**Official open-data portal:** https://odre.opendatasoft.com/  
**French public data catalogue:** https://www.data.gouv.fr/  
**Related documentation:** `methodology.md`, `eda_report.md`, `database_audit.md`, `storyboard.md`.