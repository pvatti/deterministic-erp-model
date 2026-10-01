INSERT INTO throughput_raw (
    throughput_id, site_id, work_order_id, machine_id,
    operator_id, units_produced, scrap_units,
    timestamp, shift_code, notes
)
VALUES
(1, 1, 1, 1, 1, 90.0, 5.0, "2026-01-02T14:00:00", "1st", NULL),
(2, 2, 2, 3, 3, 180.0, 10.0, "2026-01-03T15:00:00", "2nd", NULL);