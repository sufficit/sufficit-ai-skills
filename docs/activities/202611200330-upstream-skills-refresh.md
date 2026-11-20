# Upstream skills refresh: Google, Android, MikroTik, Matt Pocock

Done on 2026-11-20, after checking all six external sources of the catalog for
newer versions since the pinned revisions.

- Google: 122 of 127 mirrored packages refreshed to `dbabd354` (334 upstream
  commits since `f36c9eb`). The four `genkit-*` packages moved upstream to
  `skills/cloud/developing-genkit-*` and were re-imported at their new paths
  with unchanged ids. The 50 catalog descriptions that mirror a package's front
  matter were updated to the new upstream wording; curated descriptions were
  left alone. The 90 new Google packages upstream were deliberately not
  imported — the catalog is kept under the host's 256-entry ceiling with
  margin, and the `ads`/`developers`/`identity`/`platform-devices` trees remain
  unmirrored.
- Android: 21 packages refreshed to `c7294258` (plugin v1.0.23). Upstream
  removed the experimental `jetpack-compose/theming/styles` package on
  2026-10-26 (#258); `android-styles` left the mirror with it. The 16 new
  packages were imported (collection 22 → 37): `litert-lm`, `litert-runtime`,
  `mlkit-agent-api`, `ml-kit-genai-prompt-api`, `ink-app-builder`,
  `ink-custom-brush-builder`, `jetpack-compose-performance`, `ios-to-android`,
  `navigation-event`, `anr-audit-and-fix`, `android-permissions-security`,
  `glance-appwidget-updates-and-memory`, `glance-canonical-layouts`,
  `wear-widgets`, `android-for-cars-parked-apps` and `projected-hardware`.
- MikroTik: pin advanced to `aa007fb1`. The adapted `routeros-management`
  package merged the upstream `/import verbose dry-run` lab note as a new
  section (package 1.0.4). The upstream REST reference files (firewall, users,
  packages, licensing, device-mode and friends) were not merged wholesale: the
  adaptation already carries the REST surface in `SKILL.md`. Four new upstream
  skills (`routeros-cmr`, `routeros-webfig`, `routeros-zerotier`,
  `routeros-proprietary-protocols`) were noted but not imported.
- Matt Pocock: pin advanced to `abeeaf95`; the mirrored `prototype` package is
  byte-identical upstream. The two new skills live under `skills/in-progress`
  and were not imported.
- Refero and Jakeschincariol/instagram-agent-skill: package content unchanged
  upstream, pins stay `a9b54a3e` and `d03c56bb`. The upstream Refero v1.0.3
  release only touched plugin manifests and `VERSION`.
- `scripts/validate.py` link checking now ignores fenced code blocks and
  destinations containing spaces: upstream `android-cli` ships a sample-output
  placeholder (`path/to/screenshot`) inside a fence, and
  `ink-custom-brush-builder` has a tree diagram that parses as a link
  (`[Operators](input = SourceNode)`).

Validation after the refresh: `validate.py` covers all 212 packages, markdown
coverage, `catalog_versions.py --check` and all nine unittest modules pass.
