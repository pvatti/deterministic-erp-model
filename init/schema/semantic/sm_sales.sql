DROP VIEW IF EXISTS sm_sales;

CREATE VIEW sm_sales AS
SELECT
    f.invoice_date,
    f.customer_id,
    c.customer_code,
    c.customer_name,
    f.item_id,
    i.item_sku,
    i.item_name,
    f.sold_qty,
    f.net_revenue,
    f.net_revenue / NULLIF(f.sold_qty, 0) AS avg_price
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
JOIN dim_item i
    ON f.item_id = i.item_id;
