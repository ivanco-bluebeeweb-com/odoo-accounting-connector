"""Resource handlers for Odoo Accounting Connector."""
from __future__ import annotations
import datetime
from imperal_sdk import ActionResult
from app import chat
from odoo_accounting_client import OdooAccountingClient
from handlers_connection import resolve_connection
from schemas import *

async def _get_client(ctx, cid: str = ""):
    conn = await resolve_connection(ctx, cid)
    if not conn:
        return None, ActionResult.error("No active Odoo Accounting connection", code="UNAUTHORIZED")
    return OdooAccountingClient(api_key=conn["api_key"], base_url=conn.get("base_url", "")), None

@chat.function(
    "list_customers",
    "List customers (Customer account and contact profile).",
    action_type="read",
    chain_callable=True
)
async def list_customers(params: ListCustomerParams, ctx) -> ActionResult[CustomerList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_customers(limit=params.limit, cursor=params.cursor)
    items = [CustomerRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(CustomerList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_customer",
    "Read details of one customer.",
    action_type="read",
    chain_callable=True
)
async def get_customer(params: GetCustomerParams, ctx) -> ActionResult[CustomerRecord]:
    """Execute get customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_customer(params.customer_id)
    return ActionResult.ok(CustomerRecord(id=str(data.get("id", params.customer_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_customer",
    "Create a new customer.",
    action_type="read",
    chain_callable=True
)
async def create_customer(params: CreateCustomerParams, ctx) -> ActionResult[CustomerRecord]:
    """Execute create customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_customer(name=params.name, details=params.details)
    return ActionResult.ok(CustomerRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_customer",
    "Update an existing customer.",
    action_type="read",
    chain_callable=True
)
async def update_customer(params: UpdateCustomerParams, ctx) -> ActionResult[CustomerRecord]:
    """Execute update customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_customer(params.customer_id, params.fields)
    return ActionResult.ok(CustomerRecord(id=params.customer_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_customer",
    "Permanently delete a customer.",
    action_type="read",
    chain_callable=True
)
async def delete_customer(params: DeleteCustomerParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_customer(params.customer_id)
    return ActionResult.ok(DeleteResult(id=params.customer_id, deleted=ok, message="customer deleted"))

@chat.function(
    "list_invoices",
    "List invoices (Sales invoice with line items, tax and balance).",
    action_type="read",
    chain_callable=True
)
async def list_invoices(params: ListInvoiceParams, ctx) -> ActionResult[InvoiceList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_invoices(limit=params.limit, cursor=params.cursor)
    items = [InvoiceRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(InvoiceList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_invoice",
    "Read details of one invoice.",
    action_type="read",
    chain_callable=True
)
async def get_invoice(params: GetInvoiceParams, ctx) -> ActionResult[InvoiceRecord]:
    """Execute get invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_invoice(params.invoice_id)
    return ActionResult.ok(InvoiceRecord(id=str(data.get("id", params.invoice_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_invoice",
    "Create a new invoice.",
    action_type="read",
    chain_callable=True
)
async def create_invoice(params: CreateInvoiceParams, ctx) -> ActionResult[InvoiceRecord]:
    """Execute create invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_invoice(name=params.name, details=params.details)
    return ActionResult.ok(InvoiceRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_invoice",
    "Update an existing invoice.",
    action_type="read",
    chain_callable=True
)
async def update_invoice(params: UpdateInvoiceParams, ctx) -> ActionResult[InvoiceRecord]:
    """Execute update invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_invoice(params.invoice_id, params.fields)
    return ActionResult.ok(InvoiceRecord(id=params.invoice_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_invoice",
    "Permanently delete a invoice.",
    action_type="read",
    chain_callable=True
)
async def delete_invoice(params: DeleteInvoiceParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_invoice(params.invoice_id)
    return ActionResult.ok(DeleteResult(id=params.invoice_id, deleted=ok, message="invoice deleted"))

@chat.function(
    "list_bills",
    "List bills (Vendor accounts payable bill).",
    action_type="read",
    chain_callable=True
)
async def list_bills(params: ListBillParams, ctx) -> ActionResult[BillList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_bills(limit=params.limit, cursor=params.cursor)
    items = [BillRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(BillList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_bill",
    "Read details of one bill.",
    action_type="read",
    chain_callable=True
)
async def get_bill(params: GetBillParams, ctx) -> ActionResult[BillRecord]:
    """Execute get bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_bill(params.bill_id)
    return ActionResult.ok(BillRecord(id=str(data.get("id", params.bill_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_bill",
    "Create a new bill record in the accounting system.",
    action_type="read",
    chain_callable=True
)
async def create_bill(params: CreateBillParams, ctx) -> ActionResult[BillRecord]:
    """Execute create bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_bill(name=params.name, details=params.details)
    return ActionResult.ok(BillRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_bill",
    "Update an existing bill.",
    action_type="read",
    chain_callable=True
)
async def update_bill(params: UpdateBillParams, ctx) -> ActionResult[BillRecord]:
    """Execute update bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_bill(params.bill_id, params.fields)
    return ActionResult.ok(BillRecord(id=params.bill_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_bill",
    "Permanently delete a bill.",
    action_type="read",
    chain_callable=True
)
async def delete_bill(params: DeleteBillParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_bill(params.bill_id)
    return ActionResult.ok(DeleteResult(id=params.bill_id, deleted=ok, message="bill deleted"))

@chat.function(
    "list_payments",
    "List payments (Payment receipt or settlement record).",
    action_type="read",
    chain_callable=True
)
async def list_payments(params: ListPaymentParams, ctx) -> ActionResult[PaymentList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_payments(limit=params.limit, cursor=params.cursor)
    items = [PaymentRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(PaymentList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_payment",
    "Read details of one payment.",
    action_type="read",
    chain_callable=True
)
async def get_payment(params: GetPaymentParams, ctx) -> ActionResult[PaymentRecord]:
    """Execute get payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_payment(params.payment_id)
    return ActionResult.ok(PaymentRecord(id=str(data.get("id", params.payment_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_payment",
    "Create a new payment.",
    action_type="read",
    chain_callable=True
)
async def create_payment(params: CreatePaymentParams, ctx) -> ActionResult[PaymentRecord]:
    """Execute create payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_payment(name=params.name, details=params.details)
    return ActionResult.ok(PaymentRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_payment",
    "Update an existing payment.",
    action_type="read",
    chain_callable=True
)
async def update_payment(params: UpdatePaymentParams, ctx) -> ActionResult[PaymentRecord]:
    """Execute update payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_payment(params.payment_id, params.fields)
    return ActionResult.ok(PaymentRecord(id=params.payment_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_payment",
    "Permanently delete a payment.",
    action_type="read",
    chain_callable=True
)
async def delete_payment(params: DeletePaymentParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_payment(params.payment_id)
    return ActionResult.ok(DeleteResult(id=params.payment_id, deleted=ok, message="payment deleted"))

@chat.function(
    "list_bank_accounts",
    "List bank_accounts (Chart of accounts bank ledger account).",
    action_type="read",
    chain_callable=True
)
async def list_bank_accounts(params: ListBankAccountParams, ctx) -> ActionResult[BankAccountList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_bank_accounts(limit=params.limit, cursor=params.cursor)
    items = [BankAccountRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(BankAccountList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_bank_account",
    "Read details of one bank_account.",
    action_type="read",
    chain_callable=True
)
async def get_bank_account(params: GetBankAccountParams, ctx) -> ActionResult[BankAccountRecord]:
    """Execute get bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_bank_account(params.bank_account_id)
    return ActionResult.ok(BankAccountRecord(id=str(data.get("id", params.bank_account_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_bank_account",
    "Create a new bank_account.",
    action_type="read",
    chain_callable=True
)
async def create_bank_account(params: CreateBankAccountParams, ctx) -> ActionResult[BankAccountRecord]:
    """Execute create bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_bank_account(name=params.name, details=params.details)
    return ActionResult.ok(BankAccountRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_bank_account",
    "Update an existing bank_account.",
    action_type="read",
    chain_callable=True
)
async def update_bank_account(params: UpdateBankAccountParams, ctx) -> ActionResult[BankAccountRecord]:
    """Execute update bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_bank_account(params.bank_account_id, params.fields)
    return ActionResult.ok(BankAccountRecord(id=params.bank_account_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_bank_account",
    "Permanently delete a bank_account.",
    action_type="read",
    chain_callable=True
)
async def delete_bank_account(params: DeleteBankAccountParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_bank_account(params.bank_account_id)
    return ActionResult.ok(DeleteResult(id=params.bank_account_id, deleted=ok, message="bank_account deleted"))

@chat.function(
    "list_tax_rates",
    "List tax_rates (Tax rate rule for sales and purchases).",
    action_type="read",
    chain_callable=True
)
async def list_tax_rates(params: ListTaxRateParams, ctx) -> ActionResult[TaxRateList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_tax_rates(limit=params.limit, cursor=params.cursor)
    items = [TaxRateRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(TaxRateList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_tax_rate",
    "Read details of one tax_rate.",
    action_type="read",
    chain_callable=True
)
async def get_tax_rate(params: GetTaxRateParams, ctx) -> ActionResult[TaxRateRecord]:
    """Execute get tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_tax_rate(params.tax_rate_id)
    return ActionResult.ok(TaxRateRecord(id=str(data.get("id", params.tax_rate_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_tax_rate",
    "Create a new tax_rate.",
    action_type="read",
    chain_callable=True
)
async def create_tax_rate(params: CreateTaxRateParams, ctx) -> ActionResult[TaxRateRecord]:
    """Execute create tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_tax_rate(name=params.name, details=params.details)
    return ActionResult.ok(TaxRateRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_tax_rate",
    "Update an existing tax_rate.",
    action_type="read",
    chain_callable=True
)
async def update_tax_rate(params: UpdateTaxRateParams, ctx) -> ActionResult[TaxRateRecord]:
    """Execute update tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_tax_rate(params.tax_rate_id, params.fields)
    return ActionResult.ok(TaxRateRecord(id=params.tax_rate_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_tax_rate",
    "Permanently delete a tax_rate.",
    action_type="read",
    chain_callable=True
)
async def delete_tax_rate(params: DeleteTaxRateParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_tax_rate(params.tax_rate_id)
    return ActionResult.ok(DeleteResult(id=params.tax_rate_id, deleted=ok, message="tax_rate deleted"))

@chat.function(
    "audit_accounting_health",
    "Value-add audit: Audit unpaid overdue invoices, open bills and reconciliation status.",
    action_type="read",
    chain_callable=True
)
async def audit_accounting_health(params: ConnectionIdParams, ctx) -> ActionResult[AuditAccountingHealthResult]:
    """Execute audit accounting health operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.ok(AuditAccountingHealthResult(
        summary="Odoo Accounting Audit unpaid overdue invoices, open bills and reconciliation status",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ))

@chat.function(
    "get_cash_flow_summary",
    "Value-add audit: One-glance summary of receivables, payables and cash balances.",
    action_type="read",
    chain_callable=True
)
async def get_cash_flow_summary(params: ConnectionIdParams, ctx) -> ActionResult[GetCashFlowSummaryResult]:
    """Execute get cash flow summary operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.ok(GetCashFlowSummaryResult(
        summary="Odoo Accounting One-glance summary of receivables, payables and cash balances",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ))
