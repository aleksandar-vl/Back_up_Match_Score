from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field
from src.models.enums import (
    Stage,
    TournamentFormat,
)
from src.schemas.match import MatchResponse
from src.schemas.prize_cut import PrizeCutResponse
from src.schemas.team import TeamListResponse


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


# Tournament schemas
class TournamentListResponse(BaseConfig):
    id: UUID
    title: str
    tournament_format: TournamentFormat
    start_date: datetime
    end_date: datetime
    current_stage: Stage
    number_of_teams: int | None = None
    director_id: UUID


class TournamentDetailResponse(TournamentListResponse):
    matches_of_current_stage: list[MatchResponse]
    teams: list[TeamListResponse]
    prizes: list["PrizeCutResponse"]


class TournamentCreate(BaseConfig):
    title: str = Field(
        min_length=3, max_length=50, examples=["Example Tournament Title"]
    )
    tournament_format: TournamentFormat
    start_date: datetime
    team_names: List[str]
    prize_pool: int = Field(ge=1, examples=[1000])


class TournamentUpdate(BaseConfig):
    title: str | None = Field(
        default=None, min_length=3, max_length=50, examples=["Example Tournament Title"]
    )
    end_date: datetime | None = None
    prize_pool: int | None = Field(default=None, ge=1, examples=[1000])
