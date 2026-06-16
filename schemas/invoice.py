from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class InvoiceCreate(BaseModel):
    amount: Decimal
    is_paid: bool = False
    order_id: int


class InvoiceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal
    is_paid: bool
    issued_at: datetime
    order_id: int


class InvoiceUpdate(BaseModel):
    amount: Optional[Decimal] = None
    is_paid: Optional[bool] = None
    order_id: Optional[int] = None
