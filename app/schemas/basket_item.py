from pydantic import BaseModel,Field
from app.schemas.item import ItemShortSchema

class ItemInBasketScheme(BaseModel):
    item:ItemShortSchema
    count:int = Field(ge=1)

class BasketSchema(BaseModel):
    items:list[ItemInBasketScheme]
    full_price: float
