from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base, BaseMixin


class Player(Base, BaseMixin):
    """
    Database model representing "player" table in the database.
    UUID and table name are inherited from BaseMixin.

    Attributes:
        username (str): The username of the player.
        first_name (str): The first name of the player.
        last_name (str): The last name of the player.
        country (str): The country of the player.
        avatar (str): The URL of the player's avatar.
        played_games (int): The number of games the player has played.
        won_games (int): The number of games the player has won.
        user_id (UUID): The ID of the associated user.
        user (User): The associated user object.
        team_id (UUID): The ID of the associated team.
        team (Team): The associated team object.
        requests (list[Request]): The list of requests associated with the player.
    """

    username = Column(String(45), nullable=False, unique=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    country = Column(String(45), nullable=False)
    avatar = Column(String(255), nullable=True)
    played_games = Column(Integer, nullable=False, default=0)
    won_games = Column(Integer, nullable=False, default=0)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    user = relationship(
        "User", back_populates="player", uselist=False, single_parent=True
    )

    team_id = Column(UUID(as_uuid=True), ForeignKey("team.id"), nullable=True)
    team = relationship("Team", back_populates="players")

    requests = relationship("Request", back_populates="player")
