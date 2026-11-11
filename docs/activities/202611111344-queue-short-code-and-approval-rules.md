# Queue short-code and approval-rule clarification

sufficit-telephony-dialplan0.4.2 corrects two diagnostic conclusions:

- A prefixed numeric queue projection does not require configuring the device
  with full digits. The FreePBX6XXXpattern may normalize the authenticated
  customer's prefix and transfer to the full number. Recognized short pattern,
  normalized destination and final reachability must be checked separately.
  Never invent an intermediate five-digit form by stripping zeros.
- Read-only business SQL does not prohibit preparing a maintained dialplan fix.
  API business writes, source-controlled configuration publication and explicit
  operational approval for disruptive/shared reloads are separate boundaries.
  No ad-hoc generated-file/database edits are authorized by a reload approval.

Updated reference, package/card/catalog versions and digest. All185public skill
packages validated. Support's existing private reference is updated separately,
with prior DID/QuePasa instructions and four bindings preserved. No production
PBX mutation, reload or call is part of this training correction.

The first native retest corrected permission wording but still chose the offline
PJSIP record as caller context. Added explicit dual-driver registration comparison:
the registered technology defines the candidate context; if both are registered,
execution evidence is required. An offline alternate endpoint or memory record
cannot replace the active SIP leg. Repeated the focused native probe after this
actual training change rather than declaring wording alone sufficient.
