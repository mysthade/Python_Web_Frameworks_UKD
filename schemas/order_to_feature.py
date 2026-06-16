from pydantic import BaseModel, ConfigDict


class OrderToFeatureCreate(BaseModel):
    order_id: int
    feature_id: int


class OrderToFeatureRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    feature_id: int
