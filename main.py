from fastapi import FastAPI
from database import engine, Base
from models.user import User
from models.product import Product
from models.variant import Variant
from models.order import Order
from models.order_item import OrderItem
from routes import users, auth
from routes import users, auth, products
from routes import users, auth, products, variants
from routes import users, auth, products, variants, orders

# Luo kaikki taulut
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shoe Store API")
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(variants.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return {"message": "Welcome to Shoe Store API"}
