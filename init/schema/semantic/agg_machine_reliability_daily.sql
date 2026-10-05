CREATE TABLE IF NOT EXISTS agg_machine_reliability_daily AS
SELECT
    site_id,
    machine_id,
    DATE(timestamp) AS day,
    AVG(mtbf) AS mtbf_daily,
    AVG(mttr) AS mttr_daily,
    AVG(reliability) AS reliability_daily
FROM sm_machine_reliability_kpi
GROUP BY
    site_id,
    machine_id,
    DATE(timestamp);
