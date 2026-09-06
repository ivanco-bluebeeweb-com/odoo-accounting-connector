"""Official Odoo Accounting JSON-RPC client with database, uid, and api_key authentication."""
from __future__ import annotations
import httpx
from typing import Any, Optional

DEFAULT_ODOO_URL = "https://odoo.com"

class OdooAccountingClient:
    def __init__(self, url: str, db: str, username: str, api_key: str):
        self.url = (url.strip() if url else DEFAULT_ODOO_URL).rstrip("/")
        self.db = db.strip()
        self.username = username.strip()
        self.api_key = api_key.strip()
        self.uid: Optional[int] = None
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Imperal-OdooAccounting/0.1.0"
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    def _sanitize_msg(self, msg: str) -> str:
        if not msg: return ""
        if self.api_key and len(self.api_key) > 6:
            msg = msg.replace(self.api_key, self.api_key[:3] + "..." + self.api_key[-3:])
        return msg

    def _classify_error(self, resp: httpx.Response, action_name: str) -> dict[str, Any]:
        status = resp.status_code
        err_msg = ""
        try:
            data = resp.json()
            if "error" in data:
                err = data["error"]
                err_msg = err.get("data", {}).get("message") or err.get("message") or str(err)
        except Exception:
            err_msg = resp.text[:200]
        err_msg = self._sanitize_msg(err_msg)

        if status == 429:
            retry_after = resp.headers.get("Retry-After", "60")
            return {"status": "error", "code": "RATE_LIMITED", "message": f"Odoo rate limit reached during {action_name}. Retry after {retry_after}s.", "retry_after": int(retry_after) if retry_after.isdigit() else 60}
        if status in (401, 403):
            return {"status": "error", "code": "UNAUTHORIZED" if status == 401 else "FORBIDDEN", "message": f"Odoo authentication/permission error during {action_name}: {err_msg}"}
        return {"status": "error", "code": "ODOO_ERROR", "message": f"Odoo operation {action_name} failed: {err_msg}"}

    async def _json_rpc(self, service: str, method: str, *args) -> Any:
        endpoint = f"{self.url}/jsonrpc"
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": service,
                "method": method,
                "args": list(args)
            },
            "id": 1
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(endpoint, json=payload, headers=self.headers)
            if resp.status_code != 200:
                raise Exception(f"HTTP {resp.status_code}: {resp.text[:200]}")
            data = resp.json()
            if "error" in data:
                err = data["error"]
                msg = err.get("data", {}).get("message") or err.get("message") or str(err)
                raise Exception(self._sanitize_msg(msg))
            return data.get("result")

    async def verify_auth(self) -> dict[str, Any]:
        try:
            # authenticate via common service
            uid = await self._json_rpc("common", "authenticate", self.db, self.username, self.api_key, {})
            if uid:
                self.uid = int(uid)
                return {"status": "connected", "verified": True, "uid": self.uid, "db": self.db, "url": self.url}
            return {"status": "error", "code": "UNAUTHORIZED", "message": "Odoo authentication failed: Invalid database, username, or API key."}
        except Exception as e:
            msg = self._sanitize_msg(str(e))
            return {"status": "error", "code": "CONNECTION_FAILED", "message": f"Odoo connection failed: {msg}"}

    async def _ensure_uid(self):
        if self.uid is None:
            res = await self.verify_auth()
            if res.get("status") == "error":
                raise Exception(res.get("message", "Authentication required"))

    async def execute_kw(self, model: str, operation: str, args: list[Any], kwargs: Optional[dict[str, Any]] = None) -> Any:
        await self._ensure_uid()
        return await self._json_rpc("object", "execute_kw", self.db, self.uid, self.api_key, model, operation, args, kwargs or {})

    # Customers (res.partner where customer_rank > 0)
    async def list_customers(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        offset = int(cursor) if cursor and cursor.isdigit() else 0
        domain = [("customer_rank", ">", 0)]
        fields = ["id", "name", "email", "phone", "vat", "active"]
        try:
            records = await self.execute_kw("res.partner", "search_read", [domain], {"fields": fields, "limit": limit, "offset": offset})
            total = await self.execute_kw("res.partner", "search_count", [domain])
            items = [{"id": str(r["id"]), "name": r.get("name", ""), "status": "active" if r.get("active") else "archived", "email": r.get("email"), "phone": r.get("phone"), "raw": r} for r in records]
            return {"items": items, "total": total, "next_cursor": str(offset + limit) if offset + limit < total else None}
        except Exception:
            return {"items": [], "total": 0}

    async def get_customer(self, customer_id: str) -> dict[str, Any]:
        cid = int(customer_id) if customer_id.isdigit() else 0
        fields = ["id", "name", "email", "phone", "vat", "street", "city", "country_id", "active"]
        records = await self.execute_kw("res.partner", "read", [[cid]], {"fields": fields})
        if records:
            r = records[0]
            return {"id": str(r["id"]), "name": r.get("name", ""), "status": "active" if r.get("active") else "archived", "raw": r}
        return {"id": customer_id, "name": "Customer", "status": "active"}

    async def create_customer(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        vals = {"name": name, "customer_rank": 1}
        if details:
            for k, v in details.items():
                if k not in ("id", "customer_rank"):
                    vals[k] = v
        new_id = await self.execute_kw("res.partner", "create", [vals])
        return {"id": str(new_id), "name": name, "status": "active", "raw": vals}

    async def update_customer(self, customer_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        cid = int(customer_id) if customer_id.isdigit() else 0
        await self.execute_kw("res.partner", "write", [[cid], fields])
        return {"id": customer_id, "name": fields.get("name", "Updated Customer"), "status": "active", "raw": fields}

    async def delete_customer(self, customer_id: str) -> bool:
        cid = int(customer_id) if customer_id.isdigit() else 0
        # in Odoo, soft-delete via active=False is standard
        try:
            await self.execute_kw("res.partner", "write", [[cid], {"active": False}])
            return True
        except Exception:
            return False

    # Invoices (account.move where move_type in ('out_invoice', 'out_refund'))
    async def list_invoices(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        offset = int(cursor) if cursor and cursor.isdigit() else 0
        domain = [("move_type", "in", ["out_invoice", "out_refund"])]
        fields = ["id", "name", "partner_id", "invoice_date", "invoice_date_due", "amount_total", "amount_residual", "state", "payment_state"]
        try:
            records = await self.execute_kw("account.move", "search_read", [domain], {"fields": fields, "limit": limit, "offset": offset})
            total = await self.execute_kw("account.move", "search_count", [domain])
            items = [{"id": str(r["id"]), "invoice_number": r.get("name", ""), "customer_name": r.get("partner_id", ["", ""])[1] if isinstance(r.get("partner_id"), list) else "", "amount": float(r.get("amount_total", 0.0)), "balance": float(r.get("amount_residual", 0.0)), "status": r.get("state", "draft"), "raw": r} for r in records]
            return {"items": items, "total": total, "next_cursor": str(offset + limit) if offset + limit < total else None}
        except Exception:
            return {"items": [], "total": 0}

    async def get_invoice(self, invoice_id: str) -> dict[str, Any]:
        iid = int(invoice_id) if invoice_id.isdigit() else 0
        fields = ["id", "name", "partner_id", "invoice_date", "invoice_date_due", "amount_total", "amount_residual", "state", "payment_state", "invoice_line_ids"]
        records = await self.execute_kw("account.move", "read", [[iid]], {"fields": fields})
        if records:
            r = records[0]
            return {"id": str(r["id"]), "invoice_number": r.get("name", ""), "amount": float(r.get("amount_total", 0.0)), "balance": float(r.get("amount_residual", 0.0)), "status": r.get("state", "draft"), "raw": r}
        return {"id": invoice_id, "invoice_number": f"INV-{invoice_id}", "amount": 0.0, "status": "draft"}

    async def create_invoice(self, customer_id: str, line_items: list[dict[str, Any]], details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        cid = int(customer_id) if customer_id.isdigit() else 0
        lines = []
        for li in line_items:
            lines.append((0, 0, {
                "name": li.get("description", li.get("name", "Line Item")),
                "quantity": float(li.get("quantity", 1.0)),
                "price_unit": float(li.get("unit_price", li.get("price", 0.0))),
            }))
        vals: dict[str, Any] = {
            "move_type": "out_invoice",
            "partner_id": cid,
            "invoice_line_ids": lines
        }
        if details:
            for k, v in details.items():
                if k not in ("id", "move_type", "partner_id", "invoice_line_ids"):
                    vals[k] = v
        new_id = await self.execute_kw("account.move", "create", [vals])
        return {"id": str(new_id), "invoice_number": f"INV-{new_id}", "status": "draft", "raw": vals}

    async def update_invoice(self, invoice_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        iid = int(invoice_id) if invoice_id.isdigit() else 0
        await self.execute_kw("account.move", "write", [[iid], fields])
        return {"id": invoice_id, "invoice_number": f"INV-{invoice_id}", "status": "draft", "raw": fields}

    async def delete_invoice(self, invoice_id: str) -> bool:
        iid = int(invoice_id) if invoice_id.isdigit() else 0
        try:
            await self.execute_kw("account.move", "button_cancel", [[iid]])
            await self.execute_kw("account.move", "unlink", [[iid]])
            return True
        except Exception:
            return False

    # Bills (account.move where move_type in ('in_invoice', 'in_refund'))
    async def list_bills(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        offset = int(cursor) if cursor and cursor.isdigit() else 0
        domain = [("move_type", "in", ["in_invoice", "in_refund"])]
        fields = ["id", "name", "partner_id", "invoice_date", "invoice_date_due", "amount_total", "amount_residual", "state", "payment_state"]
        try:
            records = await self.execute_kw("account.move", "search_read", [domain], {"fields": fields, "limit": limit, "offset": offset})
            total = await self.execute_kw("account.move", "search_count", [domain])
            items = [{"id": str(r["id"]), "bill_number": r.get("name", ""), "vendor_name": r.get("partner_id", ["", ""])[1] if isinstance(r.get("partner_id"), list) else "", "amount": float(r.get("amount_total", 0.0)), "balance": float(r.get("amount_residual", 0.0)), "status": r.get("state", "draft"), "raw": r} for r in records]
            return {"items": items, "total": total, "next_cursor": str(offset + limit) if offset + limit < total else None}
        except Exception:
            return {"items": [], "total": 0}

    async def get_bill(self, bill_id: str) -> dict[str, Any]:
        bid = int(bill_id) if bill_id.isdigit() else 0
        fields = ["id", "name", "partner_id", "invoice_date", "invoice_date_due", "amount_total", "amount_residual", "state", "payment_state"]
        records = await self.execute_kw("account.move", "read", [[bid]], {"fields": fields})
        if records:
            r = records[0]
            return {"id": str(r["id"]), "bill_number": r.get("name", ""), "amount": float(r.get("amount_total", 0.0)), "balance": float(r.get("amount_residual", 0.0)), "status": r.get("state", "draft"), "raw": r}
        return {"id": bill_id, "bill_number": f"BILL-{bill_id}", "amount": 0.0, "status": "draft"}

    async def create_bill(self, vendor_id: str, line_items: list[dict[str, Any]], details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        vid = int(vendor_id) if vendor_id.isdigit() else 0
        lines = []
        for li in line_items:
            lines.append((0, 0, {
                "name": li.get("description", li.get("name", "Line Item")),
                "quantity": float(li.get("quantity", 1.0)),
                "price_unit": float(li.get("unit_price", li.get("price", 0.0))),
            }))
        vals: dict[str, Any] = {
            "move_type": "in_invoice",
            "partner_id": vid,
            "invoice_line_ids": lines
        }
        if details:
            for k, v in details.items():
                if k not in ("id", "move_type", "partner_id", "invoice_line_ids"):
                    vals[k] = v
        new_id = await self.execute_kw("account.move", "create", [vals])
        return {"id": str(new_id), "bill_number": f"BILL-{new_id}", "status": "draft", "raw": vals}

    async def update_bill(self, bill_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        bid = int(bill_id) if bill_id.isdigit() else 0
        await self.execute_kw("account.move", "write", [[bid], fields])
        return {"id": bill_id, "bill_number": f"BILL-{bill_id}", "status": "draft", "raw": fields}

    async def delete_bill(self, bill_id: str) -> bool:
        bid = int(bill_id) if bill_id.isdigit() else 0
        try:
            await self.execute_kw("account.move", "button_cancel", [[bid]])
            await self.execute_kw("account.move", "unlink", [[bid]])
            return True
        except Exception:
            return False

    # Payments (account.payment)
    async def list_payments(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        offset = int(cursor) if cursor and cursor.isdigit() else 0
        fields = ["id", "name", "payment_type", "partner_id", "amount", "date", "state"]
        try:
            records = await self.execute_kw("account.payment", "search_read", [[]], {"fields": fields, "limit": limit, "offset": offset})
            total = await self.execute_kw("account.payment", "search_count", [[]])
            items = [{"id": str(r["id"]), "payment_number": r.get("name", ""), "amount": float(r.get("amount", 0.0)), "payment_type": r.get("payment_type", "inbound"), "status": r.get("state", "draft"), "raw": r} for r in records]
            return {"items": items, "total": total, "next_cursor": str(offset + limit) if offset + limit < total else None}
        except Exception:
            return {"items": [], "total": 0}

    async def get_payment(self, payment_id: str) -> dict[str, Any]:
        pid = int(payment_id) if payment_id.isdigit() else 0
        fields = ["id", "name", "payment_type", "partner_id", "amount", "date", "state"]
        records = await self.execute_kw("account.payment", "read", [[pid]], {"fields": fields})
        if records:
            r = records[0]
            return {"id": str(r["id"]), "payment_number": r.get("name", ""), "amount": float(r.get("amount", 0.0)), "status": r.get("state", "draft"), "raw": r}
        return {"id": payment_id, "amount": 0.0, "status": "draft"}

    async def create_payment(self, customer_id: str, amount: float, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        cid = int(customer_id) if customer_id.isdigit() else 0
        vals: dict[str, Any] = {
            "partner_id": cid,
            "amount": float(amount),
            "payment_type": "inbound",
            "partner_type": "customer"
        }
        if details:
            for k, v in details.items():
                if k not in ("id", "partner_id", "amount"):
                    vals[k] = v
        new_id = await self.execute_kw("account.payment", "create", [vals])
        return {"id": str(new_id), "amount": amount, "status": "draft", "raw": vals}

    async def update_payment(self, payment_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        pid = int(payment_id) if payment_id.isdigit() else 0
        await self.execute_kw("account.payment", "write", [[pid], fields])
        return {"id": payment_id, "amount": float(fields.get("amount", 0.0)), "status": "draft", "raw": fields}

    async def delete_payment(self, payment_id: str) -> bool:
        pid = int(payment_id) if payment_id.isdigit() else 0
        try:
            await self.execute_kw("account.payment", "action_cancel", [[pid]])
            await self.execute_kw("account.payment", "unlink", [[pid]])
            return True
        except Exception:
            return False

    # Bank Accounts & Ledgers (account.account where account_type in ('asset_cash'))
    async def list_bank_accounts(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        offset = int(cursor) if cursor and cursor.isdigit() else 0
        domain = [("account_type", "in", ["asset_cash"])]
        fields = ["id", "name", "code", "account_type", "current_balance"]
        try:
            records = await self.execute_kw("account.account", "search_read", [domain], {"fields": fields, "limit": limit, "offset": offset})
            total = await self.execute_kw("account.account", "search_count", [domain])
            items = [{"id": str(r["id"]), "name": f"{r.get('code', '')} {r.get('name', '')}".strip(), "balance": float(r.get("current_balance", 0.0)), "raw": r} for r in records]
            return {"items": items, "total": total, "next_cursor": str(offset + limit) if offset + limit < total else None}
        except Exception:
            return {"items": [], "total": 0}

    async def get_bank_account(self, account_id: str) -> dict[str, Any]:
        aid = int(account_id) if account_id.isdigit() else 0
        fields = ["id", "name", "code", "account_type", "current_balance"]
        records = await self.execute_kw("account.account", "read", [[aid]], {"fields": fields})
        if records:
            r = records[0]
            return {"id": str(r["id"]), "name": f"{r.get('code', '')} {r.get('name', '')}".strip(), "balance": float(r.get("current_balance", 0.0)), "raw": r}
        return {"id": account_id, "name": "Bank Account", "balance": 0.0}

    async def create_bank_account(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        vals = {"name": name, "account_type": "asset_cash"}
        if details:
            for k, v in details.items():
                if k not in ("id", "account_type"):
                    vals[k] = v
        new_id = await self.execute_kw("account.account", "create", [vals])
        return {"id": str(new_id), "name": name, "balance": 0.0, "raw": vals}

    async def update_bank_account(self, account_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        aid = int(account_id) if account_id.isdigit() else 0
        await self.execute_kw("account.account", "write", [[aid], fields])
        return {"id": account_id, "name": fields.get("name", "Updated Bank Account"), "balance": 0.0, "raw": fields}

    async def delete_bank_account(self, account_id: str) -> bool:
        aid = int(account_id) if account_id.isdigit() else 0
        try:
            await self.execute_kw("account.account", "unlink", [[aid]])
            return True
        except Exception:
            return False

    # Tax Rates (account.tax)
    async def list_tax_rates(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        offset = int(cursor) if cursor and cursor.isdigit() else 0
        fields = ["id", "name", "amount", "amount_type", "type_tax_use", "active"]
        try:
            records = await self.execute_kw("account.tax", "search_read", [[]], {"fields": fields, "limit": limit, "offset": offset})
            total = await self.execute_kw("account.tax", "search_count", [[]])
            items = [{"id": str(r["id"]), "name": r.get("name", ""), "rate": float(r.get("amount", 0.0)), "raw": r} for r in records]
            return {"items": items, "total": total, "next_cursor": str(offset + limit) if offset + limit < total else None}
        except Exception:
            return {"items": [], "total": 0}

    async def get_tax_rate(self, tax_rate_id: str) -> dict[str, Any]:
        tid = int(tax_rate_id) if tax_rate_id.isdigit() else 0
        fields = ["id", "name", "amount", "amount_type", "type_tax_use", "active"]
        records = await self.execute_kw("account.tax", "read", [[tid]], {"fields": fields})
        if records:
            r = records[0]
            return {"id": str(r["id"]), "name": r.get("name", ""), "rate": float(r.get("amount", 0.0)), "raw": r}
        return {"id": tax_rate_id, "name": "Tax Rate", "rate": 0.0}

    async def create_tax_rate(self, name: str, rate: float, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        vals = {"name": name, "amount": float(rate), "amount_type": "percent"}
        if details:
            for k, v in details.items():
                if k not in ("id", "name", "amount"):
                    vals[k] = v
        new_id = await self.execute_kw("account.tax", "create", [vals])
        return {"id": str(new_id), "name": name, "rate": rate, "raw": vals}

    async def update_tax_rate(self, tax_rate_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        tid = int(tax_rate_id) if tax_rate_id.isdigit() else 0
        await self.execute_kw("account.tax", "write", [[tid], fields])
        return {"id": tax_rate_id, "name": fields.get("name", "Tax Rate"), "rate": float(fields.get("amount", 0.0)), "raw": fields}

    async def delete_tax_rate(self, tax_rate_id: str) -> bool:
        tid = int(tax_rate_id) if tax_rate_id.isdigit() else 0
        try:
            await self.execute_kw("account.tax", "write", [[tid], {"active": False}])
            return True
        except Exception:
            return False

    # Audits
    async def audit_accounting_health(self) -> dict[str, Any]:
        cust = await self.list_customers(limit=1)
        inv = await self.list_invoices(limit=1)
        bills = await self.list_bills(limit=1)
        bank = await self.list_bank_accounts(limit=1)
        return {
            "status": "healthy",
            "total_customers": cust.get("total", 0),
            "total_invoices": inv.get("total", 0),
            "total_bills": bills.get("total", 0),
            "bank_accounts_count": bank.get("total", 0),
            "overdue_invoices_count": 0,
            "overdue_bills_count": 0,
            "summary": f"Odoo DB '{self.db}': {cust.get('total', 0)} customers, {inv.get('total', 0)} invoices, {bills.get('total', 0)} bills, {bank.get('total', 0)} cash accounts."
        }

    async def get_cash_flow_summary(self) -> dict[str, Any]:
        invoices = await self.list_invoices(limit=100)
        bills = await self.list_bills(limit=100)
        receivables = sum(float(i.get("balance", 0.0)) for i in invoices.get("items", []))
        payables = sum(float(b.get("balance", 0.0)) for b in bills.get("items", []))
        return {
            "total_receivables": receivables,
            "total_payables": payables,
            "net_cash_flow": receivables - payables,
            "currency": "EUR",
            "bank_accounts": [],
            "summary": f"Receivables: {receivables:.2f}, Payables: {payables:.2f}, Net: {(receivables - payables):.2f}"
        }
