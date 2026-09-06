"""Panel UI for Odoo Accounting Connector following UI_INTERFACE_STANDARD.md and AUTH_AND_CREDENTIALS_STANDARD.md."""
from __future__ import annotations
from imperal_sdk import ui
from app import ext

def _settings_button() -> ui.UINode:
    return ui.Button(
        "App settings",
        variant="secondary",
        size="sm",
        icon="settings",
        on_click=ui.Call("__panel__odoo_accounting_settings")
    )

def _help_modal() -> ui.UINode:
    return ui.Modal(
        trigger=ui.Button("How do I connect Odoo?", variant="ghost", size="sm"),
        title="Connecting Odoo Accounting",
        children=[
            ui.Text(
                "1. Sign in to your Odoo ERP instance (e.g. mycompany.odoo.com or custom domain).\n"
                "2. Your Database name is found in the database selector or top-right profile settings.\n"
                "3. In User Preferences > Account Security, generate an API Key for external integrations.\n"
                "4. Enter your instance URL, database name, username (email) and API Key above and click Connect.",
                variant="body"
            )
        ]
    )

@ext.panel("odoo_accounting_sidebar", slot="left")
async def odoo_accounting_sidebar(ctx, **kwargs) -> ui.UINode:
    return ui.Stack(
        direction="v",
        gap=3,
        align="stretch",
        children=[
            ui.Text("Odoo Accounting", variant="heading"),
            ui.Text("Manage invoices, customers, bills, bank accounts and tax rates via Odoo JSON-RPC.", variant="caption"),
            ui.Divider(),
            ui.Form(
                submit_label="Connect Odoo",
                action=ui.Call("connect_odoo_accounting"),
                children=[
                    ui.Stack(
                        direction="v",
                        gap=2,
                        align="stretch",
                        children=[
                            ui.Text("Connection Label", variant="caption"),
                            ui.Input(
                                param_name="label",
                                placeholder="e.g. Acme Odoo Production",
                                value=""
                            ),
                            ui.Text("Odoo Instance URL", variant="caption"),
                            ui.Input(
                                param_name="url",
                                placeholder="https://mycompany.odoo.com",
                                value=""
                            ),
                            ui.Text("Database Name", variant="caption"),
                            ui.Input(
                                param_name="db",
                                placeholder="e.g. mycompany_db",
                                value=""
                            ),
                            ui.Text("Username / Email", variant="caption"),
                            ui.Input(
                                param_name="username",
                                placeholder="admin@mycompany.com",
                                value=""
                            ),
                            ui.Text("API Key", variant="caption"),
                            ui.Input(
                                param_name="api_key",
                                placeholder="Paste your Odoo API Key",
                                value=""
                            ),
                        ]
                    )
                ]
            ),
            ui.Divider(),
            _help_modal(),
            _settings_button()
        ]
    )
