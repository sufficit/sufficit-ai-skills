# Correlate one call with its actual ingress channel

Keep the requested investigation: the supplied caller, called DID, date and time.
Do not turn a question about this call into testing another customer's extension.
Resolve the DID's owning context through the authorized API even when it differs
from the previous topic. Explain that mismatch briefly and continue the requested
trace within the connected actor's actual access.

Normalize number presentation (including country code) and make the time window
explicit. Convert the caller's local time to the search contract's time basis;
set start/end rather than accepting server-local "today" defaults. Discover live
filters/limits, including answered-only, billed-only, pagination and maxRecords.
Do not send a new test call merely to investigate an earlier call.

The maintained read is POST /Telephony/Call/Search with CallSearchParameters
(contextid, start, end and supported filters). A POST search is read-only. Results
consolidate CDR records by LinkedId. For an identified call, GET
/Telephony/Call/Channels?contextid=<context>&linkedid=<LinkedId> reads its channels.
Use the ingress leg's actual channel/peer plus the matching caller, DID, event
time and Uniqueid/LinkedId to identify the trunk. Several legs can belong to the
same call; an outbound/transfer leg is not automatically its ingress.

A security SuccessfulAuth event proves authentication at that event. AccountID
may resemble a DID, and the source IP may belong to a known trunk, but neither
identifies the requested call or its channel. A nearby time does not close that
gap. If only those clues exist, say "candidate trunk; call/channel unconfirmed"
instead of asserting the trunk and appending a contradictory disclaimer.

An empty history search first calls for checking context, number formatting,
time basis/window and default filters. It does not establish CDR ingestion delay;
report delay only with evidence of ingestion state. If needed, use permitted
read-only PBX/channel/CEL/CDR diagnostics correlated by the same call identifiers.
A missing full log does not make authentication events a replacement for call
records. Never enable global debug/reload or use direct database writes as fallback.

A DID's configured destination and a current dialplan snapshot do not prove the
historical route executed. When correlation remains unavailable, report the
candidate evidence and missing identifier/window without inventing a channel,
claiming the customer never dialed or redirecting them to an unrelated test.
