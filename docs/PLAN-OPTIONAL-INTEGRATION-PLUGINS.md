# Optional integration plugin discovery

Session 01a1e58f-baad-7cb3-b3f6-7ed2f273f701, Genius issue #1527.

1. COMPLETED — inspect native ASAAS/Hermes/RouterOS skill routes and catalog metadata.
2. COMPLETED — add on-demand managed plugin installation before native tool use; bump versions/digests and generate index.
3. IN PROGRESS — validate packages/tests, commit/push to main and verify public catalog publication; archive this completed plan.

Keep credentials and existing production authorization rules. Native plugins execute on the tablet; absent manager means app update, not hidden desktop delegation. Preserve all unrelated packages and state.

Six packages updated: ASAAS connection/customers/payments/invoices, Hermes API and RouterOS management. All 195 packages validated, index/version/Markdown checks passed and 65 tests passed. Runtime loading does not expand provider authorization; Hermes keeps its existing API/Vault fallback for fields absent from installed native tools.
