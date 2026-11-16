# YouTube runtime plugin instructions

Session 01a1e58f-baad-7cb3-b3f6-7ed2f273f701. Follow-up: native tools move into an optional signed runtime plugin hosted in the public bucket, Genius issue #1525.

1. COMPLETED — Update the Android workflow and package metadata for plugin_runtime discovery/install before transcript/frame use. Preserve video-understand catalog identity.
2. COMPLETED — Validate package digest/index/versions/tests and native tablet acceptance against the companion Genius implementation.
3. COMPLETED — Publish validated package, record delivery, archive plan and commit/push directly to main.

Do not claim Android runtime acceptance from desktop loader tests. Main implementation state is in the Genius repository's docs/PLAN-YOUTUBE-RUNTIME-PLUGIN.md.

Instruction update and catalog metadata prepared at version 1.3.0. All 195 package checks, index/versions/Markdown checks and 65 tests passed. Publication awaits physical acceptance of the companion managed runtime implementation.

Actual native runtime acceptance passed on the trimmed Android diagnostic build: all 401 available caption segments read through has_more=false, and actual source frames at 600/150 seconds returned and inspected without shell/subagents/remote executors. Formal AOT Release acceptance remains tracked by Genius; the instruction package itself passed 195 package checks, index/version/Markdown checks and 65 tests.

Published instruction package: source 22964408860b7af1b08d0c3d4a38123b861512a0, version 1.3.0, stable id video-understand. CI 43967093664 and Genius catalog sync 43967208636 succeeded; the public catalog was read back with the exact immutable revision. A registry-only fix aligned the digest of the already-committed clear-technical-writing package after its upstream content changed; that package content and canonical parallel edits were preserved.
