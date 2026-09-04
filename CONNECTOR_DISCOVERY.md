# Odoo Accounting Connector — API Discovery

## Discovery status
**Pending live official-documentation verification.** This connector must not claim an endpoint, OAuth scope, webhook, or write capability until it is verified against Odoo Accounting's current official developer documentation and a customer-authorized account.

## Research checklist
- Official API base URLs, versions, pagination, filtering, idempotency and rate limits.
- Authentication types actually offered: OAuth 2.0 authorization code/client credentials, API token, service account, signed request, or local/self-hosted connection.
- Required scopes/roles/plan tiers, regional endpoints, admin approval and consent lifecycle.
- Read, create, update, archive/delete, search, bulk, asynchronous-job and webhook surfaces.
- Error contract, retries, eventual consistency, provider audit log, sandbox/test tenant and webhook signature verification.

## Initial implementation rule
Only operations confirmed during discovery go into `imperal.json`, schemas and handlers. Any unavailable or partner-only API is recorded as a technical blocker in the task instead of simulated.

## Source candidate
https://www.odoo.com/app/accounting
