
from sqlalchemy import Column, Integer, String, DECIMAL, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    info = Column(Text,nullable=False)
    stock = Column(Integer, nullable=False,default=0)
    is_active = Column(Boolean,nullable=False, default=True)

    order_items = relationship("OrderItem", back_populates="items")
    basket_items = relationship("BasketItem", back_populates="items")