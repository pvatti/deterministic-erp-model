
INSERT INTO work_orders_raw (
    work_order_id, site_id, item_id, planned_quantity,
    scheduled_start, scheduled_end, status, created_by
)
VALUES (1, 1, 1, 100.0, "2026-01-02", "2026-01-03", "planned", "system");

INSERT INTO work_orders_raw (
    work_order_id, site_id, item_id, planned_quantity,
    scheduled_start, scheduled_end, status, created_by
)
VALUES (2, 2, 1, 200.0, "2026-01-02", "2026-01-04", "planned", "system");
