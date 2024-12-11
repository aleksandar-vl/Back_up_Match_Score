from datetime import datetime
from typing import Literal, Type
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from src.models import Player, Request, User
from src.models.enums import RequestStatus, RequestType, Role
from src.schemas.request import RequestListResponse, ResponseRequest
from src.utils.notifications import send_email_notification
from src.utils.pagination import PaginationParams
from src.utils.validators import (
    player_already_linked,
    player_exists,
    request_exists,
    user_exists,
    user_role_is_admin,
    user_role_is_user,
)


def get_all(
    db: Session,
    current_user: User,
    pagination: PaginationParams,
    sort_by: Literal["asc", "desc"] = "desc",
    status: Literal["pending", "accepted", "rejected"] | None = None,
    request_type: (
        Literal["link user to player", "promote user to director"] | None
    ) = None,
    filter_by_admin: bool = False,
) -> list[RequestListResponse]:
    """
    Retrieve all requests from the database
    with optional filtering, sorting, and pagination.

    Args:
        db (Session): The database session.
        current_user (User): The current user making the request.
        pagination (PaginationParams): The pagination parameters.
        sort_by (Literal["asc", "desc"]): Sort order, either 'asc'
        for ascending or 'desc' for descending.
        status (Literal["pending", "accepted", "rejected"] | None):
        Optional filter for request status.
        request_type (Literal["link user to player",
        "promote user to director"] | None): Optional filter for request type.
        filter_by_admin (bool): Optional filter to only include
        requests handled by the current admin.

    Returns:
        list[RequestListResponse]: A list of request response objects.
    """
    user_role_is_admin(current_user)
    query = db.query(Request)

    if status:
        query = query.filter(Request.status == status)

    if request_type:
        query = query.filter(Request.request_type == request_type)

    if filter_by_admin:
        query = query.filter(Request.admin_id == current_user.id)

    if sort_by == "asc":
        query = query.order_by(asc(Request.request_date))
    elif sort_by == "desc":
        query = query.order_by(desc(Request.request_date))

    query = query.offset(pagination.offset).limit(pagination.limit)

    result = [
        RequestListResponse(
            id=request.id,
            email=request.user.email,
            request_type=request.request_type,
            status=request.status,
            request_date=request.request_date,
            response_date=request.response_date,
            admin_id=request.admin_id,
            username=request.username,
        )
        for request in query
    ]
    return result


def get_current_user_request(
    db: Session, current_user: User, pagination: PaginationParams
) -> list[ResponseRequest]:
    """
    Retrieve the current user's requests from the database with pagination.

    Args:
        db (Session): The database session.
        current_user (User): The current user making the request.
        pagination (PaginationParams): The pagination parameters.

    Returns:
        list[ResponseRequest]: A list of response request objects for the current user.
    """
    query = db.query(Request).filter(Request.user_id == current_user.id)
    query = query.order_by(desc(Request.request_date))
    query = query.offset(pagination.offset).limit(pagination.limit)

    result = [
        ResponseRequest(
            request_type=request.request_type,
            status=request.status,
            request_date=request.request_date,
            response_date=request.response_date,
        )
        for request in query
    ]
    return result


