# Odoo Accounting Connector — Preparation

## Product Scope
Build a comprehensive Imperal connector for **Odoo Accounting** (C27. Accounting & Bookkeeping). The integration connects directly to the official **Odoo JSON-RPC / XML-RPC endpoint** (`/jsonrpc` on Odoo Enterprise, Community, or Odoo Online), providing programmatic accounting management across partners/customers, customer invoices, vendor bills, bank journals, and tax rates.

## Official API Specifications
- **API Protocol:** Odoo Web Service (JSON-RPC 2.0 via `/jsonrpc` or XML-RPC)
- **Authentication Model:** Two-stage authentication:
  1. `common.authenticate(db, username, api_key, {})` -> resolves integer `uid`.
  2. Subsequent calls to `object.execute_kw(db, uid, api_key, model, method, args, kwargs)`.
- **Target Accounting Models:**
  - `res.partner`: Customers and Vendors
  - `account.move`: Customer Invoices and Vendor Bills
  - `account.payment`: Payments and Receipts
  - `account.journal`: Bank and Cash Accounts
  - `account.tax`: Tax Rates
- **Mandatory Requirements:**
  - Multi-instance routing support (Standard B7).
  - Explicit rate limit detection (HTTP 429) and auth classification (HTTP 401/403).
  - Sanitization of API Key in exception traces (Standard B8).
  - Multi-tenant connection tracking via `connection_id` (Standard B9).

## Delivery Gates
1. [x] Official API discovery completed with Odoo JSON-RPC `object.execute_kw` specifications.
2. [x] Two-stage authentication model (DB, UID, API Key) implemented.
3. [x] Five mandatory specification documents authored.
4. [x] Client implemented with B7-B10 compliance, secret redaction, and 429/401 classification.
5. [x] Panel sidebar implemented conforming to UI_INTERFACE_STANDARD.md.
6. [x] Action prices calibrated per PRICING_POLICY.md.
