# Composition and contracts

## From reference to component

Start with the action that the user needs to complete. Describe data, state, main/secondary actions, error states and responsive limit. Find the project equivalent before creating another button, selector, dialog or icon system.

An example gallery can serve as a reference for a flow without providing a ready-to-production implementation. Confirm accessible labels, focus, keyboard, sorting, validation, filters and actions that the example only draws. Do not invent testimonials, metrics or actual data to fill the layout; identify fixtures as a demonstration.

For operational lists, the toolbar needs to change the results and maintain consistent counting. In forms, error should be associated with the field, data should survive recoverable failure and repeated submission should be treated. In dangerous configuration, the consequence must be understandable before action and follow the confirmations already provided for in the product.

## Where the code belongs

| Signal | Likely Layer |
| --- | --- |
| Layout of a business flow or rule | Application/feature |
| Error in the contract of a reusable primitive in consumers | Shared Library |
| Value representing identity, density or cross-cutting appearance | Theme/tokens |
| Example teaching API and library variants | Catalogue/showcase |

It's not an obligation to create all these layers. Extraction is justified by stable contract or demonstrable reuse. A shared component receives data and events; services, domain entities and specific permissions remain in the consumer.

## States as a contract

Select the states that exist for the component: initial, hover, focus, selected, disabled, loading, empty, error, success, long content. Check transition and result, not only class CSS.

Size variants need rendered difference consistent with API: height, width, padding, text and icon. Do not fix global measures for all controls. Check if an icon/square override cancels the requested size and if examples are actually passing the parameter. Preserve accessibility when the visual variant is small.

## Evolution of the design system

Use four coverage perspectives according to task: product language, visual foundations, component behavior and maintenance. For each relevant gap record evidence, impact and decision; use “does not apply” with reason when necessary, without fictitious percentages of maturity.

To change public API, document behavior, default values, compatibility and migration when there is breakage. Update an executable example and meaningful regression test if change affects consumers. Identify version/pin consumed and delivery path: fixing the library repository does not automatically update an already published product.

Keep documentation close to the code and with existing ownership and conventions. Measure adoption or regressions with real data when that is the goal; do not require new governance process in each PR.
