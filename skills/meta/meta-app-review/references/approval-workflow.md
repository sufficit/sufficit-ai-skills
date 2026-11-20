# Full flow of approval (screen paths)

## 0. Prerequisites
- Business with `verification_status: verified` (`GET /{business}?fields=verification_status`).
- A person with an app administrator role; only portfolio admin links app to it.
- App and asset (WABA/Page) in the same business — see webhook trap.

## 1. Create the app

`developers.facebook.com` app > Create app > Use case "Other" > Business type > portfolio. There is no API to create, rename or link app to the portfolio.

## 2. App settings

`Configurações > Básico` app settings: icon, privacy policy, terms, website, emails, category, URL data deletion instructions. `Configurações > Avançado`: Enable "Allow API access to application settings". After that you can record everything by `POST /{app-id}` with token app.

## 3. Facebook Login to Business (when the app connects third party assets)

`Login do Facebook para Empresas > Configurações`:
- Enter with JavaScript SDK = Yes;
- Domains allowed for JavaScript SDK: one entry per domain, with `https://` and final bar;
- Valid OAuth redirect URIs: mandatory when "strict mode" is enabled.

`Login do Facebook para Empresas > Configurações (lista) > Criar configuração`: name > General variation > user access token (with system user token no assets are chosen) > permissions. Generates `config_id`, which is the dialog parameter. `FB.login(cb, { config_id })`; `scope` classic does not work on these apps.

## 4. Use cases and permissions

`Casos de uso > Personalizar > Permissões e recursos`. "Ready for testing" = standard access, which only applies to those who have a role in the app. Permissions may belong to more than one use case.

## 5. Tech Provider (irreversible)

By clicking "Add to app analysis" Meta requires turning Tech Provider: company verification + access verification + analysis. Confirm with the owner first. Once accepted, the permissions required by the use cases are automatically added to the submission.

## 6. Use permitted (by permission)

`Análise do app > Ir para o uso permitido > Começar`:
1. description of the use (what it does, what value it gives, why it is necessary);
2. screencast;
3. test API call (Meta counter, up to 24h);
4. accept compliance. `pages_messaging` also asks for reproduction instructions. `pages_manage_metadata` requires `pages_show_list` on the same submission. `public_profile` and `email` only ask for acceptance.

## 7. Data processing

Data operators (yes/no), controller (legal company name), country, requests from authorities in the last 12 months, policies applied. These are legal statements: confirm with the person responsible, do not copy them automatically.

## 8. Instructions for the environment analyst

URL, test account that works, step by step to the screen of each permission and response to "Is Facebook Login integrated on this platform?".

## 9. Submit

The button only enables with the five sections completed. Once sent, you can't edit or cancel while you're in review.
