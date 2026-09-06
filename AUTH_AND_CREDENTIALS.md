# Odoo Accounting Connector — Authentication & Credentials

## Principle
Credentials are submitted through the secure connection sidebar and stored strictly inside Imperal encrypted secrets (`odoo_accounting_connections`). The API key is never exposed to LLM context or logs.

## Credentials Required
- **Odoo URL:** Base domain (e.g., `https://mycompany.odoo.com` or custom self-hosted URL).
- **Database Name (`db`):** The Odoo PostgreSQL database identifier.
- **Username / Login:** The email or username of an authorized accounting user.
- **API Key:** User's personal API Key generated under *User Preferences > Account Security*.

## Security Standards Applied
- **B7 (Multi-Instance Routing):** Each connection stores its own instance URL and database.
- **B8 (Secret Sanitization):** `_sanitize_msg` scrubs the API key from all error responses.
- **B9 (Multi-Tenant Isolation):** Every resource handler accepts an optional `connection_id`.
- **B10 (Granular Error Codes):** Returns structured codes `RATE_LIMITED`, `UNAUTHORIZED`, `NOT_FOUND`.
