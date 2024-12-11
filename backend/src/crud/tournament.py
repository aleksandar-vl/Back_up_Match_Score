from datetime import datetime, timedelta, timezone
import math
from typing import Literal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, joinedload
from src.crud import (
    constants as c,
    match as crud_match,
    prize_cut as crud_prize_cut,
    team as crud_team,
)
from src.crud.convert_db_to_response import (
    convert_db_to_tournament_list_response,
    convert_db_to_tournament_response,
)
from src.models import Tournament
from src.models.enums import Role, Stage, TournamentFormat
from src.schemas.tournament import (
    TournamentCreate,
    TournamentDetailResponse,
    TournamentListResponse,
    TournamentUpdate,
)
from src.schemas.user import UserResponse
from src.utils import validators as v
from src.utils.pagination import PaginationParams
from starlette.status import HTTP_400_BAD_REQUEST


def get_tournaments(
    db: Session,
    pagination: PaginationParams,
    period: Literal["past", "present", "future"] | None = None,
    status: Literal["active", "finished"] | None = None,
    tournament_format: TournamentFormat | None = None,
    search: str | None = None,
    author_id: UUID | None = None,
) -> list[TournamentListResponse]:
    """
    Retrieve a list of tournaments based on various filters.

    Args:
        db (Session): The database session.
        pagination (PaginationParams): Pagination parameters.
        period (Literal["past", "present", "future"], optional):
        The period filter for tournaments.
        status (Literal["active", "finished"], optional):
        The status filter for tournaments.
        tournament_format (TournamentFormat, optional):
        The format filter for tournaments.
        search (str, optional): The search filter for tournament titles.
        author_id (UUID, optional): The author filter for tournaments.

    Returns:
        list[TournamentListResponse]: A list of tournament responses.
    """
    query = db.query(Tournament)

    filters = []
    filters.extend(_get_period_filter(period))
    filters.extend(_get_status_filter(status))
    filters.extend(_get_format_filter(tournament_format))
    filters.extend(_get_search_filter(search))
    filters.extend(_get_author_filter(author_id))

    if filters:
        query = query.filter(*filters)
    else:
        query = query.options(joinedload(Tournament.matches))

    query = query.order_by(Tournament.start_date.desc())
    query = query.offset(pagination.offset).limit(pagination.limit)

    db_tournaments = query.all()

    return [
        convert_db_to_tournament_list_response(db_tournament)
        for db_tournament in db_tournaments
    ]


def _get_period_filter(period: Literal["past", "present", "future"] | None) -> list:
    """
    Generate a filter for tournaments based on the specified period.

    Args:
        period (Literal["past", "present", "future"], optional):
        The period filter for tournaments.

    Returns:
        list: A list of SQLAlchemy filter conditions.
    """
    if not period:
        return []

    if period == "past":
        return [
            or_(
                Tournament.end_date < datetime.now(),
                Tournament.current_stage == Stage.FINISHED,
            )
        ]
    elif period == "present":
        return [
            and_(
                Tournament.start_date <= datetime.now(),
                Tournament.end_date >= datetime.now(),
                Tournament.current_stage != Stage.FINISHED,
            )
        ]
    elif period == "future":
        return [
            and_(
                Tournament.start_date > datetime.now(),
                Tournament.current_stage != Stage.FINISHED,
            )
        ]


def _get_status_filter(status: Literal["active", "finished"] | None) -> list:
    """
    Generate a filter for tournaments based on the specified status.

    Args:
        status (Literal["active", "finished"], optional):
        The status filter for tournaments.

    Returns:
        list: A list of SQLAlchemy filter conditions.
    """
    if not status:
        return []

    if status == "active":
        return [Tournament.current_stage != Stage.FINISHED]
    elif status == "finished":
        return [Tournament.current_stage == Stage.FINISHED]


