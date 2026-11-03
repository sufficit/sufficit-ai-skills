# Customer update ASAAS

The `asaas_customers_update` tool changes an existing customer in the production account through `PUT /v3/customers/{id}`. It requires explicit approval in the conversation and confirms that the customer exists before writing.

## When to use

When the user asks to fix or complete a registration, or to clear a `customer_address_incomplete` refusal or a prefeitura rejection such as "Endereço do cliente incompleto" or "CEP do cliente é inválido".

## Arguments

| Argument | Type | Mandatory | Rules |
| --- | --- | --- | --- |
| `customer` | string | yes | Customer id (`cus_...`) from `asaas_customers_list`. |
| `email` | string | no | Up to 64 characters. |
| `address`, `addressNumber`, `complement`, `province`, `postalCode`, `phone`, `mobilePhone`, `externalReference` | string | no | Same rules as [customers-create.md](customers-create.md). |

At least one field besides `customer` is required. Only the fields provided are sent, so the rest of the registration is preserved. Empty values are ignored and cannot clear a field. The name and CPF/CNPJ cannot be changed here.

## Success result

| Field | Value |
| --- | --- |
| `updated` | `true` |
| `writesPerformed` | `true` |
| `updatedFields` | Names of the fields sent, never their values |
| `customer` | Sanitized customer, including `addressComplete` and `addressMissing` |
| `guidance` | Present when the address is still incomplete |

Updating a customer does not change an invoice already issued. A rejected invoice must be issued again after the fix.

## Failure codes

| Code | Meaning | Action |
| --- | --- | --- |
| `asaas_customers_update_invalid_arguments` | Missing or unsafe id, no field to change, or an invalid value. | Correct and repeat; nothing has been called. |
| `asaas_customers_update_customer_unconfirmed` | Customer not found, removed, or the lookup failed. | Find the right id with `asaas_customers_list`. |
| `asaas_customers_update_rejected` | ASAAS refused the change; the message brings its reason. | Correct with the user and try again. |
| `asaas_customers_update_unexpected` | Update confirmed, but the response format was unexpected. | Check the customer with `asaas_customers_list`. |
| `asaas_timeout` | Time limit exceeded. | The write may have happened; check before repeating. |
