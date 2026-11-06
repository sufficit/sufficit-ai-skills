# Official notification test API guidance

Session 01a1acef-9b0e-7333-a48f-3c0f3e6b75b1. sufficit-api 1.0.25 directs the
agent to discover POST /Notification/Test in the live OpenAPI before calling it,
select the exact stored contact and customer context, and distinguish queued
receipts from delivery. The official authenticated web URL remains fallback only
when the API is absent. Source implementation and publication are separate;
this instruction never treats a documented route as already deployed.
