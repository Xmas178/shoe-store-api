from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from routes.schemas import UserCreate, UserResponse
from auth.password import hash_password
from auth.jwt import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Tarkista onko email jo käytössä
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Luo uusi käyttäjä
    new_user = User(
        name=user.name, email=user.email, hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Palauttaa kirjautuneen käyttäjän tiedot"""
    return current_user

# VULNERABLE: IDOR - Any user can access other users' data
@router.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }
