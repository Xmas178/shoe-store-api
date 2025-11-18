from database import SessionLocal
from models.user import User
from models.product import Product
from models.variant import Variant
from auth.password import hash_password


def init_demo_data():
    """Initialize demo data for in-memory database"""
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_products = db.query(Product).first()
        if existing_products:
            return  # Data already initialized

        # Create admin user
        admin = User(
            email="admin@example.com",
            username="admin",
            hashed_password=hash_password("admin123"),
            role="admin",
        )
        db.add(admin)

        # Create demo products
        products_data = [
            {
                "name": "Nike Air Max",
                "brand": "Nike",
                "description": "Classic running shoes with air cushioning",
                "base_price": 129.99,
                "image_url": "https://via.placeholder.com/300",
            },
            {
                "name": "Adidas Ultraboost",
                "brand": "Adidas",
                "description": "Premium running shoes with boost technology",
                "base_price": 179.99,
                "image_url": "https://via.placeholder.com/300",
            },
            {
                "name": "Puma Suede Classic",
                "brand": "Puma",
                "description": "Iconic streetwear sneakers",
                "base_price": 89.99,
                "image_url": "https://via.placeholder.com/300",
            },
        ]

        for prod_data in products_data:
            product = Product(**prod_data)
            db.add(product)
            db.flush()  # Get product ID

            # Add variants (sizes)
            sizes = [38, 39, 40, 41, 42, 43, 44]
            for size in sizes:
                variant = Variant(
                    product_id=product.id,
                    size=size,
                    color="Black",
                    stock=10,
                    price=prod_data["base_price"],
                )
                db.add(variant)

        db.commit()
        print("✅ Demo data initialized successfully")

    except Exception as e:
        print(f"❌ Error initializing demo data: {e}")
        db.rollback()
    finally:
        db.close()
