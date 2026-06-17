from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.invoice import Invoice
from schemas.invoice import InvoiceCreate, InvoiceUpdate
from settings.db import get_db


class InvoiceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[Invoice]:
        result = await self.db.execute(select(Invoice))
        return result.scalars().all()

    async def get_by_id(self, invoice_id: int) -> Invoice | None:
        return await self.db.get(Invoice, invoice_id)

    async def create(self, data: InvoiceCreate) -> Invoice:
        invoice = Invoice(**data.model_dump())
        self.db.add(invoice)
        await self.db.commit()
        await self.db.refresh(invoice)
        return invoice

    async def update(self, invoice_id: int, data: InvoiceUpdate) -> Invoice | None:
        invoice = await self.get_by_id(invoice_id)
        if not invoice:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(invoice, key, value)
        self.db.add(invoice)
        await self.db.commit()
        await self.db.refresh(invoice)
        return invoice

    async def delete(self, invoice_id: int) -> bool:
        invoice = await self.get_by_id(invoice_id)
        if not invoice:
            return False
        await self.db.delete(invoice)
        await self.db.commit()
        return True


async def get_invoice_service(db: AsyncSession = Depends(get_db)) -> InvoiceService:
    return InvoiceService(db)
