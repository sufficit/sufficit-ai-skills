---
name: software-development
description: Execute authorized software changes with a live plan, implementation checkpoints, proportionate validation and a delivery record. Use for implementation, fixes, refactoring and migrations; exclude read-only explanations, status checks and reviews without edit authorization.
metadata:
  version: "1.1.0"
  author: "Sufficit"
  source: "https://github.com/sufficit/sufficit-ai-skills"
---

# Software development

Take the user's authorized change through verified delivery. Repository rules and
explicit user instructions determine scope, approvals and publication. This skill
does not itself authorize messaging others, deployment, publishing or merging.

## Version and source

The canonical package is `skills/sufficit/software-development` in
`sufficit/sufficit-ai-skills`; `release.json` records its SemVer version. On the
first use in a session, when a local shell and checkout are available, run
`python3 <skill-directory>/scripts/manage.py check --remote`, resolving
`<skill-directory>` to the actual loaded folder. Read [installation and updates](references/installation.md)
only to install, repair or update the package. Check once, not between every task.

An unavailable update check is not a software-task blocker: report it briefly
and continue with the installed version. An available update is information, not
authority to replace instructions mid-task. Never claim latest without a successful
remote comparison. Without a shell, use the loaded version and state the limitation.

## 1. Establish the next concrete action

Read applicable repository instructions, inspect Git state and the relevant
implementation/tests. Preserve unrelated changes and isolate edits when required.
For a supplied path that does not exist, inspect known locations; clarify a material
ambiguity before creating a new project from a possibly mistaken name.

Identify the expected behavior and evidence that would demonstrate it. End initial
research when the contract, implementation point and validation path are known.
Further reads should answer a named uncertainty; avoid repeatedly announcing that
research is complete and then restarting it. Record hypotheses separately from facts.

## 2. Record the whole plan before implementation

Inspect `docs/` and follow local naming conventions. By default use
`docs/PLAN-<UPPERCASE-SLUG>.md` in the affected repository, never its root or the
session workspace. Reuse a plan only if it belongs to this exact task. A small
change needs only a short plan; do not invent unrelated phases to fill a template.

Include objective, acceptance evidence, ordered checkpoints, relevant constraints,
validation commands and the current blocker if any. Keep exactly one checkpoint
in progress. If a native task panel is available, keep it synchronized; otherwise
the file is the source of execution state, not an unsupported claim of panel updates.

Advance checkpoint status immediately when its evidence exists. A new priority
reorders the plan without losing the original pending work. After compaction or
interruption, consult this plan and recent results before redoing completed work.

## 3. Implement and verify incrementally

Use the available local shell directly. Prefer repository tools and existing
patterns over a new framework. Parallelize independent reads when supported;
keep dependent changes and writes ordered. Delegate only when authorized.

- Implement the smallest coherent fix that meets the requirement. A newly found
  unrelated issue is recorded separately, not silently added to the change.
- For a reproducible bug, show that its regression test fails before the fix and
  passes after it. Do not add tests that only mirror wording or implementation.
- Run checks proportionate to the change and required by the repository. After
  they pass, rerun only for changed code, failures or unresolved concerns.
- Missing tools: inspect the error and use the available fallback. A missing
  optional checker is skipped explicitly, never reported as passed.
- Deterministic errors: change the relevant argument/state or diagnostic approach
  before retrying. Do not cycle through superficial variations of the same call.
- A canceled operation needs classification first: user cancellation, timeout,
  deterministic failure or transient issue. Do not automatically restart user stops.
- An inconclusive remote write needs a state read before another write. Plan
  isolated tests so verification does not accidentally perform production actions.

Continue already authorized work without repeated permission requests. Ask only
for missing information, authority or a decision that materially affects the result.
Use the communication mechanism actually supported by the current environment;
never treat an empty tool response as consent. A real blocker records the failed
operation, evidence and the safest next action, with remaining checkpoints intact.

### Blazor rendering and event-driven state

For Blazor changes involving lists, streaming or frequently updated state, read
[Blazor rendering](references/blazor-rendering.md) before choosing component
boundaries or update scheduling. Check stable parameters, `ShouldRender` and
fixed cascading values; do not introduce a periodic render timer as the default
response to UI lag. Measure affected components and preserve event-driven updates.

## 4. Deliver only what the evidence supports

Distinguish implementation, successful tests, published PR, merged code, installed
version and observed production behavior. Never substitute one for another.
Progress updates give new findings or completed actions; do not finish a turn with
an action promise while the next safe authorized action is available.

Complete the repository's applicable delivery workflow within the user's authority.
No blanket mandate to create issues, message reviewers, merge or deploy comes from
this skill. If a required step cannot be completed, say exactly what remains.

When implementation and required validation are complete:

1. Create `docs/activities/YYYYMMDDHHmm-<slug>.md` using local time, or the repository's
   designated activity directory. Record changes, decisions, actual test results,
   delivery references and limitations; do not claim an unavailable check passed.
2. Move still-useful contracts into permanent documentation. Check references to
   the temporary plan before removing it. Keep the plan if any requested work remains.
3. Verify the final files and Git/remote state. Stage only your own files. Preserve
   branches and worktrees with unsent work or active processes.

The final reply should state what changed, what was verified and any material
remaining limitation. Do not end with an offer to perform work already requested.
