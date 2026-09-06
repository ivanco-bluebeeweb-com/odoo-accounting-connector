# Odoo Accounting Connector — UI Component Plan

## Sidebar Architecture
- **Slot:** `slot="left"`
- **Layout:** `ui.Stack(direction="v", gap=3, align="stretch")`
- **Elements:**
  1. Connector header with title and caption.
  2. Divider.
  3. `ui.Form` with `submit_label="Connect Odoo"` targeting `connect_odoo_accounting`.
  4. Form inputs (Label, URL, DB, Username, API Key) strictly respecting DUI parameter contracts (`param_name`, `placeholder`, `value`).
  5. Help modal (`_help_modal`) explaining how to generate an Odoo API key.
  6. Settings button (`_settings_button`) linking to `__panel__odoo_accounting_settings`.
