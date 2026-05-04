
with customers as (
    select
        customer_id,
        country,
        min(invoice_date)   as first_purchase_date,
        max(invoice_date)   as last_purchase_date,
        count(distinct invoice_no) as total_orders,
        sum(line_total)     as total_spent
    from {{ ref('stg_invoices') }}
    group by customer_id, country
)

select * from customers
