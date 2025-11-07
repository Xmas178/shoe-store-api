from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# USER SCHEMAS
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str


class Config:
    from_attributes = True


# PRODUCT SCHEMAS
class ProductCreate(BaseModel):
    name: str
    brand: str
    description: Optional[str] = None
    base_price: float
    image_url: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str
    description: Optional[str]
    base_price: float
    image_url: Optional[str]

    class Config:
        from_attributes = True


# VARIANT SCHEMAS
class VariantCreate(BaseModel):
    product_id: int
    size: str
    color: str
    price: float
    stock: int = 0


product_id: 1


class VariantResponse(BaseModel):
    id: int
    product_id: int
    size: str
    color: str
    price: float
    stock: int

    class Config:
        from_attributes = True


# ORDER SCHEMAS
class OrderItemCreate(BaseModel):
    variant_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    variant_id: int
    quantity: int
    price_at_purchase: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
