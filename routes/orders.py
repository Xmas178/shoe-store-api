from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.order import Order, OrderStatus
from models.order_item import OrderItem
from models.variant import Variant
from models.user import User
from routes.schemas import OrderCreate, OrderResponse
from auth.jwt import get_current_user
from auth.permissions import require_admin

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Luo uuden tilauksen"""

    # Laske kokonaishinta ja tarkista varastosaldot
    total_price = 0
    order_items_data = []

    for item in order_data.items:
        variant = db.query(Variant).filter(Variant.id == item.variant_id).first()
        if not variant:
            raise HTTPException(
                status_code=404, detail=f"Variant {item.variant_id} not found"
            )

        # Tarkista että varastossa on tarpeeksi
        if variant.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for variant {item.variant_id}. Available: {variant.stock}",
            )

        item_total = variant.price * item.quantity
        total_price += item_total

        order_items_data.append(
            {
                "variant_id": variant.id,
                "quantity": item.quantity,
                "price_at_purchase": variant.price,
            }
        )

    # Luo tilaus
    new_order = Order(
        user_id=current_user.id, total_price=total_price, status=OrderStatus.pending
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Luo tilausrivit ja vähennä varastosaldoja
    for item_data in order_items_data:
        order_item = OrderItem(order_id=new_order.id, **item_data)
        db.add(order_item)

        # Vähennä varastosta
        variant = (
            db.query(Variant).filter(Variant.id == item_data["variant_id"]).first()
        )
        variant.stock -= item_data["quantity"]

    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("/my-orders", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Hae käyttäjän omat tilaukset"""
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders


@router.get("/all", response_model=List[OrderResponse])
def get_all_orders(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """Hae kaikki tilaukset (vain admin)"""
    orders = db.query(Order).all()
    return orders


@router.patch("/{order_id}/status")
def update_order_status(
    order_id: int,
    status: OrderStatus,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Päivitä tilauksen status (vain admin)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()
    db.refresh(order)

    return {"message": f"Order {order_id} status updated to {status}"}


@router.post("/checkout", response_model=OrderResponse)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Muuta ostoskori tilaukseksi (checkout)"""
    from models.cart import Cart
    from models.cart_item import CartItem

    # Hae ostoskori
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Tarkista että korissa on tuotteita
    if not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Laske kokonaishinta ja tarkista varastosaldot
    total_price = 0
    order_items_data = []

    for cart_item in cart.items:
        variant = db.query(Variant).filter(Variant.id == cart_item.variant_id).first()
        if not variant:
            raise HTTPException(
                status_code=404, detail=f"Variant {cart_item.variant_id} not found"
            )

        # Tarkista varasto
        if variant.stock < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {variant.product.name} - {variant.size}. Available: {variant.stock}",
            )

        item_total = variant.price * cart_item.quantity
        total_price += item_total

        order_items_data.append(
            {
                "variant_id": variant.id,
                "quantity": cart_item.quantity,
                "price_at_purchase": variant.price,
            }
        )

    # Luo tilaus
    new_order = Order(
        user_id=current_user.id, total_price=total_price, status=OrderStatus.pending
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Luo tilausrivit ja vähennä varastosaldoja
    for item_data in order_items_data:
        order_item = OrderItem(order_id=new_order.id, **item_data)
        db.add(order_item)

        # Vähennä varastosta
        variant = (
            db.query(Variant).filter(Variant.id == item_data["variant_id"]).first()
        )
        variant.stock -= item_data["quantity"]

    # Tyhjennä ostoskori
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Hae yksittäinen tilaus"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Tarkista että tilaus kuuluu käyttäjälle (paitsi jos admin)
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    return order
