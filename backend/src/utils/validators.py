from datetime import datetime, timedelta, timezone
from typing import Type
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models import Match, Player, Request, Tournament, User
from src.models.enums import Role, Stage
from src.models.team import Team
from src.schemas.user import UserResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)


# existing validators
def tournament_exists(
    db: Session, tournament_id: UUID | None = None, tournament_title: str | None = None
) -> Type[Tournament]:
    """
    Checks if a tournament exists by its ID or title.

    Args:
        db (Session): The database session.
        tournament_id (UUID, optional): The ID of the tournament.
        tournament_title (str, optional): The title of the tournament.

    Returns:
        Type[Tournament]: The tournament instance if found.

    Raises:
        HTTPException: If the tournament is not found.
    """

    tournament = None
    if tournament_id:
        tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    elif tournament_title:
        tournament = (
            db.query(Tournament).filter(Tournament.title == tournament_title).first()
        )

    if not tournament:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Tournament not found"
        )

    return tournament


def team_exists(
    db: Session,
    team_id: UUID | None = None,
    team_name: str | None = None,
) -> Type[Team]:
    """
    Checks if a team exists by its ID or name.

    Args:
        db (Session): The database session.
        team_id (UUID, optional): The ID of the team.
        team_name (str, optional): The name of the team.

    Returns:
        Type[Team]: The team instance if found.

    Raises:
        HTTPException: If the team is not found.
    """

    team = None
    if team_id:
        team = db.query(Team).filter(Team.id == team_id).first()
    elif team_name:
        team = db.query(Team).filter(Team.name == team_name).first()

    if not team:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Team not found")

    return team


def match_exists(db: Session, match_id: UUID) -> Type[Match]:
    """
    Checks if a match exists by its ID.

    Args:
        db (Session): The database session.
        match_id (UUID): The ID of the match.

    Returns:
        Type[Match]: The match instance if found.

    Raises:
        HTTPException: If the match is not found.
    """
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Match not found")

    return match


def user_exists(
    db: Session,
    user_id: UUID | None = None,
    user_email: str | None = None,
) -> Type[User]:
    """
    Checks if a user exists by their ID or email.

    Args:
        db (Session): The database session.
        user_id (UUID, optional): The ID of the user.
        user_email (str, optional): The email of the user.

    Returns:
        Type[User]: The user instance if found.

    Raises:
        HTTPException: If the user is not found.
    """
    user = None

    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
    if user_email:
        user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    return user


def request_exists(db: Session, request_id: UUID) -> Type[Request]:
    """
    Checks if a request exists by its ID.

    Args:
        db (Session): The database session.
        request_id (UUID): The ID of the request.

    Returns:
        Type[Request]: The request instance if found.

    Raises:
        HTTPException: If the request is not found.
    """
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Request not found.")

    return request


def player_exists(
    db: Session, player_id: UUID | None = None, username: str | None = None
) -> Type[Player]:
    """
    Checks if a player exists by their ID or username.

    Args:
        db (Session): The database session.
        player_id (UUID, optional): The ID of the player.
        username (str, optional): The username of the player.

    Returns:
        Type[Player]: The player instance if found.

    Raises:
        HTTPException: If the player is not found.
    """

    player = None
    if player_id:
        player = db.query(Player).filter(Player.id == player_id).first()
    else:
        player = db.query(Player).filter(Player.username == username).first()

    if not player:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Player not found")

    return player


def player_username_unique(db: Session, username: str) -> None:
    """
    Checks if a player's username is unique.

    Args:
        db (Session): The database session.
        username (str): The username to check.

    Raises:
        HTTPException: If the username already exists.
    """
    if db.query(Player).filter(Player.username == username).first():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Player with this username already exists",
        )


def team_name_unique(db: Session, team_name: str) -> None:
    """
    Checks if a team's name is unique.

    Args:
        db (Session): The database session.
        team_name (str): The team name to check.

    Raises:
        HTTPException: If the team name already exists.
    """
    if db.query(Team).filter(Team.name == team_name).first():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Team '{team_name}' already exists",
        )


def player_already_linked(db: Session, username: str) -> None:
    """
    Checks if a player is already linked to a user.

    Args:
        db (Session): The database session.
        username (str): The username of the player.

    Raises:
        HTTPException: If the player is already linked to a user.
    """
    player = db.query(Player).filter(Player.username == username).first()
    if player and player.user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Player is already linked to a user.",
        )


def user_email_exists(db: Session, email: str) -> None:
    """
    Checks if a user's email already exists.

    Args:
        db (Session): The database session.
        email (str): The email to check.

    Raises:
        HTTPException: If the email already exists.
    """
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Email already exists"
        )


def tournament_title_unique(db: Session, title: str) -> None:
    """
    Checks if a tournament's title is unique.

    Args:
        db (Session): The database session.
        title (str): The title to check.

    Raises:
        HTTPException: If the title already exists.
    """
    if db.query(Tournament).filter(Tournament.title == title).first():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Tournament with this title already exists",
        )


# authorisation validators
def director_or_admin(user: UserResponse) -> None:
    """
    Checks if the user is a director or admin.

    Args:
        user (UserResponse): The user to check.

    Raises:
        HTTPException: If the user is not a director or admin.
    """
    if user.role not in [Role.DIRECTOR, Role.ADMIN]:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )


