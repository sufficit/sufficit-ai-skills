# Blazor rendering

Apply this guidance to Blazor interfaces; it does not prescribe a component tree
for unrelated stacks or require changes to working UI without evidence.

- Blazor skips child parameter updates when all parameters are recognized
  immutable types (for example string, int, bool, Guid) and their values are
  unchanged. Custom records, lists and RenderFragments do not automatically
  receive this optimization. Keep stable message data stable across updates.
- For complex parameters, use `ShouldRender` with explicit change detection when
  a costly subtree is unchanged. Include all visible inputs: text, status,
  locale, theme when relevant, selection, expiry, permissions and interactions.
  `ShouldRender` does not prevent parameter lifecycle work; avoid expensive
  preprocessing there when its inputs are unchanged. Never freeze a message
  forever merely because its streaming finished.
- `CascadingValue IsFixed="true"` avoids change subscriptions only for a cascaded
  value that remains invariant. Do not mark changing chat, theme or locale state
  fixed. `@key` controls component identity and is not a rendering suppression flag.
- Route updates to the smallest meaningful component. A new token should not
  make completed messages, the directory and composer repeat expensive work.
  Use component boundaries proportionate to visible items, and virtualize or
  page large history instead of creating thousands of active components.
- `StateHasChanged` already coalesces requests while a render is pending.
  External streaming/C# events still require notification on the rendering
  synchronization context. Avoid redundant notifications and fire-and-forget
  queues that outpace the renderer. A render/diff is not necessarily a DOM edit.
- Prefer snapshot initialization followed by deltas over retransmitting and
  deserializing unchanged history. Preserve unchanged object/string references
  where caches depend on identity; handle resynchronization, ordering and gaps.
- Rate limiting high-frequency events can be appropriate after measurement;
  distinguish event-driven coalescing from a polling timer. Do not impose an
  arbitrary 100 ms render cadence before checking the mechanisms above.
- Validate with render counts and transport/allocation measurements as well as
  observable correctness: changed messages update, unchanged messages skip,
  locale/expiry/actions remain current, reconnect retains history and no delta
  or final/error/approval state is lost.

Primary sources (check the target framework version when APIs differ):
- [Rendering performance](https://learn.microsoft.com/en-us/aspnet/core/blazor/performance/rendering?view=aspnetcore-10.0).
- [Component rendering](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/rendering?view=aspnetcore-10.0).
- [ChangeDetection.cs, .NET 10](https://github.com/dotnet/aspnetcore/blob/v10.0.0/src/Components/Components/src/ChangeDetection.cs).
