from pydantic import BaseModel, Field
from datetime import datetime

class OrderItemSchema(BaseModel):
    item_id: int
    item_name:str
    count: int = Field(ge=0)
    item_price: float

class OrderSchema(BaseModel):
    id: int
    items: list[OrderItemSchema]
    created_at: datetime = datetime.now()
    price: float

