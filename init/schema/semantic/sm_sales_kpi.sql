DROP VIEW IF EXISTS sm_sales_kpi;

CREATE VIEW sm_sales_kpi AS
SELECT
    -- Time
    f.invoice_date,
    strftime('%Y', f.invoice_date) AS fiscal_year,
    strftime('%m', f.invoice_date) AS fiscal_month,

    -- Customer
    f.customer_id,
    c.customer_code,
    c.customer_name,

    -- Item
    f.item_id,
    i.item_sku,
    i.item_name,

    -- Site
    f.site_id,
    s.site_code,

    -- Core metrics
    f.sold_qty,
    f.net_revenue,
    f.discount,
    f.extended_price,

    -- KPIs
    CASE 
        WHEN f.sold_qty > 0 THEN f.net_revenue * 1.0 / f.sold_qty
        ELSE NULL
    END AS avg_selling_price,

    CASE 
        WHEN f.extended_price > 0 THEN f.discount * 1.0 / f.extended_price
        ELSE NULL
    END AS discount_rate,

    -- Contribution metrics
    f.net_revenue AS customer_contribution,
    f.net_revenue AS item_contribution,
    f.net_revenue AS site_contribution

FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_item i ON f.item_id = i.item_id
JOIN dim_sites s ON f.site_id = s.site_id;
