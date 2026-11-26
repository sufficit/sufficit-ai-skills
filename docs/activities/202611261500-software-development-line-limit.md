# Development guidance for file size and unit tests

## Investigation

The project-level line limit and native test integration needed a reusable
policy in the canonical software development skill.

## Changes

Released [software-development 1.2.0](../../skills/sufficit/software-development/SKILL.md).
The skill sets a 400-line default, describes responsibility-based source splits
and bounded exceptions, and places the checks in each language's existing
unit test suite and CI. Both catalog records carry the new package digest.

## Validation and delivery

Package validation, catalog and Markdown checks, the skill validator, and
all 70 repository tests passed. The linked Codex install and the remote
package agreed on version 1.2.0 and content digest.
[Released revision](https://github.com/sufficit/sufficit-ai-skills/commit/78e40ae285069484123efc9fe465abb1c3c00806)
