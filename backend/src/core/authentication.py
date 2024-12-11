from datetime import datetime, timedelta, timezone
from typing import Type

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session
from src.core.config import settings
from src.core.security import verify_password
from src.models.user import User


def authenticate_user(db: Session, email: str, password: str) -> Type[User]:
    """
    Authenticate a user by their email and password.

    Args:
        db (Session): Database session dependency.
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        Type[User]: The authenticated user object.

    Raises:
        HTTPException: If the user is not found or the password is incorrect.
    """
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return user


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def is_token_blacklisted(token: str) -> bool:
    """
    Check if a token is blacklisted.

    Args:
        token (str): The token to check.

    Returns:
        bool: True if the token is blacklisted, False otherwise.
    """
    return token in settings.BLACKLISTED_TOKENS
