from typing import Literal
from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session
from src.crud.convert_db_to_response import (
    convert_db_to_team_detailed_response,
    convert_db_to_team_list_response,
)
from src.models import Match, Player, Team, Tournament
from src.models.enums import Stage
from src.schemas.team import (
    TeamCreate,
    TeamDetailedResponse,
    TeamListResponse,
    TeamUpdate,
)
from src.schemas.user import UserResponse
from src.utils import validators as v
from src.utils.pagination import PaginationParams
from src.utils.s3 import s3_service
from starlette.status import HTTP_400_BAD_REQUEST


def get_teams(
    db: Session,
    pagination: PaginationParams,
    search: str | None = None,
    is_available: Literal["true", "false"] | None = None,
    has_space: Literal["true", "false"] | None = None,
    sort_by: Literal["asc", "desc"] = "asc",
) -> list[TeamListResponse]:
    """
    Retrieve a list of teams with optional filters and sorting.

    Args:
        db (Session): The database session.
        pagination (PaginationParams): The pagination parameters.
        search (str | None): Optional search term to filter teams by name.
        is_available (Literal["true", "false"] | None): Filter teams by availability.
        has_space (Literal["true", "false"] | None): Filter teams by player space.
        sort_by (Literal["asc", "desc"]): Sort order for the teams.

    Returns:
        list[TeamListResponse]: A list of team responses.
    """
    query = db.query(Team)

    if search:
        query = query.filter(Team.name.ilike(f"%{search}%"))

    if is_available == "true":
        query = query.filter(Team.tournament_id.is_(None))
    elif is_available == "false":
        query = query.filter(Team.tournament_id.isnot(None))

    db_results = query.all()

    if has_space:
        player_counts = (
            db.query(Player.team_id, func.count(Player.id).label("count"))
            .group_by(Player.team_id)
            .all()
        )

        team_player_counts = dict(player_counts)

        filtered_teams = []
        for team in db_results:
            player_count = team_player_counts.get(team.id, 0)

            if has_space == "true" and player_count < 10:
                filtered_teams.append(team)
            elif has_space == "false" and player_count >= 10:
                filtered_teams.append(team)

        db_results = filtered_teams

    sorted_teams = sorted(
        db_results,
        key=lambda team: (
            team.won_games / team.played_games if team.played_games > 0 else 0
        ),
        reverse=(sort_by == "desc"),
    )

    sorted_teams = sorted_teams[
        pagination.offset : pagination.offset + pagination.limit
    ]

    return [convert_db_to_team_list_response(team) for team in sorted_teams]


def create_team(
    db: Session, team: TeamCreate, logo: UploadFile | None, current_user: UserResponse
) -> TeamListResponse:
    """
    Create a new team with the provided data.

    Args:
        db (Session): The database session.
        team (TeamCreate): The team data to create.
        logo (UploadFile | None): The logo file for the team.
        current_user (UserResponse): The current user creating the team.

    Returns:
        TeamListResponse: The detailed response of the created team.
    """
    v.director_or_admin(current_user)

    v.team_name_unique(db, team_name=team.name)

    logo_url = None
    if logo is not None:
        logo_url = s3_service.upload_file(logo, "teams")

    db_team = Team(
        name=team.name,
        logo=logo_url,
    )

    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    return convert_db_to_team_list_response(db_team)


def get_team(db: Session, team_id: UUID) -> TeamDetailedResponse:
    """
    Retrieve detailed information about a team, including statistics.

    Args:
        db (Session): The database session.
        team_id (UUID): The ID of the team to retrieve.

    Returns:
        TeamDetailedResponse: The detailed response of the team.
    """
    db_team = v.team_exists(db, team_id=team_id)

    stats = {
        "tournaments_played": 0,
        "tournaments_won": 0,
        "tournament_win_loss_ratio": {"ratio": "0%", "won": 0, "played": 0},
        "matches_played": db_team.played_games,
        "matches_won": db_team.won_games,
        "match_win_loss_ratio": {"ratio": "0%", "wins": 0, "losses": 0},
        "most_often_played_opponent": None,
        "best_opponent": None,
        "worst_opponent": None,
    }

    matches = (
        db.query(Match)
        .filter((Match.team1_id == team_id) | (Match.team2_id == team_id))
        .all()
    )

    if not matches:
        return convert_db_to_team_detailed_response(db_team, matches, stats)

    opponent_stats = {}
    tournaments_played = set()

    for match in matches:
        if match.tournament.current_stage == Stage.FINISHED:
            tournaments_played.add(match.tournament_id)

        opponent_id = match.team2_id if match.team1_id == team_id else match.team1_id
        opponent_name = (
            match.team2.name if match.team1_id == team_id else match.team1.name
        )

        if opponent_id not in opponent_stats:
            opponent_stats[opponent_id] = {
                "wins": 0,
                "losses": 0,
                "games": 0,
                "opponent_name": opponent_name,
            }

        opponent_stats[opponent_id]["games"] += 1
        if match.winner_team_id == team_id:
            opponent_stats[opponent_id]["wins"] += 1
        else:
            opponent_stats[opponent_id]["losses"] += 1

    stats["tournaments_played"] = len(tournaments_played)
    stats["tournaments_won"] = sum(
        1
        for match in matches
        if match.winner_team_id == team_id and match.stage == Stage.FINAL
    )

    if opponent_stats:
        most_often_played_opponent_id = max(
            opponent_stats, key=lambda k: opponent_stats[k]["games"]
        )
        best_opponent_id = max(
            opponent_stats,
            key=lambda k: opponent_stats[k]["wins"] / opponent_stats[k]["games"],
        )
        worst_opponent_id = min(
            opponent_stats,
            key=lambda k: opponent_stats[k]["losses"] / opponent_stats[k]["games"],
        )

        stats["most_often_played_opponent"] = opponent_stats[
            most_often_played_opponent_id
        ]["opponent_name"]
        stats["best_opponent"] = opponent_stats[best_opponent_id]["opponent_name"]
        stats["worst_opponent"] = opponent_stats[worst_opponent_id]["opponent_name"]

    stats["match_win_loss_ratio"]["wins"] = stats["matches_won"]
    stats["match_win_loss_ratio"]["losses"] = (
        stats["matches_played"] - stats["matches_won"]
    )
    stats["match_win_loss_ratio"]["ratio"] = (
        f"{(stats['matches_won'] / stats['matches_played']) * 100:.0f}%"
        if stats["matches_played"] > 0
        else "0%"
    )

    stats["tournament_win_loss_ratio"]["won"] = stats["tournaments_won"]
    stats["tournament_win_loss_ratio"]["played"] = stats["tournaments_played"]
    stats["tournament_win_loss_ratio"]["ratio"] = (
        f"{(stats['tournaments_won'] / stats['tournaments_played']) * 100:.0f}%"
        if stats["tournaments_played"] > 0
        else "0%"
    )

    return convert_db_to_team_detailed_response(db_team, matches, stats)


