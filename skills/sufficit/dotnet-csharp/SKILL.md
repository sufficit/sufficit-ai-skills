---
name: dotnet-csharp
description: "Change C#/.NET code (ASP.NET Core, Blazor/Razor, xUnit/bUnit, NuGet) so it builds and passes CI the first time — build every project that references what you touched, keep red tests compilable, run the repository's own gates, align package versions, follow current library APIs and read CI logs from the first error. Use for any edit to .cs, .razor, .csproj, .props or test projects in a .NET repository, and when a .NET CI job failed."
metadata:
  version: "1.0.1"
  author: "Sufficit"
---

# C# and .NET changes that pass CI

Most failed .NET pushes repeat a few mistakes: a test project never built, a gate never run, a package version never aligned. [references/ci-failures.md](references/ci-failures.md) maps each error code seen in CI to its cause and fix.

## Before every push

Run this loop on the exact tree you will push:

1. **Build in Release every project that references what you touched, above all the test projects.** Find them with `grep -rl --include=*.csproj "<Project>.csproj" .`, then run `dotnet build <Tests>.csproj -c Release`. Heads that need a workload you lack (Windows desktop, MAUI) cannot be built on Linux; build everything else and say in the PR which heads you skipped.
2. **Run the tests near the change:** `dotnet test <Tests>.csproj -c Release --no-build --filter "FullyQualifiedName~<Class>"`.
3. **Run the repository's gates.** Read `.github/workflows/*.yml` and run each non-build step that can fail, such as `bash scripts/check-file-size.sh` (C# files over 400 lines fail), format, or markdown coverage.
4. **Rebase on the current default branch and repeat step 1.** Package bumps and API renames land on main; a branch that was green yesterday can fail today.
5. Push only when steps 1–4 are clean. In the PR, list what you built and ran, and what you could not check.

## Red tests must compile

A test-first commit is useful only if the assembly **compiles** and the new tests fail on an assertion. A compile error breaks the whole assembly in every OS job, and no test runs.

- Build the test project before committing a red test.
- `CS0246 … could not be found` usually means a missing `using`. Find the namespace with `grep -rn "record <Type>\|class <Type>" src/`.
- If the production type does not exist yet, add a minimal stub so the test compiles and fails at runtime.

## Packages

- `NU1605 Detected package downgrade: X from A to B`: raise the direct reference to at least `A` in **every** project that pins it, in the same commit as the bump. Never downgrade.
- Keep one version of `Microsoft.AspNetCore.*` / `Microsoft.Extensions.*` across the solution.

## Libraries change: read the current API

When code stops compiling right after a restore, the library changed. Read its API in the restored version; do not guess casts.

- Razor: `CS1662`, or `CS0019 Operator '??' cannot be applied to operands of type 'EventArgs'`, or `CS0266` on a `ValueChanged="value => …"` lambda means the component's generic parameter was not bound (SUI renamed `T=` to `TValue=`). Fix the attribute.
- If main already adopted the new version, rebase instead of fixing it again.

## Analyzers

- `CA1416` (Windows-only API): guard with `OperatingSystem.IsWindows()` or mark the type `[SupportedOSPlatform("windows")]`.
- `CS8425`: add `[EnumeratorCancellation]` to the `CancellationToken` of an `async IAsyncEnumerable<T>`.
- Respect nullable annotations; use `!` only when you can say why the value is not null.
- Near the line limit, split by responsibility (new class, or `partial` files `<Type>.<Concern>.cs`).

## A failed CI run

1. Failed jobs: `gh run view <run> --json jobs -q '.jobs[]|select(.conclusion=="failure")|.databaseId'`. Log of each: `gh api repos/<owner>/<repo>/actions/jobs/<job>/logs`.
2. Search for `error CS|error NU|error RZ|::error|\[FAIL\]` and fix the **first** error; later ones are often cascades. The same error in the Linux, Windows and macOS jobs is one error.
3. Classify the failure before changing anything:
   - **Compile, gate and package errors** are yours to fix.
   - **A test failing in code you did not touch.** Re-run it with `--filter`. If it passes and is unrelated to your change, report it as flaky. Never weaken it or skip it.
   - **Infrastructure errors** need a re-run, not a code change. Examples: `buildx … connection reset by peer`, `mcr.microsoft.com` resolution failures, a `401` from an external service, or `The operation was canceled` on a timeout.
