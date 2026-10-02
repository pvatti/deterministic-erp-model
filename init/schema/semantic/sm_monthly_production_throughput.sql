DROP VIEW IF EXISTS sm_monthly_production_throughput;

CREATE VIEW sm_monthly_production_throughput AS
SELECT
    -- Time
    strftime('%Y', ft.timestamp) AS fiscal_year,
    strftime('%Y-%m', ft.timestamp) AS fiscal_month,

    -- Site
    ft.site_id,
    s.site_code,

    -- Machine
    ft.machine_id,
    m.machine_code,

    -- Operator
    ft.operator_id,
    o.operator_code,

    -- Item
    ft.item_id,
    i.item_sku,
    i.item_description,

    -- Aggregates
    SUM(ft.units_produced) AS monthly_units_produced,
    SUM(ft.scrap_units) AS monthly_scrap_units,
    SUM(ft.units_produced + ft.scrap_units) AS monthly_total_units,

    CASE
        WHEN SUM(ft.units_produced + ft.scrap_units) = 0 THEN 0
        ELSE SUM(ft.scrap_units) * 1.0 / SUM(ft.units_produced + ft.scrap_units)
    END AS monthly_scrap_rate

FROM fact_production_throughput ft
JOIN dim_sites s ON ft.site_id = s.site_id
JOIN dim_machines m ON ft.machine_id = m.machine_id
JOIN dim_operators o ON ft.operator_id = o.operator_id
JOIN dim_item i ON ft.item_id = i.item_id

GROUP BY
    fiscal_year,
    fiscal_month,
    ft.site_id,
    ft.machine_id,
    ft.operator_id,
    ft.item_id;
