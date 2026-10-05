CREATE TABLE IF NOT EXISTS semantic_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    duration_ms INTEGER NOT NULL,
    status TEXT NOT NULL,
    rows_returned INTEGER,
    validation_passed INTEGER,
    validation_failures INTEGER,
    error_message TEXT
);