def is_author_of_tournament(db: Session, tournament_id: UUID, user_id: UUID) -> None:
    """
    Checks if the user is the author of the tournament.

    Args:
        db (Session): The database session.
        tournament_id (UUID): The ID of the tournament.
        user_id (UUID): The ID of the user.

    Raises:
        HTTPException: If the user is not the author of the tournament.
    """
    db_tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if db_tournament.director_id != user_id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )


def user_role_is_admin(current_user: User) -> None:
    """
    Checks if the user's role is admin.

    Args:
        current_user (User): The user to check.

    Raises:
        HTTPException: If the user's role is not admin.
    """
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action.",
        )


def user_role_is_user(current_user: User) -> None:
    """
    Checks if the user's role is user.

    Args:
        current_user (User): The user to check.

    Raises:
        HTTPException: If the user's role is not user.
    """
    if current_user.role != Role.USER:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Only users can send requests."
        )


def player_update_current_user_authorization(db_player, current_user) -> None:
    """
    Checks if the current user is authorized to update the player.

    Args:
        db_player: The player to update.
        current_user: The current user.

    Raises:
        HTTPException: If the user is not authorized to update the player.
    """
    if db_player.user_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this player",
        )


# datetime validators
def validate_start_date(start_date) -> None:
    """
    Validates the start date to be at least 1 day in the future.

    Args:
        start_date: The start date to validate.

    Raises:
        HTTPException: If the start date is less than 1 day in the future.
    """
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)

    if start_date < tomorrow:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Start date must be at least 1 day in the future",
        )


def validate_old_vs_new_end_date(old_end_date, new_end_date) -> None:
    """
    Validates that the new end date is after the old end date.

    Args:
        old_end_date: The old end date.
        new_end_date: The new end date.

    Raises:
        HTTPException: If the new end date is before the old end date.
    """
    old_end_date = old_end_date.replace(tzinfo=timezone.utc)
    new_end_date = new_end_date.replace(tzinfo=timezone.utc)
    if old_end_date > new_end_date:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"New end date must be after "
            f"{old_end_date.strftime('%Y-%m-%d %H:%M:%S')}",
        )


def unique_teams_in_tournament(teams: list[str]) -> None:
    """
    Validates that there are no duplicate teams in the tournament list.

    Args:
        teams (list[str]): The list of teams.

    Raises:
        HTTPException: If there is a duplicate team in the list.
    """
    if len(teams) != len(set(teams)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="There is a duplicate team in the tournament list",
        )


# state of match
def match_is_finished(match: Type[Match]) -> None:
    """
    Checks if the match is finished.

    Args:
        match (Type[Match]): The match to check.

    Raises:
        HTTPException: If the match is already finished.
    """
    if match.is_finished:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Match is already finished"
        )


def match_has_started(match: Type[Match]) -> None:
    """
    Checks if the match has started.

    Args:
        match (Type[Match]): The match to check.

    Raises:
        HTTPException: If the match has already started.
    """
    match_start = match.start_time.replace(tzinfo=timezone.utc)
    if (match.team1_score > 0 or match.team2_score > 0) or (
        match_start < datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Match has already started"
        )


def team_has_five_players(team: Type[Team]) -> None:
    """
    Checks if the team has 5 players.

    Args:
        team (Type[Team]): The team to check.

    Raises:
        HTTPException: If the team does not have 5 players.
    """
    if len(team.players) < 5:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Team '{team.name}' must have 5 players",
        )


# state of tournament
def tournament_is_finished(tournament: Type[Tournament]) -> None:
    """
    Checks if the tournament is finished.

    Args:
        tournament (Type[Tournament]): The tournament to check.

    Raises:
        HTTPException: If the tournament is already finished.
    """
    tournament_end = tournament.end_date.replace(tzinfo=timezone.utc)
    if (tournament.current_stage == Stage.FINISHED) or (
        tournament_end < datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Tournament is already finished"
        )


def tournament_has_started(tournament: Type[Tournament]) -> None:
    """
    Checks if the tournament has started.

    Args:
        tournament (Type[Tournament]): The tournament to check.

    Raises:
        HTTPException: If the tournament has already started.
    """
    tournament_start = tournament.start_date.replace(tzinfo=timezone.utc)
    flag = False
    for match in tournament.matches:
        if match.team1_score != 0 or match.team2_score != 0:
            flag = True

    if (tournament_start < datetime.now(timezone.utc)) or flag:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Tournament has already started"
        )


def team_player_limit_reached(team: Type[Team]) -> None:
    """
    Checks if the team has reached the player limit.

    Args:
        team (Type[Team]): The team to check.

    Raises:
        HTTPException: If the team has reached the player limit.
    """
    if len(team.players) == 10:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Team has reached the player limit"
        )


def user_associated_with_player(user: User) -> None:
    """
    Checks if the user is associated with a player.

    Args:
        user (User): The user to check.

    Raises:
        HTTPException: If the user is not associated with a player.
    """
    if user.role != Role.PLAYER:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="User does not have associated player",
        )
