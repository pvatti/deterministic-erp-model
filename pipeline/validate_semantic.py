import argparse
import os
import yaml
import sqlite3

# Auto-detect project root (directory above /pipeline)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Safe defaults using full system paths
DEFAULT_DB = os.path.join(PROJECT_ROOT, "init", "schema", "gold", "gold.db")
DEFAULT_MANIFEST = os.path.join(PROJECT_ROOT, "semantic_validation.yaml")

def run_validation_rules(db_path, manifest_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    with open(manifest_path, "r") as f:
        config = yaml.safe_load(f)

    failures = []

    for rule in config["rules"]:
        for view in rule["applies_to"]:
            sql = rule["sql"].replace("{view}", view)
            cur.execute(sql)
            count = cur.fetchone()[0]

            if count > 0:
                failures.append({
                    "rule": rule["id"],
                    "view": view,
                    "count": count,
                    "description": rule["description"]
                })

    conn.close()
    return failures


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # HERE is where defaults are actually applied
    parser.add_argument(
        "--db",
        default=DEFAULT_DB,
        help="Full path to gold.db (auto-detected if not provided)"
    )

    parser.add_argument(
        "--manifest",
        default=DEFAULT_MANIFEST,
        help="Full path to semantic_validation.yaml (auto-detected if not provided)"
    )

    args = parser.parse_args()

    # Now args.db and args.manifest contain either:
    # - user-provided paths, OR
    # - the auto-resolved defaults
    results = run_validation_rules(args.db, args.manifest)

    if results:
        print("VALIDATION FAILURES DETECTED:")
        for r in results:
            print(f"- Rule {r['rule']} failed on {r['view']} ({r['count']} rows): {r['description']}")
        raise SystemExit(1)
    else:
        print("All semantic validation rules passed.")
