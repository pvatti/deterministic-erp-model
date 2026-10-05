import os
import sqlite3
import time
import json

from validate_semantic import run_validation_rules
from log_semantic import log_semantic_event

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEMANTIC_DIR = os.path.join(PROJECT_ROOT, "semantic")
ORDER_FILE = os.path.join(PROJECT_ROOT, "semantic_order.json")
DEFAULT_DB = os.path.join(PROJECT_ROOT, "gold.db")


def load_semantic_order():
    with open(ORDER_FILE, "r") as f:
        return json.load(f)["semantic_order"]


def apply_semantic_models(db_path=DEFAULT_DB):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    semantic_order = load_semantic_order()

    # Run validation BEFORE building semantic models
    failures = run_validation_rules(db_path, os.path.join(PROJECT_ROOT, "semantic_validation.yaml"))
    if failures:
        raise Exception("Semantic validation failed. See console output.")

    for model_file in semantic_order:
        model_path = os.path.join(SEMANTIC_DIR, model_file)

        with open(model_path, "r") as f:
            sql_text = f.read()

        start = time.time()
        status = "success"
        error = None

        try:
            cur.executescript(sql_text)
            conn.commit()
        except Exception as e:
            status = "failure"
            error = str(e)

        end = time.time()

        # Log the semantic execution event
        log_semantic_event(
            model_name=model_file.replace(".sql", ""),
            start_time=start,
            end_time=end,
            status=status,
            rows_returned=None,          # SQLite cannot reliably return rowcount for CREATE TABLE
            validation_passed=True,      # validation already ran above
            validation_failures=0,
            error_message=error
        )

        if status == "failure":
            raise Exception(f"Semantic model {model_file} failed: {error}")

    conn.close()

if __name__ == "__main__":
    apply_semantic_models()