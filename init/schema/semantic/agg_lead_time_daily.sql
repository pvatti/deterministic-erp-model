CREATE TABLE IF NOT EXISTS agg_lead_time_daily AS
SELECT
    site_id,
    DATE(order_date) AS day,
    AVG(lead_time_days) AS avg_lead_time_daily
FROM sm_customer_orders
GROUP BY
    site_id,
    DATE(order_date);
