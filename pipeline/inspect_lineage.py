import argparse
import os
import yaml

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LINEAGE = os.path.join(PROJECT_ROOT, "semantic_lineage.yaml")

def load_lineage(manifest_path):
    with open(manifest_path, "r") as f:
        return yaml.safe_load(f)["models"]

def reverse_dependencies(models):
    reverse = {}
    for model, cfg in models.items():
        for dep in cfg.get("depends_on", []):
            reverse.setdefault(dep, []).append(model)
    return reverse

def impact_of_change(models, target_model):
    reverse = reverse_dependencies(models)
    impacted = set()
    stack = [target_model]

    while stack:
        current = stack.pop()
        for child in reverse.get(current, []):
            if child not in impacted:
                impacted.add(child)
                stack.append(child)

    return sorted(impacted)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default=DEFAULT_LINEAGE,
        help="Full path to semantic_lineage.yaml (auto-detected if not provided)"
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Model name to inspect for downstream impact"
    )
    args = parser.parse_args()

    models = load_lineage(args.manifest)
    if args.model not in models and args.model not in [m for m in models]:
        print(f"Model {args.model} not found in lineage manifest.")
        raise SystemExit(1)

    impacted = impact_of_change(models, args.model)

    if impacted:
        print(f"Changing {args.model} impacts:")
        for m in impacted:
            print(f"- {m}")
    else:
        print(f"Changing {args.model} has no downstream semantic impact.")
