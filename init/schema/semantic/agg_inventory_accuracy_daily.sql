CREATE TABLE IF NOT EXISTS agg_inventory_accuracy_daily AS
SELECT
    site_id,
    item_id,
    DATE(snapshot_time) AS day,
    AVG(accuracy) AS inventory_accuracy_daily
FROM sm_inventory
GROUP BY
    site_id,
    item_id,
    DATE(snapshot_time);
