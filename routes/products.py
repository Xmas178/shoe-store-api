from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.product import Product
from models.user import User
from routes.schemas import ProductCreate, ProductResponse
from auth.permissions import require_admin

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Luo uuden tuotteen (vain admin)"""
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """Hae kaikki tuotteet (julkinen)"""
    products = db.query(Product).all()
    return products
