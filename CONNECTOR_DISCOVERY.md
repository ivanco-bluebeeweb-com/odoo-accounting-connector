# Odoo Accounting Connector — Connector Discovery

## Official API Landscape
Odoo exposes a universal object model via Remote Procedure Call (RPC):
- **Authentication (`common` service):**
  - Endpoint: `POST /jsonrpc` with `service: "common"`, `method: "authenticate"`.
  - Arguments: `[db, username, api_key, {}]`. Returns user ID `uid`.
- **Object Manipulation (`object` service):**
  - Endpoint: `POST /jsonrpc` with `service: "object"`, `method: "execute_kw"`.
  - Arguments: `[db, uid, api_key, model_name, method_name, args, kwargs]`.
- **Standard Accounting Methods:**
  - `search_read`: Query records with domain filters, limit, and fields list.
  - `create`: Create a new record from a dict of values.
  - `write`: Update records by IDs with a dict of modified fields.
  - `unlink`: Delete records by IDs.
