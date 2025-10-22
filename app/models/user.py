from sqlalchemy import Column, Integer, String, DECIMAL, Text, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from enum import Enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String,nullable=False)
    middle_name = Column(String,nullable=False)
    password_hash = Column(Text, nullable=False)
    email = Column(String, unique=True, nullable=False)
    money = Column(DECIMAL(10, 2,),nullable=False, default=0)
    role_id = Column(Integer,ForeignKey("roles.id"))
    is_active = Column(Boolean,nullable=False,default=True)

    orders = relationship("Order", back_populates="users")
    basket_items = relationship("BasketItem", back_populates="users",cascade='delete')
    roles = relationship("Role",back_populates="users")


