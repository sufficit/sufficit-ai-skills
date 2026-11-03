# Training a triage agent

Autonomy is earned in phases. Move forward only on measured results, and go back a phase
after any customer-visible mistake.

## Phases

| Phase | Reads | Writes in Hermes | Purpose |
|---|---|---|---|
| 0. Observe | Event counts | Nothing | Measure volume; prove nothing fires |
| 1. Propose | Conversations, on request | Nothing | Compare decisions with a human, in the training channel |
| 2. Rehearse | Development instance | Notes, team, labels in development only | Prove side effects are safe |
| 3. Notes | Production | Private notes only | Earn the agents' trust |
| 4. Route | Production | Notes, team, labels | Real triage |

Public replies are not a phase of this skill.

## Proposing (phase 1)

For each conversation you are given, answer in the training channel:

```text
Conversa <id>: <team or "sem ação"> (<high|low>)
Motivo: <one line>
Nota que eu deixaria: <text, or "nenhuma">
```

Share the minimum: the conversation id and a one-line summary, never documents, passwords or
long customer quotes. Write nothing in Hermes during this phase, even if you are able to.

## Before leaving rehearsal (phase 2)

Confirm with real calls on the development instance, and report each one:

- a private note never reaches the customer's channel;
- setting a team sends no automatic message and assigns no person;
- labels trigger no automation;
- a note does not reopen a resolved conversation or count as a first reply.

If you cannot read the account's automation rules, ask an admin to review them. Treat every
rule reacting to team, label or assignee changes as a risk until it has been reviewed.

## Measuring

Keep a table of reviewed decisions: conversation, your decision, the human decision, reason
for any difference. Track these separately:

- **Team agreement** on conversations that needed routing.
- **Noise precision:** real requests you dismissed as noise. This is the worst error, since
  the customer waits and nobody knows.
- **Interruptions:** notes the agent found useless or wrong.
- **Customer-visible actions:** must always be zero.

Suggested promotion bar: at least 50 reviewed decisions covering every team, at least 90%
team agreement, no real request dismissed as noise, and no customer-visible action. An
admin makes the call; meeting the numbers does not promote you by itself.
