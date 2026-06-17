from fastapi import APIRouter, Depends, HTTPException, status

from core.handlers import run_handler
from schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceUpdate
from services.invoices import InvoiceService, get_invoice_service

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.get("", response_model=list[InvoiceRead])
async def get_invoices(invoice_service: InvoiceService = Depends(get_invoice_service)):
    return await run_handler(
        lambda: invoice_service.get_all(),
        log_message="Error fetching invoices",
    )


@router.get("/{invoice_id}", response_model=InvoiceRead)
async def get_invoice(
    invoice_id: int,
    invoice_service: InvoiceService = Depends(get_invoice_service),
):
    async def handler():
        invoice = await invoice_service.get_by_id(invoice_id=invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found",
            )
        return invoice

    return await run_handler(
        handler,
        log_message="Error fetching invoice %s",
        log_args=(invoice_id,),
    )


@router.post("", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    data: InvoiceCreate,
    invoice_service: InvoiceService = Depends(get_invoice_service),
):
    return await run_handler(
        lambda: invoice_service.create(data=data),
        log_message="Error creating invoice",
    )


@router.patch("/{invoice_id}", response_model=InvoiceRead)
async def update_invoice(
    invoice_id: int,
    data: InvoiceUpdate,
    invoice_service: InvoiceService = Depends(get_invoice_service),
):
    async def handler():
        invoice = await invoice_service.update(invoice_id=invoice_id, data=data)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found",
            )
        return invoice

    return await run_handler(
        handler,
        log_message="Error updating invoice %s",
        log_args=(invoice_id,),
    )


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(
    invoice_id: int,
    invoice_service: InvoiceService = Depends(get_invoice_service),
):
    async def handler():
        deleted = await invoice_service.delete(invoice_id=invoice_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found",
            )
        return None

    return await run_handler(
        handler,
        log_message="Error deleting invoice %s",
        log_args=(invoice_id,),
    )
