# Local skill installation and update — completed

Objective: install and update the sufficit-ai-skills catalog in the current user's Codex skills directory. Preserve unrelated skills, local source edits and previous installations. No Genius catalog publication requested.

## Checkpoints
1. Completed — inspect remote revision, manifest names, installed packages and safe update paths.
2. Completed — install missing packages and update existing packages from the immutable remote revision, keeping backups and managed installation contracts.
3. Completed — verify installed files against catalog digests, record evidence, convert this plan to an activity and commit/push only task documentation.

Acceptance: every catalog skill discoverable by its manifest name; content verified against the selected remote revision, with managed installer transformations documented. Existing unrelated skills and source edits preserved.

Context: the requested audio screen reorganization in sufficit-blazor remains pending, with no screen code edits made. This user priority precedes that work; this installation plan does not close the frontend task.

Research: 195 unique manifest names; use manifest names instead of directory basenames (14 differ). Canonical checkout has an unrelated clear-technical-writing edit and .worktrees; install from a downloaded immutable origin/main archive, without advancing or editing that checkout. Preserve canonical software-development and reconciliation links when digest matches.

Installed from immutable revision 6c4e94fe1cfde2d5d8bf2d00068621d66e32641e: 169 new, 2 updated, 24 already current; 195 verified digests. Frontend managed installer reports version 1.0.5. Receipt: /home/hugodeco/.codex/skill-installations/sufficit-catalog-20261116155804.json.

## Evidence and delivery

- Downloaded the pinned GitHub archive using the Codex skill-installer helper and validated all 195 packages with its repository scripts/validate.py.
- Used manifest names, including the 14 packages whose folder basename differs from their skill name.
- Installation: 169 new; updated restore-credentials and sufficit-frontend; retained 24 identical packages. Frontend uses its own managed installer and reports current version 1.0.5.
- Independently recomputed all 195 installed package digests against the manifest read with git show at the pinned revision. The frontend installation receipt and Python cache files are excluded from the package hash.
- software-development check --remote: current, version 1.1.1. Existing canonical links retained.
- Preserved six unrelated skills: taste, impeccable, ui-ux-pro-max, awesome-design-md, sufficit-private-ci, playwright-cli; also preserved system skills and plugin installations.
- Backup of the replaced unmanaged restore-credentials package: /home/hugodeco/.codex/skill-backups/sufficit-catalog-20261116155804. Frontend replacement followed its managed installer contract.
- The canonical checkout was not advanced during installation: its unrelated clear-technical-writing edit and .worktrees remain intact. Published clear-technical-writing was installed from the remote archive, without copying the uncommitted edit.
- No Genius catalog publication, external service deployment, or other-client installation requested or performed. Skills are available at the next turn/discovery; an existing client's cached catalog may require a new session.
- Delivery is the documentation-only commit containing this activity, pushed to main. Local receipt above records machine-specific installed package names and revision.

The audio-screen task remains pending and is not marked complete by this installation activity.
