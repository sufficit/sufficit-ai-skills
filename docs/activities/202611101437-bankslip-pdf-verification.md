# Verify boleto PDF before delivery

Updated sufficit-api 1.0.32 to 1.0.33 after a Download response converted the provider HTML page and produced a different, broken-layout PDF. The same boleto already exposed its ready PDF through documentUrl.

The bank-slip reference now distinguishes HTML payment pages from PDF documents, explains the historical Download behavior without assuming every deployment has the repair, and requires opening/rendering the file for visual inspection before claiming delivery readiness. If a viewer is unavailable, report that limitation. A filename, signature or successful save does not establish correct layout, and multiple pages alone do not establish a defect.

Preserve the existing issuance and idempotency key when recovering the document; do not reissue or implicitly enable public access. The document may carry Sufficit branding but comes from the provider PDF pipeline. No customer identifiers or billing details were added to the skill.

Version metadata, release descriptor, catalog version and package digest updated. Package validation (185 skills), index check and version check passed. Markdown coverage passed and all 45 managed installation tests passed. This commit/push updates the source package; Genius activation depends on its catalog synchronization workflow.
