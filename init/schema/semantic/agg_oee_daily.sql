CREATE TABLE IF NOT EXISTS agg_oee_daily AS
SELECT
    site_id,
    machine_id,
    DATE(timestamp) AS day,
    AVG(availability) AS availability_daily,
    AVG(performance) AS performance_daily,
    AVG(quality) AS quality_daily,
    AVG(oee) AS oee_daily
FROM sm_oee_kpi
GROUP BY
    site_id,
    machine_id,
    DATE(timestamp);
