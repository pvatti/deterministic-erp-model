
INSERT INTO inventory_transactions_raw (
    txn_id, site_id, item_id, txn_type, quantity,
    timestamp, reference_id, notes
)
VALUES (1, 1, 1, "RECEIPT", 150.0, "2026-01-01T08:00:00", 1, None);

INSERT INTO inventory_transactions_raw (
    txn_id, site_id, item_id, txn_type, quantity,
    timestamp, reference_id, notes
)
VALUES (2, 1, 2, "RECEIPT", 500.0, "2026-01-01T09:00:00", 2, None);

INSERT INTO inventory_transactions_raw (
    txn_id, site_id, item_id, txn_type, quantity,
    timestamp, reference_id, notes
)
VALUES (3, 2, 3, "ISSUE", -25.0, "2026-01-01T10:00:00", 3, "WIP consumption");

