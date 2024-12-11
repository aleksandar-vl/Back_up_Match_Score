from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.crud.convert_db_to_response import (
    convert_db_to_player_detail_response,
    convert_db_to_player_list_response,
)
from src.models import Player
from src.schemas.player import (
    PlayerCreate,
    PlayerDetailResponse,
    PlayerListResponse,
    PlayerUpdate,
)
from src.schemas.user import UserResponse
from src.utils import validators as v
from src.utils.pagination import PaginationParams
from src.utils.s3 import s3_service


def create_player(
    db: Session,
    player: PlayerCreate,
    avatar: UploadFile | None,
    current_user: UserResponse,
) -> PlayerListResponse:
    """
    Create a new player in the database.

    Args:
        db (Session): The database session.
        player (PlayerCreate): The player creation schema.
        avatar (UploadFile | None): The player's avatar file.
        current_user (UserResponse): The current user making the request.

    Returns:
        PlayerListResponse: The response schema for the created player.
    """
    v.player_username_unique(db, username=player.username)
    v.director_or_admin(current_user)

    if player.team_name:
        db_team = v.team_exists(db, team_name=player.team_name)
        v.team_player_limit_reached(db_team)

    avatar_url = None
    if avatar is not None:
        avatar_url = s3_service.upload_file(avatar, "players")

    db_player = Player(
        username=player.username,
        first_name=player.first_name,
        last_name=player.last_name,
        country=player.country,
        avatar=avatar_url,
        team_id=db_team.id if player.team_name else None,
    )

    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return convert_db_to_player_list_response(db_player)


def get_players(
    db: Session,
    pagination: PaginationParams,
    search: str | None = None,
    team: str | None = None,
    country: str | None = None,
    sort_by: str = "asc",
) -> list[PlayerListResponse]:
    """
    Retrieve a list of players from the database
    with optional filtering, sorting, and pagination.

    Args:
        db (Session): The database session.
        pagination (PaginationParams): The pagination parameters.
        search (str | None): Optional search term for player username.
        team (str | None): Optional filter for team name.
        country (str | None): Optional filter for country.
        sort_by (str): Sort order, either 'asc' for ascending or 'desc' for descending.

    Returns:
        list[PlayerListResponse]: A list of player response objects.
    """
    query = db.query(Player).order_by(Player.username.asc())

    filters = []
    if search:
        filters.append(Player.username.ilike(f"%{search}%"))
    if team:
        filters.append(Player.team.ilike(f"%{team}%"))
    if country:
        filters.append(Player.country.ilike(f"%{country}%"))

    if filters:
        query = query.filter(*filters)

    query = query.offset(pagination.offset).limit(pagination.limit)

    db_players = query.all()

    sorted_players = sorted(
        db_players,
        key=lambda player: (
            player.won_games / player.played_games if player.played_games > 0 else 0
        ),
        reverse=(sort_by == "desc"),
    )

    return [convert_db_to_player_list_response(player) for player in sorted_players]


def get_player(db: Session, player_id: UUID) -> PlayerDetailResponse:
    """
    Retrieve a player's details from the database.

    Args:
        db (Session): The database session.
        player_id (UUID): The ID of the player.

    Returns:
        PlayerDetailResponse: The detailed response schema for the player.
    """
    db_player = v.player_exists(db, player_id)

    tournament_title = None
    if db_player.team_id and db_player.team.tournament_id:
        tournament_title = db_player.team.tournament.title

    return convert_db_to_player_detail_response(db_player, tournament_title)


def get_player_by_user_id(
    db: Session, current_user: UserResponse
) -> PlayerDetailResponse:
    """
    Retrieve a player's details by the user ID from the database.

    Args:
        db (Session): The database session.
        current_user (UserResponse): The current user making the request.

    Returns:
        PlayerDetailResponse: The detailed response schema for the player.
    """
    v.user_associated_with_player(current_user)
    db_player = db.query(Player).filter(Player.user_id == current_user.id).first()

    tournament_title = None
    if db_player.team_id and db_player.team.tournament_id:
        tournament_title = db_player.team.tournament.title

    return convert_db_to_player_detail_response(db_player, tournament_title)


def update_player(
    db: Session,
    player_id: UUID,
    player: PlayerUpdate,
    avatar: UploadFile | None,
    current_user: UserResponse,
) -> PlayerListResponse:
    """
    Update an existing player's details in the database.

    Args:
        db (Session): The database session.
        player_id (UUID): The ID of the player to update.
        player (PlayerUpdate): The player update schema.
        avatar (UploadFile | None): The player's new avatar file.
        current_user (UserResponse): The current user making the request.

    Returns:
        PlayerListResponse: The response schema for the updated player.
    """
    db_player = v.player_exists(db, player_id=player_id)

    if db_player.user_id:
        v.player_update_current_user_authorization(db_player, current_user)
    else:
        v.director_or_admin(current_user)

    if player.username is not None:
        v.player_username_unique(db, username=player.username)
        db_player.username = player.username
    if player.first_name is not None:
        db_player.first_name = player.first_name
    if player.last_name is not None:
        db_player.last_name = player.last_name
    if player.country is not None:
        db_player.country = player.country
    if player.team_name is not None:
        team = v.team_exists(db, team_name=player.team_name)
        v.team_player_limit_reached(team)
        db_player.team_id = team.id

    if avatar is not None:
        if db_player.avatar:
            s3_service.delete_file(str(db_player.avatar))

        avatar_url = s3_service.upload_file(avatar, "players")
        db_player.avatar = avatar_url

    db.commit()
    db.refresh(db_player)

    return convert_db_to_player_list_response(db_player)
