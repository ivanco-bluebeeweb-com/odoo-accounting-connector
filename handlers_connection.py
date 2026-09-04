"""Connection lifecycle for Odoo Accounting Connector."""
from __future__ import annotations
import json, uuid
from imperal_sdk import ActionResult
from odoo_accounting_client import OdooAccountingClient
from app import chat
from schemas import (
    NoParams,
    ConnectParams, ConnectionIdParams, ConnectionList, ConnectionRecord, DeleteResult
)

_SECRET = "odoo_accounting_connections"

def _mask(value: str) -> str:
    return value[:4] + "…" + value[-4:] if len(value) > 10 else "***"

async def _load_connections(ctx) -> list[dict]:
    raw = await ctx.secrets.get(_SECRET)
    if not raw: return []
    try: data = json.loads(raw)
    except: return []
    return data if isinstance(data, list) else []

async def _save_connections(ctx, conns: list[dict]) -> None:
    await ctx.secrets.set(_SECRET, json.dumps(conns))

async def resolve_connection(ctx, connection_id: str = "") -> dict | None:
    conns = await _load_connections(ctx)
    if not conns: return None
    if not connection_id:
        for c in conns:
            if c.get("is_active"):
                return c
        return conns[0]
    for c in conns:
        if c["id"] == connection_id:
            return c
    return None

@chat.function(
    "connect_odoo_accounting",
    "Connect Odoo Accounting account via credentials.",
    action_type="write",
    chain_callable=True,
    event="odoo-accounting-connector.connect_odoo_accounting",
    effects=["create:connection"],
    data_model=ConnectParams
)
async def connect_odoo_accounting(params: ConnectParams, ctx) -> ActionResult[ConnectionRecord]:
    """Connect a new account."""
    client = OdooAccountingClient(api_key=params.api_key, base_url=params.base_url)
    await client.verify_auth()
    conns = await _load_connections(ctx)
    cid = f"conn_{uuid.uuid4().hex[:8]}"
    record = {
        "id": cid,
        "label": params.label or "Odoo Accounting Account",
        "api_key": params.api_key,
        "base_url": params.base_url,
        "is_active": True
    }
    for c in conns: c["is_active"] = False
    conns.append(record)
    await _save_connections(ctx, conns)
    return ActionResult.ok(ConnectionRecord(id=cid, label=record["label"], masked_key=_mask(params.api_key), base_url=params.base_url, is_active=True))

@chat.function(
    "list_connections",
    "List connected Odoo Accounting accounts.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionList
)
async def list_connections(params: NoParams, ctx) -> ActionResult[ConnectionList]:
    """List connected accounts."""
    conns = await _load_connections(ctx)
    records = [ConnectionRecord(id=c["id"], label=c["label"], masked_key=_mask(c.get("api_key", "")), base_url=c.get("base_url", ""), is_active=c.get("is_active", False)) for c in conns]
    return ActionResult.ok(ConnectionList(connections=records, total=len(records)))

@chat.function(
    "disconnect_odoo_accounting",
    "Disconnect Odoo Accounting account.",
    action_type="write",
    chain_callable=True,
    event="odoo-accounting-connector.disconnect_odoo_accounting",
    effects=["delete:connection"],
    data_model=DeleteResult
)
async def disconnect_odoo_accounting(params: ConnectionIdParams, ctx) -> ActionResult[DeleteResult]:
    """Disconnect an account."""
    conns = await _load_connections(ctx)
    target = await resolve_connection(ctx, params.connection_id)
    if not target:
        return ActionResult.error("Connection not found", code="NOT_FOUND")
    new_conns = [c for c in conns if c["id"] != target["id"]]
    if new_conns and target.get("is_active"):
        new_conns[0]["is_active"] = True
    await _save_connections(ctx, new_conns)
    return ActionResult.ok(DeleteResult(id=target["id"], deleted=True, message="Disconnected successfully"))
