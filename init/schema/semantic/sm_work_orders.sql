DROP VIEW IF EXISTS sm_work_orders;

CREATE VIEW sm_work_orders AS
SELECT
    f.work_order_id,
    f.wo_number,
    f.site_id,
    s.site_code,
    f.item_id,
    i.item_sku,
    i.item_name,
    f.planned_qty,
    f.completed_qty,
    f.scrap_qty,
    f.duration_hours,
    f.total_cost,
    CASE
        WHEN f.planned_qty > 0 THEN f.completed_qty / f.planned_qty
        ELSE NULL
    END AS completion_ratio,
    CASE
        WHEN f.completed_qty > 0 THEN f.total_cost / f.completed_qty
        ELSE NULL
    END AS cost_per_unit
FROM fact_work_order f
JOIN dim_sites s
    ON f.site_id = s.site_id
JOIN dim_item i
    ON f.item_id = i.item_id;
