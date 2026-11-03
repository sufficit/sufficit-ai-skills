# Legacy renewal guidance

## Objective
Prevent Genius from treating a native writer handoff refusal or missing commercial authority headers as proof that a legacy service cannot be renewed.

## Checkpoints
1. Completed: inspect incident and deployed-source contracts; legacy Session supplies mandatory headers and the generic API tool supports them.
2. Completed: clarify per-service routing, conflict recovery and stopping conditions in sufficit-api; validate package and catalog digests.
3. In progress: commit/push main, verify skills CI and published catalog revision, record delivery and remove this plan.

## Acceptance
Legacy services remain renewable through their existing audited flow; mixed customers are handled per service. No migration, payment marking or renewal is performed as part of guidance publication. The incident client version is unknown, so publication alone does not prove the installed client consumed the update.

## Validation
python3 scripts/validate.py; python3 scripts/markdown_coverage.py; published catalog must pin the new skills revision.
