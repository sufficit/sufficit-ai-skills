# Linked installation and verification

Canonical source: https://github.com/sufficit/sufficit-ai-skills/tree/main/skills/sufficit/software-development. The skill version is independent of the version of Codex. `release.json` and `metadata.version` must match; the catalog records the full package SHA-256.

## Install in Codex

Use reviewed and clean canonical checkout, not a temporary worktree:

```sh
python3 skills/sufficit/software-development/scripts/manage.py install
# Only when migrating an old copy that has already been reviewed:
python3 skills/sufficit/software-development/scripts/manage.py install --migrate-existing
python3 skills/sufficit/software-development/scripts/manage.py check --remote
```

The destination is `$CODEX_HOME/skills/software-development`, or `$HOME/.codex/skills/software-development`. `--codex-home /directory` allows testing alone. The installation is a symlink to the canonical folder; the old copy is preserved in `skill-backups/` outside the discovery of skills. Links to another source are refused. The receipt in `skill-installations/software-development.json` records initial version, Git revision, digest, origin, destination and backup.

The helper itself is used because the default Codex installer copies the package without maintaining this link. Codex supports symlink-connected skill directories: https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills. This installation preserves the root `.codex/skills` already used by the client; other environments can use `.agents/skills` according to local configuration/discovery. Do not create two entries with the same name on different roots.

## Check and update

`check` checks link, version and digest against the local manifest. `check --remote` consults the current SHA of `main` and reads release/manifest in this immutable SHA with timeouts. Doesn't run pull, doesn't change branches and doesn't change files. Without network, it returns remote state `unavailable`, not a false update confirmation. It runs once per session when the skill is used; there is no timer/daemon installed.

Remote states: `current`, `update-available`, `local-ahead`, `version-conflict` or `unavailable`. `current` compares the package, not just the global repository commit. Changes in another skill do not produce a false warning. A same SemVer with different digest is version conflict and needs to be investigated.

When an update is desired and authorised:

```sh
git fetch origin main
git diff HEAD..origin/main -- skills/sufficit/software-development catalog/import-manifest.json
# Confirm a clean Git state and no divergence before advancing the checkout.
git merge --ff-only origin/main
python3 skills/sufficit/software-development/scripts/manage.py install
python3 skills/sufficit/software-development/scripts/manage.py check --remote
```

Because the installation is linked, advancing or editing the checkout changes the files visible in Codex. Keep the canonical checkout in main and develop the skill in separate worktree. The receipt records the explicit installation/update, not each reading. The checker detects altered local content or digest divergence and does not replace it. New instructions are available at the next discovery/turn; a disk check does not prove that a running turn has reloaded them.

## Maintain a release

Update `release.json`, `metadata.version` and the versioned description of the catalog; recalculate the digest with `scripts/validate.py::digest` in both manifests. Run `python3 scripts/validate.py`, the manager tests and the skill validator. Publish the revision and recheck the remote version. Do not edit the installed copy as if it were independent: the symlink changes the source.
