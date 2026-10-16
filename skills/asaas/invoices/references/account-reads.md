# Account reading queries ASAAS

These two operations were verified in the production account of Sufficit in 2026-09-23 and returned HTTP 200. The record describes actual consultations, not just the success codes provided in schema. No invoices were scheduled and no records were changed during the verification.

## Trade data — identify the account

```http
GET https://api.asaas.com/v3/myAccount/commercialInfo
```

- Purpose: to identify the holder and consult current commercial data.
- Useful fields for identification: `companyName`, `name` and `personType`.
- Observed result: HTTP 200; commercial identity confirmed Sufficit account. Do not confuse this identification with the identification of the recipient of an invoice.
- This query does not identify the standard Tax Invoices service › Settings › Services.
- Source: [Recovering commercial data](https://docs.asaas.com/reference/recuperar-dados-comerciais).

## Tax information — see existing configuration

```http
GET https://api.asaas.com/v3/fiscalInfo/
```

- Purpose: consult the current tax configuration before drawing conclusions on the account or proposing changes.
- Result observed: HTTP 200, with `object: "customerFiscalInfo"`.
- Relevant returned fields: `simplesNacional`, `cnae`, `specialTaxRegime`, `serviceListItem`, `nbsCode`, `nationalPortalTaxCalculationRegime` and `serviceProvisionCityDefaultType`. Values can be null or void; do not complete or interpret as a fiscal choice without evidence.
- `serviceProvisionCityDefaultType` represents the default city of the provision, not the standard service. Returned `null` in the observed query.
- The observed response did not bring the list of pre-registered services of the panel or the service identifier marked as standard.
- According to documentation, HTTP 404 means that there is no tax configuration registered. Notify absence; consult does not authorize setting up.
- Source: [Retrieve tax information](https://docs.asaas.com/reference/recuperar-informacoes-fiscais).

## Evidence Limits

HTTP 200 confirms that the query has been attended, not that all the data required for the issue is available or that some service has been chosen. These readings do not confirm automatic filling of fields omitted in the scheduling and do not authorize issuing an invoice to find the pattern.

`GET /v3/fiscalInfo/services` is another operation: list municipal services, not pre-registered services in the panel. In the same investigation returned HTTP 400, with the message "The city service code is not enabled for this account." Do not register it as a successful query and do not interpret this refusal as the absence of services registered in the panel.

## Use in Genius and data protection

- These endpoints are API verified capabilities of Asaas. The inclusion of this reference in the skill does not implement new tools in the plugin. In the version inspected in 2026-09-23, there were no tools dedicated to these two queries; `asaas_connection_test` consult `/v3/myAccount/status` and does not replace any of them.
- Find out if the version in use offers matching tools. If not, please inform the limit and report the need to the plugin team; do not invent tool names or pretend to run the query.
- Run read-only, no body. Do not use POST/PUT or book an invoice as part of the query. Do not change settings to resolve a refusal.
- Authentication must stay in the trusted host, by reference of Vault `personal/asaas/production/api-key`. Do not bypass the lack of tool by shell/script or ask the user for the key in the conversation.
- Never expose credentials, authentication headers or the raw body of the answer. Present only the fields necessary for the question, respecting the personal data policy of the ASAAS skills. Do not copy to public skill private data returned by account.
- A HTTP 200 observed in this account and date does not guarantee success in other future accounts or queries. Report the actual status and motive of each execution, without changing the account or automatically repeating refusals.
