from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.crud.request import (
    check_request_status,
    check_valid_request,
    get_all,
    get_current_user_request,
    send_director_request,
    send_link_to_player_request,
    update_request,
)
from src.models import Request, User
from src.models.enums import RequestStatus, RequestType, Role
from src.schemas.request import RequestListResponse
from src.utils.pagination import PaginationParams

load_dotenv()


class RequestServiceShould(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user_id = uuid4()
        self.admin_id = uuid4()
        self.current_user = User(
            id=self.user_id, email="user@example.com", role=Role.USER
        )
        self.admin_user = User(
            id=self.admin_id, email="admin@example.com", role=Role.ADMIN
        )
        self.pagination = PaginationParams(offset=0, limit=10)

    @patch("src.utils.validators.user_role_is_admin")
    @patch("src.models.Request")
    def test_get_all_requests_success(
        self, mock_request_model, mock_user_role_is_admin
    ):
        """Test get_all requests successfully retrieves requests for admin."""
        mock_user_role_is_admin.return_value = None

        mock_request = Request(
            id=uuid4(),
            user=User(email="test_user@example.com"),
            request_type=RequestType.PROMOTE_USER_TO_DIRECTOR,
            status=RequestStatus.PENDING,
            request_date=datetime.now(),
            response_date=None,
            admin_id=self.admin_id,
            username="test_user",
        )

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = [mock_request]
        self.db.query.return_value = mock_query

        result = get_all(
            db=self.db,
            current_user=self.admin_user,
            pagination=self.pagination,
            sort_by="desc",
            status=None,
            request_type=None,
            filter_by_admin=False,
        )

        self.db.query.assert_called_with(Request)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], RequestListResponse)
        self.assertEqual(result[0].email, "test_user@example.com")
        self.assertEqual(result[0].status, RequestStatus.PENDING)
        self.assertEqual(result[0].username, "test_user")

    @patch("src.utils.validators.user_role_is_admin")
    def test_get_all_requests_not_admin(self, mock_user_role_is_admin):
        """Test get_all raises an exception when current_user is not admin."""
        mock_user_role_is_admin.side_effect = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action.",
        )

        with self.assertRaises(HTTPException) as context:
            get_all(
                db=self.db,
                current_user=self.current_user,
                pagination=self.pagination,
            )

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            context.exception.detail, "Only admins can perform this action."
        )

    @patch("src.utils.validators.user_role_is_user")
    @patch("src.crud.request.check_valid_request")
    def test_send_director_request_success(
        self, mock_check_valid_request, mock_user_role_is_user
    ):
        """Test send_director_request successfully creates a director request."""
        mock_user_role_is_user.return_value = None
        mock_check_valid_request.return_value = None

        mock_request = MagicMock(
            request_type=RequestType.PROMOTE_USER_TO_DIRECTOR,
            status=RequestStatus.PENDING,
            request_date=datetime.now(),
            response_date=None,
        )

        self.db.add = MagicMock()
        self.db.commit = MagicMock()

        def refresh_side_effect(obj):
            obj.request_type = mock_request.request_type
            obj.status = mock_request.status
            obj.request_date = mock_request.request_date
            obj.response_date = mock_request.response_date

        self.db.refresh = MagicMock(side_effect=refresh_side_effect)

        response = send_director_request(self.db, self.current_user)

        self.db.add.assert_called()
        self.db.commit.assert_called()
        self.db.refresh.assert_called()
        self.assertEqual(response.request_type, RequestType.PROMOTE_USER_TO_DIRECTOR)
        self.assertEqual(response.status, RequestStatus.PENDING)
        self.assertIsNotNone(response.request_date)
        self.assertIsNone(response.response_date)

    @patch("src.utils.validators.user_role_is_user")
    def test_send_director_request_not_user(self, mock_user_role_is_user):
        """Test send_director_request raises exception when current_user
        is not a standard user."""
        mock_user_role_is_user.side_effect = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can send requests.",
        )

        with self.assertRaises(HTTPException) as context:
            send_director_request(self.db, self.admin_user)

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(context.exception.detail, "Only users can send requests.")

    @patch("src.crud.request.user_role_is_user")
    @patch("src.crud.request.player_exists")
    @patch("src.crud.request.player_already_linked")
    @patch("src.crud.request.check_valid_request")
    def test_send_link_to_player_request_success(
        self,
        mock_check_valid_request,
        mock_player_already_linked,
        mock_player_exists,
        mock_user_role_is_user,
    ):
        """Test send_link_to_player_request successfully creates a link request."""
        mock_user_role_is_user.return_value = None
        mock_player_exists.return_value = None
        mock_player_already_linked.return_value = None
        mock_check_valid_request.return_value = None

        mock_request = MagicMock(
            request_type=RequestType.LINK_USER_TO_PLAYER,
            status=RequestStatus.PENDING,
            request_date=datetime.now(),
            response_date=None,
        )

        self.db.add = MagicMock()
        self.db.commit = MagicMock()

        def refresh_side_effect(obj):
            obj.status = mock_request.status
            obj.request_date = mock_request.request_date

        self.db.refresh = MagicMock(side_effect=refresh_side_effect)

        response = send_link_to_player_request(self.db, self.current_user, "player1")

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        self.assertEqual(response.request_type, RequestType.LINK_USER_TO_PLAYER)
        self.assertEqual(response.status, RequestStatus.PENDING)
        self.assertIsNotNone(response.request_date)
        self.assertIsNone(response.response_date)

    from unittest.mock import patch

    from fastapi import HTTPException, status
    from src.crud.request import send_link_to_player_request

    @patch("src.crud.request.player_already_linked")
    @patch("src.crud.request.player_exists")
    @patch("src.crud.request.user_role_is_user")
    def test_send_link_to_player_request_player_not_exist(
        self, mock_user_role, mock_player_exists, mock_player_already_linked
    ):

        mock_user_role.side_effect = lambda x: None
        mock_player_exists.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )

        with self.assertRaises(HTTPException) as context:
            send_link_to_player_request(
                self.db, self.current_user, "nonexistent_player"
            )

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, "Player not found")

        mock_user_role.assert_called_once_with(self.current_user)
        mock_player_exists.assert_called_once_with(
            self.db, username="nonexistent_player"
        )
        mock_player_already_linked.assert_not_called()

    @patch("src.crud.request.send_email_notification")
    @patch("src.crud.request.check_request_status")
    @patch("src.crud.request.user_exists")
    @patch("src.crud.request.request_exists")
    @patch("src.utils.validators.user_role_is_admin")
    def test_update_request_accept_director(
        self,
        mock_user_role_is_admin,
        mock_request_exists,
        mock_user_exists,
        mock_check_request_status,
        mock_send_email_notification,
    ):
        """Test update_request accepts a director promotion request."""
        # Mock the validators and dependencies
        mock_user_role_is_admin.return_value = None
        mock_check_request_status.return_value = None

        request_id = uuid4()
        request = Request(
            id=request_id,
            user_id=self.current_user.id,
            request_type=RequestType.PROMOTE_USER_TO_DIRECTOR,
            status=RequestStatus.PENDING,
            request_date=datetime.now(),
            response_date=None,
        )
        mock_request_exists.return_value = request
        mock_user_exists.return_value = self.current_user

        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        # Call the function being tested
        response = update_request(
            db=self.db,
            current_user=self.admin_user,
            status=RequestStatus.ACCEPTED,
            request_id=request_id,
        )

        # Assert email notification is sent
        mock_send_email_notification.assert_called_with(
            email=self.current_user.email,
            subject="Request Accepted",
            message="Your request to be promoted to director has been accepted.",
        )
        # Assert database operations are performed
        self.db.commit.assert_called()
        self.assertEqual(response.status, RequestStatus.ACCEPTED)

    @patch("src.utils.validators.user_role_is_admin")
    @patch("src.crud.request.request_exists")
    @patch("src.crud.request.user_exists")
    @patch("src.crud.request.check_request_status")
    def test_update_request_already_responded(
        self,
        mock_check_request_status,
        mock_user_exists,
        mock_request_exists,
        mock_user_role_is_admin,
    ):
        """Test update_request raises exception when request has already
        been responded to."""
        mock_user_role_is_admin.return_value = None

        request_id = uuid4()
        request = Request(
            id=request_id,
            user_id=self.current_user.id,
            request_type=RequestType.PROMOTE_USER_TO_DIRECTOR,
            status=RequestStatus.ACCEPTED,
            request_date=datetime.now(),
            response_date=datetime.now(),
        )
        mock_request_exists.return_value = request
        mock_check_request_status.side_effect = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request has already been responded to.",
        )

        with self.assertRaises(HTTPException) as context:
            update_request(
                db=self.db,
                current_user=self.admin_user,
                status=RequestStatus.ACCEPTED,
                request_id=request_id,
            )

        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail, "Request has already been responded to."
        )

    def test_check_valid_request_has_pending(self):
        """Test check_valid_request raises exception when user has a pending request."""
        pending_request = Request(
            user_id=self.current_user.id,
            status=RequestStatus.PENDING,
            request_type=RequestType.PROMOTE_USER_TO_DIRECTOR,
        )
        self.db.query.return_value.filter.return_value.first.return_value = (
            pending_request
        )

        with self.assertRaises(HTTPException) as context:
            check_valid_request(self.db, self.current_user)

        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail, "You have already have a pending request."
        )

    def test_check_valid_request_no_pending(self):
        """Test check_valid_request passes when user has no pending requests."""
        self.db.query.return_value.filter.return_value.first.return_value = None
        try:
            check_valid_request(self.db, self.current_user)
        except HTTPException:
            self.fail("check_valid_request raised HTTPException unexpectedly!")

    def test_check_request_status_already_responded(self):
        """Test check_request_status raises exception when request has response_date."""
        request = Request(response_date=datetime.now())
        with self.assertRaises(HTTPException) as context:
            check_request_status(request)

        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail, "Request has already been responded to."
        )

    def test_check_request_status_not_responded(self):
        """Test check_request_status passes when request has not been responded to."""
        request = Request(response_date=None)

        try:
            check_request_status(request)
        except HTTPException:
            self.fail("check_request_status raised HTTPException unexpectedly!")

    def test_get_all_filter_by_admin(self):
        """Test get_all with filter_by_admin=True
        returns only requests by current admin."""
        self.admin_user.id = uuid4()
        mock_request = Request(
            id=uuid4(),
            user=User(email="test_user_admin@example.com"),
            request_type=RequestType.PROMOTE_USER_TO_DIRECTOR,
            status=RequestStatus.PENDING,
            request_date=datetime.now(),
            response_date=None,
            admin_id=self.admin_user.id,
            username="test_user",
        )
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = [mock_request]
        self.db.query.return_value = mock_query

        with patch("src.utils.validators.user_role_is_admin", return_value=None):
            result = get_all(
                db=self.db,
                current_user=self.admin_user,
                pagination=self.pagination,
                filter_by_admin=True,
            )

        self.db.query.assert_called_with(Request)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].admin_id, self.admin_user.id)

    def test_get_all_asc_order_and_filters(self):
        """Test get_all with ascending order, specific request_type and status."""
        mock_request = Request(
            id=uuid4(),
            user=User(email="filtered_user@example.com"),
            request_type=RequestType.LINK_USER_TO_PLAYER,
            status=RequestStatus.ACCEPTED,
            request_date=datetime.now(),
            response_date=datetime.now(),
            admin_id=self.admin_id,
            username="filtered_user",
        )
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = [mock_request]
        self.db.query.return_value = mock_query

        with patch("src.utils.validators.user_role_is_admin", return_value=None):
            result = get_all(
                db=self.db,
                current_user=self.admin_user,
                pagination=self.pagination,
                sort_by="asc",
                status=RequestStatus.ACCEPTED,
                request_type=RequestType.LINK_USER_TO_PLAYER,
            )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].status, RequestStatus.ACCEPTED)
        self.assertEqual(result[0].request_type, RequestType.LINK_USER_TO_PLAYER)

    def test_get_all_empty_result(self):
        """Test get_all returns empty list when no requests found."""
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = []
        self.db.query.return_value = mock_query

        with patch("src.utils.validators.user_role_is_admin", return_value=None):
            result = get_all(
                db=self.db, current_user=self.admin_user, pagination=self.pagination
            )

        self.assertEqual(result, [])

    def test_get_current_user_request_success(self):
        """Test get_current_user_request retrieves current user's requests."""
        mock_request = Request(
            id=uuid4(),
            user_id=self.current_user.id,
            request_type=RequestType.LINK_USER_TO_PLAYER,
            status=RequestStatus.PENDING,
            request_date=datetime.now(),
            response_date=None,
        )
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = [mock_request]
        self.db.query.return_value = mock_query

        result = get_current_user_request(
            db=self.db, current_user=self.current_user, pagination=self.pagination
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].request_type, RequestType.LINK_USER_TO_PLAYER)
        self.assertIsNotNone(result[0].request_date)

    def test_get_current_user_request_empty(self):
        """Test get_current_user_request returns empty when no requests for user."""
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = []
        self.db.query.return_value = mock_query

        result = get_current_user_request(
            db=self.db, current_user=self.current_user, pagination=self.pagination
        )
        self.assertEqual(result, [])

    @patch("src.crud.request.player_exists")
    @patch("src.crud.request.user_role_is_admin")
    @patch("src.crud.request.request_exists")
    @patch("src.crud.request.user_exists")
    @patch("src.crud.request.check_request_status")
    @patch("src.crud.request.send_email_notification")
    def test_update_request_link_user_to_player_accepted(
        self,
        mock_send_email_notification,
        mock_check_request_status,
        mock_user_exists,
        mock_request_exists,
        mock_user_role_is_admin,
        mock_player_exists,
    ):
        """Test update_request accepting link user to player request."""
        mock_user_role_is_admin.return_value = None
        mock_check_request_status.return_value = None
        player_id = uuid4()
        player = MagicMock(username="test_player", user_id=None, id=player_id)
        mock_player_exists.return_value = player

        request_id = uuid4()
        request = Request(
            id=request_id,
            user_id=self.current_user.id,
            request_type=RequestType.LINK_USER_TO_PLAYER,
            status=RequestStatus.PENDING,
            request_date=datetime.now(),
            response_date=None,
            username="test_player",
        )
        mock_request_exists.return_value = request
        mock_user_exists.return_value = self.current_user

        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        response = update_request(
            db=self.db,
            current_user=self.admin_user,
            status=RequestStatus.ACCEPTED,
            request_id=request_id,
        )

        mock_send_email_notification.assert_called_once()
        self.db.commit.assert_called()
        self.assertEqual(response.status, RequestStatus.ACCEPTED)

    @patch("src.crud.request.player_exists")
    @patch("src.crud.request.user_role_is_admin")
    @patch("src.crud.request.request_exists")
    @patch("src.crud.request.user_exists")
    @patch("src.crud.request.check_request_status")
    @patch("src.crud.request.send_email_notification")
    def test_update_request_link_user_to_player_rejected(
        self,
        mock_send_email_notification,
        mock_check_request_status,
        mock_user_exists,
        mock_request_exists,
        mock_user_role_is_admin,
        mock_player_exists,
    ):
        """Test update_request rejecting link user to player request."""
        mock_user_role_is_admin.return_value = None
        mock_check_request_status.return_value = None
        player_id = uuid4()
        player = MagicMock(username="test_player", user_id=None, id=player_id)
        mock_player_exists.return_value = player

        request_id = uuid4()
        request = Request(
            id=request_id,
            user_id=self.current_user.id,
            request_type=RequestType.LINK_USER_TO_PLAYER,
            status=RequestStatus.PENDING,
            request_date=datetime.now(),
            response_date=None,
            username="test_player",
        )
        mock_request_exists.return_value = request
        mock_user_exists.return_value = self.current_user

        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        response = update_request(
            db=self.db,
            current_user=self.admin_user,
            status=RequestStatus.REJECTED,
            request_id=request_id,
        )

        mock_send_email_notification.assert_called_once()
        self.db.commit.assert_called()
        self.assertEqual(response.status, RequestStatus.REJECTED)

    @patch("src.crud.request.send_email_notification")
    @patch("src.crud.request.check_request_status")
    @patch("src.crud.request.user_exists")
    @patch("src.crud.request.request_exists")
    @patch("src.utils.validators.user_role_is_admin")
    def test_update_request_director_rejected(
        self,
        mock_user_role_is_admin,
        mock_request_exists,
        mock_user_exists,
        mock_check_request_status,
        mock_send_email_notification,
    ):
        """Test update_request rejects a director request."""
        mock_user_role_is_admin.return_value = None
        mock_check_request_status.return_value = None

        request_id = uuid4()
        request = Request(
            id=request_id,
            user_id=self.current_user.id,
            request_type=RequestType.PROMOTE_USER_TO_DIRECTOR,
            status=RequestStatus.PENDING,
            request_date=datetime.now(),
            response_date=None,
        )
        mock_request_exists.return_value = request
        mock_user_exists.return_value = self.current_user

        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        response = update_request(
            db=self.db,
            current_user=self.admin_user,
            status=RequestStatus.REJECTED,
            request_id=request_id,
        )

        mock_send_email_notification.assert_called_once()
        self.db.commit.assert_called()
        self.assertEqual(response.status, RequestStatus.REJECTED)

    def test_update_request_unknown_request_type(self):
        """Test update_request when request has unknown request_type."""
        with patch("src.utils.validators.user_role_is_admin", return_value=None):
            request_id = uuid4()
            request = Request(
                id=request_id,
                user_id=self.current_user.id,
                request_type="UNKNOWN_TYPE",
                status=RequestStatus.PENDING,
                request_date=datetime.now(),
                response_date=None,
            )
            with (
                patch("src.crud.request.request_exists", return_value=request),
                patch("src.crud.request.user_exists", return_value=self.current_user),
                patch("src.crud.request.check_request_status", return_value=None),
            ):
                self.db.commit = MagicMock()
                self.db.refresh = MagicMock()

                response = update_request(
                    db=self.db,
                    current_user=self.admin_user,
                    status=RequestStatus.ACCEPTED,
                    request_id=request_id,
                )

                self.assertIsNone(response)
                self.db.commit.assert_not_called()
                self.db.refresh.assert_not_called()
