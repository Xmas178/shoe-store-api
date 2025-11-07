from passlib.context import CryptContext

# Bcrypt konteksti salasanojen hashaamiseen
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashaa salasanan"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Tarkistaa onko salasana oikein"""
    return pwd_context.verify(plain_password, hashed_password)
