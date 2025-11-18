import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
# Falls back to SQLite if DATABASE_URL is not set
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./shoe_store.db")

# PostgreSQL doesn't need check_same_thread, but SQLite does
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create engine (connection to database)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

# Session (used for communicating with database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


# Helper function that provides database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
