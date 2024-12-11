from uuid import UUID

from pydantic import BaseModel


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


# PrizeCut schemas
class PrizeCutResponse(BaseConfig):
    id: UUID
    place: int
    prize_cut: float
    tournament_id: UUID
    tournament_name: str
    team_id: UUID | None
    team_name: str | None
    team_logo: str | None


class PrizeCutUpdate(BaseConfig):
    team_id: UUID
