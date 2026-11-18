NZ Property Intelligence AI — Data Quality Report

Project: NZ Property Intelligence AI
Stage: Day 2 — Data Cleaning and Validation
Dataset: properties.csv

1. Dataset Overview

The dataset contains 10,000 New Zealand property listings across 11 property categories. It includes information about property location, bedrooms, bathrooms, land area, listing date descriptions and advertised pricing.

2. Data Quality Findings

Issue

Records

Percentage

Missing locations

3,980

39.80%

Missing land areas

2,551

25.51%

Missing bedrooms

549

5.49%

Missing bathrooms

540

5.40%

Possible duplicate rows

527

5.27%

Unusually high room counts

23

0.23%

The dataset contains 3,731 listings with extractable numerical advertised prices. Other listings use pricing methods such as auction, negotiation, tender or price on application.

3. Cleaning and Transformation

The cleaning pipeline standardised text fields, converted numerical columns, transformed land areas into square metres and extracted available advertised prices.

Missing values were preserved where appropriate rather than automatically replaced. Possible duplicates and unusually high room counts were flagged for further investigation.

All 10,000 original records were retained.

4. Validation

Seven automated tests were executed using pytest, covering record preservation, land-area conversion, missing-value handling, price extraction, pricing categories, outlier identification and duplicate detection.

Result: 7 tests passed, 0 failed.

5. Limitations

The dataset contains advertised prices and price guides rather than confirmed sale prices. Nearly 40% of records have missing locations, which limits geographical analysis.

The absence of unique property listing identifiers also makes it difficult to distinguish genuine duplicates from similar listings.

These limitations must be considered when developing dashboards and predictive models.