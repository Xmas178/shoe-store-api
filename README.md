# Shoe Store API

## Demo Video
Watch the full-stack demo: [View on YouTube](https://youtu.be/TC2oMAiqvFo)

## Related Repositories
- Frontend: [shoe-store-frontend](https://github.com/Xmas178/shoe-store-frontend)


RESTful API backend for an e-commerce shoe store application. Built with FastAPI and SQLAlchemy.

## Features

- JWT-based authentication and authorization
- Role-based access control (admin/customer)
- Product catalog management
- Product variants (sizes, colors, stock)
- Shopping cart functionality
- Order processing
- SQLite database with SQLAlchemy ORM

## Tech Stack

- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic for data validation
- JWT tokens for authentication
- Bcrypt for password hashing
- CORS middleware for frontend integration

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/shoe-store-api.git
cd shoe-store-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API documentation is automatically generated and available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database

The application uses SQLite database (`shoe_store.db`). The database is created automatically on first run.

### Models

**User**
- id (Primary Key)
- name
- email (Unique)
- hashed_password
- role (admin/customer)

**Product**
- id (Primary Key)
- name
- brand
- description
- base_price
- image_url
- category

**Variant**
- id (Primary Key)
- product_id (Foreign Key)
- size (EU format)
- color
- price
- stock

**Cart**
- id (Primary Key)
- user_id (Foreign Key)
- created_at

**CartItem**
- id (Primary Key)
- cart_id (Foreign Key)
- variant_id (Foreign Key)
- quantity

**Order**
- id (Primary Key)
- user_id (Foreign Key)
- total_amount
- status
- shipping_address
- created_at

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and receive JWT token

### Products
- `GET /products` - List all products
- `GET /products/{id}` - Get single product
- `POST /products` - Create product (admin only)
- `DELETE /products/{id}` - Delete product (admin only)

### Variants
- `GET /variants/product/{product_id}` - Get variants for product
- `POST /variants` - Create variant (admin only)
- `DELETE /variants/{id}` - Delete variant (admin only)

### Shopping Cart
- `GET /cart` - Get user's cart
- `POST /cart/items` - Add item to cart
- `PUT /cart/items/{id}` - Update item quantity
- `DELETE /cart/items/{id}` - Remove item from cart

### Orders
- `GET /orders` - Get user's orders
- `POST /orders` - Create order from cart

## Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_token_here>
```

### Admin Access

To grant admin privileges to a user, update the database directly:
```bash
sqlite3 shoe_store.db
UPDATE users SET role = 'admin' WHERE email = 'user@example.com';
```

## CORS Configuration

CORS is configured to allow requests from `http://localhost:3000` (React frontend). Update CORS settings in `main.py` for production deployment.

## Environment Variables

Currently using default configuration. For production, consider adding:
- `SECRET_KEY` - JWT signing key
- `DATABASE_URL` - Database connection string
- `ALLOWED_ORIGINS` - CORS allowed origins

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Development

Run with auto-reload during development:
```bash
uvicorn main:app --reload
```

## Testing

API endpoints can be tested using:
- Swagger UI at `/docs`
- Thunder Client (VS Code extension)
- Postman
- curl commands

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens expire after 30 days
- Admin routes are protected with role verification
- SQL injection protection via SQLAlchemy ORM

## Future Enhancements

- PostgreSQL migration for production
- Rate limiting
- Email verification
- Password reset functionality
- Payment processing integration
- Order status tracking
- Logging and monitoring
- Unit and integration tests

## License

This project is for portfolio purposes.

## Author

Xmas178 - Dev