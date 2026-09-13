#!/usr/bin/env python3
"""Validates every mirrored skill and its pinned import provenance."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/sufficit/sufficit-ai-skills"
LINK = re.compile(r"\[[^]]*\]\(([^)]+)\)")


def digest(directory: Path) -> str:
    value = hashlib.sha256()
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        relative = path.relative_to(directory).as_posix().encode()
        value.update(len(relative).to_bytes(4, "big"))
        value.update(relative)
        content = path.read_bytes()
        value.update(len(content).to_bytes(8, "big"))
        value.update(content)
    return value.hexdigest()


def validate_document(directory: Path, expected_name: str) -> None:
    document = directory / "SKILL.md"
    text = document.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"missing front matter in {document}"
    front_matter = text.split("---\n", 2)[1]
    name = re.search(r"^name:\s*([^\s]+)\s*$", front_matter, re.MULTILINE)
    description = re.search(r"^description:\s*(.+)$", front_matter, re.MULTILINE)
    assert name and name.group(1) == expected_name, f"unexpected name in {document}"
    assert description and description.group(1).strip(), f"missing description in {document}"

    for target in LINK.findall(text):
        target = target.split("#", 1)[0]
        if not target or "://" in target or target.startswith(("#", "mailto:")):
            continue
        resolved = (directory / target).resolve()
        assert resolved.is_relative_to((ROOT / "skills").resolve()), f"link escapes skills: {document}: {target}"
        assert resolved.exists(), f"missing linked resource: {document}: {target}"


def main() -> None:
    catalog = json.loads((ROOT / "catalog/upstream-v2.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "catalog/import-manifest.json").read_text(encoding="utf-8"))
    catalog_by_id = {item["id"]: item for item in catalog["skills"]}
    manifest_by_id = {item["id"]: item for item in manifest["skills"]}
    assert catalog.get("schemaVersion") == 2, "catalog must use schema v2"
    assert manifest.get("schemaVersion") == 1, "unsupported import manifest"
    assert len(catalog_by_id) == len(catalog["skills"]), "duplicate catalog ids"
    assert len(manifest_by_id) == len(manifest["skills"]), "duplicate manifest ids"
    assert catalog_by_id.keys() == manifest_by_id.keys(), "manifest does not cover the catalog"
    assert manifest["catalogEntries"] == len(catalog_by_id), "catalog count differs"
    assert manifest["sources"] == catalog["sources"], "source provenance differs"

    expected_documents: set[Path] = set()
    for skill_id, item in manifest_by_id.items():
        catalog_item = catalog_by_id[skill_id]
        directory = (ROOT / item["path"]).resolve()
        assert directory.is_relative_to((ROOT / "skills").resolve()), f"unsafe package path: {skill_id}"
        assert (directory / "SKILL.md").is_file(), f"missing package: {skill_id}"
        assert item["name"] == catalog_item["name"], f"name provenance differs: {skill_id}"
        assert item["sourceId"] == catalog_item["sourceId"], f"source provenance differs: {skill_id}"
        assert item["upstreamSource"] == catalog_item["source"], f"upstream URL differs: {skill_id}"
        assert item["contentSha256"] == digest(directory), f"content digest differs: {skill_id}"
        validate_document(directory, item["name"])
        expected_documents.add((directory / "SKILL.md").resolve())

        release_file = directory / "release.json"
        if release_file.exists():
            release = json.loads(release_file.read_text(encoding="utf-8"))
            assert release["repository"] == REPOSITORY, f"release repository differs: {skill_id}"
            assert release["path"] == item["path"], f"release path differs: {skill_id}"
            assert re.fullmatch(r"\d+\.\d+\.\d+", release["version"]), f"invalid version: {skill_id}"

    actual_documents = {path.resolve() for path in (ROOT / "skills").glob("**/SKILL.md")}
    assert actual_documents == expected_documents, "untracked or missing skill packages"
    print(f"Validated all {len(expected_documents)} public skill packages.")


if __name__ == "__main__":
    main()
