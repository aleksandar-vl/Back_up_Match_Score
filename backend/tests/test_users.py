import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.crud.user import (
    convert_db_to_user_response,
    create_user,
    get_by_id,
    update_email,
)
from src.models.enums import Role
from src.models.user import User
from src.schemas.user import UserCreate


class UserServiceShould(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user_id = str(uuid4())
        self.current_user = User(
            id=self.user_id,
            email="test_user@example.com",
            role=Role.USER,
        )

    @patch("src.crud.user.get_password_hash")
    @patch("src.crud.user.user_email_exists")
    @patch("src.crud.user.send_email_notification")
    def test_create_user_success(
        self,
        mock_send_email_notification,
        mock_user_email_exists,
        mock_get_password_hash,
    ):
        """Test user creation succeeds with valid data."""
        mock_user_email_exists.side_effect = lambda db, email: None
        mock_get_password_hash.return_value = "hashed_password"

        user_data = UserCreate(email="new_user@example.com", password="Secure@123")

        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        created_user = create_user(user=user_data, db=self.db)

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        mock_send_email_notification.assert_called_with(
            email="new_user@example.com",
            subject="Account Created",
            message="Your account has been created with email new_user@example.com",
        )
        self.assertEqual(created_user.email, "new_user@example.com")
        self.assertEqual(created_user.password_hash, "hashed_password")

    @patch("src.utils.notifications.send_email_notification")
    @patch("src.utils.validators.user_email_exists")
    def test_create_user_email_exists(
        self, mock_user_email_exists, mock_send_email_notification
    ):
        """Test user creation fails when email already exists."""
        mock_user_email_exists.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email already exists."
        )

        user_data = UserCreate(email="existing_user@example.com", password="Secure@123")

        with self.assertRaises(HTTPException) as context:
            create_user(user=user_data, db=self.db)

        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(context.exception.detail, "Email already exists")

        mock_send_email_notification.assert_not_called()

    def test_get_user_by_id_success(self):
        """Test retrieving a user by ID succeeds."""
        self.db.query.return_value.filter.return_value.first.return_value = (
            self.current_user
        )

        retrieved_user = get_by_id(db=self.db, user_id=self.user_id)

        self.assertEqual(retrieved_user.id, self.user_id)
        self.assertEqual(retrieved_user.email, self.current_user.email)

    def test_get_user_by_id_not_found(self):
        """Test retrieving a user by ID raises exception when user not found."""
        self.db.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(HTTPException) as context:
            get_by_id(db=self.db, user_id=self.user_id)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, "User not found.")

    @patch("src.crud.user.user_email_exists")
    @patch("src.crud.user.send_email_notification")
    def test_update_email_success(
        self, mock_send_email_notification, mock_user_email_exists
    ):
        """Test updating user email succeeds."""
        mock_user_email_exists.return_value = None

        updated_email = "updated_email@example.com"
        self.db.query.return_value.filter.return_value.first.return_value = (
            self.current_user
        )
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        response = update_email(
            db=self.db, email=updated_email, current_user=self.current_user
        )

        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        mock_send_email_notification.assert_any_call(
            email="test_user@example.com",
            subject="Email Updated",
            message=f"Your email has been changed from "
            f"test_user@example.com to {updated_email}",
        )
        mock_send_email_notification.assert_any_call(
            email=updated_email,
            subject="Email Updated",
            message=f"Your email has been changed from "
            f"test_user@example.com to {updated_email}",
        )

        self.assertEqual(response["message"], "Email updated successfully.")

    @patch("src.utils.validators.user_email_exists")
    def test_update_email_conflict(self, mock_user_email_exists):
        """Test updating user email fails when the new email already exists."""
        mock_user_email_exists.side_effect = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists."
        )

        with self.assertRaises(HTTPException) as context:
            update_email(
                db=self.db,
                email="conflicting_email@example.com",
                current_user=self.current_user,
            )

        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(context.exception.detail, "Email already exists")

    def test_convert_db_to_user_response(self):
        """Test converting database User model to UserResponse schema."""
        # Arrange
        test_user = User(id=self.user_id, email="test_user@example.com", role=Role.USER)

        # Act
        user_response = convert_db_to_user_response(test_user)

        # Assert
        self.assertEqual(str(user_response.id), self.user_id)
        self.assertEqual(user_response.email, "test_user@example.com")
        self.assertEqual(user_response.role, Role.USER)
