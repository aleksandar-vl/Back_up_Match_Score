from sqlalchemy import Column, DateTime, Enum, String, func
from sqlalchemy.orm import relationship
from src.models.base import Base, BaseMixin
from src.models.enums import Role


class User(Base, BaseMixin):
    """
    Database model representing "user" table in the database.
    UUID and table name are inherited from BaseMixin.

    Attributes:
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        role (Role): The role of the user (e.g., USER, ADMIN).
        created_at (datetime): The date and time when the user was created.
        requests_user (list[Request]): The list of requests made by the user.
        requests_admin (list[Request]): The list of requests responded to by the admin.
        tournaments (list[Tournament]): The list of tournaments directed by the user.
        player (Player): The player object associated with the user.
    """

    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    requests_user = relationship(
        "Request", back_populates="user", foreign_keys="[Request.user_id]"
    )
    requests_admin = relationship(
        "Request", back_populates="admin", foreign_keys="[Request.admin_id]"
    )

    tournaments = relationship("Tournament", back_populates="director")
    player = relationship(
        "Player", back_populates="user", uselist=False, foreign_keys="[Player.user_id]"
    )
