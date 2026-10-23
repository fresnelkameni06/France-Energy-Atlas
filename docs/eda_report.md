# EDA Report — Reproducible Analysis Plan

The results below are intentionally data-driven rather than pre-filled. The dashboard computes the statistics from the validated Excel data.

## Questions examined
- Which regions have the highest average consumption in MW?
- Which dates have the largest cumulative reported energy in MWh?
- How does source mix change between comparable months of different years?
- Are the peaks consistent across weekdays/hours and seasons?
- Which numerical measurements display Pearson correlation, and are those associations stable across regions?
- What is the rate of null readings, invalid values, duplicate keys and overlap between provisional and definitive data?

## Reproducibility
Run `python -m scripts.prepare_data` and `python -m scripts.validate_data`. Analytical outputs appear in `data/processed`. Source data remain unchanged. No external RTE requests are made.

## Methodological warnings
2026 is partial, region sizes differ, weather and population are not controlled for, missing values are not imputed, and correlation does not prove causality. Prepared data are appropriate for descriptive exploration, not causal or policy-impact claims.
