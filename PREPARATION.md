# Odoo Accounting Connector — Preparation

## Product scope
Build a secure Imperal connector for **Odoo Accounting** in **C27. Accounting & Bookkeeping**. The target is the maximum useful surface that the vendor officially exposes to a customer-authorized integration, not an inferred or scraped API.

## Delivery gates
1. Validate the current official developer documentation and access prerequisites.
2. Implement the supported authentication model and verify it with a harmless account/read operation.
3. Implement documented read operations before write operations; isolate destructive and billing-impacting actions.
4. Add onboarding and the planned UI before the panel implementation.
5. Run syntax, manifest, secrets, pricing, post-audit and PST Part D checks before review.

## Source to validate
- Catalog source: https://www.odoo.com/app/accounting
- This document is a discovery starting point, not evidence that every endpoint is publicly available.

## Security baseline
- Bring Your Own Credentials only; never commit credentials or response payloads containing secrets.
- Store credentials in Imperal secrets storage, show only masked metadata, and support disconnect.
- Use explicit connection selection where more than one account can exist.
- Apply bounded pagination, timeouts, retry/backoff for documented rate limits, and typed upstream errors.
- Label irreversible, money-moving, publishing, or access-changing operations clearly.
