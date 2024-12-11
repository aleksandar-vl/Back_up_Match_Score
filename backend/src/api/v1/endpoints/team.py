from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from src.api.deps import get_current_user, get_db
from src.crud import team as team_crud
from src.schemas.team import (
    TeamCreate,
    TeamDetailedResponse,
    TeamListResponse,
    TeamUpdate,
)
from src.schemas.user import UserResponse
from src.utils.pagination import PaginationParams, get_pagination

router = APIRouter()


@router.get("/")
def get_teams(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
    search: str | None = None,
    is_available: Literal["true", "false"] | None = None,
    has_space: Literal["true", "false"] | None = None,
    sort_by: Literal["asc", "desc"] = "asc",
):
    """
    Retrieve a list of teams with optional filtering and sorting parameters.

    Args:
        db (Session): Database session dependency.
        pagination (PaginationParams): Pagination parameters for the query.
        search (str | None): Optional search term for team names.
        is_available (Literal["true", "false"] | None):
        Optional filter by availability.
        has_space (Literal["true", "false"] | None):
        Optional filter by space availability.
        sort_by (Literal["asc", "desc"]): Sort order, either ascending or descending.

    Returns:
        list[TeamListResponse]: A list of team responses matching the filters.
    """
    return team_crud.get_teams(db, pagination, search, is_available, has_space, sort_by)


@router.get("/{team_id}", response_model=TeamDetailedResponse)
def get_team(team_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a team by its ID.

    Args:
        team_id (UUID): The unique identifier of the team.
        db (Session): Database session dependency.

    Returns:
        TeamDetailedResponse: The team details response object.
    """
    return team_crud.get_team(db, team_id)


@router.post("/", response_model=TeamListResponse, status_code=201)
def create_team(
    team: TeamCreate = Depends(),
    logo: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Create a new team.

    Args:
        team (TeamCreate): The team creation data.
        logo (UploadFile | None): Optional logo file for the team.
        db (Session): Database session dependency.
        current_user (UserResponse): The current authenticated user.

    Returns:
        TeamListResponse: The created team response object.
    """
    return team_crud.create_team(db, team, logo, current_user)


@router.put("/{team_id}", response_model=TeamListResponse)
def update_team(
    team_id: UUID,
    team: TeamUpdate = Depends(),
    logo: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Update a team's details by its ID.

    Args:
        team_id (UUID): The unique identifier of the team.
        team (TeamUpdate): The team update data.
        logo (UploadFile | None): Optional logo file for the team.
        db (Session): Database session dependency.
        current_user (UserResponse): The current authenticated user.

    Returns:
        TeamListResponse: The updated team response object.
    """
    return team_crud.update_team(db, team_id, team, logo, current_user)
