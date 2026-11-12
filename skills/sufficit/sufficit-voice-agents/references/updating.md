# Updating this skill

Canonical package: `skills/sufficit/sufficit-voice-agents` in the public repository
`https://github.com/sufficit/sufficit-ai-skills` (branch `main`). The version is SemVer, declared in two places that
always match: `metadata.version` in `SKILL.md` and `version` in `release.json`.

## Check

1. Read your installed version from `SKILL.md` front matter.
2. Fetch `https://raw.githubusercontent.com/sufficit/sufficit-ai-skills/main/skills/sufficit/sufficit-voice-agents/release.json`.
3. Compare as SemVer:
   - remote higher: update available. Read the remote
     `https://raw.githubusercontent.com/sufficit/sufficit-ai-skills/main/skills/sufficit/sufficit-voice-agents/CHANGELOG.md`
     and apply the update before the next voice operation, or now when the changelog says **required**.
   - equal: current.
   - remote lower or unreadable: keep yours and report the check result once.

Check once per working session, not before every call. A check never changes files by itself.

## Update

Replace the whole folder, never a single file, so references stay consistent with `SKILL.md`:

- with git: `git clone --depth 1 --filter=blob:none --sparse https://github.com/sufficit/sufficit-ai-skills.git` then
  `git sparse-checkout set skills/sufficit/sufficit-voice-agents` and copy that folder over your installed one;
- without git: download every file listed in the folder at
  `https://github.com/sufficit/sufficit-ai-skills/tree/main/skills/sufficit/sufficit-voice-agents` from
  `raw.githubusercontent.com` (same path), keeping the relative paths.

After replacing, read the new `SKILL.md` front matter and confirm its version equals the remote `release.json`. New
instructions apply from the next task; finish or pause an operation already in progress under the old version.

## Pinned revision

To audit exactly what you run, note the commit of the update:
`https://api.github.com/repos/sufficit/sufficit-ai-skills/commits?path=skills/sufficit/sufficit-voice-agents&per_page=1`.
Do not edit the installed copy locally; local changes are lost on the next update.
