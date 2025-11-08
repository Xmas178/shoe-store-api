# Shoe Store API

A comprehensive REST API for an e-commerce shoe store built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- **User Authentication**: JWT-based authentication with role-based access control (customer/admin)
- **Product Management**: Full CRUD operations for products with variants (sizes, colors, stock)
- **Shopping Cart**: Add, update, and remove items from cart
- **Order Management**: Checkout process with inventory tracking and order history
- **Admin Controls**: Product and order management for administrators

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt

## Project Structure
```
shoe-store-api/
├── auth/               # Authentication logic (JWT, password hashing)
├── database/           # Database configuration and connection
├── models/             # SQLAlchemy database models
├── routes/             # API endpoints and schemas
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
└── .env               # Environment variables (not in git)
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/Xmas178/shoe-store-api.git
cd shoe-store-api
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up PostgreSQL**
```bash
sudo service postgresql start
sudo -u postgres psql
```

In PostgreSQL shell:
```sql
CREATE USER sami WITH PASSWORD 'your_password';
CREATE DATABASE shoe_store_db OWNER sami;
GRANT ALL PRIVILEGES ON DATABASE shoe_store_db TO sami;
\q
```

5. **Configure environment variables**

Create `.env` file:
```
DATABASE_URL=postgresql://sami:your_password@localhost/shoe_store_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a secure secret key:
```bash
openssl rand -hex 32
```

6. **Run the application**
```bash
uvicorn main:app --reload
```

API will be available at `http://127.0.0.1:8000`

## API Documentation

Once running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and receive JWT token

### Products
- `GET /products` - List all products
- `GET /products/{id}` - Get single product
- `POST /products` - Create product (admin only)
- `PUT /products/{id}` - Update product (admin only)
- `DELETE /products/{id}` - Delete product (admin only)

### Variants
- `POST /variants` - Add product variant (admin only)
- `GET /variants/product/{product_id}` - Get variants for product

### Shopping Cart
- `GET /cart` - Get user's cart
- `POST /cart/items` - Add item to cart
- `PUT /cart/items/{id}` - Update item quantity
- `DELETE /cart/items/{id}` - Remove item from cart
- `DELETE /cart` - Clear cart

### Orders
- `POST /orders/checkout` - Create order from cart
- `GET /orders/my-orders` - Get user's order history
- `GET /orders/{id}` - Get single order
- `GET /orders/all` - Get all orders (admin only)
- `PATCH /orders/{id}/status` - Update order status (admin only)

## Database Models

- **User**: User accounts with roles (customer/admin)
- **Product**: Shoe products with name, description, brand, base price
- **Variant**: Product variants (size, color, stock, price)
- **Cart**: User shopping carts
- **CartItem**: Items in shopping cart
- **Order**: Customer orders with status tracking
- **OrderItem**: Individual items in orders

## Authentication

Protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <your_token_here>
```

## Development

Built as part of a portfolio project to demonstrate:
- RESTful API design
- Database modeling and relationships
- Authentication and authorization
- Role-based access control
- E-commerce business logic

## Future Enhancements

- Product categories and filtering
- Search functionality
- Payment integration
- Image upload for products
- Email notifications

## Author

Xmas178 - [GitHub](https://github.com/Xmas178)

## License

This project is for portfolio purposes.