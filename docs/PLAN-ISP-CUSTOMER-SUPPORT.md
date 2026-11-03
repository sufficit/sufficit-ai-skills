# ISP customer support skill

Objective: turn observed support scenarios into an anonymized, reusable ISP
customer-service manual and skill; deliver on main and remove this task's local
recording/transcription artifacts after preserving the generalized guidance.

1. [completed] Author skill and scenario manual; register package in catalog.
2. [completed] Validate package, references, catalog integrity and anonymization.
3. [in_progress] Record delivery, commit and push only reviewed task files to main.
4. [pending] Delete the exact local artifact directory and verify absence.

Acceptance: practical handling of repeat contacts, router reset vs restart,
missed/contested visits, access restrictions, installation feasibility, invoices,
channel handoffs and closure; no customer data or invented provider commitments.
Package instructions in English per repository convention; responses adapt to
customer language. No production ticket or billing mutations.

Validation: scripts/validate.py; skill-creator quick_validate.py; repository tests;
review scenario decisions, links and git diff. Cleanup is limited to the local
call-review artifact directory created in this session.

Validation: 179 packages valid; quick_validate passed; index and Markdown
coverage passed; 38 repository tests passed. Reviewed six training scenarios
against the manual; no live actions or independent agent evaluation performed.
