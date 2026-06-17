from models.invoice import Invoice
from schemas.invoice import InvoiceCreate, InvoiceUpdate
from services.base import BaseCRUDService, service_dependency


class InvoiceService(BaseCRUDService[Invoice, InvoiceCreate, InvoiceUpdate]):
    model = Invoice


get_invoice_service = service_dependency(InvoiceService)
