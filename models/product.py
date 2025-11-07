from sqlalchemy import Column, Integer, String, Float, Text
from database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    description = Column(Text)
    base_price = Column(Float, nullable=False)
    image_url = Column(String)
    variants = relationship("Variant", back_populates="product")
