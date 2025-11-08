from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models.user import User
from auth.password import verify_password
from auth.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # Etsi käyttäjä emaililla
    user = db.query(User).filter(User.email == form_data.username).first()

    # Tarkista onko käyttäjä olemassa ja salasana oikein
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Luo token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
def register(user_data: dict, db: Session = Depends(get_db)):
    """Rekisteröi uusi käyttäjä"""
    from auth.password import hash_password
    from routes.schemas import UserRegister

    # Validoi data
    try:
        validated_data = UserRegister(**user_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Tarkista onko käyttäjä jo olemassa
    existing_user = db.query(User).filter(User.email == validated_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Luo uusi käyttäjä
    hashed_password = hash_password(validated_data.password)
    new_user = User(
        name=validated_data.name,
        email=validated_data.email,
        hashed_password=hashed_password,
        role="customer",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role,
    }
