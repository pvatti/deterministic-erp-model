DROP VIEW IF EXISTS sm_production_throughput;

CREATE VIEW sm_production_throughput AS
SELECT
    ft.timestamp,
    ds.site_code,
    ds.site_name,
    di.item_code,
    di.item_description,
    dm.machine_code,
    do.operator_code,
    wo.work_order_number,
    -- Measures
    ft.units_produced,
    ft.scrap_units,
    -- Business metrics
    (ft.units_produced + ft.scrap_units) AS total_units,
    CASE 
        WHEN (ft.units_produced + ft.scrap_units) = 0 THEN 0
        ELSE ft.scrap_units * 1.0 / (ft.units_produced + ft.scrap_units)
    END AS scrap_rate
FROM gold_throughput ft
LEFT JOIN gold_sites ds ON ft.site_key = ds.site_key
LEFT JOIN gold_items di ON ft.item_key = di.item_key
LEFT JOIN gold_machines dm ON ft.machine_key = dm.machine_key
LEFT JOIN gold_operators do ON ft.operator_key = do.operator_key
LEFT JOIN gold_work_orders wo ON ft.work_order_key = wo.work_order_key;
