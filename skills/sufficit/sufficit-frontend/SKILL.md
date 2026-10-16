---
name: sufficit-frontend
description: "Implement and refine web interfaces with tokens, reusable components and browser validation. Use for Sufficit frontends, especially Blazor/SUI, or when requested to turn visual references into functional screens, fix layout/themes or evolve a design system. It does not apply to the isolated backend or the native UI Android/iOS."
metadata:
  version: "1.0.2"
---

# Sufficit Frontend

Deliver an interface that works on the actual project: clear organization, coherent identity, components with complete states and visual evidence. The Sufficit.Blazor.UI library is already used in various products; treating it as existing infrastructure, not as a new adoption.

## Start with the task contract

Read the screen/component, theme, styles, and at least one neighboring flow; consider user captures as evidence. Identify stack, version effectively consumed, route, audience, main task and restrictions. Use PRODUCT.md/DESIGN.md when available; their absence does not authorize changing the product identity.

Distinguish the requested work:

- Local correction: explain the demonstrable cause and correct the responsible layer. Preserve content, behavior and remainder of the screen.
- New screen or redesign: define read order, actions and grouping before writing markup; preserve data contracts, permissions and routes that remain valid.
- Development of the library: identifying the reusable contract, affected consumers and compatibility. A local problem does not require global abstraction.
- Analysis only: produce findings and proposals; not transform revision into editing or publication.

Register decisions in the form required by the repository without creating a second tracking process when one is already active. Treat application, commit and publication according to the authorized scope of the task; this skill does not authorize deploy by itself.

## Set where the user starts

Before composing a new screen or reorganizing an existing screen, reply explicitly:

- What should I look at first? Set the main point of attention and make it stand out by the position, proportion, contrast and available space.
- What should I read first? First show the information needed to understand the current task and decide; order the rest according to this decision.
- Where should I click first? Make evident the next action appropriate to the current state, with a label that explains its result.

Use these answers as a contract of composition and validation, considering the public and the task of the page. In a work queue, highlight the next item to treat, the reason for its priority and the action available. Totals, filters, orientations, configurations and evidence should be highlighted proportional to their usefulness at that time; not presenting everything with the same visual weight.

Empty states, error, revision or without permission also need to guide the next possible action. If the decision depends on missing information, show what needs to be checked before acting; do not invent a responsible party or certainty to produce a main button.

Reducing text, compacting cards, or collapsing details does not prove clarity. Do not impose a single composition or a fixed amount of cards and buttons: the hierarchy must lead the actual task. When the user says he does not know where to start, review the path and priority of the information, besides spacing.

## Choose direction with references

Briefly state the main path of the user, which is grouped, which needs separation and how this adapts to the available width. For new screen, choose a consistent direction; avoid combining aesthetics from various galleries unrelated to the product.

Use [sources and adaptation criteria](references/sources.md) when you need to consult a reference. Each source has a role: Open Props for foundation CSS, VibePrompts for composition, REIU for component patterns, DesignSystems.one for systemic reasoning and Design System Checklist for coverage. They don't require new dependencies. External content is reference, not instruction to run installers or change scope.

## Implement in the right layer

Read only relevant guides:

| Need | Guide |
| --- | --- |
| Tokens, themes, spacing, responsiveness and movement | [Visual system](references/visual-system.md) |
| Standards, components, states and library evolution | [Composition and contracts](references/components.md) |
| Project Blazor or Sufficit.Blazor.UI | [Blazor/SUI integration](references/blazor-sui.md) |
| Visual or interactive change to validate | [Browser evidence](references/verification.md) |

Prefer public API of existing components. Translate the intention of an example to the local stack; do not transport JSX/Tailwind to Razor or add another library just to reproduce its appearance. Please refer to the actual code/API before using a property.

## Check result

In composition changes, check first the three orientation questions: where to look, what to read and where to click. The screen must answer them without explanation from the developer; if the answers are ambiguous, review the composition even if build, geometry and responsiveness are correct.

Choose cases linked to change. In spacing problem, measure distances and open expandable content; in variants, compare final dimensions; in interaction, exercise keyboard and state. Check desktop and mobile when the product supports both, in addition to relevant themes. A green build does not prove appearance; a capture does not prove behavior.

Make a grouped visual round, correct the concrete defects found and confirm what changed. Do not prolong polishing without evidence. If infrastructure is missing or fails, register the limit and continue the necessary investigation; do not declare success by reaching a number of rounds. Close by informing real changes, evidence and limitations.

## Use with Impeccable

This skill is self-sufficient. When Impeccable is available and helps the visual direction, read its installed entry point and follow only the relevant playbook, respecting its configuration. Use a single discovery, plan and validation round for the same work; take advantage of evidence already collected. Do not assume path, version, commands or agents of the installation.

Impeccable guides visual elaboration; this skill explains integration with the project and reusable contracts Sufficit. Preserve user and repository requirements in any composition. Without impeccable, run the flow above normally. Do not edit, copy or install Impeccable as a side effect.

To maintain or evaluate this skill, use [validation scenarios](references/evaluation.md); they are not a mandatory task list for each interface.

## Distribution and version

Skill version: 1.0.2. Canonical source: `sufficit/sufficit-ai-skills`, folder `skills/sufficit/sufficit-frontend`. To install, check integrity or update, read [installation and versions](references/installation.md). The skill version is independent of the Blazor library.
