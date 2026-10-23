---
name: dotnet-csharp
description: "Change C#/.NET code (ASP.NET Core, Blazor/Razor, xUnit/bUnit, NuGet) so it builds and passes CI the first time — build every project that references what you touched, keep red tests compilable, run the repository's own gates, align package versions, follow current library APIs and read CI logs from the first error. Use for any edit to .cs, .razor, .csproj, .props or test projects in a .NET repository, and when a .NET CI job failed."
metadata:
  version: "1.0.0"
  author: "Sufficit"
---

# C# and .NET changes that pass CI

Most failed .NET pushes are not hard problems. They are the same few mistakes, repeated: a test project that was never built, a gate script that was never run, a package version that was never aligned. The rules below remove them. [references/ci-failures.md](references/ci-failures.md) maps each error code seen in CI to its cause and fix.

## Before you push: the loop

Run this loop on the exact tree you will push. "It compiles in my head" is not a check.

1. **Restore and build every affected project in Release.** Not just the one you edited: every project that references it, and above all every **test project**. CI builds with `-c Release` and treats warnings as errors in several repos; do the same.
   - Find what references a project: `grep -rl --include=*.csproj "<ProjectName>.csproj" .`
   - Prefer building the test project; it pulls in what it references: `dotnet build tests/<Tests>.csproj -c Release`.
   - Heads that need a platform workload you do not have (Windows desktop, MAUI/Android/iOS) cannot be built on Linux. Build everything else, and say in the PR which heads you could not build.
2. **Run the tests you touched,** then the tests near your change: `dotnet test <Tests>.csproj -c Release --no-build --filter "FullyQualifiedName~<Class>"`. Run the full assembly too when the time budget allows.
3. **Run the repository's gates locally.** Open `.github/workflows/*.yml` and run every non-build step that can fail: file-size guards, format/lint, markdown coverage, license or manifest checks. Example: `bash scripts/check-file-size.sh` (C# files over 400 lines fail).
4. **Rebase on the current default branch, then repeat step 1.** Main moves; package bumps and API renames land there. A branch that was green yesterday can fail today without any edit of yours.
5. **Push only when 1–4 are clean.** If something could not be checked, write in the PR exactly what and why.

## Red tests must still compile

A test-first commit ("add failing tests that reproduce #N") is useful only if the test assembly **compiles** and the new tests fail on an assertion. A compile error breaks the whole assembly: every OS job fails, no test runs and the PR gives zero signal.

- Build the test project before committing a red test.
- Types from another namespace need their `using`. The compiler error is `CS0246 … could not be found (are you missing a using directive…)`. Find the namespace with `grep -rn "record <Type>\|class <Type>\|interface <Type>" src/`.
- If the production type does not exist yet, create a minimal stub (an empty method that throws or returns a default) so the test compiles and fails at runtime.

## Packages (NuGet)

- **Never downgrade a transitive dependency.** `NU1605 Detected package downgrade: X from A to B` means a direct reference pins `X` lower than a package you depend on needs. Raise the direct reference to at least `A`, in **every** project that pins it, in the same commit as the bump that caused it.
- Bump related packages together: one `Microsoft.AspNetCore.*` / `Microsoft.Extensions.*` version across the solution.
- Do not add a package for something the BCL or an existing dependency already does.
- After any version change, restore and build all affected projects again (step 1).

## Libraries change: read the current API

Internal packages (for example `Sufficit.Blazor.UI`) release often and sometimes rename things. When a component or method call stops compiling right after a restore, the library changed; your code did not suddenly become wrong.

- Read the API in the version you actually restore (the package's XML docs, its source repository at that tag, or the decompiled type) instead of guessing casts.
- Razor symptom: errors `CS1662`, `CS0019 Operator '??' cannot be applied to operands of type 'EventArgs'…` and `CS0266` on a `ValueChanged="value => …"` lambda mean the component's generic type parameter was not bound. Example: SUI renamed `T="string"` to `TValue="string"`. Fix the attribute; never cast around it.
- If main already adopted the new version, rebase; do not fix it a second time in your branch.

## Code that passes analyzers

- **Platform APIs (`CA1416`).** Calls that only exist on one OS (`Marshal.ReleaseComObject`, registry, WinRT) must be guarded with `if (OperatingSystem.IsWindows())`, or the containing type must be marked `[SupportedOSPlatform("windows")]`. Do not add new `CA1416` warnings, even in a Windows-only head.
- **Async iterators (`CS8425`).** An `async IAsyncEnumerable<T>` method with a `CancellationToken` parameter needs `[EnumeratorCancellation]` on that parameter.
- **Nullable.** Respect the annotations; do not silence them with `!` unless you can say why the value cannot be null at that line.
- **No `async void`** except event handlers; pass the `CancellationToken` through.
- **Files stay small.** When a file approaches the repository's line limit, split it by responsibility (a new class, or `partial` files named `<Type>.<Concern>.cs`), not by moving arbitrary code.

## Reading a failed CI run

1. List failed jobs: `gh run view <run-id> --json jobs -q '.jobs[]|select(.conclusion=="failure")|"\(.databaseId) \(.name)"'`.
2. Get the log of each failed job: `gh api repos/<owner>/<repo>/actions/jobs/<job-id>/logs` (more reliable than `gh run view --log-failed`).
3. Search for `error CS|error NU|error MSB|error RZ|::error|\[FAIL\]` and fix the **first** error first. Later errors are often cascades.
4. The same compile error repeated in the Linux, Windows and macOS jobs is one error.
5. Classify before changing code:
   - **Compile, gate or package errors** are yours: fix them.
   - **A test failing in code you did not touch.** Re-run it locally with `--filter`. If it passes and is unrelated to your diff, report it as flaky (test name, run link). Never weaken or skip it to make your PR green.
   - **Infrastructure errors** (`buildx … connection reset by peer`, registry or `mcr.microsoft.com` resolution failures, `401` from external APIs, `The operation was canceled` on timeout) are not code problems. Re-run the job; do not commit "fixes" for them.

## Delivery

In the PR, state what you built and ran (commands and result), what you could not build, and any test you believe is flaky. A reviewer should be able to trust that the branch compiles everywhere you said it does.
