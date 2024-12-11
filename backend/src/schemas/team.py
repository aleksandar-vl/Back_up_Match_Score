from uuid import UUID

from pydantic import BaseModel, Field
from src.schemas.match import MatchResponse
from src.schemas.player import PlayerBaseResponse
from src.schemas.prize_cut import PrizeCutResponse


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


# Team schemas
class TeamListResponse(BaseConfig):
    id: UUID
    name: str
    logo: str | None
    game_win_ratio: str | None
    players: list[PlayerBaseResponse]


class TeamDetailedResponse(BaseConfig):
    id: UUID
    name: str
    logo: str | None
    tournament_id: UUID | None
    matches: list["MatchResponse"]
    players: list[PlayerBaseResponse]
    prize_cuts: list["PrizeCutResponse"]
    team_stats: dict


class TeamCreate(BaseConfig):
    name: str = Field(
        min_length=5,
        max_length=25,
        pattern="^[a-zA-Z0-9_\s-]+$",
        examples=["example_team"],
    )


class TeamUpdate(BaseConfig):
    name: str | None = Field(
        default=None,
        min_length=5,
        max_length=25,
        pattern="^[a-zA-Z0-9_\s-]+$",
        examples=["example_team"],
    )
