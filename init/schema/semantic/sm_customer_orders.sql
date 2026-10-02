DROP VIEW IF EXISTS sm_customer_orders;

CREATE VIEW sm_customer_orders AS
SELECT
    co.customer_id,
    c.customer_code,
    c.customer_name,
    co.site_id,
    s.site_code,
    co.item_id,
    i.item_sku,
    i.item_description,
    co.order_date,
    co.promise_date,
    co.shipped_date,
    co.ordered_qty,
    co.shipped_qty,
    co.open_qty,
    CASE 
        WHEN co.ordered_qty > 0 THEN co.shipped_qty * 1.0 / co.ordered_qty
        ELSE NULL
    END AS fill_rate,
    CASE 
        WHEN co.shipped_date IS NULL THEN NULL
        WHEN co.shipped_date <= co.promise_date THEN 1
        ELSE 0
    END AS on_time_flag
FROM fact_customer_orders co
JOIN dim_customer c ON co.customer_id = c.customer_id
JOIN dim_sites s ON co.site_id = s.site_id
JOIN dim_item i ON co.item_id = i.item_id;
