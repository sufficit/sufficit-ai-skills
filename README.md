# Sufficit AI Skills

Espelho público e versionado de 213 skills preparadas para o catálogo v2 do
Sufficit AI Genius. A publicação no Genius depende de sincronizar uma revisão
imutável deste repositório. Os pacotes mantêm instruções e recursos sob demanda; o
manifesto registra a origem, a revisão, a autoria, a licença e o digest de cada
conteúdo importado.

## Skills

| Coleção | Quantidade | Origem |
| --- | ---: | --- |
| Android | 37 | `android/skills`, Apache-2.0 |
| Google | 127 | `google/skills`, Apache-2.0 |
| Refero | 1 | `referodesign/refero_skill`, MIT |
| Unslop | 1 | `heydamir/unslop`, CC BY 4.0 |
| Matt Pocock | 1 | `mattpocock/skills`, MIT |
| MikroTik | 1 | `tikoci/routeros-skills` (adaptação Sufficit), MIT |
| Hermes | 2 | `Sufficit`, MIT-0 |
| Sufficit | 23 | Sufficit, MIT-0 |
| Asterisk | 1 | Sufficit, MIT-0 |
| Images | 1 | Sufficit, MIT-0 |
| Meta / Instagram | 3 | Sufficit, MIT-0 |
| Meta / Instagram (adaptação) | 3 | `Jakeschincariol/instagram-agent-skill` (adaptação Sufficit), MIT |
| Meta | 2 | Sufficit, MIT-0 |
| Videos | 2 | Sufficit, MIT-0 |
| Asaas | 4 | Sufficit, MIT-0 |
| QuePasa | 2 | Sufficit, MIT-0 |
| IXC | 1 | Sufficit, MIT-0 |
| MetaTrader | 1 | Sufficit, MIT-0 |

As skills ficam em [`skills/android`](skills/android),
[`skills/asaas`](skills/asaas),
[`skills/google`](skills/google), [`skills/hermes`](skills/hermes), [`skills/images`](skills/images),
[`skills/ixc`](skills/ixc),
[`skills/meta`](skills/meta),
[`skills/metatrader`](skills/metatrader), [`skills/mikrotik`](skills/mikrotik), [`skills/quepasa`](skills/quepasa),
[`skills/refero`](skills/refero),
[`skills/unslop`](skills/unslop),
[`skills/videos`](skills/videos) e
[`skills/sufficit`](skills/sufficit). O
snapshot importado está em [`catalog/upstream-v2.json`](catalog/upstream-v2.json)
e a correspondência verificável em
[`catalog/import-manifest.json`](catalog/import-manifest.json).
O [índice de skills](catalog/SKILLS.md) lista cada pacote com link para o
seu `SKILL.md`.

O catálogo distribuído pelo Genius fixa cada pacote em um commit completo.
Alterações em `main` não substituem silenciosamente uma versão já revisada ou
instalada. Consulte [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) para
autoria e licenças.

A skill `software-development` possui instalação vinculada para Codex e conferência
de versão remota: [pacote](skills/sufficit/software-development/SKILL.md).

A skill [`dotnet-csharp`](skills/sufficit/dotnet-csharp/SKILL.md) orienta mudanças em C#/.NET
para passar no CI na primeira vez: compilar os projetos de teste afetados, manter testes
vermelhos compiláveis, rodar os gates do repositório e alinhar versões de pacotes.

O [plano de respostas curtas](docs/PLAN-CHAT-REPLY-LENGTH.md) registra a política de mensagens de chat.

A skill [`clear-technical-writing`](skills/sufficit/clear-technical-writing/SKILL.md) orienta escrita técnica
clara, com adaptação em português e distinção entre revisão editorial e conformidade
com o padrão inglês. É uma adaptação independente da Sufficit.
Delivery: [support chat readability](docs/activities/20261030-chat-readability.md).

The [`instagram-video-download`](skills/meta/instagram/instagram-video-download/SKILL.md) skill saves Instagram
videos locally with yt-dlp and verifies the resulting media streams. The
[`video-transcribe`](skills/videos/video-transcribe/SKILL.md) skill turns local videos or audio into a
Markdown transcript with Whisper and ffmpeg. The
[`instagram-profile-setup`](skills/meta/instagram/instagram-profile-setup/SKILL.md) skill audits and writes
searchable, converting Instagram business profiles and covers a new account's first steps;
[`instagram-profile-manage`](skills/meta/instagram/instagram-profile-manage/SKILL.md) reads the live profile and
applies approved changes through the cheapest working channel;
[`instagram-caption`](skills/meta/instagram/instagram-caption/SKILL.md) writes and lints captions in Portuguese or
English; [`instagram-audit`](skills/meta/instagram/instagram-audit/SKILL.md) ranks published posts against the
account's own median and separates hook problems from profile problems;
[`instagram-reel`](skills/meta/instagram/instagram-reel/SKILL.md) writes Reel scripts with a timed beat sheet and
a per-brand voice file.

