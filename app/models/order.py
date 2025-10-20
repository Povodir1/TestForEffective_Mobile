from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime,nullable=False, default=datetime.now)

    users = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="orders",cascade='delete')