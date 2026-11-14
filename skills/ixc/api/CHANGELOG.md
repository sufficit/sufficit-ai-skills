# Changelog

## 1.0.2 — 2026-11-14

- Checked read-only against a production IXC: mechanics, field names and read tool bodies confirmed.
- Open invoices now filter `status != R` and `!= C`: `IN A,P` on `fn_areceber.status` breaks with a non-JSON
  HTTP 200 error. Non-JSON 200 and HTML 401 bodies documented.

## 1.0.1 — 2026-11-14

- Package moved to `skills/ixc/api`, matching the vendor-named collections.

## 1.0.0 — 2026-11-14

- First release: request mechanics (auth, search, operators, `grid_param`, update and error rules) and module
  references for customers and contracts, financial, support, network, inventory and sales, and administration,
  built from IXCSoft's official API collection and per-form wiki plus flows a Sufficit customer runs in production.
- Fleet tool pack for ISP voice and chat agents (customer, contracts, connection, invoices, PIX, tickets, trust
  unblock) with persona instructions.
