from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.bot_order import BotOrder


class BotFeature(Base):
    __tablename__ = "bot_features"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)

    orders: Mapped[list["BotOrder"]] = relationship(
        secondary="order_to_features", back_populates="features"
    )
