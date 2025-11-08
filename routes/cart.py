from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.cart import Cart
from models.cart_item import CartItem
from models.user import User
from models.variant import Variant
from routes.schemas import CartItemCreate, CartResponse
from auth.jwt import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Hae käyttäjän ostoskori"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    # Jos ostoskoria ei ole, luo se
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart


@router.post("/items", response_model=CartResponse)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lisää tuote ostoskoriin"""
    # Tarkista että variantti on olemassa
    variant = db.query(Variant).filter(Variant.id == item.variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")

    # Tarkista varastosaldo
    if variant.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    # Hae tai luo ostoskori
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Tarkista onko tuote jo korissa
    existing_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.variant_id == item.variant_id)
        .first()
    )

    if existing_item:
        # Päivitä määrää
        existing_item.quantity += item.quantity
        if variant.stock < existing_item.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock")
    else:
        # Lisää uusi tuote
        cart_item = CartItem(
            cart_id=cart.id, variant_id=item.variant_id, quantity=item.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart)
    return cart


@router.put("/items/{item_id}", response_model=CartResponse)
def update_cart_item(
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Päivitä ostoskorin tuotteen määrää"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.cart_id == cart.id)
        .first()
    )

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    # Tarkista varastosaldo
    variant = db.query(Variant).filter(Variant.id == cart_item.variant_id).first()
    if variant.stock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart)
    return cart


@router.delete("/items/{item_id}", response_model=CartResponse)
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Poista tuote ostoskorista"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.cart_id == cart.id)
        .first()
    )

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db.delete(cart_item)
    db.commit()
    db.refresh(cart)
    return cart


@router.delete("/", response_model=dict)
def clear_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Tyhjennä ostoskori"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Poista kaikki tuotteet
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()

    return {"message": "Cart cleared successfully"}