def _get_format_filter(tournament_format: TournamentFormat | None) -> list:
    """
    Generate a filter for tournaments based on the specified format.

    Args:
        tournament_format (TournamentFormat, optional):
        The format filter for tournaments.

    Returns:
        list: A list of SQLAlchemy filter conditions.
    """
    if not tournament_format:
        return []

    return [Tournament.tournament_format == tournament_format]


def _get_search_filter(search: str | None) -> list:
    """
    Generate a filter for tournaments based on the search query.

    Args:
        search (str, optional): The search filter for tournament titles.

    Returns:
        list: A list of SQLAlchemy filter conditions.
    """
    if not search:
        return []

    return [Tournament.title.ilike(f"%{search}%")]


def _get_author_filter(author_id: UUID | None) -> list:
    """
    Generate a filter for tournaments based on the author's ID.

    Args:
        author_id (UUID, optional): The author's ID filter for tournaments.

    Returns:
        list: A list of SQLAlchemy filter conditions.
    """
    if not author_id:
        return []

    return [Tournament.director_id == author_id]


def get_tournament(db: Session, tournament_id: UUID) -> TournamentListResponse:
    """
    Retrieve a tournament by its ID and gather its participants.

    Args:
        db (Session): The database session.
        tournament_id (UUID): The ID of the tournament to retrieve.

    Returns:
        TournamentListResponse: The detailed response of the tournament.
    """
    db_tournament = v.tournament_exists(db, tournament_id)

    participants = []
    for db_match in db_tournament.matches:
        if db_match.team1_id not in participants:
            participants.append(db_match.team1)
        if db_match.team2_id not in participants:
            participants.append(db_match.team2)

    return convert_db_to_tournament_response(db_tournament)


def create_tournament(
    db: Session, tournament: TournamentCreate, current_user: UserResponse
) -> TournamentDetailResponse:
    """
    Create a new tournament and validate the provided data.

    Args:
        db (Session): The database session.
        tournament (TournamentCreate): The tournament data to create.
        current_user (UserResponse): The current user creating the tournament.

    Returns:
        TournamentDetailResponse: The detailed response of the created tournament.
    """
    try:
        # Creating a new tournament
        db.begin_nested()

        # Validating the tournament data
        v.unique_teams_in_tournament(tournament.team_names)
        v.tournament_title_unique(db, tournament.title)
        v.director_or_admin(current_user)
        v.validate_start_date(tournament.start_date)
        tournament.start_date = tournament.start_date.replace(
            hour=11, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
        )

        # get current stage for tournament
        total_teams = len(tournament.team_names)
        current_stage = _get_tournament_current_stage(
            tournament.tournament_format.value, total_teams
        )

        # calculating the end date
        end_date = _calculate_tournament_end_date(
            tournament.start_date,
            tournament.tournament_format,
            current_stage,
            total_teams,
        )

        # Creating the tournament
        db_tournament = Tournament(
            title=tournament.title,
            tournament_format=TournamentFormat(tournament.tournament_format),
            start_date=tournament.start_date,
            end_date=end_date,
            prize_pool=tournament.prize_pool,
            current_stage=current_stage,
            director_id=current_user.id,
        )

        db.add(db_tournament)
        db.flush()

        crud_prize_cut.create_prize_cuts_for_tournament(
            db, db_tournament, db_tournament.prize_pool
        )
        crud_team.create_teams_lst_for_tournament(
            db, tournament.team_names, db_tournament.id
        )

        db.flush()

        crud_match.generate_matches(db, db_tournament)
        tournament = convert_db_to_tournament_response(db_tournament)
        db.commit()

        return tournament

    except Exception as e:
        # Ensure no changes are made to the database
        db.rollback()
        raise e


