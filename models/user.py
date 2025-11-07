from sqlalchemy import Column, Integer, String, Enum
from database import Base
from sqlalchemy.orm import relationship
import enum


# Käyttäjäroolit
class UserRole(str, enum.Enum):
    customer = "customer"
    admin = "admin"


# User-taulu
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.customer)
    orders = relationship("Order", back_populates="user")
