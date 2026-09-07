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
    "Connect your own Odoo instance with URL, database name, username and API Key.",
    action_type="write",
    chain_callable=True,
    event="odoo-accounting-connector.connect_odoo_accounting",
    effects=["create:connection"],
    data_model=ConnectParams
)
async def connect_odoo_accounting(ctx, params: ConnectParams) -> ActionResult[ConnectionRecord]:
    """Connect a new Odoo instance."""
    client = OdooAccountingClient(
        url=params.url,
        db=params.db,
        username=params.username,
        api_key=params.api_key
    )
    v_res = await client.verify_auth()
    if v_res.get("status") == "error":
        return ActionResult.error(
            v_res.get("message", "Failed to authenticate against Odoo JSON-RPC"),
            code=v_res.get("code", "UNAUTHORIZED")
        )

    conns = await _load_connections(ctx)
    cid = f"conn_{uuid.uuid4().hex[:8]}"
    record = {
        "id": cid,
        "label": params.label or f"Odoo ({params.db})",
        "url": params.url,
        "db": params.db,
        "username": params.username,
        "api_key": params.api_key,
        "masked_key": _mask(params.api_key),
        "is_active": len(conns) == 0
    }
    conns.append(record)
    await _save_connections(ctx, conns)
    return ActionResult.success(ConnectionRecord(
        id=cid,
        label=record["label"],
        masked_key=record["masked_key"],
        url=record["url"],
        db=record["db"],
        username=record["username"],
        is_active=record["is_active"]
    ), summary="Odoo accounting connected.")

@chat.function(
    "list_connections",
    "List connected Odoo organizations without exposing sensitive passwords or API keys.",
    action_type="read",
    chain_callable=True,
    data_model=NoParams
)
async def list_connections(ctx, params: NoParams) -> ActionResult[ConnectionList]:
    """List all saved connections."""
    conns = await _load_connections(ctx)
    records = [
        ConnectionRecord(
            id=c["id"],
            label=c.get("label", "Odoo Account"),
            masked_key=c.get("masked_key", _mask(c.get("api_key", ""))),
            url=c.get("url", ""),
            db=c.get("db", ""),
            username=c.get("username", ""),
            is_active=c.get("is_active", False)
        )
        for c in conns
    ]
    return ActionResult.success(ConnectionList(connections=records, total=len(records)), summary="List connections completed successfully.")

@chat.function(
    "disconnect_odoo_accounting",
    "Disconnect an Odoo organization and delete its stored credentials.",
    action_type="write",
    chain_callable=True,
    event="odoo-accounting-connector.disconnect_odoo_accounting",
    effects=["delete:connection"],
    data_model=ConnectionIdParams
)
async def disconnect_odoo_accounting(ctx, params: ConnectionIdParams) -> ActionResult[DeleteResult]:
    """Disconnect and delete an account."""
    conns = await _load_connections(ctx)
    target = params.connection_id
    if not target:
        for c in conns:
            if c.get("is_active"):
                target = c["id"]
                break
        if not target and conns:
            target = conns[0]["id"]
    if not target:
        return ActionResult.error("No connection to disconnect")
    new_conns = [c for c in conns if c["id"] != target]
    if len(new_conns) == len(conns):
        return ActionResult.error(f"Connection {target} not found")
    if new_conns and not any(c.get("is_active") for c in new_conns):
        new_conns[0]["is_active"] = True
    await _save_connections(ctx, new_conns)
    return ActionResult.success(DeleteResult(id=target, deleted=True, message=f"Connection {target} removed."), summary="Disconnect odoo accounting completed successfully.")
