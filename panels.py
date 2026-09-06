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
        trigger=ui.Button("How do I set this up?", variant="ghost", size="sm"),
        title="Connecting Odoo Accounting",
        children=[
            ui.Text(
                "1. Sign in to your Odoo Accounting account and navigate to Security or User Settings.\n2. Choose your preferred authentication method (OAuth SSO, API Key / Token, or Username & Password Basic Auth).\n3. Enter your credentials and click Connect.",
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
            ui.Stack(
                direction="v",
                gap=1,
                align="stretch",
                children=[
                    ui.Text("Manage your Odoo Accounting connections and integrations.", variant="caption"),
                ]
            ),
            ui.Divider(),
            ui.Stack(
                direction="v",
                gap=2,
                align="stretch",
                children=[
                    ui.Button(
                        "Sign in with Odoo Accounting (OAuth / SSO)",
                        variant="primary",
                        size="sm",
                        icon="login"
                    ),
                    ui.Divider(),
                    ui.Text("Or connect via API Key or Login Credentials", variant="caption"),
                    ui.Form(
                        submit_label="Connect Odoo Accounting",
                        action=ui.Call("connect_odoo_accounting"),
                        children=[
                            ui.Stack(
                                direction="v",
                                gap=2,
                                align="stretch",
                                children=[
                                    ui.Stack(
                                        direction="v",
                                        gap=1,
                                        align="stretch",
                                        children=[
                                            ui.Text("Authentication Method", variant="label"),
                                            ui.Select(
                                                param_name="auth_mode",
                                                value="api_key",
                                                options=[
                                                    {"label": "API Key / Personal Access Token", "value": "api_key"},
                                                    {"label": "OAuth 2.0 Bearer Token", "value": "oauth"},
                                                    {"label": "Basic Auth (Username & Password / Master Key)", "value": "basic_auth"},
                                                ]
                                            ),
                                        ]
                                    ),
                                    ui.Stack(
                                        direction="v",
                                        gap=1,
                                        align="stretch",
                                        children=[
                                            ui.Text("Connection Label", variant="label"),
                                            ui.Input(param_name="label", placeholder="e.g. Production Odoo Accounting"),
                                        ]
                                    ),
                                    ui.Stack(
                                        direction="v",
                                        gap=1,
                                        align="stretch",
                                        children=[
                                            ui.Text("API Key / Access Token", variant="label"),
                                            ui.Input(param_name="api_key", placeholder="Paste API Key, Token or Password"),
                                        ]
                                    ),
                                ]
                            )
                        ]
                    ),
                ]
            ),
            _help_modal(),
            ui.Spacer(),
            _settings_button(),
        ]
    )
