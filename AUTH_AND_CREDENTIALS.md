# Odoo Accounting Connector — Authentication & Credentials

## Principle
This connector uses customer-provided credentials and holds them only in Imperal encrypted secrets storage. The panel never displays saved secret values.

## Authentication decision gate
Before implementation, determine the officially supported model for Odoo Accounting:
- **OAuth 2.0:** use authorization code + PKCE where supported; persist refresh metadata securely and handle re-consent.
- **Service-to-service OAuth:** request only documented client credentials/scopes and validate with a harmless call.
- **API token/key:** ask for the exact token plus required account/tenant/base URL only when the vendor requires them.
- **Self-hosted/local:** require HTTPS base URL and validate ownership/connectivity without exposing credential material.

## Required UX behavior
- Every credential input has a visible label and contextual placeholder.
- Explain where the credential is obtained only in the help modal, not duplicated in the sidebar.
- On connect, validate without mutating the provider account; on failure, return a safe actionable message.
- Connection lists show label, provider identity/tenant where safe, health/reauthorization state, and masked identifiers.
- Disconnect deletes only the locally stored Imperal credential.
