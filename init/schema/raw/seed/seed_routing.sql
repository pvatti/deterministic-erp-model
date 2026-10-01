
INSERT INTO routing_raw (
    routing_id, item_id, site_id, step_number,
    operation_code, machine_id, standard_duration_minutes,
    updated_by, notes
    )
VALUES (1, 1, 1, 1, "CUT", 1, 15.0, "system", None);

INSERT INTO routing_raw (
routing_id, item_id, site_id, step_number,
operation_code, machine_id, standard_duration_minutes,
updated_by, notes
)
VALUES (2, 1, 1, 2, "PRESS", 2, 10.0, "system", None);

INSERT INTO routing_raw (
    routing_id, item_id, site_id, step_number,
    operation_code, machine_id, standard_duration_minutes,
    updated_by, notes
)
VALUES (3, 1, 2, 1, "ASSEMBLE", 3, 20.0, "system", None);
