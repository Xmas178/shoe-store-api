from fastapi import Depends, HTTPException, status
from models.user import User, UserRole
from auth.jwt import get_current_user


def require_admin(current_user: User = Depends(get_current_user)):
    """Varmistaa että käyttäjä on admin"""
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin required"
        )
    return current_user
