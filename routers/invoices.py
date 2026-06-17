import logging

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceUpdate
from services.invoices import InvoiceService, get_invoice_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.get("", response_model=list[InvoiceRead])
async def get_invoices(invoice_service: InvoiceService = Depends(get_invoice_service)):
    try:
        return await invoice_service.get_all()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching invoices")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{invoice_id}", response_model=InvoiceRead)
async def get_invoice(
    invoice_id: int,
    invoice_service: InvoiceService = Depends(get_invoice_service),
):
    try:
        invoice = await invoice_service.get_by_id(invoice_id=invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found",
            )
        return invoice
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching invoice %s", invoice_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    data: InvoiceCreate, invoice_service: InvoiceService = Depends(get_invoice_service)
):
    try:
        return await invoice_service.create(data=data)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error creating invoice")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.patch("/{invoice_id}", response_model=InvoiceRead)
async def update_invoice(
    invoice_id: int,
    data: InvoiceUpdate,
    invoice_service: InvoiceService = Depends(get_invoice_service),
):
    try:
        invoice = await invoice_service.update(invoice_id=invoice_id, data=data)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found",
            )
        return invoice
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error updating invoice %s", invoice_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(
    invoice_id: int,
    invoice_service: InvoiceService = Depends(get_invoice_service),
):
    try:
        deleted = await invoice_service.delete(invoice_id=invoice_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found",
            )
        return None
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error deleting invoice %s", invoice_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
