# apply_semantic.py
import os
import sqlite3

def apply_semantic_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # gold.db absolute path
    gold_db = os.path.abspath(os.path.join(base_dir, "..", "data", "gold.db"))

    # semantic SQL directory absolute path
    semantic_dir = os.path.abspath(os.path.join(base_dir, "..", "init", "schema", "semantic"))

    print("Using gold.db:", gold_db)
    print("Using semantic dir:", semantic_dir)

    conn = sqlite3.connect(gold_db)
    cursor = conn.cursor()

    for filename in os.listdir(semantic_dir):
        if filename.endswith(".sql"):
            file_path = os.path.join(semantic_dir, filename)
            print("Applying semantic model:", filename)
            with open(file_path, "r", encoding="utf-8") as f:
                cursor.executescript(f.read())

    conn.commit()
    conn.close()

if __name__ == "__main__":
    apply_semantic_models()
