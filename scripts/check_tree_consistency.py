import json
import sys

# Usage: python scripts/check_tree_consistency.py [path_to_tree.json]
TREE_PATH = sys.argv[1] if len(sys.argv) > 1 else "story/narrative_oriented_tree.json"

with open(TREE_PATH, "r", encoding="utf-8") as f:
    tree = json.load(f)

def check_node(node, path="root"):
    errors = []
    # Build a set of child ids
    child_ids = set(child["id"] for child in node.get("children", []))
    # Check that every id in options is present in children
    for word, child_id in node.get("options", {}).items():
        if child_id not in child_ids:
            errors.append(f"[MISSING CHILD] At {path}: option '{word}' points to id '{child_id}' not found in children.")
    # Check that every child is referenced in options (optional, warning only)
    for child in node.get("children", []):
        if child["id"] not in node.get("options", {}).values():
            errors.append(f"[UNREFERENCED CHILD] At {path}: child id '{child['id']}' not referenced in options.")
    # Recurse
    for idx, child in enumerate(node.get("children", [])):
        errors.extend(check_node(child, path + f" -> {child['id']}"))
    return errors

all_errors = check_node(tree)
if all_errors:
    print("Inconsistencies found:")
    for err in all_errors:
        print(err)
else:
    print("No inconsistencies found. Tree is consistent!")
