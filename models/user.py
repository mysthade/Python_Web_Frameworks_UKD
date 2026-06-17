import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.bot_order import BotOrder
    from models.profile import Profile


class UserRole(str, enum.Enum):
    CLIENT = "CLIENT"
    DEVELOPER = "DEVELOPER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(
        String(255), server_default="", nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, server_default=text("true"), nullable=False
    )
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    profile: Mapped["Profile | None"] = relationship(
        back_populates="user", uselist=False
    )
    orders: Mapped[list["BotOrder"]] = relationship(back_populates="client")