def update_team(
    db: Session,
    team_id: UUID,
    team: TeamUpdate,
    logo: UploadFile | None,
    current_user: UserResponse,
) -> TeamListResponse:
    """
    Update an existing team with the provided data.

    Args:
        db (Session): The database session.
        team_id (UUID): The ID of the team to update.
        team (TeamUpdate): The updated team data.
        logo (UploadFile | None): The logo file for the team.
        current_user (UserResponse): The current user performing the update.

    Returns:
        TeamListResponse: The detailed response of the updated team.
    """
    db_team = v.team_exists(db, team_id=team_id)
    v.director_or_admin(current_user)

    if team.name:
        v.team_name_unique(db, team_name=team.name)
        db_team.name = team.name

    if logo is not None:
        if db_team.logo:
            s3_service.delete_file(str(db_team.logo))

        logo_url = s3_service.upload_file(logo, "teams")
        db_team.logo = logo_url

    db.commit()
    db.refresh(db_team)

    return convert_db_to_team_list_response(db_team)


def create_teams_lst_for_tournament(
    db: Session, team_names: list[str], tournament_id: UUID
) -> None:
    """
    Create a list of teams for a tournament, ensuring each team is unique
    and not already participating in another tournament.

    Args:
        db (Session): The database session.
        team_names (list[str]): The list of team names to add to the tournament.
        tournament_id (UUID): The ID of the tournament.

    Raises:
        HTTPException: If a team already participates in another tournament.
    """
    teams = []
    for name in team_names:
        db_team = db.query(Team).filter(Team.name == name).first()

        if db_team is None:
            v.team_name_unique(db, team_name=name)
            new_team = Team(name=name)
            db.add(new_team)
            db.flush()
            teams.append(new_team)
        else:
            if db_team.tournament_id is not None:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail=f"Team '{db_team.name}' already "
                    f"participates in another tournament",
                )

            teams.append(db_team)

    for db_team in teams:
        db_team.tournament_id = tournament_id


def leave_top_teams_from_robin_round(db, db_tournament: Tournament) -> None:
    """
    Retain the top two teams from a round-robin tournament and remove the rest.

    Args:
        db (Session): The database session.
        db_tournament (Tournament): The tournament object containing teams and matches.

    Returns:
        None
    """
    team_stats = {}
    for team in db_tournament.teams:
        team_stats[team] = {
            "points": 0,
            "wins": 0,
            "score_difference": 0,
            "total_score": 0,
        }

    for match in db_tournament.matches:
        team1 = match.team1
        team2 = match.team2

        team_stats[team1]["total_score"] += match.team1_score
        team_stats[team2]["total_score"] += match.team2_score

        team_stats[team1]["score_difference"] += match.team1_score - match.team2_score
        team_stats[team2]["score_difference"] += match.team2_score - match.team1_score

        winner = team1 if match.winner_team_id == team1.id else team2
        team_stats[winner]["points"] += 2
        team_stats[winner]["wins"] += 1

    sorted_teams = sorted(
        team_stats.keys(),
        key=lambda t: (
            team_stats[t]["points"],
            team_stats[t]["wins"],
            team_stats[t]["score_difference"],
            team_stats[t]["total_score"],
        ),
        reverse=True,
    )

    for team in sorted_teams[2:]:
        team.tournament_id = None

    db.flush()
