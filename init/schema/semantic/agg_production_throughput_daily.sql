CREATE TABLE IF NOT EXISTS agg_production_throughput_daily AS
SELECT
    site_id,
    item_id,
    DATE(timestamp) AS day,
    SUM(good_units) AS good_units_daily,
    SUM(scrap_units) AS scrap_units_daily,
    SUM(good_units) AS total_good_units_daily,
    SUM(scrap_units) AS total_scrap_units_daily,
    SUM(good_units) * 1.0 / COUNT(DISTINCT DATE(timestamp)) AS avg_throughput_daily
FROM sm_production_throughput
GROUP BY
    site_id,
    item_id,
    DATE(timestamp);
