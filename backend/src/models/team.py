from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base, BaseMixin


class Team(Base, BaseMixin):
    """
    Database model representing "team" table in the database.
    UUID and table name are inherited from BaseMixin.

    Attributes:
        name (str): The name of the team.
        logo (str): The URL of the team's logo.
        played_games (int): The number of games the team has played.
        won_games (int): The number of games the team has won.
        tournament_id (UUID): The ID of the associated tournament.
        players (list[Player]): The list of players in the team.
        matches_as_team1 (list[Match]): The list of matches where the team is team1.
        matches_as_team2 (list[Match]): The list of matches where the team is team2.
        prize_cuts (list[PrizeCut]): The list of prize cuts associated with the team.
        tournament (Tournament): The associated tournament object.
        wins (list[Match]): The list of matches the team has won.
    """

    name = Column(String(45), nullable=False, unique=True)
    logo = Column(String(255), nullable=True)
    played_games = Column(Integer, nullable=False, default=0)
    won_games = Column(Integer, nullable=False, default=0)
    tournament_id = Column(
        UUID(as_uuid=True), ForeignKey("tournament.id"), nullable=True
    )

    players = relationship("Player", back_populates="team")

    matches_as_team1 = relationship(
        "Match", foreign_keys="[Match.team1_id]", back_populates="team1"
    )
    matches_as_team2 = relationship(
        "Match", foreign_keys="[Match.team2_id]", back_populates="team2"
    )
    prize_cuts = relationship("PrizeCut", back_populates="team")
    tournament = relationship("Tournament", back_populates="teams")

    wins = relationship(
        "Match", foreign_keys="[Match.winner_team_id]", back_populates="winner_team"
    )
