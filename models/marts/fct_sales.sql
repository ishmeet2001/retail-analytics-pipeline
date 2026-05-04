with sales as (
    select
        invoice_no,
        stock_code,
        customer_id,
        country,
        invoice_date,
        quantity,
        unit_price,
        line_total,
        date_trunc(invoice_date, MONTH)  as invoice_month
    from {{ ref('stg_invoices') }}
)

select * from sales
