#!/usr/bin/env python3
"""Link a reviewed checkout into Codex and check package updates without pulling."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.request
import uuid

NAME = "software-development"
REPOSITORY = "https://github.com/sufficit/sufficit-ai-skills"
PACKAGE = f"skills/sufficit/{NAME}"


def git(root, *args):
    process = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                             text=True, timeout=10)
    if process.returncode:
        raise ValueError(f"Git operation failed: {process.stderr.strip()[:500]}")
    return process.stdout.strip()


def digest(root):
    result = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Unexpected symlink inside package: {path.name}")
        if path.is_file():
            relative = path.relative_to(root).as_posix().encode()
            content = path.read_bytes()
            result.update(len(relative).to_bytes(4, "big"))
            result.update(relative)
            result.update(len(content).to_bytes(8, "big"))
            result.update(content)
    return result.hexdigest()


def version(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError("Expected a three-component SemVer release")
    return tuple(map(int, value.split(".")))


def validate_release(meta):
    if (meta.get("name"), meta.get("repository"), meta.get("path")) != (NAME, REPOSITORY, PACKAGE):
        raise ValueError("Unexpected release identity or source")
    version(meta.get("version"))
    return meta


def entry(manifest):
    entries = [item for item in manifest["skills"] if item["id"] == NAME]
    if len(entries) != 1 or entries[0]["path"] != PACKAGE:
        raise ValueError("Missing or ambiguous package in import manifest")
    value = entries[0]["contentSha256"]
    if not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("Invalid manifest digest")
    return value


def source_metadata(source):
    source = source.resolve(strict=True)
    root = Path(git(source, "rev-parse", "--show-toplevel")).resolve()
    if source != root / PACKAGE:
        raise ValueError("Source is not the canonical package path in a Git checkout")
    origin = git(root, "remote", "get-url", "origin")
    if origin.removesuffix(".git").rstrip("/") not in (REPOSITORY, "git@github.com:sufficit/sufficit-ai-skills"):
        raise ValueError("Source origin is not sufficit/sufficit-ai-skills")
    meta = validate_release(json.loads((source / "release.json").read_text()))
    text = (source / "SKILL.md").read_text()
    declared = re.search(r'^  version: "([^"\n]+)"$', text, re.MULTILINE)
    if not declared or declared.group(1) != meta["version"]:
        raise ValueError("Skill metadata version differs from release.json")
    actual = digest(source)
    expected = entry(json.loads((root / "catalog/import-manifest.json").read_text()))
    if actual != expected:
        raise ValueError("Source package modified: digest differs from import manifest")
    dirty = git(root, "status", "--porcelain", "--", PACKAGE, "catalog/import-manifest.json")
    if dirty:
        raise ValueError("Source package or manifest has uncommitted changes")
    return {**meta, "source": str(source), "revision": git(root, "rev-parse", "HEAD"),
            "contentSha256": actual}


def paths(codex_home):
    return (codex_home / "skills" / NAME,
            codex_home / "skill-installations" / f"{NAME}.json")


def installation_state(target, source):
    if target.is_symlink():
        return "linked" if target.resolve() == source.resolve() else "foreign-link"
    return "unmanaged" if target.exists() else "missing"


def write_receipt(path, receipt):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}-{uuid.uuid4().hex}")
    try:
        temporary.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def install(source, codex_home, migrate_existing=False):
    meta = source_metadata(source)
    source = Path(meta["source"])
    target, receipt_path = paths(codex_home)
    state = installation_state(target, source)
    previous = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
    if state == "foreign-link":
        raise ValueError("Existing link has a different source; left untouched")
    if state == "unmanaged" and (not migrate_existing or not target.is_dir()):
        raise ValueError("Existing copy preserved; review it and use --migrate-existing to back it up")
    if source == target.resolve() and state != "linked":
        raise ValueError("Cannot replace the source directory itself")
    target.parent.mkdir(parents=True, exist_ok=True)
    stage = target.with_name(f".{NAME}-stage-{uuid.uuid4().hex}")
    backup = None
    created = False
    try:
        if state != "linked":
            stage.symlink_to(source, target_is_directory=True)
            if state == "unmanaged":
                stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                backup = codex_home / "skill-backups" / f"{NAME}-{stamp}-{uuid.uuid4().hex[:8]}"
                backup.parent.mkdir(parents=True, exist_ok=True)
                target.rename(backup)
            os.replace(stage, target)
            created = True
        if target.resolve() != source or digest(source) != meta["contentSha256"]:
            raise ValueError("Source changed while linking; installation rolled back")
        receipt = {**meta, "mode": "symlink", "target": str(target),
                   "installedAt": datetime.now(timezone.utc).isoformat(),
                   "backup": str(backup) if backup else previous.get("backup")}
        write_receipt(receipt_path, receipt)
        return {"state": "linked", **receipt, "receipt": str(receipt_path)}
    except Exception:
        if created:
            target.unlink()
        if backup is not None:
            backup.rename(target)
        raise
    finally:
        stage.unlink(missing_ok=True)


def remote_json(revision, path):
    url = f"https://raw.githubusercontent.com/sufficit/sufficit-ai-skills/{revision}/{path}"
    request = urllib.request.Request(url, headers={"User-Agent": "sufficit-skill-update-check/1"})
    with urllib.request.urlopen(request, timeout=10) as response:
        data = response.read(2_000_001)
    if len(data) > 2_000_000:
        raise ValueError("Remote metadata exceeds limit")
    return json.loads(data)


def remote_metadata():
    # Query a fixed repository; all subsequent reads use this immutable commit.
    process = subprocess.run(["git", "ls-remote", REPOSITORY + ".git", "refs/heads/main"],
                             capture_output=True, text=True, timeout=10)
    if process.returncode or not process.stdout.strip():
        raise ValueError("Cannot determine published main revision")
    revision = process.stdout.split()[0]
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Invalid published revision")
    meta = validate_release(remote_json(revision, PACKAGE + "/release.json"))
    return {**meta, "revision": revision,
            "contentSha256": entry(remote_json(revision, "catalog/import-manifest.json"))}


def compare(local, remote):
    if local["version"] == remote["version"]:
        return "current" if local["contentSha256"] == remote["contentSha256"] else "version-conflict"
    return "update-available" if version(remote["version"]) > version(local["version"]) else "local-ahead"


def check(source, codex_home, remote=False):
    local = source_metadata(source)
    target, receipt_path = paths(codex_home)
    result = {"local": local, "installation": installation_state(target, source),
              "target": str(target), "receipt": str(receipt_path) if receipt_path.exists() else None,
              "remote": {"state": "not-checked"}}
    if remote:
        try:
            latest = remote_metadata()
            result["remote"] = {**latest, "state": compare(local, latest)}
        except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
            result["remote"] = {"state": "unavailable", "error": str(error)[:500]}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "check"])
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--codex-home", type=Path,
                        default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))))
    parser.add_argument("--migrate-existing", action="store_true")
    parser.add_argument("--remote", action="store_true")
    args = parser.parse_args()
    try:
        source, home = args.source.resolve(), args.codex_home.expanduser().resolve()
        if args.action == "install":
            result = install(source, home, args.migrate_existing)
            code = 0
        else:
            result = check(source, home, args.remote)
            state = result["remote"]["state"]
            code = 0 if result["installation"] == "linked" and state in ("current", "not-checked") else 1
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return code
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(json.dumps({"state": "error", "error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
