from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.params import Path
from sqlalchemy.orm import Session
from src.api.deps import get_current_user, get_db
from src.crud.request import (
    get_all,
    get_current_user_request,
    send_director_request,
    send_link_to_player_request,
    update_request,
)
from src.models import User
from src.utils.pagination import PaginationParams, get_pagination

router = APIRouter()


@router.post("/directors/{user_id}")
def director_request(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Send a request to promote the current user to a director.

    Args:
        db (Session): Database session dependency.
        current_user (User): The current authenticated user.

    Returns:
        The result of the director request operation.
    """
    return send_director_request(db, current_user)


@router.post("/players/{username}")
def player_request(
    username: str = Path(description="player_username"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send a request to link the current user to a player by username.

    Args:
        username (str): The username of the player to link.
        db (Session): Database session dependency.
        current_user (User): The current authenticated user.

    Returns:
        The result of the link to player request operation.
    """
    return send_link_to_player_request(db, current_user, username)


@router.get("/")
def get_all_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    sort_by: Literal["asc", "desc"] = "desc",
    status: Literal["pending", "accepted", "rejected"] | None = None,
    request_type: (
        Literal["link user to player", "promote user to director"] | None
    ) = None,
    filter_by_current_admin: bool = False,
    pagination: PaginationParams = Depends(get_pagination),
):
    """
    Retrieve all requests with optional filters and pagination.

    Args:
        db (Session): Database session dependency.
        current_user (User): The current authenticated user.
        sort_by (Literal["asc", "desc"]): Sort order for the requests.
        status (Literal["pending", "accepted", "rejected"] | None):
        Filter by request status.
        request_type (Literal["link user to player",
        "promote user to director"] | None): Filter by request type.
        filter_by_current_admin (bool): Filter requests by the current admin.
        pagination (PaginationParams): Pagination parameters.

    Returns:
        List[Request]: A list of requests matching the filters.
    """
    return get_all(
        db,
        current_user,
        pagination,
        sort_by,
        status,
        request_type,
        filter_by_current_admin,
    )


@router.put("/{request_id}")
def put_request(
    status: Literal["accepted", "rejected"],
    request_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the status of a request by its ID.

    Args:
        status (Literal["accepted", "rejected"]):
        The new status of the request.
        request_id (UUID): The unique identifier of the request.
        db (Session): Database session dependency.
        current_user (User): The current authenticated user.

    Returns:
        The result of the update request operation.
    """
    return update_request(db, current_user, status, request_id)


@router.get("/me")
def get_my_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(get_pagination),
):
    """
    Retrieve the current user's requests with pagination.

    Args:
        db (Session): Database session dependency.
        current_user (User): The current authenticated user.
        pagination (PaginationParams): Pagination parameters.

    Returns:
        List[Request]: A list of the current user's requests.
    """
    return get_current_user_request(db, current_user, pagination)