def send_director_request(db: Session, current_user: User) -> ResponseRequest:
    """
    Send a request to promote the current user to director.

    Args:
        db (Session): The database session.
        current_user (User): The current user making the request.

    Returns:
        ResponseRequest: The response request object for the director promotion request.
    """
    user_role_is_user(current_user)
    check_valid_request(db, current_user)

    db_request = Request(
        user_id=current_user.id, request_type=RequestType.PROMOTE_USER_TO_DIRECTOR
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return ResponseRequest(
        request_type=db_request.request_type,
        request_date=db_request.request_date,
        status=db_request.status,
        response_date=db_request.response_date,
    )


def send_link_to_player_request(
    db: Session, current_user: User, username: str
) -> ResponseRequest:
    """
    Send a request to link the current user to a player.

    Args:
        db (Session): The database session.
        current_user (User): The current user making the request.
        username (str): The username of the player to link to.

    Returns:
        ResponseRequest: The response request object for the link to player request.
    """
    user_role_is_user(current_user)
    player_exists(db, username=username)
    player_already_linked(db, username)
    check_valid_request(db, current_user)

    db_request = Request(
        user_id=current_user.id,
        request_type=RequestType.LINK_USER_TO_PLAYER,
        username=username,
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return ResponseRequest(
        request_type=db_request.request_type,
        request_date=db_request.request_date,
        status=db_request.status,
        response_date=db_request.response_date,
    )


def check_valid_request(db: Session, current_user: User) -> None:
    """
    Check if the current user has a pending request.

    Args:
        db (Session): The database session.
        current_user (User): The current user making the request.

    Raises:
        HTTPException: If the user already has a pending request.
    """
    existing_request = (
        db.query(Request)
        .filter(
            Request.user_id == current_user.id, Request.status == RequestStatus.PENDING
        )
        .first()
    )
    if existing_request and existing_request.status == RequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already have a pending request.",
        )


def update_request(
    db: Session,
    current_user: User,
    status: Literal["accepted", "rejected"],
    request_id: UUID,
) -> ResponseRequest:
    """
    Update the status of a request.

    Args:
        db (Session): The database session.
        current_user (User): The current user making the request.
        status (Literal["accepted", "rejected"]): The new status of the request.
        request_id (UUID): The ID of the request to update.

    Returns:
        ResponseRequest: The response request object with the updated status.
    """
    user_role_is_admin(current_user)
    request = request_exists(db, request_id)
    user = user_exists(db, request.user_id)
    check_request_status(request)

    if request.request_type == RequestType.LINK_USER_TO_PLAYER:
        player = player_exists(db, username=request.username)
        return get_link_to_player_requests(
            db, current_user, user, status, request, player
        )

    elif request.request_type == RequestType.PROMOTE_USER_TO_DIRECTOR:
        return get_director_requests(db, current_user, status, request)


def get_director_requests(
    db, admin: User, status: str, request: Request
) -> ResponseRequest:
    """
    Handle a request to promote a user to director.

    Args:
        db (Session): The database session.
        admin (User): The admin handling the request.
        status (str): The status of the request, either 'accepted' or 'rejected'.
        request (Request): The request object.

    Returns:
        ResponseRequest: The response request object with the updated status.
    """
    user_id = request.user_id
    user = user_exists(db, user_id)

    if status == RequestStatus.ACCEPTED:
        send_email_notification(
            email=user.email,
            subject="Request Accepted",
            message="Your request to be promoted to director has been accepted.",
        )
        return accept_director_request(db, admin, user, request)

    elif status == RequestStatus.REJECTED:
        send_email_notification(
            email=user.email,
            subject="Request Rejected",
            message="Your request to be promoted to director has been rejected.",
        )
        return reject_director_request(db, admin, request)


def accept_director_request(
    db, admin: User, user: User, request: Request
) -> ResponseRequest:
    """
    Accept a request to promote a user to director.

    Args:
        db (Session): The database session.
        admin (User): The admin handling the request.
        user (User): The user to be promoted.
        request (Request): The request object.

    Returns:
        ResponseRequest: The response request object with the updated status.
    """
    request.status = RequestStatus.ACCEPTED
    request.admin_id = admin.id
    request.response_date = datetime.now()
    user.role = Role.DIRECTOR
    db.commit()
    db.refresh(request)
    db.refresh(user)

    return ResponseRequest(
        request_type=request.request_type,
        request_date=request.request_date,
        status=request.status,
        response_date=request.response_date,
    )


def reject_director_request(db, admin: User, request: Request) -> ResponseRequest:
    """
    Reject a request to promote a user to director.

    Args:
        db (Session): The database session.
        admin (User): The admin handling the request.
        request (Request): The request object.

    Returns:
        ResponseRequest: The response request object with the updated status.
    """
    request.status = RequestStatus.REJECTED
    request.admin_id = admin.id
    request.response_date = datetime.now()
    db.commit()
    db.refresh(request)

    return ResponseRequest(
        request_type=request.request_type,
        request_date=request.request_date,
        status=request.status,
        response_date=request.response_date,
    )


def check_request_status(request: Type[Request]) -> None:
    """
    Check if the request has already been responded to.

    Args:
        request (Type[Request]): The request object.

    Raises:
        HTTPException: If the request has already been responded to.
    """
    if request.response_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request has already been responded to.",
        )


def get_link_to_player_requests(
    db, admin: User, user: User, status: str, request: Request, player: Player
) -> ResponseRequest:
    """
    Handle a request to link a user to a player.

    Args:
        db (Session): The database session.
        admin (User): The admin handling the request.
        user (User): The user making the request.
        status (str): The status of the request, either 'accepted' or 'rejected'.
        request (Request): The request object.
        player (Player): The player to link to.

    Returns:
        ResponseRequest: The response request object with the updated status.
    """
    if status == RequestStatus.ACCEPTED:
        send_email_notification(
            email=user.email,
            subject="Request Accepted",
            message=f"Your request to be linked "
            f"to the player '{player.username}' has been accepted.",
        )
        return accept_link_to_player_request(db, admin, user, request, player)

    elif status == RequestStatus.REJECTED:
        send_email_notification(
            email=user.email,
            subject="Request Rejected",
            message=f"Your request to be linked "
            f"to the player '{player.username}' has been rejected.",
        )
        return reject_link_to_player_request(db, admin, request)


def accept_link_to_player_request(
    db, admin: User, user: User, request: Request, player: Player
) -> ResponseRequest:
    """
    Accept a request to link a user to a player.

    Args:
        db (Session): The database session.
        admin (User): The admin handling the request.
        user (User): The user to be linked to the player.
        request (Request): The request object.
        player (Player): The player to link to.

    Returns:
        ResponseRequest: The response request object with the updated status.
    """
    request.status = RequestStatus.ACCEPTED
    request.admin_id = admin.id
    request.response_date = datetime.now()
    player.user_id = request.user_id
    user.role = Role.PLAYER
    db.commit()
    db.refresh(request)
    db.refresh(player)

    return ResponseRequest(
        request_type=request.request_type,
        request_date=request.request_date,
        status=request.status,
        response_date=request.response_date,
    )


def reject_link_to_player_request(db, admin: User, request: Request) -> ResponseRequest:
    """
    Reject a request to link a user to a player.

    Args:
        db (Session): The database session.
        admin (User): The admin handling the request.
        request (Request): The request object.

    Returns:
        ResponseRequest: The response request object with the updated status.
    """
    request.status = RequestStatus.REJECTED
    request.admin_id = admin.id
    request.response_date = datetime.now()
    db.commit()
    db.refresh(request)

    return ResponseRequest(
        request_type=request.request_type,
        request_date=request.request_date,
        status=request.status,
        response_date=request.response_date,
    )
