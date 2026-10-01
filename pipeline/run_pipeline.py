import subprocess
import sys
import os


def run_step(label, cmd):
    print(f"\n=== {label} ===")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[ERROR] {label} failed with code {result.returncode}")
        sys.exit(result.returncode)
    print(f"[OK] {label} completed")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. RAW → raw.db
    raw_loader = os.path.join(base_dir, "load_raw.py")
    run_step("RAW load", f"{sys.executable} {raw_loader}")

    # 2. STAGING → staging.db
    staging_loader = os.path.join(base_dir, "load_staging.py")
    run_step("STAGING load", f"{sys.executable} {staging_loader}")

    # 3. GOLD → gold.db
    gold_loader = os.path.join(base_dir, "load_gold.py")
    run_step("GOLD load", f"{sys.executable} {gold_loader}")

    print("\n=== Pipeline complete: RAW → STAGING → GOLD ===")


if __name__ == "__main__":
    main()
