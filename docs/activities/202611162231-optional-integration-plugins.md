# Optional integration plugin discovery

Session 01a1e58f-baad-7cb3-b3f6-7ed2f273f701, Genius issue #1527.

1. COMPLETED — inspect native ASAAS/Hermes/RouterOS skill routes and catalog metadata.
2. COMPLETED — add on-demand managed plugin installation before native tool use; bump versions/digests and generate index.
3. COMPLETED — validate packages/tests, commit/push to main and verify public catalog publication; archive this completed plan.

Keep credentials and existing production authorization rules. Native plugins execute on the tablet; absent manager means app update, not hidden desktop delegation. Preserve all unrelated packages and state.

Six packages updated: ASAAS connection/customers/payments/invoices, Hermes API and RouterOS management. All 195 packages validated, index/version/Markdown checks passed and 65 tests passed. Runtime loading does not expand provider authorization; Hermes keeps its existing API/Vault fallback for fields absent from installed native tools.

Delivery complete: commits 291a9b0 and 116af09 pushed directly to main. CI
43991959082 passed; all 195 packages, index/version/Markdown checks and 65 tests
passed. Public catalog readback verified immutable source 116af09cc87f5d0371ac1dd390a03c36975e306e
and versions ASAAS connection/payments 0.1.3, customers 0.4.2, invoices 0.8.2,
Hermes API 0.4.4 and RouterOS management 1.0.3. Five previously unversioned
front matters now declare their release version so native update discovery can
compare versions. No provider operation or credential change was authorized by
these instructions. Genius application migration/remote CI remains tracked in
Genius issue #1527, separate from this completed skill publication.
