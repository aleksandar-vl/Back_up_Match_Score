from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


class PlayerBaseResponse(BaseConfig):
    id: UUID
    username: str
    first_name: str
    last_name: str
    country: str
    user_email: EmailStr | None = None
    team_name: str | None = None
    avatar: str | None


# Player schemas
class PlayerListResponse(PlayerBaseResponse):
    game_win_ratio: str | None


class PlayerDetailResponse(PlayerListResponse):
    team_id: UUID | None
    current_tournament_title: str | None
    current_tournament_id: UUID | None


class PlayerCreate(BaseConfig):
    username: str = Field(
        min_length=5,
        max_length=15,
        pattern="^[a-zA-Z0-9_-]+$",
        examples=["example_user"],
    )
    first_name: str = Field(
        min_length=2,
        max_length=25,
        pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
        examples=["Example"],
    )
    last_name: str = Field(
        min_length=2,
        max_length=25,
        pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
        examples=["Example"],
    )
    country: str = Field(
        min_length=2,
        max_length=25,
        pattern="^[a-zA-Z]+(?:[-\s][a-zA-Z]+)?$",
        examples=["Example"],
    )
    team_name: str | None = None

    @field_validator("first_name", "last_name", mode="before")
    def capitalize_names(cls, value):
        return "-".join(part.capitalize() for part in value.split("-"))

    @field_validator("country", mode="before")
    def capitalize_country(cls, value):
        return value.title()


class PlayerUpdate(BaseConfig):
    username: str | None = Field(
        default=None,
        min_length=5,
        max_length=15,
        pattern="^[a-zA-Z0-9_-]+$",
        examples=["example_user"],
    )
    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=25,
        pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
        examples=["Example"],
    )
    last_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=25,
        pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
        examples=["Example"],
    )
    country: str | None = Field(
        default=None,
        min_length=2,
        max_length=25,
        pattern="^[a-zA-Z]+(?:[-\s][a-zA-Z]+)?$",
        examples=["Example"],
    )
    team_name: str | None = None

    @field_validator("first_name", "last_name")
    def capitalize_names(cls, value):
        if value is not None:
            return "-".join(part.capitalize() for part in value.split("-"))
        return value

    @field_validator("country")
    def capitalize_country(cls, value):
        if value is not None:
            return value.title()
        return value
