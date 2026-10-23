# Sources, Provenance and Licensing

**Data provider:** RTE / ODRÉ (Réseau de Transport d'Électricité).

**Official open-data catalogs:**
- https://www.data.gouv.fr/datasets
- https://odre.opendatasoft.com/

**Datasets:**
- `eco2mix-regional-cons-def` — historical consolidated / definitive regional electricity data.
- `eco2mix-regional-tr` — recent / provisional regional electricity data.

The original official API downloads were processed via Python, validated and stored in a local SQLite database before conversion into a seven-sheet Excel workbook. The present repository reads the Excel workbook as its **only input**, then generates Parquet analytical extracts. It contains neither a scraping job nor the large original SQLite database.

**Licensing:** Verify and record the specific dataset reuse licence on the official ODRÉ dataset pages prior to publishing the final submission, and reproduce any required attribution or licence text. Do not assume licence terms for a derivative workbook that are not documented in the dataset metadata.

**Personal data:** The source is regional electricity data, not personally identifying traveler/customer records.
