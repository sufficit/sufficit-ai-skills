#!/usr/bin/env python3
"""Checks that every Markdown file is part of the documentation hierarchy.

Rules:
- every Markdown file is reachable from README.md through relative links;
- maintained documents do not link to Markdown files that do not exist.

Exempt from both rules (links pointing INTO them are still validated):
- paths matched by .markdown-coverage-ignore ("dir/" prefixes or glob patterns);
- files inside third-party skill packages other than their SKILL.md. Those
  packages are digest-pinned copies of upstream content (see
  catalog/import-manifest.json) whose internal navigation we cannot edit; their
  SKILL.md must still be reachable, through catalog/SKILLS.md.

Links follow CommonMark semantics: inline, reference-style and HTML anchors
count; code spans and blocks, images, comments and external links do not.

Usage: python3 scripts/markdown_coverage.py   (exit status 1 on violations)
"""

from __future__ import annotations

import fnmatch
import json
import posixpath
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINT = "README.md"
IGNORE_FILE = ".markdown-coverage-ignore"
# Sources whose packages are maintained here; every file inside them must be
# reachable (normally from the package's SKILL.md).
FIRST_PARTY_SOURCES = {"sufficit-genius", "sufficit-ui"}

_EXTERNAL = re.compile(r"^(?:[a-z][a-z\d+.-]*:|//|[?#])", re.IGNORECASE)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_PRE = re.compile(r"<(pre|code)\b.*?</\1>", re.DOTALL | re.IGNORECASE)
_PARSER = MarkdownIt("commonmark")


class _Anchors(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.hrefs += [value for name, value in attrs if name == "href" and value is not None]


def destinations(content: str) -> list[str]:
    """Link destinations a CommonMark renderer would produce, excluding images and code."""
    hrefs: list[str] = []
    html: list[str] = []
    for token in _PARSER.parse(content):
        if token.type == "html_block":
            html.append(token.content)
        for child in token.children or []:
            if child.type == "link_open":
                hrefs.append(str(child.attrGet("href") or ""))
            elif child.type == "html_inline":
                html.append(child.content)
    anchors = _Anchors()
    anchors.feed(_PRE.sub("", _COMMENT.sub("", "".join(html))))
    return hrefs + anchors.hrefs


class MarkdownGraph:
    def __init__(self, documents: dict[str, str]) -> None:
        self.documents = set(documents)
        self.links = {
            path: list(dict.fromkeys(t for href in destinations(text) if (t := self.local_target(path, href))))
            for path, text in documents.items()
        }

    @classmethod
    def from_repository(cls, root: Path) -> "MarkdownGraph":
        try:
            output = subprocess.run(
                ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                cwd=root, check=True, capture_output=True,
            ).stdout.decode()
        except (OSError, subprocess.CalledProcessError) as error:
            raise RuntimeError(f"cannot inventory documentation: {error}") from error
        paths = sorted({p for p in output.split("\0") if p.lower().endswith(".md") and (root / p).is_file()})
        return cls({path: (root / path).read_text(encoding="utf-8") for path in paths})

    def local_target(self, source: str, href: str) -> str | None:
        if not href or _EXTERNAL.match(href):
            return None
        destination = unquote(re.split(r"[?#]", href, maxsplit=1)[0])
        if destination.startswith("/"):
            target = posixpath.normpath(destination.lstrip("/"))
        else:
            target = posixpath.normpath(posixpath.join(posixpath.dirname(source), destination))
        if target == ".." or target.startswith("../"):
            return None
        if target.lower().endswith(".md"):
            return target
        readme = posixpath.join(target, "README.md")
        return readme if readme in self.documents else None

    def paths(self) -> list[str]:
        return sorted(self.documents)

    def unreachable(self, entrypoint: str = ENTRYPOINT) -> list[str]:
        visited: set[str] = set()
        pending = [entrypoint]
        while pending:
            path = pending.pop()
            if path in self.documents and path not in visited:
                visited.add(path)
                pending += self.links[path]
        return sorted(self.documents - visited)

    def missing_targets(self, sources: list[str]) -> dict[str, list[str]]:
        missing = {s: sorted(t for t in self.links.get(s, []) if t not in self.documents) for s in sources}
        return {source: targets for source, targets in missing.items() if targets}


class Exemptions:
    def __init__(self, patterns: list[str], packages: list[str] = ()) -> None:
        self.patterns = [p.lstrip("/") for p in patterns]
        self.packages = [p.rstrip("/") + "/" for p in packages]

    @classmethod
    def load(cls, root: Path) -> "Exemptions":
        ignore = root / IGNORE_FILE
        lines = ignore.read_text(encoding="utf-8").splitlines() if ignore.exists() else []
        patterns = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
        manifest = root / "catalog/import-manifest.json"
        skills = json.loads(manifest.read_text(encoding="utf-8"))["skills"] if manifest.exists() else []
        return cls(patterns, [s["path"] for s in skills if s["sourceId"] not in FIRST_PARTY_SOURCES])

    def matches(self, path: str) -> bool:
        if any(path.startswith(p) and path != p + "SKILL.md" for p in self.packages):
            return True
        return any(path.startswith(p) if p.endswith("/") else _segment_match(path, p) for p in self.patterns)

    def filter(self, paths: list[str]) -> list[str]:
        return [path for path in paths if not self.matches(path)]


def _segment_match(path: str, pattern: str) -> bool:
    """Glob where "*" does not cross "/" (same as Go's path.Match)."""
    parts, pattern_parts = path.split("/"), pattern.split("/")
    return len(parts) == len(pattern_parts) and all(fnmatch.fnmatchcase(a, b) for a, b in zip(parts, pattern_parts))


def check(root: Path = ROOT) -> list[str]:
    graph = MarkdownGraph.from_repository(root)
    exempt = Exemptions.load(root)
    errors = []
    orphans = exempt.filter(graph.unreachable())
    if orphans:
        errors.append(
            f"Markdown files unreachable from {ENTRYPOINT} ({len(orphans)}):\n"
            + "".join(f"  - {path}\n" for path in orphans)
            + "Link each one from a document already in the hierarchy (its skill's SKILL.md, a guide or index); "
            + f"new skill packages appear through catalog/SKILLS.md (scripts/build_skill_index.py). "
            + f"Use {IGNORE_FILE} only for intentionally unindexed history."
        )
    missing = graph.missing_targets(exempt.filter(graph.paths()))
    if missing:
        errors.append("Markdown links to missing documents:\n"
                      + "".join(f"  - {source} -> {', '.join(targets)}\n" for source, targets in missing.items()))
    return errors


def main() -> int:
    errors = check()
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print("Markdown coverage: every document is reachable from README.md.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
