from sqlalchemy import Column, Integer, ForeignKey,String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False,unique=True)

    users = relationship("User",back_populates="roles")
    permissions = relationship("Permission",back_populates="roles")



