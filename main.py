import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from models.user import User
from models.product import Product
from models.variant import Variant
from models.order import Order
from models.order_item import OrderItem
from models.cart import Cart
from models.cart_item import CartItem
from routes import users, auth, products, variants, orders, cart

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shoe Store API")

# CORS middleware - Allow frontend origins
origins = [
    "http://localhost:3000",  # Local development
    "https://shoe-store-frontend.vercel.app",  # Production (päivitä tämä oikeaksi)
    "https://*.vercel.app",  # All Vercel deployments
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(variants.router)
app.include_router(orders.router)
app.include_router(cart.router)


@app.get("/")
def root():
    return {"message": "Welcome to Shoe Store API"}
