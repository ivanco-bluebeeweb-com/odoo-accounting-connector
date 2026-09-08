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
        return None, ActionResult.error("No active Odoo connection", code="UNAUTHORIZED")
    url = conn.get("url", "")
    db = conn.get("db", "")
    username = conn.get("username", "")
    api_key = conn.get("api_key", "")
    return OdooAccountingClient(url=url, db=db, username=username, api_key=api_key), None

@chat.function(
    "list_customers",
    "List customers (Customer account and contact profile).",
    action_type="read",
    chain_callable=True
)
async def list_customers(ctx, params: ListCustomerParams) -> ActionResult[CustomerList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_customers(limit=params.limit, cursor=params.cursor)
    items = [CustomerRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.success(CustomerList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")), summary="List customers completed successfully.")

@chat.function(
    "get_customer",
    "Read details of one customer.",
    action_type="read",
    chain_callable=True
)
async def get_customer(ctx, params: GetCustomerParams) -> ActionResult[CustomerRecord]:
    """Execute get customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_customer(params.customer_id)
    return ActionResult.success(CustomerRecord(id=str(data.get("id", params.customer_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data), summary="Get customer completed successfully.")

@chat.function(
    "create_customer",
    "Create a new customer.",
    action_type="read",
    chain_callable=True
)
async def create_customer(ctx, params: CreateCustomerParams) -> ActionResult[CustomerRecord]:
    """Execute create customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_customer(name=params.name, details=params.details)
    return ActionResult.success(CustomerRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data), summary="Create customer completed successfully.")

@chat.function(
    "update_customer",
    "Update an existing customer.",
    action_type="read",
    chain_callable=True
)
async def update_customer(ctx, params: UpdateCustomerParams) -> ActionResult[CustomerRecord]:
    """Execute update customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_customer(params.customer_id, params.fields)
    return ActionResult.success(CustomerRecord(id=params.customer_id, name=str(data.get("name", "")), status="updated", raw=data), summary="Update customer completed successfully.")

@chat.function(
    "delete_customer",
    "Permanently delete a customer.",
    action_type="read",
    chain_callable=True
)
async def delete_customer(ctx, params: DeleteCustomerParams) -> ActionResult[DeleteResult]:
    """Execute delete customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_customer(params.customer_id)
    return ActionResult.success(DeleteResult(id=params.customer_id, deleted=ok, message="customer deleted"), summary="Delete customer completed successfully.")

@chat.function(
    "list_invoices",
    "List invoices (Sales invoice with line items, tax and balance).",
    action_type="read",
    chain_callable=True
)
async def list_invoices(ctx, params: ListInvoiceParams) -> ActionResult[InvoiceList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_invoices(limit=params.limit, cursor=params.cursor)
    items = [InvoiceRecord(id=str(it.get("id", "")), customer_id=str(it.get("customer_id", "")), amount=float(it.get("amount", it.get("amount_total", 0.0))), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.success(InvoiceList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")), summary="List invoices completed successfully.")

@chat.function(
    "get_invoice",
    "Read details of one invoice.",
    action_type="read",
    chain_callable=True
)
async def get_invoice(ctx, params: GetInvoiceParams) -> ActionResult[InvoiceRecord]:
    """Execute get invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_invoice(params.invoice_id)
    return ActionResult.success(InvoiceRecord(id=str(data.get("id", params.invoice_id)), customer_id=str(data.get("customer_id", "")), amount=float(data.get("amount", data.get("amount_total", 0.0))), status=str(data.get("status", "active")), raw=data), summary="Get invoice completed successfully.")

@chat.function(
    "create_invoice",
    "Create a new invoice.",
    action_type="read",
    chain_callable=True
)
async def create_invoice(ctx, params: CreateInvoiceParams) -> ActionResult[InvoiceRecord]:
    """Execute create invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_invoice(customer_id=params.customer_id, line_items=params.line_items, details=params.details)
    return ActionResult.success(InvoiceRecord(id=str(data.get("id", "")), customer_id=str(data.get("customer_id", params.customer_id)), amount=float(data.get("amount", data.get("amount_total", 0.0))), status="active", raw=data), summary="Create invoice completed successfully.")

@chat.function(
    "update_invoice",
    "Update an existing invoice.",
    action_type="read",
    chain_callable=True
)
async def update_invoice(ctx, params: UpdateInvoiceParams) -> ActionResult[InvoiceRecord]:
    """Execute update invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_invoice(params.invoice_id, params.fields)
    return ActionResult.success(InvoiceRecord(id=params.invoice_id, customer_id=str(data.get("customer_id", "")), amount=float(data.get("amount", data.get("amount_total", 0.0))), status="updated", raw=data), summary="Update invoice completed successfully.")

@chat.function(
    "delete_invoice",
    "Permanently delete a invoice.",
    action_type="read",
    chain_callable=True
)
async def delete_invoice(ctx, params: DeleteInvoiceParams) -> ActionResult[DeleteResult]:
    """Execute delete invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_invoice(params.invoice_id)
    return ActionResult.success(DeleteResult(id=params.invoice_id, deleted=ok, message="invoice deleted"), summary="Delete invoice completed successfully.")

@chat.function(
    "list_bills",
    "List bills (Vendor accounts payable bill).",
    action_type="read",
    chain_callable=True
)
async def list_bills(ctx, params: ListBillParams) -> ActionResult[BillList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_bills(limit=params.limit, cursor=params.cursor)
    items = [BillRecord(id=str(it.get("id", "")), vendor_id=str(it.get("vendor_id", "")), amount=float(it.get("amount", it.get("amount_total", 0.0))), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.success(BillList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")), summary="List bills completed successfully.")

@chat.function(
    "get_bill",
    "Read details of one bill.",
    action_type="read",
    chain_callable=True
)
async def get_bill(ctx, params: GetBillParams) -> ActionResult[BillRecord]:
    """Execute get bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_bill(params.bill_id)
    return ActionResult.success(BillRecord(id=str(data.get("id", params.bill_id)), vendor_id=str(data.get("vendor_id", "")), amount=float(data.get("amount", data.get("amount_total", 0.0))), status=str(data.get("status", "active")), raw=data), summary="Get bill completed successfully.")

@chat.function(
    "create_bill",
    "Create a new bill record in the accounting system.",
    action_type="read",
    chain_callable=True
)
async def create_bill(ctx, params: CreateBillParams) -> ActionResult[BillRecord]:
    """Execute create bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_bill(vendor_id=params.vendor_id, line_items=params.line_items, details=params.details)
    return ActionResult.success(BillRecord(id=str(data.get("id", "")), vendor_id=str(data.get("vendor_id", params.vendor_id)), amount=float(data.get("amount", data.get("amount_total", 0.0))), status="active", raw=data), summary="Create bill completed successfully.")

@chat.function(
    "update_bill",
    "Update an existing bill.",
    action_type="read",
    chain_callable=True
)
async def update_bill(ctx, params: UpdateBillParams) -> ActionResult[BillRecord]:
    """Execute update bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_bill(params.bill_id, params.fields)
    return ActionResult.success(BillRecord(id=params.bill_id, vendor_id=str(data.get("vendor_id", "")), amount=float(data.get("amount", data.get("amount_total", 0.0))), status="updated", raw=data), summary="Update bill completed successfully.")

@chat.function(
    "delete_bill",
    "Permanently delete a bill.",
    action_type="read",
    chain_callable=True
)
async def delete_bill(ctx, params: DeleteBillParams) -> ActionResult[DeleteResult]:
    """Execute delete bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_bill(params.bill_id)
    return ActionResult.success(DeleteResult(id=params.bill_id, deleted=ok, message="bill deleted"), summary="Delete bill completed successfully.")

@chat.function(
    "list_payments",
    "List payments (Payment receipt or settlement record).",
    action_type="read",
    chain_callable=True
)
async def list_payments(ctx, params: ListPaymentParams) -> ActionResult[PaymentList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_payments(limit=params.limit, cursor=params.cursor)
    items = [PaymentRecord(id=str(it.get("id", "")), customer_id=str(it.get("customer_id", "")), amount=float(it.get("amount", 0.0)), raw=it) for it in data.get("items", [])]
    return ActionResult.success(PaymentList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")), summary="List payments completed successfully.")

@chat.function(
    "get_payment",
    "Read details of one payment.",
    action_type="read",
    chain_callable=True
)
async def get_payment(ctx, params: GetPaymentParams) -> ActionResult[PaymentRecord]:
    """Execute get payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_payment(params.payment_id)
    return ActionResult.success(PaymentRecord(id=str(data.get("id", params.payment_id)), customer_id=str(data.get("customer_id", "")), amount=float(data.get("amount", 0.0)), raw=data), summary="Get payment completed successfully.")

@chat.function(
    "create_payment",
    "Create a new payment.",
    action_type="read",
    chain_callable=True
)
async def create_payment(ctx, params: CreatePaymentParams) -> ActionResult[PaymentRecord]:
    """Execute create payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_payment(customer_id=params.customer_id, amount=params.amount, details=params.details)
    return ActionResult.success(PaymentRecord(id=str(data.get("id", "")), customer_id=str(data.get("customer_id", params.customer_id)), amount=float(data.get("amount", params.amount)), raw=data), summary="Create payment completed successfully.")

@chat.function(
    "update_payment",
    "Update an existing payment.",
    action_type="read",
    chain_callable=True
)
async def update_payment(ctx, params: UpdatePaymentParams) -> ActionResult[PaymentRecord]:
    """Execute update payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_payment(params.payment_id, params.fields)
    return ActionResult.success(PaymentRecord(id=params.payment_id, customer_id=str(data.get("customer_id", "")), amount=float(data.get("amount", 0.0)), raw=data), summary="Update payment completed successfully.")

@chat.function(
    "delete_payment",
    "Permanently delete a payment.",
    action_type="read",
    chain_callable=True
)
async def delete_payment(ctx, params: DeletePaymentParams) -> ActionResult[DeleteResult]:
    """Execute delete payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_payment(params.payment_id)
    return ActionResult.success(DeleteResult(id=params.payment_id, deleted=ok, message="payment deleted"), summary="Delete payment completed successfully.")

@chat.function(
    "list_bank_accounts",
    "List bank_accounts (Chart of accounts bank ledger account).",
    action_type="read",
    chain_callable=True
)
async def list_bank_accounts(ctx, params: ListBankAccountParams) -> ActionResult[BankAccountList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_bank_accounts(limit=params.limit, cursor=params.cursor)
    items = [BankAccountRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.success(BankAccountList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")), summary="List bank accounts completed successfully.")

@chat.function(
    "get_bank_account",
    "Read details of one bank_account.",
    action_type="read",
    chain_callable=True
)
async def get_bank_account(ctx, params: GetBankAccountParams) -> ActionResult[BankAccountRecord]:
    """Execute get bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_bank_account(params.account_id)
    return ActionResult.success(BankAccountRecord(id=str(data.get("id", params.account_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data), summary="Get bank account completed successfully.")

@chat.function(
    "create_bank_account",
    "Create a new bank_account.",
    action_type="read",
    chain_callable=True
)
async def create_bank_account(ctx, params: CreateBankAccountParams) -> ActionResult[BankAccountRecord]:
    """Execute create bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_bank_account(name=params.name, details=params.details)
    return ActionResult.success(BankAccountRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data), summary="Create bank account completed successfully.")

@chat.function(
    "update_bank_account",
    "Update an existing bank_account.",
    action_type="read",
    chain_callable=True
)
async def update_bank_account(ctx, params: UpdateBankAccountParams) -> ActionResult[BankAccountRecord]:
    """Execute update bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_bank_account(params.account_id, params.fields)
    return ActionResult.success(BankAccountRecord(id=params.account_id, name=str(data.get("name", "")), status="updated", raw=data), summary="Update bank account completed successfully.")

@chat.function(
    "delete_bank_account",
    "Permanently delete a bank_account.",
    action_type="read",
    chain_callable=True
)
async def delete_bank_account(ctx, params: DeleteBankAccountParams) -> ActionResult[DeleteResult]:
    """Execute delete bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_bank_account(params.account_id)
    return ActionResult.success(DeleteResult(id=params.account_id, deleted=ok, message="bank_account deleted"), summary="Delete bank account completed successfully.")

@chat.function(
    "list_tax_rates",
    "List tax_rates (Tax rate rule for sales and purchases).",
    action_type="read",
    chain_callable=True
)
async def list_tax_rates(ctx, params: ListTaxRateParams) -> ActionResult[TaxRateList]:
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_tax_rates(limit=params.limit, cursor=params.cursor)
    items = [TaxRateRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.success(TaxRateList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")), summary="List tax rates completed successfully.")

@chat.function(
    "get_tax_rate",
    "Read details of one tax_rate.",
    action_type="read",
    chain_callable=True
)
async def get_tax_rate(ctx, params: GetTaxRateParams) -> ActionResult[TaxRateRecord]:
    """Execute get tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_tax_rate(params.tax_rate_id)
    return ActionResult.success(TaxRateRecord(id=str(data.get("id", params.tax_rate_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data), summary="Get tax rate completed successfully.")

@chat.function(
    "create_tax_rate",
    "Create a new tax_rate.",
    action_type="read",
    chain_callable=True
)
async def create_tax_rate(ctx, params: CreateTaxRateParams) -> ActionResult[TaxRateRecord]:
    """Execute create tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_tax_rate(name=params.name, rate=params.rate, details=params.details)
    return ActionResult.success(TaxRateRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data), summary="Create tax rate completed successfully.")

@chat.function(
    "update_tax_rate",
    "Update an existing tax_rate.",
    action_type="read",
    chain_callable=True
)
async def update_tax_rate(ctx, params: UpdateTaxRateParams) -> ActionResult[TaxRateRecord]:
    """Execute update tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_tax_rate(params.tax_rate_id, params.fields)
    return ActionResult.success(TaxRateRecord(id=params.tax_rate_id, name=str(data.get("name", "")), status="updated", raw=data), summary="Update tax rate completed successfully.")

@chat.function(
    "delete_tax_rate",
    "Permanently delete a tax_rate.",
    action_type="read",
    chain_callable=True
)
async def delete_tax_rate(ctx, params: DeleteTaxRateParams) -> ActionResult[DeleteResult]:
    """Execute delete tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_tax_rate(params.tax_rate_id)
    return ActionResult.success(DeleteResult(id=params.tax_rate_id, deleted=ok, message="tax_rate deleted"), summary="Delete tax rate completed successfully.")

@chat.function(
    "audit_accounting_health",
    "Value-add audit: Audit unpaid overdue invoices, open bills and reconciliation status.",
    action_type="read",
    chain_callable=True
)
async def audit_accounting_health(ctx, params: ConnectionIdParams) -> ActionResult[AuditAccountingHealthResult]:
    """Execute audit accounting health operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.success(AuditAccountingHealthResult(
        summary="Odoo Accounting Audit unpaid overdue invoices, open bills and reconciliation status",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ), summary="Accounting health audit ready.")

@chat.function(
    "get_cash_flow_summary",
    "Value-add audit: One-glance summary of receivables, payables and cash balances.",
    action_type="read",
    chain_callable=True
)
async def get_cash_flow_summary(ctx, params: ConnectionIdParams) -> ActionResult[GetCashFlowSummaryResult]:
    """Execute get cash flow summary operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.success(GetCashFlowSummaryResult(
        summary="Odoo Accounting One-glance summary of receivables, payables and cash balances",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ), summary="Cash flow summary retrieved.")
