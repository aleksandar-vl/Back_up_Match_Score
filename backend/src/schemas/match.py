from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from src.models.enums import MatchFormat, Stage


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


# Match schemas
class MatchResponse(BaseConfig):
    id: UUID
    match_format: MatchFormat
    start_time: datetime
    is_finished: bool
    stage: Stage
    team1_id: UUID
    team2_id: UUID
    team1_score: int
    team2_score: int
    team1_name: str
    team1_logo: str | None
    team2_name: str
    team2_logo: str | None
    winner_id: UUID | None = None
    tournament_id: UUID
    tournament_title: str


class MatchUpdate(BaseConfig):
    start_time: datetime | None = None
    stage: Stage | None = None
    team1_name: str | None = None
    team2_name: str | None = None
