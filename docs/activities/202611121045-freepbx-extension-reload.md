# Apply FreePBX extension batches

The owner clarified that legacy numeric SIP registration must remain supported alongside GUID-based PJSIP. A read-only production check found four newly created dual-protocol extensions in FreePBX devices/users/SIP records, but no corresponding sections in sip_additional.conf and no loaded chan_sip peers. The API reported both technologies enabled and pending=true. These observations establish a saved-versus-applied gap; they do not identify why generation was skipped.

Updated [provisioning](../../skills/sufficit/sufficit-telephony-extensions/references/provisioning.md#apply-the-freepbx-batch-before-handover), onboarding and the skill entrypoint: after an API-created FreePBX batch, run fwconsole reload once on the owning PBX within the provisioning authorization and server policy, inspect its result and verify each enabled driver independently. Legacy SIP uses the numeric canonical title; PJSIP uses the endpoint GUID without hyphens. Missing SIP peers cannot be dismissed because PJSIP exists.

Reload is shared configuration application, not API creation or a fallback for refused API writes. Do not edit generated files, write SQL, restart Asterisk, recreate successful endpoints or rotate credentials. A failed/uncertain reload requires state reconciliation before retrying. Loaded peers do not prove registration or audio.

Published sufficit-telephony-extensions 0.7.4 in commit 448ed66. Isolated validation excluding the unrelated writing-skill draft passed all 185 packages, catalog versions, skill index and Markdown coverage. The skill-creator quick validator and whitespace check also passed. No new executable code was introduced.

Rafael's existing managed onboarding bundle carries the application step directly in its injected root, with legacy SIP guidance. The four bindings total 39921 characters, within the instruction budget; existing resource files and the other three bound skill hashes were preserved. Native install and independent persisted read-back confirmed content hash 3040ae31d1fb3b8b3b5fbad9c3a372c57ceb82a197b8d7c3d0a93325200ff12b. Active turns were not interrupted; a later model response was not tested.

No production PBX reload, credential change or group message was performed: this delivery updates the requested playbook and agent training. Applying the previously created peers remains an operational action separate from this documentation update.

Voice training version `70ba04ac-cb2e-443a-9fed-96d65706e8ae` was synchronized and confirmed by provider read-back, without changing voice tools or bindings.
