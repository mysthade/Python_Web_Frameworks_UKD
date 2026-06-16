from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProfileCreate(BaseModel):
    telegram_username: Optional[str] = None
    phone: Optional[str] = None
    user_id: int


class ProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_username: Optional[str] = None
    phone: Optional[str] = None
    user_id: int


class ProfileUpdate(BaseModel):
    telegram_username: Optional[str] = None
    phone: Optional[str] = None
    user_id: Optional[int] = None
