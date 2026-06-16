import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.invoice import Invoice
from schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceUpdate
from settings.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/invoices", tags=["Invoices"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[InvoiceRead])
async def get_invoices(session: SessionDepend):
    try:
        result = await session.execute(select(Invoice))
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching invoices")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{invoice_id}", response_model=InvoiceRead)
async def get_invoice(invoice_id: int, session: SessionDepend):
    try:
        invoice = await session.get(Invoice, invoice_id)
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
async def create_invoice(data: InvoiceCreate, session: SessionDepend):
    try:
        invoice = Invoice(**data.model_dump())
        session.add(invoice)
        await session.flush()
        await session.refresh(invoice)
        return invoice
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error creating invoice")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.patch("/{invoice_id}", response_model=InvoiceRead)
async def update_invoice(invoice_id: int, data: InvoiceUpdate, session: SessionDepend):
    try:
        invoice = await session.get(Invoice, invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found",
            )
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(invoice, key, value)
        await session.flush()
        await session.refresh(invoice)
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
async def delete_invoice(invoice_id: int, session: SessionDepend):
    try:
        invoice = await session.get(Invoice, invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found",
            )
        await session.delete(invoice)
        return None
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error deleting invoice %s", invoice_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
