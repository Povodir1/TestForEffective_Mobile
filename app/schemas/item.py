from pydantic import BaseModel, Field
from typing import Optional


class ItemShortSchema(BaseModel):
    id: int
    name: str
    price: float
    info:str | None
    stock: int = Field(ge=0)

class ItemCreateSchema(BaseModel):
    name: str
    price: float = 0
    info: str|None = None
    stock: int = Field(ge=0)

class ItemPatchSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    info: Optional[str] = None
    stock: Optional[int] = None
