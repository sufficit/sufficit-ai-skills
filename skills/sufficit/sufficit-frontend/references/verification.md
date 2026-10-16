# Evidence in the browser

Choose the matrix for risk and for what has changed. For a common layout correction: reported state, wide and narrow width, affected theme and a neighboring state that shares styles. For shared primitive: include variants and representative consumer. Do not confuse this with obligation to audit the entire product.

## Ready

Use the available browser/tool and project commands. Wait for interactive rendering, relevant fonts and transitions before measuring. Exercise realistic data without performing unnecessary real mutations. If you use fixture, make it clear what it does not validate.

Reproduce the reported problem before correction when possible; store comparable evidence. For spacing, open the panels; for dropdown, open the menu and navigate by keyboard; for sizes, render the variants side by side. Do not satisfy with closed-state screenshot.

## Check

- Task orientation: evaluate the capture and flow without narration of the developer. Identify where to look first, what to read to decide and what action to take. Check whether the priority and reason for the items are understandable with realistic data, including on the tablet. If everything disputes attention or the user needs to look where to start, review the hierarchy; correct alignment and collapsed details are not enough.
- Geometry: real distance between siblings, padding, size of controls/icons, alignment and overflow. Read the computed value and winning rule when there is divergence.
- Use: visible focus, tab order, accessible name, disabled controls, submission and recovery in the relevant states.
- Adaptation: long texts, zoom and representative breakpoint when they reach change. Deliberate local scrolling is different from accidental overflow of the page.
- Appearance: hierarchy, theme, contrast and states; automatic accessibility analysis does not prove complete compliance or replace the visual review.
- Delivery: matching CSS and component version in the tested artifact and destination, if publication is part of the task. Without authenticated access, health and assets do not prove authenticated flow.

Do not introduce universal thresholds from a screen. For contrasts, target sizes and formal compliance, apply the standard required by the project and consult your current normative source when necessary.

## Reusable measurement

[scripts/measure-layout.mjs](../scripts/measure-layout.mjs) is a function for evaluation within an already open page. It does not start a browser, navigate, modify the DOM, or decide whether a result passes. Returns values of elements found and vertical distance between consecutive selectors; compare these values with the screen contract.

Example with Playwright already installed in the project:

```js
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const moduleUrl = pathToFileURL(path.join(skillDir, 'scripts/measure-layout.mjs'));
const { default: measureLayout } = await import(moduleUrl.href);
const evidence = await page.evaluate(measureLayout, {
  selectors: ['.settings-control', '.settings-warning', '.settings-next-task']
});
```

`skillDir` and `page` are provided by the existing harness; do not install a second harness only for this function. Missing/invalid selectors and contents without visible box appear explicitly. A negative distance can mean overlapping or layout in columns; interpreting in context. For lists, the helper uses the first element and records the count: ambiguous selectors require refining.

Save screenshots, measures and result of checks at the project convention. Automated regression should detect the actual defect (e.g. final height unaffected by the parameter), do not mirror class names or accept any existing capture file.
