from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base, BaseMixin
from src.models.enums import Stage, TournamentFormat


class Tournament(Base, BaseMixin):
    """
    Database model representing "tournament" table in the database.
    UUID and table name are inherited from BaseMixin.

    Attributes:
        title (str): The title of the tournament.
        tournament_format (TournamentFormat): The format of the tournament.
        start_date (datetime): The start date of the tournament.
        end_date (datetime): The end date of the tournament.
        prize_pool (int): The prize pool of the tournament.
        current_stage (Stage): The current stage of the tournament.
        director_id (UUID): The ID of the director of the tournament.
        director (User): The director of the tournament.
        matches (list[Match]): The list of matches in the tournament.
        prize_cuts (list[PrizeCut]): The list of prize cuts in the tournament.
        teams (list[Team]): The list of teams in the tournament.
    """

    title = Column(String(45), unique=True, nullable=False)
    tournament_format = Column(Enum(TournamentFormat), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    prize_pool = Column(Integer, nullable=False)
    current_stage = Column(Enum(Stage), nullable=False)

    director_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    director = relationship("User", back_populates="tournaments")

    matches = relationship("Match", back_populates="tournament")
    prize_cuts = relationship("PrizeCut", back_populates="tournament")
    teams = relationship("Team", back_populates="tournament")
