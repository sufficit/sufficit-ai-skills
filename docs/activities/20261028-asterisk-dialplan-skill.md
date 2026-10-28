# Sufficit Asterisk dialplan skill

Created the canonical `sufficit-asterisk-dialplan` 1.0.0 package under
`skills/asterisk/dialplan`, registered its catalog entry and content digest, and regenerated
the skill index. Updated the existing local Codex copy to the same package bytes.

The skill requires English authored instructions, comments, diagnostics and change
descriptions; preserves protocol literals, existing deployed identifiers, historical
entries and the exact ownership notice. It defines the two latest real header
changes, context comments below declarations, one literal TAB for exten and two
for same. It distinguishes house style from Asterisk syntax and includes official
references and proportionate validation guidance.

[Execution plan](../PLAN-ASTERISK-DIALPLAN-SKILL.md).

Initial validation: all 174 package digests/provenance checks and skill-creator's
quick validation passed. Local package digest equals the canonical package digest.
Repository index, Markdown coverage and unit test results are recorded below.

No commit, push, remote publication or production dialplan change. Existing edits
in other skill packages and manifest entries were preserved.

Final validation: index current; all Markdown reachable; 21 unit tests passed;
`git diff --check` passed. No remaining implementation steps.

User-requested relocation: canonical package now lives in `skills/asterisk/dialplan`;
skill name and version remain unchanged. Catalog URLs, release path and digest updated.

Generalized the skill as `asterisk-dialplan`: neutral title, examples and instructions;
ownership notices, paths, timezone and call-path policy now follow each repository.
English, TAB layout and two-entry change history remain the defaults. Author/license
and hosting provenance remain accurate. Local installation renamed to match.

Generalization checks passed: package validation (174), current index, Markdown
coverage, skill quick validation and diff whitespace check. No publication.

Added the user-requested blank line before instruction-specific comment blocks.
Applied it to the selected directcall comment without changing executable lines;
updated package digests and synchronized the local skill.
