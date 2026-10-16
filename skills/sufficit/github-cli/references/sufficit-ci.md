# CI Sufficit

Use this flow when a PR, issue or mission mention CI, checks, Actions, runner, build or tests. The GitHub account connected to Genius is the first way to diagnose. Infrastructure manuals are internal administrative source and should never be copied for a response, issue, log, public skill or product repository.

## Sources of Truth

See in this order:

1. `AGENTS.md` or equivalent repository instruction;
2. `.github/workflows/*.yml` in the revision that ran;
3. `scripts/ci-local.sh` and scripts it invokes;
4. checks, jobs, steps, logs and execution artifacts in GitHub;
5. Runner status, only if the job is waiting for infrastructure.

The workflow of the repository itself wins any example of this reference. The default Linux label is `aireset-ci` (renamed from `openclaw-ci` on 2026-09-18); do not change labels by name association.

## Autonomous diagnosis

1. Read PR with `statusCheckRollup`, `headRefOid`, `baseRefName`, `files` and URL.
2. For each unsuccessful check, identify workflow, execution, job, step and time.
3. If the job is finished, read `--log-failed`; if necessary, see the specific job and download the result artifact. Do not ask the human to paste logs available in GitHub.
4. Read the PR diff and the changed tests, but do not conclude that a failure is pre-existing only because the test name does not match the modified files.
5. Look for evidence: reproduce in the worktree, check out the same suite at the base or compare recent executions of the base branch. Record command, failure and causal relationship in few lines.
6. Take the next action that is already authorized: correct the regression, return to the author, repeat a transient failure once or monitor the runner. Send decision to the human only when there is a choice of product or risk without rule in the repository.

Useful queries, always like the `arguments` list of `github_cli`:

```json
["pr", "view", "536", "--repo", "owner/repo", "--json", "number,title,headRefOid,baseRefName,files,statusCheckRollup,url"]
```

```json
["run", "view", "34672730158", "--repo", "owner/repo", "--json", "status,conclusion,jobs,url"]
```

```json
["run", "view", "34672730158", "--repo", "owner/repo", "--job", "103497052889", "--log-failed"]
```

```json
["run", "list", "--repo", "owner/repo", "--branch", "main", "--workflow", "CI", "--limit", "5", "--json", "databaseId,status,conclusion,headSha,createdAt,url"]
```

## Classification and action

| Evidence | Classification | Next action |
|---|---|---|
| Test reproduces on the PR branch and passes at the base | PR regression | Author fixes; reviewer requests change and returns task |
| Same test failed base or previous comparable execution | Proven pre-existing failure | Link existing failure and apply repository merge policy |
| Timeout, temporary download or external service oscillates; new attempt does not repeat | Transient | Reexecute only failed jobs and follow until finished |
| Job gets `queued` and no compatible runner is online/free | Runner unavailable or busy | See runners/labels; wait if busy or forward objective operational failure |
| Execution cancelled | Cancellation | Determine whether it was manual, by concurrency, timeout or superseded before repeating |
| Logs/API return denied access | Insufficient authorisation | Inform permission and endpoint absent; do not invent diagnosis |

Preexisting failures are not automatically irrelevant. Make sure they break the PR contract, prevent a reliable review or hide another regression. The final decision follows the branch rules and revision of the repository.

## Reruns and monitoring

Before repeating, refer to the current state. A written call with ambiguous result must be confirmed by a new reading to avoid duplicate executions.

```json
["run", "rerun", "34672730158", "--repo", "owner/repo", "--failed"]
```

Then follow `run view` to `completed`. Do not create a fast loop: self-hosted jobs can wait for capacity and each instance processes one job at a time. A job `queued` is wait, not error. A repeated deterministic failure shall be corrected or returned to the person responsible, without further identical attempts.

Use `workflow run` only if YAML declares `workflow_dispatch` and the request authorizes dispatch. A correction push usually creates another execution; confirm before firing another one.

## Current runners contract Sufficit

The shared CI has platform separated runners. In Genius, the current contract is:

| Platform | Labels requested by workflow | Genius Primary Runner |
|---|---|---|
| Linux | `self-hosted, Linux, X64, aireset-ci, ci-primary` | `linux-ci-genius-contigencia` |
| Windows | `self-hosted, Windows, X64, windows-ci, ci-primary` | `windows-ci-contigencia` |
| macOS/iOS | `self-hosted, macOS, X64, macos-ci, ci-primary` | `macos-ci` |

`aireset-ci` names the host provider (Aireset); it does not identify the real machine alone. Until 2026-09-18 was called `openclaw-ci`, heritage of the former openclaw-server host. `ci-primary` selects the preferred destination and must exist in only one platform and repository compatible runner. Other repositories can use different combinations, so read `runs-on` in the workflow before diagnosing.

This map identifies the primary destination of `sufficit/sufficit-ai-genius`, does not allow access to the host. Workflow selects labels, not runner name. A legacy or reserve runner without `ci-primary` does not satisfy a job that requires this label and should not be presented as the correct server. Always refer to API, as state, capacity and failover change without changing this skill.

If the account has administrative permission, please refer to the state without revealing credentials:

```json
["api", "repos/owner/repo/actions/runners", "--jq", ".runners[] | {name,status,busy,labels:[.labels[].name]}"]
```

Cross job labels with labels returned by API:

- `online` and `busy=true` means that the correct runner is healthy and running another job; follow the queue without asking for server restoration;
- `online` and free, but a job stays in line, requires `runs-on` conference, runner scope and workflow concurrency;
- `offline` only blocks the job when this runner is the only one that satisfies all required labels;
- an offline backup runner without `ci-primary` does not explain the failure of a primary job;
- a job that ran and ended with failure requires reading the logs; this does not prove that the server is offline.

Do not offer “approve without check” as an automatic solution for unavailability of the runner. If the check is mandatory, preserve it. When primary is temporarily offline, record the operational failure with available evidence, monitor its recovery at moderate intervals, and rerun only failed jobs as soon as there is online compatible runner. Escalate to the operator only when API proves persistent absence of compatible capacity or when it is necessary to change hosts, registration or labels; this is an operational action, not a user product decision.

The development/review agent should not restart hosts, change labels, register runner or use administrative access only to unlock a PR. When there is infrastructure failure, provide the operator with: repository, workflow, run/job, platform, required labels, observed status, time and link. Never include registration token, password, private address or Vault content.

## Local CI before merge

When the repository provides `scripts/ci-local.sh`, run it in clean worktree before completing. Do not inject GitHub credentials into the shell. The shell executes local validation; `github_cli` consults and updates GitHub within its own credential limit. If the repository requires a commit status, publish it by API only after the local command has ended successfully and according to the process documented in the repository itself.

Summarize to the human the result in direct language: what failed, proven cause, relationship with PR, action taken and current state. Do not pour complete logs, metadata or commands into the conversation.
