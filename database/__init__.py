import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./shoe_store.db")

# For Render.com deployment, use in-memory SQLite
if os.getenv("RENDER"):
    DATABASE_URL = "sqlite:///:memory:"

# Create engine
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Flag to track if tables are created
_tables_created = False


# Helper function
def get_db():
    global _tables_created

    # Ensure tables exist (critical for in-memory SQLite!)
    if not _tables_created:
        Base.metadata.create_all(bind=engine)
        _tables_created = True

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
