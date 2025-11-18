import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./shoe_store.db")

# For Render.com deployment, use in-memory SQLite
if os.getenv("RENDER"):
    DATABASE_URL = "sqlite:///:memory:"

# Create engine with special settings for in-memory SQLite
if DATABASE_URL == "sqlite:///:memory:":
    # Use StaticPool to keep the same connection alive
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Critical for in-memory SQLite!
    )
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args=(
            {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
        ),
    )

# Enable foreign keys for SQLite
if DATABASE_URL.startswith("sqlite"):

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


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
