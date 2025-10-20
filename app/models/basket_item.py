from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class BasketItem(Base):
    __tablename__ = "basket_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"),nullable=False)
    count = Column(Integer,nullable=False, default=1)

    users = relationship("User", back_populates="basket_items")
    items = relationship("Item", back_populates="basket_items")




