# Installation, update and version

Canonical source: [sufficit/sufficit-ai-skills — skills/sufficit/sufficit-frontend](https://github.com/sufficit/sufficit-ai-skills/tree/main/skills/sufficit/sufficit-frontend). The SemVer version in `release.json` and `metadata.version` in SKILL.md belongs to the skill, not NuGet SUI.

## Install or check

At the reviewed `sufficit-ai-skills` checkout, run:

```sh
python3 skills/sufficit/sufficit-frontend/scripts/install.py install --target all
python3 skills/sufficit/sufficit-frontend/scripts/install.py status --target all
```

Requires Python 3. The installer copies full snapshots for Codex (`$CODEX_HOME/skills`, or `.codex/skills`), Claude (`.claude/skills`), Zcode (`.zcode/skills`) and Symposium (`.symposium/repo/skills` and `.symposium/skills` for compatibility). The paths are related to the user's home; `--home /path` allows testing another profile without changing the actual environment. For a tool, use `--target codex`, `claude`, `zcode` or `symposium`.

Symposium also receives `version` at the top of the frontmatter for its metadata reader; its `skill-card.md` allows discovery by OpenAI adapter. The difference is known and enters the hash of the installation. If Symposium uses a custom root, install/copy to the configured root, do not assume that the default folder is read.

The `.sufficit-installation.json` receipt contains version, source commit and SHA256 per file. `status` compares the contents installed with the receipt and checkout provided: `current`, `missing`, `modified`, `unmanaged`, `legacy-link` or `update-available`. A checkout may be delayed from the remote: `current` means equal to the local source, not “last version of GitHub”. No network query is made by the installer.

## Verifiable updates

```sh
git fetch origin main
git diff HEAD..origin/main -- skills/sufficit/sufficit-frontend
git show origin/main:skills/sufficit/sufficit-frontend/release.json
# After review, in a clean tree with no divergence:
git merge --ff-only origin/main
python3 skills/sufficit/sufficit-frontend/scripts/install.py install --target all --update
python3 skills/sufficit/sufficit-frontend/scripts/install.py status --target all
```

Run commands from the source repository, not from an installed copy. `--update` replaces only managed snapshots without local editing. The exchange uses staging and backup with restoration if it fails. Directory without receipt or edited content is preserved; review and save your changes before reinstalling. For the initial migration of an old symlink, `--migrate-from /exact/old/path` authorizes only that target. Do not use this parameter for unknown directories.

After installation, the new skill is available at the client's next discovery/turn; sessions that store catalog in memory may need to be reopened. Disk installation does not prove that an old session has already reloaded instructions.

## Genius

The `sufficit-frontend` entry in the v2 catalog points to `skills/sufficit/sufficit-frontend` in an immutable Git SHA. Search by name, `frontend`, `blazor` or `design-system`. The client loads SKILL.md and reads references on demand; Python/JS helper does not run automatically through the catalog.

To publish new version: update version, metadata, card and guidelines in this repository; validate and publish the revision; update SHA from source Sufficit in `sufficit-ai-genius/skills/sources.json`; regenerate with `scripts/update-skill-catalog.sh`; review diff and tests; publish by stream `scripts/publish-skill-catalog.sh`. Do not exchange for URL of `main`. Check the SHA of the public catalog entry and the `release.json` in that same SHA. Skills already installed in Genius can continue in the previous revision: check source in Extensions → Skills and reinstall for the new revision as per client workflow.
