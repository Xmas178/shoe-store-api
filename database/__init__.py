from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite tietokanta
SQLALCHEMY_DATABASE_URL = "sqlite:///./shoe_store.db"

# Luo engine (yhteys tietokantaan)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Tarvitaan SQLite:lle
)

# Sessio (käytetään tietokannan kanssa kommunikointiin)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base luokka kaikille malleille
Base = declarative_base()


# Apufunktio joka antaa tietokantayhteyden
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
