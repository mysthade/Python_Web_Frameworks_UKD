from typing import Optional

from pydantic import BaseModel, ConfigDict


class BotFeatureCreate(BaseModel):
    name: str
    description: str


class BotFeatureRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str


class BotFeatureUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
