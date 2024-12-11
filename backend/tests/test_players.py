from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from src.crud.player import (
    create_player,
    get_player,
    get_player_by_user_id,
    get_players,
    update_player,
)
from src.models import Player, Team, Tournament, User
from src.models.enums import Role
from src.schemas.player import PlayerCreate, PlayerUpdate
from src.utils.pagination import PaginationParams


class PlayerServiceShould(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db = MagicMock(spec=Session)
        self.user_id = uuid4()
        self.admin_id = uuid4()
        self.director_id = uuid4()
        self.player_id = uuid4()
        self.team_id = uuid4()
        self.tournament_id = uuid4()

        self.current_user = User(
            id=self.user_id, email="user@example.com", role=Role.USER
        )
        self.admin_user = User(
            id=self.admin_id, email="admin@example.com", role=Role.ADMIN
        )
        self.director_user = User(
            id=self.director_id, email="director@example.com", role=Role.DIRECTOR
        )
        self.player_user = User(
            id=self.user_id, email="player@example.com", role=Role.PLAYER
        )

        self.tournament = Tournament(
            id=self.tournament_id,
            title="Test Tournament",
            start_date=datetime.now(),
            end_date=datetime.now(),
        )

        self.team = Team(
            id=self.team_id,
            name="Test Team",
            tournament_id=self.tournament_id,
            tournament=self.tournament,
            players=[],
        )

        self.player = Player(
            id=self.player_id,
            username="testplayer",
            first_name="Test",
            last_name="Player",
            country="TestCountry",
            avatar="test_avatar.jpg",
            user_id=self.user_id,
            team_id=self.team_id,
            team=self.team,
            played_games=10,
            won_games=5,
        )

        self.pagination = PaginationParams(offset=0, limit=10)

    def test_create_player_success(self):
        """Test creating a player successfully."""
        with (
            patch("src.utils.validators.player_username_unique", return_value=None),
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.team_exists", return_value=self.team),
            patch("src.utils.validators.team_player_limit_reached", return_value=None),
            patch("src.utils.s3.s3_service.upload_file", return_value="avatar_url"),
        ):
            player_create = PlayerCreate(
                username="newplayer",
                first_name="New",
                last_name="Player",
                country="NewCountry",
                team_name="Test Team",
            )
            avatar = MagicMock(spec=UploadFile)

            def mock_add(player):
                player.id = uuid4()
                player.played_games = 0
                player.won_games = 0
                player.team = self.team
                player.user = None
                player.username = "newplayer"
                player.first_name = "New"
                player.last_name = "Player"
                player.country = "NewCountry"
                player.avatar = "avatar_url"

            self.db.add = MagicMock(side_effect=mock_add)

            result = create_player(self.db, player_create, avatar, self.director_user)

            self.db.add.assert_called_once()
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once()
            self.assertEqual(result.username, "newplayer")
            self.assertEqual(result.avatar, "avatar_url")
            self.assertEqual(result.team_name, "Test Team")

    def test_create_player_no_team(self):
        """Test creating a player without a team."""
        with (
            patch("src.utils.validators.player_username_unique", return_value=None),
            patch("src.utils.validators.director_or_admin", return_value=None),
        ):
            player_create = PlayerCreate(
                username="newplayer",
                first_name="New",
                last_name="Player",
                country="NewCountry",
            )

            def mock_add(player):
                player.id = uuid4()
                player.played_games = 0
                player.won_games = 0
                player.team = None
                player.user = None
                player.avatar = None
                player.username = "newplayer"
                player.first_name = "New"
                player.last_name = "Player"
                player.country = "NewCountry"

            self.db.add = MagicMock(side_effect=mock_add)

            result = create_player(self.db, player_create, None, self.director_user)

            self.db.add.assert_called_once()
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once()
            self.assertEqual(result.username, "newplayer")
            self.assertIsNone(result.team_name)

    def test_create_player_not_authorized(self):
        """Test creating a player fails when user is not authorized."""
        with patch(
            "src.utils.validators.director_or_admin",
            side_effect=HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action",
            ),
        ) as mock_auth:
            player_create = PlayerCreate(
                username="newplayer",
                first_name="New",
                last_name="Player",
                country="NewCountry",
            )

            with patch(
                "src.utils.validators.player_username_unique", return_value=None
            ) as mock_username:
                with self.assertRaises(HTTPException) as context:
                    create_player(self.db, player_create, None, self.current_user)

                mock_username.assert_called_once()
                mock_auth.assert_called_once_with(self.current_user)

                self.assertEqual(
                    context.exception.status_code, status.HTTP_403_FORBIDDEN
                )
                self.assertEqual(
                    context.exception.detail,
                    "You are not authorized to perform this action",
                )

    def test_get_players_with_filters(self):
        """Test getting players with various filters."""
        mock_query = MagicMock()
        mock_query.order_by.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [self.player]
        self.db.query.return_value = mock_query

        result = get_players(
            self.db,
            self.pagination,
            search="test",
            country="TestCountry",
            sort_by="desc",
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].username, "testplayer")
        mock_query.filter.assert_called()
        mock_query.order_by.assert_called_once()

    def test_get_players_with_team_filter(self):
        """Test getting players with team filter."""
        mock_query = MagicMock()
        mock_query.order_by.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [self.player]
        self.db.query.return_value = mock_query

        mock_team = MagicMock()
        mock_team.ilike = MagicMock()

        with patch("src.models.Player.team", mock_team):
            result = get_players(
                self.db,
                self.pagination,
                team="Test Team",
            )

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].username, "testplayer")
            mock_team.ilike.assert_called_once_with("%Test Team%")
            mock_query.filter.assert_called()

    def test_get_players_no_filters(self):
        """Test getting players without any filters."""
        mock_query = MagicMock()
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [self.player]
        self.db.query.return_value = mock_query

        result = get_players(self.db, self.pagination)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].username, "testplayer")
        mock_query.order_by.assert_called_once()

    def test_get_player_success(self):
        """Test getting a specific player successfully."""
        with patch("src.utils.validators.player_exists", return_value=self.player):
            result = get_player(self.db, self.player_id)

            self.assertEqual(result.id, self.player_id)
            self.assertEqual(result.username, "testplayer")
            self.assertEqual(result.current_tournament_title, "Test Tournament")

    def test_get_player_not_found(self):
        """Test getting a player that doesn't exist."""
        with patch(
            "src.utils.validators.player_exists",
            side_effect=HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Player not found",
            ),
        ):
            with self.assertRaises(HTTPException) as context:
                get_player(self.db, uuid4())

            self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_player_by_user_id_success(self):
        """Test getting a player by user ID successfully."""
        with patch(
            "src.utils.validators.user_associated_with_player", return_value=None
        ):
            mock_query = MagicMock()
            mock_query.filter.return_value = mock_query
            mock_query.first.return_value = self.player
            self.db.query.return_value = mock_query

            result = get_player_by_user_id(self.db, self.player_user)

            self.assertEqual(result.id, self.player_id)
            self.assertEqual(result.username, "testplayer")
            self.assertEqual(result.current_tournament_title, "Test Tournament")

    def test_get_player_by_user_id_not_associated(self):
        """Test getting a player by user ID when user
        is not associated with a player."""
        with patch(
            "src.utils.validators.user_associated_with_player",
            side_effect=HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not associated with player",
            ),
        ):
            with self.assertRaises(HTTPException) as context:
                get_player_by_user_id(self.db, self.current_user)

            self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_player_success(self):
        """Test updating a player successfully."""
        with (
            patch("src.utils.validators.player_exists", return_value=self.player),
            patch(
                "src.utils.validators.player_update_current_user_authorization",
                return_value=None,
            ),
            patch("src.utils.validators.player_username_unique", return_value=None),
            patch("src.utils.validators.team_exists", return_value=self.team),
            patch("src.utils.validators.team_player_limit_reached", return_value=None),
            patch("src.utils.s3.s3_service.delete_file", return_value=None),
            patch("src.utils.s3.s3_service.upload_file", return_value="new_avatar_url"),
        ):
            player_update = PlayerUpdate(
                username="updatedplayer",
                first_name="Updated",
                last_name="Player",
                country="UpdatedCountry",
                team_name="Test Team",
            )
            avatar = MagicMock(spec=UploadFile)

            result = update_player(
                self.db, self.player_id, player_update, avatar, self.player_user
            )

            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once()
            self.assertEqual(result.username, "updatedplayer")
            self.assertEqual(result.avatar, "new_avatar_url")

    def test_update_player_no_user_id(self):
        """Test updating a player without user_id (requires admin/director)."""
        self.player.user_id = None

        with (
            patch("src.utils.validators.player_exists", return_value=self.player),
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.player_username_unique", return_value=None),
        ):
            player_update = PlayerUpdate(username="updatedplayer")

            result = update_player(
                self.db, self.player_id, player_update, None, self.admin_user
            )

            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once()
            self.assertEqual(result.username, "updatedplayer")

    def test_update_player_not_authorized(self):
        """Test updating a player fails when user is not authorized."""
        with (
            patch("src.utils.validators.player_exists", return_value=self.player),
            patch(
                "src.utils.validators.player_update_current_user_authorization",
                side_effect=HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized",
                ),
            ),
        ):
            player_update = PlayerUpdate(username="updatedplayer")

            with self.assertRaises(HTTPException) as context:
                update_player(
                    self.db, self.player_id, player_update, None, self.current_user
                )

            self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_player_no_changes(self):
        """Test updating a player with no changes provided."""
        with patch("src.utils.validators.player_exists", return_value=self.player):
            player_update = PlayerUpdate()

            result = update_player(
                self.db, self.player_id, player_update, None, self.admin_user
            )

            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once()
            self.assertEqual(result.username, "testplayer")

    def test_get_player_no_tournament(self):
        """Test getting a player when not part of any tournament."""
        player_no_tournament = Player(
            id=uuid4(),
            username="notournament",
            first_name="No",
            last_name="Tournament",
            country="TestCountry",
            team_id=None,
            team=None,
            played_games=0,
            won_games=0,
            avatar=None,
            user=None,
        )

        with patch(
            "src.utils.validators.player_exists", return_value=player_no_tournament
        ):
            result = get_player(self.db, player_no_tournament.id)

            self.assertEqual(result.username, "notournament")
            self.assertIsNone(result.current_tournament_title)
