#!/usr/bin/env python3
"""Validates the public skill packages without external dependencies."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REPOSITORY = "https://github.com/sufficit/sufficit-ai-genius-skills"
LINK = re.compile(r"\[[^]]*\]\(([^)]+)\)")


def validate_skill(directory: Path) -> None:
    document = directory / "SKILL.md"
    release_file = directory / "release.json"
    assert document.is_file(), f"missing {document}"
    assert release_file.is_file(), f"missing {release_file}"

    text = document.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"missing front matter in {document}"
    front_matter = text.split("---\n", 2)[1]
    name_match = re.search(r"^name:\s*([^\s]+)\s*$", front_matter, re.MULTILINE)
    assert name_match, f"missing skill name in {document}"
    assert name_match.group(1) == directory.name, f"skill name differs from directory: {directory}"

    release = json.loads(release_file.read_text(encoding="utf-8"))
    assert release["name"] == directory.name, f"release name differs for {directory.name}"
    assert re.fullmatch(r"\d+\.\d+\.\d+", release["version"]), "invalid semantic version"
    assert release["repository"] == EXPECTED_REPOSITORY, "release points to another repository"
    assert release["path"] == f"skills/{directory.name}", "release path differs from package path"

    for target in LINK.findall(text):
        if "://" in target or target.startswith("#"):
            continue
        resolved = (directory / target).resolve()
        assert resolved.is_relative_to(directory.resolve()), f"reference escapes package: {target}"
        assert resolved.is_file(), f"missing referenced resource: {target}"


def main() -> None:
    skill_directories = sorted(path.parent for path in (ROOT / "skills").glob("*/SKILL.md"))
    assert skill_directories, "no skill packages found"
    for directory in skill_directories:
        validate_skill(directory)
    print(f"Validated {len(skill_directories)} public skill package(s).")


if __name__ == "__main__":
    main()
