"""Pydantic schemas for Odoo Accounting Connector (C27. Accounting & Bookkeeping)."""
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameter model."""
    pass

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Acme Odoo Accounting.")
    api_key: str = Field(description="Accounting API Key / OAuth Access Token.")
    base_url: str = Field(default="", description="Optional custom base URL or instance domain.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    base_url: str
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
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    customer_id: str = Field(description="Unique identifier of the customer.")

class CreateCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
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
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    invoice_id: str = Field(description="Unique identifier of the invoice.")

class CreateInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    invoice_id: str = Field(description="Unique identifier of the invoice.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    invoice_id: str = Field(description="Unique identifier of the invoice.")

class InvoiceRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class InvoiceList(BaseModel):
    items: list[InvoiceRecord]
    total: int
    next_cursor: Optional[str] = None

class ListBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bill_id: str = Field(description="Unique identifier of the bill.")

class CreateBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bill_id: str = Field(description="Unique identifier of the bill.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bill_id: str = Field(description="Unique identifier of the bill.")

class BillRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class BillList(BaseModel):
    items: list[BillRecord]
    total: int
    next_cursor: Optional[str] = None

class ListPaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetPaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payment_id: str = Field(description="Unique identifier of the payment.")

class CreatePaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdatePaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payment_id: str = Field(description="Unique identifier of the payment.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeletePaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payment_id: str = Field(description="Unique identifier of the payment.")

class PaymentRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class PaymentList(BaseModel):
    items: list[PaymentRecord]
    total: int
    next_cursor: Optional[str] = None

class ListBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bank_account_id: str = Field(description="Unique identifier of the bank_account.")

class CreateBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bank_account_id: str = Field(description="Unique identifier of the bank_account.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bank_account_id: str = Field(description="Unique identifier of the bank_account.")

class BankAccountRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class BankAccountList(BaseModel):
    items: list[BankAccountRecord]
    total: int
    next_cursor: Optional[str] = None

class ListTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page token.")

class GetTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    tax_rate_id: str = Field(description="Unique identifier of the tax_rate.")

class CreateTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Name or title of the record.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    tax_rate_id: str = Field(description="Unique identifier of the tax_rate.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    tax_rate_id: str = Field(description="Unique identifier of the tax_rate.")

class TaxRateRecord(BaseModel):
    id: str
    name: str
    status: str = "active"
    raw: dict[str, Any] = {}

class TaxRateList(BaseModel):
    items: list[TaxRateRecord]
    total: int
    next_cursor: Optional[str] = None

class AuditAccountingHealthResult(BaseModel):
    summary: str
    metrics: dict[str, Any]
    timestamp: str

class GetCashFlowSummaryResult(BaseModel):
    summary: str
    metrics: dict[str, Any]
    timestamp: str
