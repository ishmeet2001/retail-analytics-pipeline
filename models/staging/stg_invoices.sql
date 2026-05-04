with source as (
    select * from {{ source('retail_raw', 'raw_invoices') }}
),

staged as (
    select
        InvoiceNo                           as invoice_no,
        StockCode                           as stock_code,
        Description                         as description,
        cast(Quantity as INT64)             as quantity,
        cast(InvoiceDate as TIMESTAMP)      as invoice_date,
        cast(UnitPrice as FLOAT64)          as unit_price,
        CustomerID                          as customer_id,
        Country                             as country,
        cast(Quantity as FLOAT64) 
            * cast(UnitPrice as FLOAT64)    as line_total
    from source
    where Quantity > 0
      and UnitPrice > 0
)

select * from staged
