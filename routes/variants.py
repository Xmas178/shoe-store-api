from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.variant import Variant
from models.product import Product
from models.user import User
from routes.schemas import VariantCreate, VariantResponse
from auth.permissions import require_admin

router = APIRouter(prefix="/variants", tags=["variants"])


@router.post("/", response_model=VariantResponse)
def create_variant(
    variant: VariantCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Luo uuden variantin (vain admin)"""
    # Tarkista että tuote on olemassa
    product = db.query(Product).filter(Product.id == variant.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_variant = Variant(**variant.model_dump())
    db.add(new_variant)
    db.commit()
    db.refresh(new_variant)
    return new_variant


@router.get("/product/{product_id}", response_model=List[VariantResponse])
def get_product_variants(product_id: int, db: Session = Depends(get_db)):
    """Hae tuotteen kaikki variantit"""
    variants = db.query(Variant).filter(Variant.product_id == product_id).all()
    return variants
