# from datetime import datetime, timezone
# from typing import List
# from uuid import UUID
#
# from pydantic import BaseModel, EmailStr, Field, field_validator
# from src.models.enums import (
#     MatchFormat,
#     RequestStatus,
#     RequestType,
#     Stage,
#     TournamentFormat,
# )
#
#
# # Base configs
# class BaseConfig(BaseModel):
#     model_config = {"from_attributes": True}
#
#
# # Token schemas
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
#
# class TokenData(BaseModel):
#     user_identifier: int | None = None
#     user_email: str | None = None
#
#
# # User schemas
# class UserBase(BaseConfig):
#     email: EmailStr
#
#
# class UserCreate(UserBase):
#     password: str = Field(min_length=4, max_length=36, examples=["Example123@"])
#
#     @field_validator("password")
#     def validate_password(cls, value):
#         if not (
#             any(c.isupper() for c in value)
#             and any(c.islower() for c in value)
#             and any(c.isdigit() for c in value)
#             and any(c in "@$!%*?&" for c in value)
#             and not any(c.isspace() for c in value)
#         ):
#             raise ValueError(
#                 "Password must contain at least "
#                 "one uppercase letter, one lowercase letter, "
#                 "one number, one special character, "
#                 "and must not contain any spaces"
#             )
#         return value
#
#
# class UserResponse(UserBase):
#     id: UUID
#     email: EmailStr
#     role: str
#
#
# class UserRegisterResponse(BaseConfig):
#     email: EmailStr
#     role: str
#
#
# class UserUpdate(UserBase):
#     pass
#
#
# class PlayerBaseResponse(BaseConfig):
#     id: UUID
#     username: str
#     first_name: str
#     last_name: str
#     country: str
#     user_email: EmailStr | None = None
#     team_name: str | None = None
#     avatar: str | None
#
#
# # Player schemas
# class PlayerListResponse(PlayerBaseResponse):
#     game_win_ratio: str | None
#
#
# class PlayerDetailResponse(PlayerListResponse):
#     current_tournament_title: str | None
#
#
# class PlayerCreate(BaseConfig):
#     username: str = Field(
#         min_length=5,
#         max_length=15,
#         pattern="^[a-zA-Z0-9_-]+$",
#         examples=["example_user"],
#     )
#     first_name: str = Field(
#         min_length=2,
#         max_length=25,
#         pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
#         examples=["Example"],
#     )
#     last_name: str = Field(
#         min_length=2,
#         max_length=25,
#         pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
#         examples=["Example"],
#     )
#     country: str = Field(
#         min_length=2,
#         max_length=25,
#         pattern="^[a-zA-Z]+(?:[-\s][a-zA-Z]+)?$",
#         examples=["Example"],
#     )
#     team_name: str | None = None
#
#     @field_validator("first_name", "last_name", mode="before")
#     def capitalize_names(cls, value):
#         return "-".join(part.capitalize() for part in value.split("-"))
#
#     @field_validator("country", mode="before")
#     def capitalize_country(cls, value):
#         return value.title()
#
#
# class PlayerUpdate(BaseConfig):
#     username: str | None = Field(
#         default=None,
#         min_length=5,
#         max_length=15,
#         pattern="^[a-zA-Z0-9_-]+$",
#         examples=["example_user"],
#     )
#     first_name: str | None = Field(
#         default=None,
#         min_length=2,
#         max_length=25,
#         pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
#         examples=["Example"],
#     )
#     last_name: str | None = Field(
#         default=None,
#         min_length=2,
#         max_length=25,
#         pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
#         examples=["Example"],
#     )
#     country: str | None = Field(
#         default=None,
#         min_length=2,
#         max_length=25,
#         pattern="^[a-zA-Z]+(?:[-\s][a-zA-Z]+)?$",
#         examples=["Example"],
#     )
#     team_name: str | None = None
#
#     @field_validator("first_name", "last_name")
#     def capitalize_names(cls, value):
#         if value is not None:
#             return "-".join(part.capitalize() for part in value.split("-"))
#         return value
#
#     @field_validator("country")
#     def capitalize_country(cls, value):
#         if value is not None:
#             return value.title()
#         return value
#
#
# # Team schemas
# class TeamListResponse(BaseConfig):
#     id: UUID
#     name: str
#     logo: str | None
#     game_win_ratio: str | None
#     players: list[PlayerBaseResponse]
#
#
# class TeamDetailedResponse(BaseConfig):
#     id: UUID
#     name: str
#     logo: str | None
#     matches: list["MatchListResponse"]
#     tournament_id: UUID | None
#     prize_cuts: list["PrizeCutResponse"]
#     team_stats: dict
#
#
# class TeamCreate(BaseConfig):
#     # id: UUID
#     name: str = Field(
#         min_length=5,
#         max_length=25,
#         pattern="^[a-zA-Z0-9_-]+$",
#         examples=["example_team"],
#     )
#
#
# class TeamUpdate(BaseConfig):
#     name: str | None = None
#
#
# # Match schemas
# class MatchListResponse(BaseConfig):
#     id: UUID
#     match_format: MatchFormat
#     start_time: datetime
#     is_finished: bool
#     stage: Stage
#     team1_id: UUID
#     team2_id: UUID
#     team1_score: int
#     team2_score: int
#     team1_name: str
#     team2_name: str
#     winner_id: UUID | None = None
#     tournament_id: UUID
#     tournament_title: str
#
#
# class MatchDetailResponse(MatchListResponse):
#     team1_logo: str | None = None
#     team2_logo: str | None = None
#
#
# class MatchUpdate(BaseConfig):
#     start_time: datetime | None = None
#     stage: Stage | None = None
#     team1_id: UUID | None = None
#     team2_id: UUID | None = None
#
#
# # Tournament schemas
# class TournamentListResponse(BaseConfig):
#     id: UUID
#     title: str
#     tournament_format: TournamentFormat
#     start_date: datetime
#     end_date: datetime
#     current_stage: Stage
#     number_of_teams: int | None = None
#
#
# class TournamentDetailResponse(TournamentListResponse):
#     matches_of_current_stage: list[MatchListResponse]
#     teams: list[TeamListResponse]
#     prizes: list["PrizeCutResponse"]
#
#
# class TournamentCreate(BaseConfig):
#     title: str = Field(
#         min_length=3, max_length=50, examples=["Example Tournament Title"]
#     )
#     tournament_format: TournamentFormat
#     start_date: datetime
#     team_names: List[str]
#     prize_pool: int = Field(ge=1, examples=[1000])
#
#
# class TournamentUpdate(BaseConfig):
#     title: str | None = None
#     end_date: datetime | None = None
#     prize_pool: int | None = None
#
#
# # PrizeCut schemas
# class PrizeCutResponse(BaseConfig):
#     id: UUID
#     place: int
#     prize_cut: float
#     tournament_id: UUID
#     tournament_name: str
#     team_id: UUID | None
#     team_name: str | None
#
#
# class PrizeCutUpdate(BaseConfig):
#     team_id: UUID
#
#
# # Request schemas
# class RequestBase(BaseConfig):
#     response_date: str | None = None
#     user_id: UUID
#     request_type: RequestType
#     player_id: str | None = None
#     admin_id: str | None = None
#
#
# class RequestUpdate(BaseConfig):
#     request_id: UUID
#     # response_date: datetime = datetime.now()
#
#
# class ResponseRequest(BaseConfig):
#     request_type: RequestType = RequestType.PROMOTE_USER_TO_DIRECTOR
#     status: RequestStatus
#     request_date: datetime
#     response_date: datetime | None
#
#     @field_validator("request_date")
#     def convert_utc_to_local(cls, v: datetime) -> datetime:
#         if v.tzinfo is None:
#             v = v.replace(tzinfo=timezone.utc)
#         return v.astimezone()
#
#
# class RequestListResponse(BaseConfig):
#     id: UUID
#     email: str
#     request_type: RequestType
#     status: RequestStatus
#     request_date: datetime
#     response_date: datetime | None
#     admin_id: UUID | None
#     username: str | None
#
#     @field_validator("request_date")
#     def convert_utc_to_local(cls, v: datetime) -> datetime:
#         if v.tzinfo is None:
#             v = v.replace(tzinfo=timezone.utc)
#         return v.astimezone()
