from sqlalchemy import UUID, Column, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from src.models.base import Base, BaseMixin


class PrizeCut(Base, BaseMixin):
    """
    Database model representing "prize_cut" table in the database.
    UUID and table name are inherited from BaseMixin.

    Attributes:
        place (int): The place/rank for which the prize cut is awarded.
        prize_cut (float): The percentage or amount of the prize.
        tournament_id (UUID): The ID of the associated tournament.
        tournament (Tournament): The associated tournament object.
        team_id (UUID): The ID of the associated team (optional).
    """

    place = Column(Integer, nullable=False)
    prize_cut = Column(Float, nullable=False)

    tournament_id = Column(
        UUID(as_uuid=True), ForeignKey("tournament.id"), nullable=False
    )
    tournament = relationship("Tournament", back_populates="prize_cuts")

    team_id = Column(
        UUID(as_uuid=True), ForeignKey("team.id"), nullable=True, default=None
    )
    team = relationship("Team", back_populates="prize_cuts")

    # Unique constraint to prevent
    # multiple prize cuts for the same place in the same tournament.
    __table_args__ = (UniqueConstraint("tournament_id", "place"),)
