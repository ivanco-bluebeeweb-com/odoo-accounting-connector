"""Extension declaration, capabilities, health check for Odoo Accounting Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "odoo-accounting-connector",
    version="0.1.0",
    display_name="Odoo Accounting",
    icon="icon.svg",
    capabilities=["odoo_accounting:manage"],
    description="Official Imperal connector for Odoo Accounting (C27. Accounting & Bookkeeping). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("odoo_accounting_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} Odoo Accounting connection(s) configured." if count else "Not connected yet."
    }