The [`hermes-api`](skills/hermes/api/SKILL.md) skill discovers the Hermes helpdesk API from the
server's own OpenAPI document and calls it as the agent's own user (profile, avatar,
conversations, private notes); [`hermes-triage`](skills/hermes/triage/SKILL.md) routes
conversations to the right team with private notes, never replying to customers.
The [Hermes Kanban API guide](skills/hermes/api/references/kanban.md) covers board operations and the plugin routes omitted from the public OpenAPI.
The [Kanban documentation activity](docs/activities/202611181054-hermes-kanban.md) records the contract review and validation.
The [Hermes connection activity](docs/activities/202611161205-hermes-token-onboarding.md) records token onboarding and tablet acceptance.

The [`ixc-api`](skills/ixc/api/SKILL.md) skill calls an ISP's IXC Provedor (IXCSoft) webservice across
every module — customers and contracts, receivables, tickets and service orders, Radius and fiber, inventory and
administration — with safe write rules, plus a tool pack for Sufficit Fleet voice and chat agents.

The [`quepasa-api`](skills/quepasa/api/SKILL.md) skill calls the QuePasa API as a
client; [`quepasa-production`](skills/quepasa/production/SKILL.md) operates Sufficit's
production QuePasa (health, session diagnosis, re-pair, dead-letter replay, rollout and
rollback) and lists the grant each task needs.


The [seo-geo](skills/sufficit/seo-geo/SKILL.md) skill diagnoses
incorrect shared-link images and improves landing-page identity, conventional SEO
and AI search eligibility (SEO, GEO and AEO) using dated primary sources.
Execution record: [landing discovery delivery](docs/activities/202610262106-landing-discovery.md).

## Skill language

Write all skill instructions, supporting documentation, cards, and agent metadata
in English. Catalog descriptions must also be English. Preserve API identifiers,
commands, and exact UI labels or provider messages when translating would make
instructions inaccurate; explain those literals in English. This package-language
rule does not override a user's requested response language.

Refinement record: [SEO/GEO naming and scope](docs/activities/202610271100-seo-geo.md).

The [Asterisk dialplan skill](skills/asterisk/dialplan/SKILL.md) defines English authoring, literal TAB indentation, context comments and change headers.
Delivery: [dialplan skill](docs/activities/20261028-asterisk-dialplan-skill.md).

The [ISP customer support skill](skills/sufficit/isp-customer-support/SKILL.md)
provides a scenario-based manual for internet-provider service teams, including
repeat faults, disputed visits, installation checks and invoice delivery.

Delivery: [ISP support manual and artifact cleanup](docs/activities/202611031032-isp-customer-support.md).

Delivery: [legacy renewal guidance](docs/activities/20261103-legacy-renewal-guidance.md).

The [campaigns skill](skills/sufficit/sufficit-campaigns/SKILL.md) operates outreach campaigns through the corporate API, which has no management screen. Activating a voice campaign places real calls, so it requires an explicit request and confirmation.

