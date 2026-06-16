import enum
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.bot_feature import BotFeature
    from models.invoice import Invoice
    from models.user import User


class BotOrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    TESTING = "TESTING"
    COMPLETED = "COMPLETED"


class BotOrder(Base):
    __tablename__ = "bot_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[BotOrderStatus] = mapped_column(Enum(BotOrderStatus))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    client: Mapped["User"] = relationship(back_populates="orders")
    invoice: Mapped["Invoice | None"] = relationship(
        back_populates="order", uselist=False
    )
    features: Mapped[list["BotFeature"]] = relationship(
        secondary="order_to_features", back_populates="orders"
    )