def _get_tournament_current_stage(
    tournament_format: str, number_of_teams: int
) -> Stage:
    """
    Determine the current stage of a tournament
    based on its format and number of teams.

    Args:
        tournament_format (str): The format of the tournament.
        number_of_teams (int): The number of teams in the tournament.

    Returns:
        Stage: The current stage of the tournament.

    Raises:
        HTTPException: If the number of teams is invalid
        for the given tournament format.
    """
    if tournament_format == TournamentFormat.SINGLE_ELIMINATION:
        if number_of_teams not in c.SINGLE_ELIMINATION_TEAMS:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid number of teams for single elimination "
                "- must be 4, 8 or 16",
            )

        if number_of_teams == 4:
            return Stage.SEMI_FINAL
        elif number_of_teams == 8:
            return Stage.QUARTER_FINAL

    elif tournament_format == TournamentFormat.ROUND_ROBIN:
        if number_of_teams not in c.ROUND_ROBIN_TEAMS:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid number of teams for round robin - must be 4 or 5",
            )
        return Stage.GROUP_STAGE

    elif tournament_format == TournamentFormat.ONE_OFF_MATCH:
        if number_of_teams not in c.ONE_OFF_MATCH_TEAMS:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid number of teams for one off match - must be 2",
            )
        return Stage.FINAL


def _calculate_tournament_end_date(
    start_date: datetime,
    tournament_format: TournamentFormat,
    current_stage: Stage,
    total_teams: int,
) -> datetime:
    """
    Calculate the end date of a tournament based on its start date,
    format, current stage, and total number of teams.

    Args:
        start_date (datetime): The start date of the tournament.
        tournament_format (TournamentFormat): The format of the tournament.
        current_stage (Stage): The current stage of the tournament.
        total_teams (int): The total number of teams in the tournament.

    Returns:
        datetime: The calculated end date of the tournament.
    """
    if tournament_format == TournamentFormat.ROUND_ROBIN:
        total_matches = total_teams * (total_teams - 1) // 2
        required_days = math.ceil((total_matches - 1) / c.MAX_MATCHES_PER_DAY) + 1
    else:
        required_days = c.STAGE_DAYS[current_stage]

    end_date = start_date + timedelta(days=required_days)
    end_date = end_date.replace(hour=23, minute=59, second=59)
    return end_date


def update_tournament(
    db: Session,
    tournament_id: UUID,
    tournament: TournamentUpdate,
    current_user: UserResponse,
) -> TournamentDetailResponse:
    """
    Update an existing tournament with the provided data.

    Args:
        db (Session): The database session.
        tournament_id (UUID): The ID of the tournament to update.
        tournament (TournamentUpdate): The updated tournament data.
        current_user (UserResponse): The current user performing the update.

    Returns:
        TournamentDetailResponse: The detailed response of the updated tournament.

    Raises:
        HTTPException: If any validation fails.
    """
    try:
        db.begin_nested()

        # Validating the tournament data
        v.director_or_admin(current_user)
        db_tournament = v.tournament_exists(db, tournament_id)
        v.tournament_is_finished(db_tournament)

        if current_user.role != Role.ADMIN:
            v.tournament_has_started(db_tournament)

        if current_user.role == Role.DIRECTOR:
            v.is_author_of_tournament(db, tournament_id, current_user.id)

        if tournament.title is not None:
            if len(tournament.title) == 0:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST, detail="Title must not be empty"
                )
            v.tournament_title_unique(db, tournament.title)
            db_tournament.title = tournament.title

        if tournament.end_date is not None:
            v.validate_old_vs_new_end_date(db_tournament.end_date, tournament.end_date)
            db_tournament.end_date = tournament.end_date

        if tournament.prize_pool is not None:
            crud_prize_cut.delete_prize_cuts_for_tournament(db, db_tournament)
            db_tournament.prize_pool = tournament.prize_pool

        if tournament.prize_pool:
            crud_prize_cut.create_prize_cuts_for_tournament(
                db, db_tournament, int(tournament.prize_pool)
            )

        db.commit()
        db.refresh(db_tournament)

        return convert_db_to_tournament_response(db_tournament)

    except Exception as e:
        db.rollback()
        raise e
