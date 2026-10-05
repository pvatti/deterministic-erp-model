CREATE TABLE IF NOT EXISTS agg_fill_rate_daily AS
SELECT
    site_id,
    DATE(order_date) AS day,
    AVG(fill_rate) AS avg_fill_rate_daily
FROM sm_customer_orders
GROUP BY
    site_id,
    DATE(order_date);
