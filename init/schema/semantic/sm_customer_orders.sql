CREATE VIEW sm_customer_orders AS
SELECT
    co.order_date,
    co.promise_date,
    co.shipped_date,
    dc.customer_code,
    dc.customer_name,
    ds.site_code,
    di.item_code,
    co.ordered_qty,
    co.shipped_qty,
    co.open_qty,
    -- Business metric
    CASE 
        WHEN co.ordered_qty = 0 THEN 0
        ELSE co.shipped_qty * 1.0 / co.ordered_qty
    END AS fill_rate,
    CASE 
        WHEN co.shipped_date IS NULL THEN NULL
        WHEN co.shipped_date <= co.promise_date THEN 1
        ELSE 0
    END AS on_time_flag
FROM gold_customer_order_lines co
LEFT JOIN gold_customers dc ON co.customer_key = dc.customer_key
LEFT JOIN gold_sites ds ON co.site_key = ds.site_key
LEFT JOIN gold_items di ON co.item_key = di.item_key;
