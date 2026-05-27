import os
from google.cloud import bigquery
from groq import Groq

# Authenticate depending on environment (Local vs GitHub Actions)
if not os.environ.get("GITHUB_ACTIONS"):
    # Local path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/ishmeet16/Downloads/cloudpersonal-756-bc45aa7935f5.json"
    groq_api_key = os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY")
else:
    # GitHub Actions environment variables
    groq_api_key = os.environ.get("GROQ_API_KEY")

bq_client = bigquery.Client(project="cloudpersonal-756")
groq_client = Groq(api_key=groq_api_key)

# Query BigQuery aggregates
query = """
SELECT
    DATE(invoice_date) as sale_date,
    ROUND(SUM(line_total), 2) as total_revenue,
    COUNT(DISTINCT invoice_no) as total_orders,
    APPROX_TOP_COUNT(country, 1)[OFFSET(0)].value as top_country,
    APPROX_TOP_COUNT(stock_code, 1)[OFFSET(0)].value as top_product
FROM retail_analytics.fct_sales
GROUP BY sale_date
ORDER BY sale_date DESC
LIMIT 1
"""

rows = list(bq_client.query(query).result())
row = rows[0]
print(f"Date: {row.sale_date}")
print(f"Revenue: ${row.total_revenue}")
print(f"Orders: {row.total_orders}")

# Step 2 — Send to Groq
prompt = f"""
You are a retail analytics assistant. Summarize these daily sales metrics 
in 2-3 sentences for an executive dashboard:

Date: {row.sale_date}
Total Revenue: ${row.total_revenue}
Total Orders: {row.total_orders}
Top Country: {row.top_country}
Top Product: {row.top_product}

Be concise, highlight any notable patterns, and suggest one action item.
"""

chat = groq_client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="llama-3.1-8b-instant",
)

summary = chat.choices[0].message.content
print(f"\nLLM Summary:\n{summary}")

# Step 3 — Write back to BigQuery
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("insight_date", "DATE", row.sale_date),
        bigquery.ScalarQueryParameter("total_revenue", "FLOAT64", float(row.total_revenue)),
        bigquery.ScalarQueryParameter("total_orders", "INT64", row.total_orders),
        bigquery.ScalarQueryParameter("top_country", "STRING", row.top_country),
        bigquery.ScalarQueryParameter("top_product", "STRING", row.top_product),
        bigquery.ScalarQueryParameter("llm_summary", "STRING", summary),
    ]
)

insert_query = """
INSERT INTO retail_raw.daily_insights
(insight_date, total_revenue, total_orders, top_country, top_product, llm_summary, created_at)
VALUES
(@insight_date, @total_revenue, @total_orders, @top_country, @top_product, @llm_summary, CURRENT_TIMESTAMP())
"""

bq_client.query(insert_query, job_config=job_config).result()
print("\nInsight written to BigQuery successfully")
