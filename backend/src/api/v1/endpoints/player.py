from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from src.api.deps import get_current_user, get_db
from src.crud import player as player_crud
from src.schemas.player import (
    PlayerCreate,
    PlayerDetailResponse,
    PlayerListResponse,
    PlayerUpdate,
)
from src.schemas.user import UserResponse
from src.utils.pagination import PaginationParams, get_pagination

router = APIRouter()


@router.post("/", response_model=PlayerListResponse, status_code=201)
def create_player(
    player: PlayerCreate = Depends(),
    avatar: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Create a new player.

    Args:
        player (PlayerCreate): The player creation data.
        avatar (UploadFile | None): Optional avatar file for the player.
        db (Session): Database session dependency.
        current_user (UserResponse): The current authenticated user.

    Returns:
        PlayerListResponse: The created player response object.
    """
    return player_crud.create_player(db, player, avatar, current_user)


@router.get("/")
def get_players(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
    search: str | None = None,
    team: str | None = None,
    country: str | None = None,
    sort_by: Literal["asc", "desc"] = "asc",
):
    """
    Retrieve a list of players with optional filtering and sorting parameters.

    Args:
        db (Session): Database session dependency.
        pagination (PaginationParams): Pagination parameters for the query.
        search (str | None): Optional search term for player names.
        team (str | None): Optional filter by team name.
        country (str | None): Optional filter by country.
        sort_by (Literal["asc", "desc"]): Sort order, either ascending
        or descending.

    Returns:
        list[PlayerListResponse]: A list of player responses matching the filters.
    """
    return player_crud.get_players(db, pagination, search, team, country, sort_by)


@router.get("/users", response_model=PlayerDetailResponse)
def get_players_by_user(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Retrieve player details for the current authenticated user.

    Args:
        db (Session): Database session dependency.
        current_user (UserResponse): The current authenticated user.

    Returns:
        PlayerDetailResponse: The player details response object.
    """
    return player_crud.get_player_by_user_id(db, current_user)


@router.get("/{player_id}", response_model=PlayerDetailResponse)
def get_player(player_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a player by their ID.

    Args:
        player_id (UUID): The unique identifier of the player.
        db (Session): Database session dependency.

    Returns:
        PlayerDetailResponse: The player details response object.
    """
    return player_crud.get_player(db, player_id)


@router.put("/{player_id}", response_model=PlayerListResponse)
def update_player(
    player_id: UUID,
    player: PlayerUpdate = Depends(),
    avatar: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Update a player's details by their ID.

    Args:
        player_id (UUID): The unique identifier of the player.
        player (PlayerUpdate): The player update data.
        avatar (UploadFile | None): Optional avatar file for the player.
        db (Session): Database session dependency.
        current_user (UserResponse): The current authenticated user.

    Returns:
        PlayerListResponse: The updated player response object.
    """
    return player_crud.update_player(db, player_id, player, avatar, current_user)
