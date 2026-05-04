
with products as (
    select
        stock_code,
        description,
        avg(unit_price)     as avg_price,
        sum(quantity)       as total_units_sold
    from {{ ref('stg_invoices') }}
    group by stock_code, description
)

select * from products
