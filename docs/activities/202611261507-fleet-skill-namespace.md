# Fleet skill namespace

Fleet-specific packages live under `skills/sufficit/fleet/`. The
[skill index](../../catalog/SKILLS.md#sufficitfleet) lists them as a group.
Future packages whose use is specific to Fleet belong in the same namespace.

- [Agent scenarios](../../skills/sufficit/fleet/sufficit-fleet-agent-scenarios/SKILL.md)
- [Agent training](../../skills/sufficit/fleet/sufficit-fleet-agent-training/SKILL.md)

Both packages keep their existing skill IDs and version `1.0.0`. Their release
metadata, catalog paths and package digests reflect the move. The self-training
activity in `sufficit-services-run` links to the new training package path.

Package validation covered 215 entries. The generated index, catalog versions,
Markdown hierarchy and all 70 Python tests passed. Genius distribution uses a
separate catalog synchronization.
