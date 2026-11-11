# Device provisioning: acting for the technician and diagnosing failures

sufficit-telephony-extensions 0.7.1 extends references/device-provisioning.md
with two sections requested by the owner: acting for the technician (find the
recent device through discoveries and unregistered requests, correlate by time
and site IP, register the MAC on the right extension, ask for one reboot,
verify) and a failure table mapping access-log evidence to cause and next step.

It depends on sufficit-provisioning 41eadfe (2026-11-11 18:20 UTC on all three
apps nodes): access_log now records transport (tftp/http/https), outcome slug,
detail and the real device IP for HTTP; TFTP transfers the device never
acknowledged get a transfer-failed row; diagnostics/requests filters by client,
outcome, transport, since and unregistered. Validated end to end with a dummy
MAC over HTTPS, HTTP and TFTP read through the support helper.

Catalog version/digest updated; 185 packages validated. The support executor
copy at /data/support/provisioning/DEVICE-PROVISIONING.md was replaced; the
bound pointer is unchanged.
