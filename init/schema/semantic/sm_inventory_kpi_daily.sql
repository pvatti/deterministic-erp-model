DROP VIEW IF EXISTS sm_inventory_kpi_daily;

CREATE VIEW sm_inventory_kpi_daily AS
SELECT
    snapshot_date,
    site_id,
    SUM(on_hand_qty) AS total_on_hand_qty,
    SUM(on_hand_qty * standard_cost) AS total_inventory_value
FROM sm_inventory_kpi
GROUP BY snapshot_date, site_id;
