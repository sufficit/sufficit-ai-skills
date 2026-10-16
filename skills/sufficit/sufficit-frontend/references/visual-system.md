# Visual system applied

## Tokens and themes

Inventory the values actually loaded before creating tokens. Separate, when useful to the system, primitive value (color/measure), semantic role (surface/text/action) and specific component need. Do not insert three layers of aliases to solve a single gap.

The same suffix does not mean the same measure between libraries: `space-5` can be 20px on one system and 24px on another. Check computed value, theme scale and consumer. Map by role and desired measure.

Open Props is a foundation option, not a mandatory theme. If adopted, import only the useful sets by the project pipeline. Normalization and element styles can affect existing controls: check the cascade before including them. Do not add a global reset to a local fix. Validate resource support as a custom media in the built/target browsers; a CSS variable does not replace a media query condition.

Themes share structure, but may need different background/text/edge/focus pairs. Use existing roles also in hover, selection, warnings and overlays; do not invert colors blindly. Do not copy a gallery palette because it looks similar to the brand.

## Spacing and composition

Distinguishing three relationships: within a control; items of the same subject; separation between subjects. Choose intervals from the local scale. Space before a new subtitle must communicate the subject change, not attach it to the last previous line.

Use `gap` when the container defines the relationship between siblings; padding delimits internal area and margin separates independent blocks. Observe margin collapse, `min-width`, alignment and break. Classes for a simple stack should not accidentally inherit the contract of an accordion, grid or card.

Maintaining proper density to the task: operating tools can be compact without stacking controls; presentation pages can have more space without hiding the action. Do not impose the same card layout on all subjects. Typography and proximity should explain the organization before decoration.

## Adaptation

Choose breakpoints for project content and conventions. In grids, allow the column to fit in the available width; in flex, check minimum child size. Long technical texts, translations and zoom may require deliberate local breaking or scrolling.

When turning table into compact list, save required fields, actions, filters and pagination. Do not hide a function to make the layout fit. A control should remain keyboard operable and touch; the clickable area can surpass the visual size of the icon. Visual scale and target size are distinct contracts.

## Movement and performance

Use motion to explain state change, content entry or spatial relationship. Prefer project duration and easing by avoiding animating all blocks by default. `prefers-reduced-motion` should leave content immediately usable and preserve functional feedback.

Before using continuous animation, blur, extensive shadows or layout transitions, evaluate painting/composition cost on representative device. Save space for media/fonts and loading states to avoid jumping. Measure before/after when the task involves performance; bundle and rendering limits come from the project, not from a universal number of this skill.
