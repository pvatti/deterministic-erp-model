
INSERT INTO inventory_raw (
    inventory_id, site_id, item_id, quantity_on_hand,
    location_code, last_updated_at, last_updated_by, notes
)
VALUES (1, 1, 1, 150.0, "A1", "2026-01-01", "system", NULL);

INSERT INTO inventory_raw (
            inventory_id, site_id, item_id, quantity_on_hand,
            location_code, last_updated_at, last_updated_by, notes
)
VALUES (2, 1, 2, 500.0, "RM-01", "2026-01-01", "system", NULL);

INSERT INTO inventory_raw (
    inventory_id, site_id, item_id, quantity_on_hand,
    location_code, last_updated_at, last_updated_by, notes
)
VALUES (3, 2, 3, 75.0, "WIP-02", "2026-01-01", "system", NULL);

