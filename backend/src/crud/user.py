from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.core.security import get_password_hash
from src.models.user import User
from src.schemas.user import UserCreate, UserResponse
from src.utils.notifications import send_email_notification
from src.utils.validators import user_email_exists


def create_user(user: UserCreate, db: Session) -> User:
    """
    Create a new user with the provided data.

    Args:
        user (UserCreate): The user data to create.
        db (Session): The database session.

    Returns:
        User: The created user object.
    """
    user_email_exists(db, user.email)
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    send_email_notification(
        email=user.email,
        subject="Account Created",
        message=f"Your account has been created with email {user.email}",
    )
    return db_user


def get_by_id(db: Session, user_id: str) -> Type[User]:
    """
    Retrieve a user by their ID.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user to retrieve.

    Returns:
        User: The user object if found.

    Raises:
        HTTPException: If the user is not found.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return user


def update_email(db: Session, email: str, current_user: User) -> dict:
    """
    Update the email address of the current user.

    Args:
        db (Session): The database session.
        email (str): The new email address.
        current_user (User): The current user object.

    Returns:
        dict: A message indicating the email update was successful.
    """
    user_email_exists(db, email)
    user = db.query(User).filter(User.id == current_user.id).first()
    old_email = user.email

    user.email = email
    db.commit()
    db.refresh(user)

    send_email_notification(
        email=old_email,
        subject="Email Updated",
        message=f"Your email has been changed from {old_email} to {email}",
    )

    send_email_notification(
        email=email,
        subject="Email Updated",
        message=f"Your email has been changed from {old_email} to {email}",
    )
    return {"message": "Email updated successfully."}


def convert_db_to_user_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, email=user.email, role=user.role)
