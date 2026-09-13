#!/usr/bin/env python3
"""Imports every package from a pinned Genius catalog into this repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^]]*\]\(([^)]+)\)")


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        metavar="ID=CHECKOUT",
        help="checkout at the exact revision declared for a catalog source",
    )
    parser.add_argument(
        "--preserve",
        action="append",
        default=[],
        metavar="SKILL_ID",
        help="record an existing local package instead of copying its old source",
    )
    parser.add_argument("--replace", action="store_true")
    return parser.parse_args()


def parse_sources(values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        source_id, separator, checkout = value.partition("=")
        if not separator or not source_id or source_id in result:
            raise ValueError(f"invalid or duplicate --source: {value}")
        result[source_id] = Path(checkout).resolve()
    return result


def git_revision(checkout: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def relative_source_path(item: dict, source: dict) -> Path:
    prefix = f"{source['repository'].rstrip('/')}/tree/{source['revision']}/"
    url = item["source"]
    if not url.startswith(prefix):
        raise ValueError(f"{item['id']}: source does not match its declared revision")
    relative = Path(unquote(url.removeprefix(prefix)))
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"{item['id']}: package path is unsafe")
    return relative


def source_path(item: dict, source: dict, checkout: Path) -> Path:
    relative = relative_source_path(item, source)
    candidate = (checkout / relative).resolve()
    if not candidate.is_relative_to(checkout) or not (candidate / "SKILL.md").is_file():
        raise ValueError(f"{item['id']}: package path is missing or unsafe")
    return candidate


def destination_path(item: dict, source: dict) -> Path:
    relative = relative_source_path(item, source)
    source_id = item["sourceId"]
    if source_id == "android":
        destination = ROOT / "skills" / "android" / relative
    elif source_id == "google":
        if not relative.parts or relative.parts[0] != "skills":
            raise ValueError(f"{item['id']}: unexpected Google package path")
        destination = ROOT / "skills" / "google" / Path(*relative.parts[1:])
    else:
        destination = ROOT / "skills" / "sufficit" / item["id"]
    return destination.resolve()


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


def add_case_compatibility_files(directory: Path) -> None:
    """Preserves links authored for case-insensitive checkouts on Linux hosts."""
    document = directory / "SKILL.md"
    for target in LINK.findall(document.read_text(encoding="utf-8")):
        target = target.split("#", 1)[0]
        if not target or "://" in target or "/" in target or "\\" in target:
            continue
        requested = directory / target
        if requested.exists():
            continue
        matches = [path for path in directory.iterdir() if path.name.casefold() == target.casefold()]
        if len(matches) == 1 and matches[0].is_file():
            shutil.copyfile(matches[0], requested)


def main() -> None:
    args = arguments()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    if catalog.get("schemaVersion") != 2 or not 1 <= len(catalog.get("skills", [])) <= 256:
        raise ValueError("expected a valid reviewed Genius catalog v2")
    if len({item["id"] for item in catalog["skills"]}) != len(catalog["skills"]):
        raise ValueError("catalog contains duplicate skill ids")

    declared_sources = {item["id"]: item for item in catalog["sources"]}
    checkouts = parse_sources(args.source)
    for source_id, checkout in checkouts.items():
        source = declared_sources.get(source_id)
        if source is None:
            raise ValueError(f"checkout supplied for unknown source: {source_id}")
        if git_revision(checkout) != source["revision"]:
            raise ValueError(f"{source_id}: checkout revision differs from catalog")

    preserved = set(args.preserve)
    entries: list[dict] = []
    for item in sorted(catalog["skills"], key=lambda value: value["id"]):
        skill_id = item["id"]
        source = declared_sources[item["sourceId"]]
        destination = destination_path(item, source)
        if not destination.is_relative_to((ROOT / "skills").resolve()):
            raise ValueError(f"unsafe skill id: {skill_id}")

        if skill_id in preserved:
            if not (destination / "SKILL.md").is_file():
                raise ValueError(f"preserved package is missing: {skill_id}")
        else:
            checkout = checkouts.get(item["sourceId"])
            if checkout is None:
                raise ValueError(f"missing checkout for source: {item['sourceId']}")
            origin = source_path(item, source, checkout)
            if destination.exists():
                if not args.replace:
                    raise FileExistsError(f"destination already exists: {destination}")
                shutil.rmtree(destination)
            shutil.copytree(origin, destination)

        add_case_compatibility_files(destination)
        entries.append(
            {
                "id": skill_id,
                "name": item["name"],
                "sourceId": item["sourceId"],
                "author": item.get("author"),
                "license": item.get("license"),
                "upstreamSource": item["source"],
                "path": destination.relative_to(ROOT).as_posix(),
                "contentSha256": digest(destination),
            }
        )

    catalog_directory = ROOT / "catalog"
    catalog_directory.mkdir(exist_ok=True)
    shutil.copyfile(args.catalog, catalog_directory / "upstream-v2.json")
    manifest = {
        "schemaVersion": 1,
        "catalogEntries": len(entries),
        "sources": catalog["sources"],
        "skills": entries,
    }
    (catalog_directory / "import-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Imported and recorded {len(entries)} skill packages.")


if __name__ == "__main__":
    main()
