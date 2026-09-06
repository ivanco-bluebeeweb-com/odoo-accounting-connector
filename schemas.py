"""Pydantic schemas for Odoo Accounting Connector (C27. Accounting & Bookkeeping)."""
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameter model."""
    pass

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Acme Odoo ERP.")
    url: str = Field(description="Odoo instance URL (e.g. https://mycompany.odoo.com or self-hosted).")
    db: str = Field(description="Odoo database name.")
    username: str = Field(description="Odoo user email or login.")
    api_key: str = Field(description="Odoo API Key or account password.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    url: str
    db: str
    username: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int

class DeleteResult(BaseModel):
    id: str
    deleted: bool
    message: str

class ListCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination offset / cursor.")

class GetCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    customer_id: str = Field(description="Unique identifier of the customer.")

class CreateCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the customer.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    customer_id: str = Field(description="Unique identifier of the customer.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    customer_id: str = Field(description="Unique identifier of the customer.")

class CustomerRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class CustomerList(BaseModel):
    items: list[CustomerRecord]
    total: int
    next_cursor: Optional[str] = None

class ListInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination offset / cursor.")

class GetInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    invoice_id: str = Field(description="Unique identifier of the invoice.")

class CreateInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    customer_id: str = Field(description="Customer identifier.")
    line_items: list[dict[str, Any]] = Field(default=[], description="Invoice line items.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Additional invoice fields.")

class UpdateInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    invoice_id: str = Field(description="Unique identifier of the invoice.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    invoice_id: str = Field(description="Unique identifier of the invoice.")

class InvoiceRecord(BaseModel):
    id: str
    customer_id: str
    amount: float
    status: str
    raw: dict[str, Any] = {}

class InvoiceList(BaseModel):
    items: list[InvoiceRecord]
    total: int
    next_cursor: Optional[str] = None

class ListBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination offset / cursor.")

class GetBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bill_id: str = Field(description="Unique identifier of the bill.")

class CreateBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    vendor_id: str = Field(description="Vendor identifier.")
    line_items: list[dict[str, Any]] = Field(default=[], description="Bill line items.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Additional bill fields.")

class UpdateBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bill_id: str = Field(description="Unique identifier of the bill.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bill_id: str = Field(description="Unique identifier of the bill.")

class BillRecord(BaseModel):
    id: str
    vendor_id: str
    amount: float
    status: str
    raw: dict[str, Any] = {}

class BillList(BaseModel):
    items: list[BillRecord]
    total: int
    next_cursor: Optional[str] = None

class ListPaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination offset / cursor.")

class GetPaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payment_id: str = Field(description="Unique identifier of the payment.")

class CreatePaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    customer_id: str = Field(description="Customer identifier.")
    amount: float = Field(description="Payment amount.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Payment details.")

class UpdatePaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payment_id: str = Field(description="Unique identifier of the payment.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeletePaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payment_id: str = Field(description="Unique identifier of the payment.")

class PaymentRecord(BaseModel):
    id: str
    customer_id: str
    amount: float
    raw: dict[str, Any] = {}

class PaymentList(BaseModel):
    items: list[PaymentRecord]
    total: int
    next_cursor: Optional[str] = None

class ListBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination offset / cursor.")

class GetBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    account_id: str = Field(description="Unique identifier of the bank account.")

class CreateBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Bank account name.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Bank account details.")

class UpdateBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    account_id: str = Field(description="Unique identifier of the bank account.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    account_id: str = Field(description="Unique identifier of the bank account.")

class BankAccountRecord(BaseModel):
    id: str
    name: str
    balance: float = 0.0
    raw: dict[str, Any] = {}

class BankAccountList(BaseModel):
    items: list[BankAccountRecord]
    total: int
    next_cursor: Optional[str] = None

class ListTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination offset / cursor.")

class GetTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    tax_rate_id: str = Field(description="Unique identifier of the tax rate.")

class CreateTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Tax rate name.")
    rate: float = Field(description="Tax percentage rate.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Tax rate details.")

class UpdateTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    tax_rate_id: str = Field(description="Unique identifier of the tax rate.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    tax_rate_id: str = Field(description="Unique identifier of the tax rate.")

class TaxRateRecord(BaseModel):
    id: str
    name: str
    rate: float = 0.0
    raw: dict[str, Any] = {}

class TaxRateList(BaseModel):
    items: list[TaxRateRecord]
    total: int
    next_cursor: Optional[str] = None

class AuditAccountingHealthResult(BaseModel):
    status: str = "healthy"
    total_customers: int = 0
    total_invoices: int = 0
    total_bills: int = 0
    bank_accounts_count: int = 0
    overdue_invoices_count: int = 0
    overdue_bills_count: int = 0
    summary: str = ""

class GetCashFlowSummaryResult(BaseModel):
    total_receivables: float = 0.0
    total_payables: float = 0.0
    net_cash_flow: float = 0.0
    currency: str = "EUR"
    bank_accounts: list[dict[str, Any]] = []
    summary: str = ""
