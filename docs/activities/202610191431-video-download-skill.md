# Video download skill

Created `skills/sufficit/video-download/SKILL.md` at the user's request to preserve the successful linked-video download workflow from this session.

## Delivered

- English skill instructions for installed yt-dlp or an isolated uvx invocation, output naming, bounded retries, merge completion, and ffprobe verification.
- Missing-tool alternatives, process polling, cancellation handling and concrete access-error reporting.
- Catalog and import-manifest registration with a matching SHA-256 digest; README counts and package link updated.
- Scope remains local downloading. No installation, commit or publication was requested or performed.

## Validation

- skill-creator `quick_validate.py`: Skill is valid.
- Repository `scripts/validate.py`: validated all 167 public skill packages.
- yt-dlp accepted the documented option set with `--version` (2026.08.19). This checks option parsing, not another network download.
- ffprobe verified the session's existing downloaded MP4: video and audio streams, 61.166667 seconds, 6,345,975 bytes. No duplicate download was performed.
- uvx emitted SSL_CERT_DIR permission warnings for two local certificate files but exited successfully. Certificate settings were left unchanged.
- Final catalog and README diff reviewed. The previous catalogEntries field lagged the actual list by one; it now matches the actual 167 entries.
- Software-development update check reported installed version 1.1.1 current.

The skill links to the official yt-dlp usage documentation. It does not promise that every provider or private URL is accessible.
