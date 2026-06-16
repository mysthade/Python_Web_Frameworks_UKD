from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class OrderToFeature(Base):
    __tablename__ = "order_to_features"

    order_id: Mapped[int] = mapped_column(ForeignKey("bot_orders.id"), primary_key=True)
    feature_id: Mapped[int] = mapped_column(
        ForeignKey("bot_features.id"), primary_key=True
    )
