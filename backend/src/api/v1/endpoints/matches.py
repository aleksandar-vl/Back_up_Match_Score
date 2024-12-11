from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.deps import get_current_user, get_db
from src.crud import match as match_crud
from src.models.enums import Stage
from src.schemas.match import (
    MatchResponse,
    MatchUpdate,
)
from src.utils.pagination import PaginationParams, get_pagination

router = APIRouter()


@router.get("/", response_model=list[MatchResponse])
def read_matches(
    pagination: PaginationParams = Depends(get_pagination),
    db: Session = Depends(get_db),
    tournament_title: str | None = None,
    stage: Stage | None = None,
    is_finished: bool | None = None,
    team_name: str | None = None,
):
    """
    Retrieve a list of matches with optional filtering parameters.

    Args:
        pagination (PaginationParams): Pagination parameters for the query.
        db (Session): Database session dependency.
        tournament_title (str | None): Optional filter by tournament title.
        stage (Stage | None): Optional filter by match stage.
        is_finished (bool | None): Optional filter by match completion status.
        team_name (str | None): Optional filter by team name.

    Returns:
        list[MatchResponse]: A list of match responses matching the filters.
    """

    return match_crud.get_all_matches(
        db,
        pagination,
        tournament_title,
        stage,
        is_finished,
        team_name,
    )


@router.get("/{match_id}", response_model=MatchResponse)
def read_match(match_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a match by its ID.

    Args:
        match_id (UUID): The unique identifier of the match.
        db (Session): Database session dependency.

    Returns:
        MatchResponse: The match response object.
    """
    return match_crud.get_match(db, match_id)


@router.put("/{match_id}", response_model=MatchResponse)
def update_match(
    match_id: UUID,
    match: MatchUpdate = Depends(),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update a match by its ID.

    Args:
        match_id (UUID): The unique identifier of the match.
        match (MatchUpdate): The match update data.
        db (Session): Database session dependency.
        current_user: The current authenticated user.

    Returns:
        MatchResponse: The updated match response object.
    """
    return match_crud.update_match(db, match_id, match, current_user)


@router.put("/{match_id}/team-scores", response_model=MatchResponse)
def update_match_score(
    match_id: UUID,
    team_to_upvote_score: Literal["team1", "team2"],
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update the score of a match by its ID.

    Args:
        match_id (UUID): The unique identifier of the match.
        team_to_upvote_score (Literal["team1", "team2"]):
        The team whose score should be upvoted.
        db (Session): Database session dependency.
        current_user: The current authenticated user.

    Returns:
        MatchResponse: The updated match response object.
    """
    return match_crud.update_match_score(
        db, match_id, team_to_upvote_score, current_user
    )
