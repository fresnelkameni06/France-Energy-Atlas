# Data Dictionary

| Field | Meaning | Unit / notes |
|---|---|---|
| source | Official RTE Eco2mix dataset | Historical / provisional identifier |
| region_code | INSEE region code | Text |
| region | French region label | Text |
| observation_utc | Measurement timestamp | UTC datetime |
| retrieved_utc | Original API collection timestamp | UTC datetime |
| consumption_mw | Reported electricity demand | MW (power) |
| nuclear_mw | Nuclear generation | MW |
| wind_mw | Wind generation | MW |
| solar_mw | Solar generation | MW |
| hydro_mw | Hydroelectric generation | MW |
| thermal_mw | Thermal generation | MW |
| bioenergy_mw | Bioenergy generation | MW |
| exchange_mw | Net physical interregional exchanges | MW, may be negative |
| quality_flag | Quality status created during original ingestion | Category |
| interval_hours | Duration of one record | 0.5 historical, 0.25 provisional |
| *_mwh | Observed power integrated over its time interval | MWh = MW × hours |
| generation_mw | Sum of available generation source indicators | MW; reported only with all components present |
| renewable_mw | Wind + Solar + Hydro + Bioenergy | MW; missing if component missing |
| renewable_share_pct | Renewable generation / total generation | %, not household consumption mix |
| year / month / hour / weekday | Local temporal features | Europe/Paris |
| missing_measurements | Count of missing quantitative measures | Integer |

**Critical rule:** Do not sum MW to calculate energy over time; use interval-aware MWh. Do not interpret missing data as zero.
