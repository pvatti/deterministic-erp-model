DROP VIEW IF EXISTS sm_production_throughput;

CREATE VIEW sm_production_throughput AS
SELECT
    ft.timestamp,
    ft.site_id,
    s.site_code,
    ft.item_id,
    i.item_sku,
    i.item_description,
    ft.machine_id,
    m.machine_code,
    ft.operator_id,
    o.operator_code,
    ft.work_order_id,
    wo.wo_number,
    ft.units_produced,
    ft.scrap_units,
    (ft.units_produced + ft.scrap_units) AS total_units,
    CASE 
        WHEN (ft.units_produced + ft.scrap_units) = 0 THEN 0
        ELSE ft.scrap_units * 1.0 / (ft.units_produced + ft.scrap_units)
    END AS scrap_rate
FROM fact_production_throughput ft
JOIN dim_sites s ON ft.site_id = s.site_id
JOIN dim_item i ON ft.item_id = i.item_id
JOIN dim_machines m ON ft.machine_id = m.machine_id
JOIN dim_operators o ON ft.operator_id = o.operator_id
JOIN fact_work_order wo ON ft.work_order_id = wo.work_order_id;
