# Retail Analytics Pipeline

An end-to-end batch data warehouse built on GCP, processing 541K+ retail transactions into analytics-ready datasets for business reporting and KPI analysis.

## Architecture

```
OnlineRetail.csv (541K records)
        |
        v
  Python Ingestion Script
  (loads raw data into BigQuery)
        |
        v
  BigQuery - raw_invoices
        |
        v
     dbt ELT
  (staging + mart layers)
        |
        v
  Star Schema
  stg_invoices --> dim_customers
              --> dim_products
              --> fct_sales
        |
        v
  Soda Data Quality Checks
        |
        v
  Looker Studio Dashboard
  (revenue trends, top products, customer insights)
```

## Stack
- **Ingestion**: Python + BigQuery Python client
- **Warehouse**: Google BigQuery
- **Transformation**: dbt (star schema)
- **Data Quality**: Soda Core + dbt schema tests
- **Orchestration**: GitHub Actions (scheduled daily)
- **Dashboard**: Looker Studio

## Pipeline
1. Python script loads 541K raw records into BigQuery `raw_invoices`
2. Null CustomerIDs removed, InvoiceDate parsed to TIMESTAMP in staging (406K valid records after filtering)
3. dbt builds star schema: `stg_invoices` --> `dim_products`, `dim_customers`, `fct_sales`
4. Soda runs 7 data quality assertions across raw and staging layers
5. Looker Studio dashboard visualizes key business metrics

## dbt Models
- `stg_invoices` - cleaned, filtered staging layer (removes nulls, casts types, filters invalid rows)
- `dim_products` - product dimension with avg price and total units sold
- `dim_customers` - customer dimension with purchase history and total spend
- `fct_sales` - fact table with line-level sales data and monthly partitioning

## Soda Checks
- No missing CustomerIDs (raw + staging)
- Quantity within expected range
- Table not empty
- All staging quantities positive
- All staging prices positive

## Dashboard
![Looker Studio Dashboard](screenshots/dashboard.png)
