# Asaas skills: customer address and update — 2026-11-03

Follows `sufficit-ai-genius` issue #1375. A customer registered with only name, CNPJ, and e-mail received an NFS-e that the prefeitura rejected for lack of an address.

## Changes

- `asaas-customers` 0.4.0: registration collects the address, new `references/customers-update.md`, the limits now describe what the update tool cannot do, and the page limit is corrected to 100.
- `asaas-invoices` 0.7.0: documents the `customer_address_incomplete` refusal, notes in `ERROR` or `CANCELED` not blocking a reissue, canceling a note in `ERROR`, and the local status filter.

## Validation

`scripts/validate.py` and `scripts/markdown_coverage.py` pass with the recalculated digests.
