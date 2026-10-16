# Sources and adaptation

References consulted on 2026-09-08. Sufficit's own synthesis and criteria; no package, template or external catalogue is redistributed here. Before importing code, check the artifact license and compatibility of the chosen version. Public examples do not make the whole collection free.

| Source | What to Watch | How to use in this skill |
| --- | --- | --- |
| [Open Props](https://open-props.style/) and [official repository](https://github.com/argyleink/open-props) | Custom properties for space, typography, colors, shadows and motion; adoption by sets | Take advantage of a token base if the project needs to; map semantic roles to the local theme. Check values, not numerical suffix equivalence. |
| [ VibePrompts](https://vibeprompts.dev/) | Interface compositions and examples; [table with toolbar](https://vibeprompts.dev/dashboards/dashboards-data-table-with-toolbar/) includes search, sorting and state without results | Extract task, hierarchy and states. Write the implementation in the project stack and check semantics/keyboard; a preview does not prove accessibility. |
| [REUI: introduction](https://reui.io/docs) and [styles](https://reui.io/docs/styling) | Composition of primitives in examples and blocks; state semantic roles | Check API and infrastructure before adopting. React/shadcn examples are not Blazor components. Open components/examples and materials Pro have different conditions. |
| [DesignSystems.one: foundations](https://www.designsystems.one/foundations) and [spacing](https://www.designsystems.one/foundations/spacing) | Relationships between fundamentals, density and consistent application | Use comparison to justify choices; preserve local scale and identity. The catalogue is an editorial reference, not a compliance standard. |
| [Design System Checklist](https://github.com/ardakaracizmeli/design-system-checklist) | Organisation in language, fundamentals, components and maintenance, available in [src/data](https://github.com/ardakaracizmeli/design-system-checklist/tree/master/src/data) | Select applicable criteria and register evidence. Do not require completing an entire design system to fix a screen. |

## Choose without hoarding dependencies

1. Start from the gap observed in the project; search for a directly related example, not the entire catalog.
2. Register the useful pattern and what you need to change to meet local data, brand, stack and accessibility.
3. Prefer existing code/API. Only adopt dependency when the gain justifies build, weight, maintenance and license.
4. Pin the version approved by the project and test the production artifact. Unversioned links are query references, not CDN instructions for production.

Open Props declares MIT. In the query, the Design System Checklist root did not have explicit license file; README is described as open-source, which alone does not determine redistribution conditions. REUI distinguishes free and paid materials. For VibePrompts and DesignSystems.one, we use links and own analysis, without reproducing their catalogs or assuming a code license.

If a source is unavailable, continue with the local context and declare the limitation of the query. Do not state that the reference was examined if only a search snippet was seen.
