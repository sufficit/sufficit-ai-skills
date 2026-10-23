# .NET CI failures: cause and fix

This catalog was built from 40 failed CI runs of `sufficit/sufficit-ai-genius` (October 2026). Each counted error repeats once per OS job (Linux, Windows, macOS). Add new cases when a failure repeats.

## Compile and package errors (yours to fix)

| Error | Typical cause | Fix |
| --- | --- | --- |
| `NU1605 Detected package downgrade: Microsoft.AspNetCore.Components.Web from 10.0.13 to 10.0.12` | A newer internal package (e.g. `Sufficit.Blazor.UI`) needs a higher framework package than the version a project pins directly. | Raise the direct reference in every project that pins it, in the same commit as the bump. Never lower the package that needs it. |
| `CS1662`, `CS0019 Operator '??' cannot be applied to operands of type 'EventArgs' and 'string'`, `CS0266 Cannot implicitly convert type 'object' to 'string'` in a `.razor` lambda | A component's generic parameter was renamed in the library (SUI `T` → `TValue`); the old attribute no longer binds the type. | Use the current parameter name from the restored package; rebase if main already adopted it. |
| `CS0029`, `CS1503 cannot convert from 'X' to 'Y'` after a restore | The library changed a signature. | Read the API in the restored version; adapt the call. Do not cast blindly. |
| `CS0246 The type or namespace name 'X' could not be found` in a test project | A red test referencing a type in another namespace without its `using`; the test project was never built before the push. | Add the `using`; build the test project before committing. |
| `File-size guard failed` / `409 lines > 400 limit` | A C# file grew past the repository limit. | Split by responsibility (`partial` files or a new class); run `scripts/check-file-size.sh` before pushing. |

## Warnings to keep at zero

| Warning | Fix |
| --- | --- |
| `CA1416 This call site is reachable on all platforms. 'X' is only supported on: 'windows'` | Guard with `OperatingSystem.IsWindows()` or mark the type `[SupportedOSPlatform("windows")]`. |
| `CS8425 Async-iterator … has one or more parameters of type 'CancellationToken' but none of them is decorated with the 'EnumeratorCancellation' attribute` | Add `[EnumeratorCancellation]` (namespace `System.Runtime.CompilerServices`) to the token parameter. |

## Not code problems (re-run, do not commit a fix)

- `buildx failed … read tcp … connection reset by peer`
- `failed to resolve source metadata for mcr.microsoft.com/…`
- `Error response from daemon: … unable to decode token response`
- `Failed to query builds for processing state. (401)` (external service credential, not your diff)
- `The operation was canceled.` after a job timeout

## Single test failures

These appeared once each, in tests unrelated to the diff: `ExternalNavigationGuardTests`, `ToolCallingTests`, `WorkspaceEndpointTests`, `SessionDirectoryEventsTests`, `LoopbackFileEndpointTests`, `ChatComponentsTests`. Re-run the test with `--filter`. If it passes and is unrelated to your change, report it as flaky with the run link.
