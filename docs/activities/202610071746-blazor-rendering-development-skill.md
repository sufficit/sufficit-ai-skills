# Blazor rendering guidance in the development skill

Issue: https://github.com/sufficit/sufficit-ai-skills/issues/7
PR: https://github.com/sufficit/sufficit-ai-skills/pull/8

Software-development 1.1.0 requires its Blazor rendering reference when working
on streaming, lists or frequent state changes. It covers recognized immutable
parameters, explicit ShouldRender comparisons for custom records/complex models,
and IsFixed only for invariant cascading values. Component identity via @key
is distinguished from render suppression; lifecycle work still needs attention.

The guidance includes locale, expiry, callbacks and local UI interaction when
comparing render inputs. It prioritizes snapshots plus deltas, preserving earlier
message references, targeted notifications and persistence outside the renderer.
It does not introduce a default 100 ms timer. Any throttling needs measurements
and an explicit latency/durability contract.

The reference links to Microsoft's Blazor rendering/performance documentation
and ASP.NET Core's ChangeDetection implementation. It is loaded for relevant
Blazor work; it does not burden unrelated implementation tasks.

Validation: all 165 mirrored packages, skill quick_validate, and nine managed
installation tests passed. Tests ran with PYTHONDONTWRITEBYTECODE=1 so Python
cache files are not mistaken for published package content by digest validation.
Version metadata, release metadata, versioned catalog description and both
manifest digests updated together. Linked installation verification follows
publication of the canonical revision.
