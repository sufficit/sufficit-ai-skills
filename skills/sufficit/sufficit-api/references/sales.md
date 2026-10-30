# Sales representatives

Representatives are contacts identified by GUID. Discover the routes in the live OpenAPI by `representative customers`, `representative list` or `representatives` before calling.

## Customer portfolio

`GET /Sales/Representative/Customers?representativeId=...` returns the representative's own row first and then every customer with a service commissioned to it, with `title`, `balance`, `commitment`, `activeServices` and `entries` (inbound numbers). The portfolio also keeps former customers whose commissioned services ended; they come with `activeServices = 0`.

Always narrow the request instead of reading the whole list:

- `onlyActive=true`: only customers with at least one service active now;
- `filter`: customer title fragment or exact customer GUID;
- `skip` and `take`: pages ordered by title;
- `includeRepresentative=false`: omits the representative's own row.

The `X-Total-Count` response header carries the filtered total before paging. To count the active portfolio, call with `onlyActive=true&includeRepresentative=false&take=1` and read the header; to list it, page with `take` of up to 100 and keep going while rows remain. Never sum `activeServices` from a truncated answer.

The representative itself may read its own portfolio; managers and administrators may read any.

## Which count to use

- Active portfolio: `Representative/Customers` with `onlyActive=true` (header `X-Total-Count`). This is the official count of a representative's active customers.
- `GET /Sales/Representative/List` (management only) counts every customer ever commissioned, including former ones.
- `GET /Sales/Representatives/ById` shows `customers` and `commissionedCustomers` from the commission program registry. A representative whose portfolio was not yet registered there shows `0`; this is not the size of its customer base.

## Customer contact data

The portfolio returns aggregates only, never the customers' e-mail or phone. A representative's permission does not extend to its customers' records. Do not try to obtain them by passing a customer GUID as `contextId` or `contactId` to `POST /Contact/Search`; the server refuses it (`403`) and it is outside the authorised scope. When a campaign needs contact data, report that it requires an export authorised by Sufficit management.
