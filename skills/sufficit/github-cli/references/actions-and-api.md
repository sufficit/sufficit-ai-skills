# Actions, releases and API

## Actions and workflows

Use `run list` to discover executions and `run view` to identify the job and step that failed. Search logs only when needed; summarize the relevant cause and excerpt. Never ask the user to copy the log while the connected account can get it from GitHub.

```json
["run", "list", "--repo", "owner/repo", "--limit", "10", "--json", "databaseId,workflowName,status,conclusion,headBranch,headSha,url,createdAt"]
```

```json
["run", "view", "123456", "--repo", "owner/repo", "--json", "status,conclusion,jobs,url"]
```

```json
["run", "view", "123456", "--repo", "owner/repo", "--log-failed"]
```

If the summary does not bring the error, list the jobs to get `databaseId` and see the job:

```json
["run", "view", "123456", "--repo", "owner/repo", "--json", "jobs", "--jq", ".jobs[] | {id: .databaseId, name, status, conclusion, steps}"]
```

```json
["run", "view", "123456", "--repo", "owner/repo", "--job", "987654", "--log-failed"]
```

When workflow posts results, find and download only the relevant artifact with `run download`. If logs remain unavailable, please inform which call failed and which permission is missing; requesting a manual copy is the last resort.

Before `run rerun`, check if the failure seems transient or if the code/configuration has already changed. Don't repeat it indefinitely. Dispatches through `workflow run` and cancellations are real changes and need to be within the current request.

## REST and GraphQL

Use `gh api` when a high-level subcommand does not offer the fields or operation. See the correct endpoint and pass parameters as separate items. For paginated REST reads, use `--paginate`; match with `--slurp` only when you need a single collection.

```json
["api", "repos/owner/repo/issues/480/comments", "--paginate", "--jq", ".[] | {id,body,user:.user.login,created_at}"]
```

For complex payload, create JSON in file and use `--input`. Do not place multiline content in a shell expression and do not include Authorization header: the host already authenticates `gh`.

Use GraphQL for relationships that would require many REST calls. Limit fields and pagination; a wide query can generate a response too large for the session.

## Releases and Actions artifacts

Discover releases before downloading and use `release download` with explicit directory. For workflow artifacts, use `run download`. Do not automatically run downloaded binaries; inspect type, origin, and integrity according to task.

```json
["release", "download", "v1.2.3", "--repo", "owner/repo", "--dir", "/destination", "--pattern", "*.zip"]
```

```json
["run", "download", "123456", "--repo", "owner/repo", "--dir", "/destination"]
```