The [support skill](skills/sufficit/sufficit-support/SKILL.md) is the two-way channel between a customer company and Sufficit (issues, improvements, questions and Sufficit's requests); every customer skill points to it.

The [voice agents skill](skills/sufficit/sufficit-voice-agents/SKILL.md) lets a customer company build and operate its own Sufficit voice agents through the APIs (ElevenLabs agent, SIP number, virtual extension, training publication, test calls), including how to check for and apply updates of the skill itself.

The [telephony low-balance alert workflow](skills/sufficit/sufficit-api/references/low-balance-alerts.md)
resolves an initial threshold and primary notification destination from customer
evidence before asking optional preference questions.
Delivery: [low-balance alert training](docs/activities/20261105-low-balance-alert-training.md).
Device evidence: [tablet acceptance](docs/activities/20261105-low-balance-tablet-acceptance.md).
Open acceptance blockers: [tablet test plan](docs/PLAN-LOW-BALANCE-TABLET-TEST.md).

A [skill de relatórios de telefonia](skills/sufficit/sufficit-telephony-reports/SKILL.md)
orienta o acesso do cliente pelo portal, a geração via API e a exportação Excel.
[Acesso ao relatório de ligações tarifadas](docs/activities/202611181113-telephony-report-portal-link.md).
[Período da última recarga no relatório](docs/activities/202611181121-telephony-report-recharge-link.md).
[Contrato de datas dos relatórios](docs/activities/202611181157-report-range-contract.md).
[Carregamento automático e geração em segundo plano](docs/activities/202611181905-telephony-report-jobs-skill.md).

[Gestão de filas pela API nas skills de telefonia](docs/activities/202611191520-queue-api-skills.md).
[Extension NAT and video](docs/activities/202611191545-extension-nat-and-video.md).
[Extension channel variables](docs/activities/202611211500-extension-channel-variables.md).

Declared package versions are copied into the reviewed catalog by
`scripts/catalog_versions.py`; CI checks that they match `SKILL.md` metadata.
Packages without a declared version stay unversioned; a Git revision is provenance,
not a substitute for a semantic version.

Delivery: [inbound route lookup guidance and retest](docs/activities/20261109-inbound-route-guidance.md).

Delivery: [chronology in support replies](docs/activities/20261109-support-chronology.md).

Delivery: [customer WhatsApp number diagnostics](docs/activities/20261109-quepasa-number-diagnostics.md).

Delivery: [QuePasa linked-device limit in call diagnostics](docs/activities/202611101640-quepasa-linked-device-limit.md).

Delivery: [customer preferred due-day guidance](docs/activities/202611091706-customer-preferred-due-day.md).

Delivery: [customer preference without checkout](docs/activities/202611091743-independent-customer-payment-preference.md).

Training: [customer telephony onboarding](skills/sufficit/sufficit-telephony-extensions/references/customer-onboarding.md).

Delivery: [telephony onboarding and domain access](docs/activities/202611101100-telephony-onboarding-access.md).

Delivery: [onboarding defaults](docs/activities/202611101144-onboarding-defaults.md).

The [telephony credit workflow plan](docs/PLAN-TELEPHONY-CREDIT-WORKFLOW.md) tracks the agent guidance for credit purchases, commitments and service-history preservation.

The [commercial session handoff plan](docs/PLAN-COMMERCIAL-SESSION-HANDOFF.md) tracks the November 2026 reconciliation guidance and verified delivery.

Delivery: [PJSIP registration guidance](docs/activities/202611121037-pjsip-registration-guidance.md).

Delivery: [FreePBX extension reload](docs/activities/202611121045-freepbx-extension-reload.md).

Registro de entrega: [validade de contratos recorrentes](docs/activities/202611121436-recurring-contract-validity.md).

Delivery: [Rafael device-model and call-evidence review](docs/activities/202611121506-rafael-model-and-call-evidence.md).

Delivery: [Provisioning with an inferred model](docs/activities/202611121511-provisioning-model-inference.md).

Delivery: [PJSIP-first provisioning training](docs/activities/202611121537-pjsip-first-training.md).

A skill [sufficit-service-reconciliation](skills/sufficit/sufficit-service-reconciliation/SKILL.md)
orienta consolidação, continuidade das competências e emissão financeira, com
verificação somente leitura de capturas reais antes/depois.

Entrega: [skill de reconciliação e aceite independente](docs/activities/202611141900-service-reconciliation-skill.md).

Training delivery: [inbound diagnostic update](docs/activities/202611160844-rafael-inbound-diagnostic-training.md).

Diagnostic follow-up: [call correlation](docs/activities/202611160924-rafael-call-correlation.md).

The [youtube-video-understand](skills/videos/youtube-video-understand/SKILL.md) skill combines complete
timestamped YouTube/local transcripts with frame inspection at arbitrary times.
Delivery: [video understanding](docs/activities/202611161526-video-understanding.md).

Delivery: [YouTube naming and tablet acceptance](docs/activities/202611161700-youtube-tablet-acceptance.md).

Delivery: [YouTube runtime plugin](docs/activities/202611161915-youtube-runtime-plugin.md).

- [Optional native integration plugins](docs/activities/202611162231-optional-integration-plugins.md) — installation/discovery updates for Genius.

[Registro da consolidação da main](docs/activities/202611182023-skills-main-consolidation.md).

[Diagnóstico de filas por nó e confirmação do atendimento](docs/PLAN-QUEUE-DIAGNOSTIC-TRAINING.md).
