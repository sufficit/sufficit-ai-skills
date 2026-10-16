# Blazor and Sufficit.Blazor.UI

Confirm names, parameters and commands in the current checkout; this guide describes decisions, does not freeze a version of SUI.

## Before changing

- Inspect `.csproj`, build files and lock/pins: does the consumer use NuGet, project reference or fixed checkout? Identify effective version.
- Read Razor component, code-behind, theme, source CSS and generated files. Discover loading order, CSS isolation, theme root selector and associated JS modules.
- Browse the standard component in the catalog and code. A parallel `<select>` does not automatically reproduce the API, the theme and the library selector states.

## Solve at responsible level

If only a feature mixes classes with different meanings, correct local composition. If a public property does not have its effect on multiple consumers, correct the library, its examples and regression test, within the authorized scope. Do not mask a global size defect with more specific CSS in each application.

Use available SUI components and tokens. If an example uses React/Tailwind, port the behavior and structure; do not introduce these dependencies into Blazor. Avoid selectors that depend on internal details when there is public customization API. In CSS isolation, check where the scope attribute actually appears before resorting to `::deep`.

## Rendering and integration

Preserve binding, callbacks, validation, status and disposal of resources. Do not use DOM manipulation to replace the state Blazor controls. JS interop must respect the availability of DOM and the actual rendering mode; a prerendered component does not prove that its interaction has been initiated.

In selection/tabs/dialogs, exercise focus and keyboard, do not just click. For navigation, keep deep URLs and context parameters required. In Blazor Server, distinguish visual defects from a disconnected circuit or incompatible JS module.

## Build and delivery

Change source of CSS and regenerate bundles by repository command if any; check the generated result. Do not declare conclusion after changing only one copy that the app does not load. Run build in relevant configuration, library checks and affected consumer as per contract.

If delivery includes customer update, align package/pin and validate the artifact with this dependency. If not, please inform the consumer that the improvement has not yet reached the consumer. For authorized publication, check CSS/JS cache, path base, static web assets and module compatibility with open sessions. Use the project fingerprint/version mechanism when available, without requiring manual query strings on all assets.

Service restart, package update and deploy are distinct actions; record only those effectively performed. Use fixture for actions testing that would change real resources and declare this limitation.
