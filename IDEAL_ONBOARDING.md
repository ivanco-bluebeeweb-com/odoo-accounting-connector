# Odoo Accounting Connector — Ideal Onboarding

## User outcome
A user connects a Odoo Accounting account safely, immediately confirms the account that was connected, then starts with a useful read-only operational overview rather than a blank tool list.

## Flow
1. **Welcome:** explain the connector's verified capability categories and any vendor plan/admin prerequisite.
2. **Connect:** collect only the credentials documented in `AUTH_AND_CREDENTIALS.md`; provide setup instructions in a modal.
3. **Verify:** make one harmless identity, tenant, or health request and save a labeled connection only after success.
4. **First value:** present a focused summary/audit action plus primary resource browsing.
5. **Operate:** group actions by read, create/update, automation/webhooks and high-impact operations.
6. **Recover:** show reconnect guidance for expired OAuth, revoked keys, unavailable roles, rate limiting or disabled API access.

## Trust and safety
High-impact writes always describe their provider-side effect. Destructive actions must use the platform's required confirmation behavior. No provider capability is implied until official discovery verifies it.
