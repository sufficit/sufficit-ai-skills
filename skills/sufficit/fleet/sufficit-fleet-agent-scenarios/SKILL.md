---
name: sufficit-fleet-agent-scenarios
description: "Manage reusable, agent-owned test scenarios in Sufficit Fleet and replay them against the agent's Genius executor. Use for cenários de teste, reproduction of a support case, or training regression checks."
metadata:
  version: "1.0.0"
---

# Agent regression scenarios

Use the agent's durable Fleet ID and a Fleet credential authorized for its context.
The collection URL is `https://fleet.sufficit.com.br/api/fleet/v1/agents/{agentId}/scenarios`.
Check the [Fleet API contract](https://fleet.sufficit.com.br/swagger/v1/swagger.json)
for the deployed operation schemas.

## Manage the exercise

List the collection with GET and inspect an existing exercise with GET
`{collection}/{scenarioId}`. To save a new exercise, POST a JSON body to the
collection. Use a synthetic prompt that reproduces the decision the agent must
make. Put the operator's acceptance criteria in `expected`. For example:

```json
{
  "title": "Atribuir a confirmação de um teste",
  "prompt": "O operador disse que testou e funcionou. Escreva a resposta para ele.",
  "expected": "Agradecer e atribuir a confirmação ao operador. Uma verificação própria exigiria evidência independente.",
  "skillIds": []
}
```

To exercise specific training, supply the exact installed skill IDs from that
agent's executor. Save the returned scenario ID and revision. Edit with PUT
on the item URL, sending the full exercise and its current revision in
`expectedRevision`. Delete the item with DELETE and the query parameter
`expectedRevision`. On a revision conflict, reread the item before editing.
Retiring the agent preserves its exercises. Permanent deletion of the agent
cascades to its scenarios.

## Replay and assess

1. POST to `{collection}/{scenarioId}/runs`. Each POST starts a distinct run
   in a fresh two-hour session using the agent's current preset and the scenario's
   pinned skills. The tool set is empty and discovery is disabled. Fleet sends
   the prompt and keeps the rubric on the operator side.
2. Keep the HTTP 202 receipt with the scenario ID, revision and session ID.
   Follow its `Location` with authenticated GET. The response is the session
   export. Poll that URL until the turn completes. Inspect `chat.error`,
   `chat.activeTurnId` and the agent's Markdown answer in `chat.parts`.
3. Compare the answer with each criterion while the session is available.
   Mark partial results explicitly. Describe a proposed operation as a decision
   made in simulation. A claim that a real call, DTMF or API write succeeded
   requires separate execution evidence.
4. To assess a training update, repeat the same scenario revision and record the
   preset, installed skill versions and observed differences. The scenario
   revision identifies the exercise; it does not freeze the model or skill content.
