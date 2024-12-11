from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import relationship
from src.models.base import Base, BaseMixin
from src.models.enums import RequestStatus, RequestType


class Request(Base, BaseMixin):
    """
    Database model representing "request" table in the database.
    UUID and table name are inherited from BaseMixin.

    Attributes:
        status (RequestStatus): The status of the request.
        request_date (datetime): The date and time when the request was made.
        response_date (datetime): The date and time when the request was responded to.
        request_type (RequestType): The type of the request.
        user_id (UUID): The ID of the user who made the request.
        username (str): The username of the player associated with the request.
        admin_id (UUID): The ID of the admin who responded to the request.
        user (User): The user object associated with the request.
        admin (User): The admin object associated with the request.
        player (Player): The player object associated with the request.
    """

    status = Column(Enum(RequestStatus), nullable=False, default=RequestStatus.PENDING)
    request_date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    response_date = Column(DateTime(timezone=True), nullable=True)
    request_type = Column(Enum(RequestType), nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    username = Column(String(45), ForeignKey("player.username"), nullable=True)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)

    user = relationship("User", back_populates="requests_user", foreign_keys=[user_id])
    admin = relationship(
        "User", back_populates="requests_admin", foreign_keys=[admin_id]
    )

    player = relationship("Player", back_populates="requests")
