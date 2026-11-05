#!/usr/bin/env python3
"""Keep reviewed catalog versions aligned with declared SKILL.md metadata."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def declared_version(document):
    parts = document.replace("\r\n", "\n").lstrip("\ufeff").split("---\n", 2)
    if len(parts) < 3 or parts[0]:
        return None
    # Same scalar metadata convention used by the host; never infer from prose or a Git SHA.
    match = re.search(r'^\s*version:\s*["\']?([0-9][A-Za-z0-9.+_-]*)["\']?\s*$', parts[1], re.MULTILINE)
    return match.group(1) if match else None


def updated(root=ROOT):
    catalog = json.loads((root / "catalog/upstream-v2.json").read_text())
    manifest = json.loads((root / "catalog/import-manifest.json").read_text())
    paths = {entry["id"]: root / entry["path"] / "SKILL.md" for entry in manifest["skills"]}
    for entry in catalog["skills"]:
        version = declared_version(paths[entry["id"]].read_text(encoding="utf-8"))
        if version is None:
            entry.pop("version", None)
        else:
            entry["version"] = version
    return catalog


if __name__ == "__main__":
    path = ROOT / "catalog/upstream-v2.json"
    expected = updated()
    if "--check" in sys.argv:
        if json.loads(path.read_text()) != expected:
            raise SystemExit("Catalog versions are stale; run python3 scripts/catalog_versions.py")
        print("Catalog versions match package metadata.")
    else:
        path.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n")
