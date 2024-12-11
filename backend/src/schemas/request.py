from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, field_validator
from src.models.enums import (
    RequestStatus,
    RequestType,
)


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


# Request schemas
class RequestBase(BaseConfig):
    response_date: str | None = None
    user_id: UUID
    request_type: RequestType
    player_id: str | None = None
    admin_id: str | None = None


class RequestUpdate(BaseConfig):
    request_id: UUID
    # response_date: datetime = datetime.now()


class ResponseRequest(BaseConfig):
    request_type: RequestType = RequestType.PROMOTE_USER_TO_DIRECTOR
    status: RequestStatus
    request_date: datetime
    response_date: datetime | None

    @field_validator("request_date")
    def convert_utc_to_local(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        return v.astimezone()


class RequestListResponse(BaseConfig):
    id: UUID
    email: str
    request_type: RequestType
    status: RequestStatus
    request_date: datetime
    response_date: datetime | None
    admin_id: UUID | None
    username: str | None

    @field_validator("request_date")
    def convert_utc_to_local(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        return v.astimezone()
