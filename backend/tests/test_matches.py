from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.crud.match import (
    generate_matches,
    get_all_matches,
    get_match,
    update_match,
    update_match_score,
)
from src.models import Match, Team, Tournament, User
from src.models.enums import MatchFormat, Role, Stage, TournamentFormat
from src.schemas.match import MatchUpdate
from src.utils.pagination import PaginationParams
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND


class MatchServiceShould(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user_id = uuid4()
        self.admin_id = uuid4()
        self.director_id = uuid4()
        self.team1_id = uuid4()
        self.team2_id = uuid4()
        self.tournament_id = uuid4()
        self.match_id = uuid4()

        self.current_user = User(
            id=self.user_id, email="user@example.com", role=Role.USER
        )
        self.admin_user = User(
            id=self.admin_id, email="admin@example.com", role=Role.ADMIN
        )
        self.director_user = User(
            id=self.director_id, email="director@example.com", role=Role.DIRECTOR
        )

        self.team1 = Team(
            id=self.team1_id,
            name="Team 1",
            logo="logo1.png",
            played_games=5,
            won_games=3,
            tournament_id=self.tournament_id,
            players=[],
        )

        self.team2 = Team(
            id=self.team2_id,
            name="Team 2",
            logo="logo2.png",
            played_games=5,
            won_games=2,
            tournament_id=self.tournament_id,
            players=[],
        )

        self.tournament = Tournament(
            id=self.tournament_id,
            title="Test Tournament",
            tournament_format=TournamentFormat.SINGLE_ELIMINATION,
            start_date=datetime.now(timezone.utc) + timedelta(days=1),
            end_date=datetime.now(timezone.utc) + timedelta(days=5),
            prize_pool=1000,
            current_stage=Stage.QUARTER_FINAL,
            director_id=self.director_id,
            director=self.director_user,
        )

        self.match = Match(
            id=self.match_id,
            match_format=MatchFormat.MR15,
            start_time=datetime.now(timezone.utc) + timedelta(days=2),
            is_finished=False,
            stage=Stage.QUARTER_FINAL,
            team1_id=self.team1_id,
            team2_id=self.team2_id,
            team1_score=0,
            team2_score=0,
            tournament_id=self.tournament_id,
            team1=self.team1,
            team2=self.team2,
            tournament=self.tournament,
        )

        self.pagination = PaginationParams(offset=0, limit=10)

    def test_get_match_success(self):
        """Test get_match successfully retrieves a match."""
        self.db.query.return_value.filter.return_value.first.return_value = self.match

        result = get_match(self.db, self.match_id)

        self.assertEqual(result.id, self.match_id)
        self.assertEqual(result.match_format, MatchFormat.MR15)
        self.assertEqual(result.team1_id, self.team1_id)
        self.assertEqual(result.team2_id, self.team2_id)
        self.assertEqual(result.tournament_id, self.tournament_id)

    def test_get_match_not_found(self):
        """Test get_match raises exception when match not found."""
        self.db.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(HTTPException) as context:
            get_match(self.db, uuid4())

        self.assertEqual(context.exception.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, "Match not found")

    def test_get_all_matches_with_filters(self):
        """Test get_all_matches with various filters."""
        mock_base_query = MagicMock()

        mock_tournament = MagicMock()
        mock_tournament.id = self.tournament_id
        mock_tournament.title = "Test Tournament"

        mock_tournament_query = MagicMock()
        mock_tournament_query.filter.return_value.all.return_value = [mock_tournament]

        mock_team_query = MagicMock()
        mock_team_query.filter.return_value.first.return_value = self.team1

        def mock_query(model):
            if model == Tournament:
                return mock_tournament_query
            if model == Team:
                return mock_team_query
            return mock_base_query

        self.db.query.side_effect = mock_query

        mock_base_query.order_by.return_value = mock_base_query
        mock_base_query.join.return_value = mock_base_query
        mock_base_query.filter.return_value = mock_base_query
        mock_base_query.distinct.return_value = mock_base_query
        mock_base_query.offset.return_value = mock_base_query
        mock_base_query.limit.return_value = mock_base_query
        mock_base_query.all.return_value = [self.match]

        result = get_all_matches(
            self.db,
            self.pagination,
            tournament_title="Test Tournament",
            stage=Stage.QUARTER_FINAL,
            is_finished=False,
            team_name="Team 1",
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.match_id)
        self.assertEqual(result[0].stage, Stage.QUARTER_FINAL)
        self.assertEqual(result[0].is_finished, False)

        mock_base_query.order_by.assert_called_once()
        mock_base_query.join.assert_called_once()
        mock_base_query.distinct.assert_called_once()
        mock_base_query.filter.assert_called()
        mock_base_query.all.assert_called_once()

    @patch("src.utils.validators.director_or_admin")
    @patch("src.utils.validators.match_exists")
    @patch("src.utils.validators.match_is_finished")
    @patch("src.utils.validators.match_has_started")
    @patch("src.utils.validators.is_author_of_tournament")
    @patch("src.crud.match.send_email_notification")
    def test_update_match_success(
        self,
        mock_send_email,
        mock_is_author_of_tournament,
        mock_match_has_started,
        mock_match_is_finished,
        mock_match_exists,
        mock_director_or_admin,
    ):
        """Test update_match successfully updates match details."""
        mock_director_or_admin.return_value = None
        mock_match_exists.return_value = self.match
        mock_match_is_finished.return_value = None
        mock_match_has_started.return_value = None
        mock_is_author_of_tournament.return_value = None
        mock_send_email.return_value = None

        new_start_time = datetime.now(timezone.utc) + timedelta(days=3)
        match_update = MatchUpdate(start_time=new_start_time, stage=Stage.SEMI_FINAL)

        result = update_match(self.db, self.match_id, match_update, self.director_user)

        self.assertEqual(result.start_time, new_start_time)
        self.assertEqual(result.stage, Stage.SEMI_FINAL)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        mock_send_email.assert_called_once()

    @patch("src.utils.validators.director_or_admin")
    def test_update_match_not_authorized(self, mock_director_or_admin):
        """Test update_match raises exception when user not authorized."""
        mock_director_or_admin.side_effect = HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )

        match_update = MatchUpdate(
            start_time=datetime.now(timezone.utc) + timedelta(days=1)
        )

        with self.assertRaises(HTTPException) as context:
            update_match(self.db, self.match_id, match_update, self.current_user)

        self.assertEqual(context.exception.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(
            context.exception.detail, "You are not authorized to perform this action"
        )

    @patch("src.utils.validators.director_or_admin")
    @patch("src.utils.validators.match_exists")
    @patch("src.utils.validators.match_is_finished")
    @patch("src.utils.validators.team_has_five_players")
    @patch("src.utils.validators.is_author_of_tournament")
    def test_update_match_score_success(
        self,
        mock_is_author_of_tournament,
        mock_team_has_five_players,
        mock_match_is_finished,
        mock_match_exists,
        mock_director_or_admin,
    ):
        """Test update_match_score successfully updates score."""
        # Set up the mocks
        mock_director_or_admin.return_value = None
        mock_match_exists.return_value = self.match
        mock_match_is_finished.return_value = None
        mock_team_has_five_players.return_value = None
        mock_is_author_of_tournament.return_value = None

        # Add 5 players to each team
        for player in range(5):
            self.match.team1.players.append(MagicMock(played_games=0, won_games=0))
            self.match.team2.players.append(MagicMock(played_games=0, won_games=0))

        result = update_match_score(self.db, self.match_id, "team1", self.director_user)

        self.assertEqual(result.team1_score, 1)
        self.assertEqual(result.team2_score, 0)
        self.db.commit.assert_called()
        mock_is_author_of_tournament.assert_called_once()

    def test_get_all_matches_no_results(self):
        """Test get_all_matches returns empty when no matches found."""
        mock_query = MagicMock()
        mock_query.join.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value.all.return_value = []
        self.db.query.return_value = mock_query

        result = get_all_matches(
            self.db,
            self.pagination,
            tournament_title=None,
            stage=None,
            is_finished=None,
            team_name=None,
        )

        self.assertEqual(result, [])

    def test_get_all_matches_no_filters(self):
        """Test get_all_matches with no filters just returns all matches."""
        mock_query = MagicMock()
        mock_query.join.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value.all.return_value = [self.match]
        self.db.query.return_value = mock_query

        result = get_all_matches(self.db, self.pagination)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.match_id)

    @patch(
        "src.utils.validators.team_exists",
        side_effect=HTTPException(status_code=404, detail="Team not found"),
    )
    @patch("src.utils.validators.director_or_admin")
    @patch("src.utils.validators.match_exists")
    @patch("src.utils.validators.match_is_finished")
    @patch("src.utils.validators.match_has_started")
    @patch("src.utils.validators.is_author_of_tournament")
    def test_update_match_invalid_team_name(
        self,
        mock_is_author,
        mock_match_has_started,
        mock_match_is_finished,
        mock_match_exists,
        mock_director_or_admin,
        mock_team_exists,
    ):
        """Test update_match fails when team_exists
        raises exception due to invalid team name."""
        mock_director_or_admin.return_value = None
        mock_match_exists.return_value = self.match
        mock_match_is_finished.return_value = None
        mock_match_has_started.return_value = None
        mock_is_author.return_value = None

        update_data = MatchUpdate(team1_name="Invalid Team")

        with self.assertRaises(HTTPException) as ctx:
            update_match(self.db, self.match_id, update_data, self.director_user)
        self.assertEqual(ctx.exception.detail, "Team not found")

    @patch("src.utils.validators.director_or_admin")
    @patch("src.utils.validators.match_exists")
    @patch("src.utils.validators.match_is_finished")
    @patch("src.utils.validators.team_has_five_players")
    @patch("src.utils.validators.is_author_of_tournament")
    def test_update_match_score_winner_mr15(
        self,
        mock_is_author,
        mock_team_has_five,
        mock_match_is_finished,
        mock_match_exists,
        mock_director_admin,
    ):
        """Test update_match_score with MR15 format that decides a winner."""
        mock_director_admin.return_value = None
        mock_match_exists.return_value = self.match
        mock_match_is_finished.return_value = None
        mock_team_has_five.return_value = None
        mock_is_author.return_value = None

        self.match.match_format = MatchFormat.MR15
        self.match.team1_score = 15
        self.match.team2_score = 13

        for i in range(5):
            self.team1.players.append(MagicMock(played_games=0, won_games=0))
            self.team2.players.append(MagicMock(played_games=0, won_games=0))

        result = update_match_score(self.db, self.match_id, "team1", self.director_user)

        self.assertTrue(result.is_finished)
        self.assertEqual(result.team1_score, 16)
        self.assertEqual(result.team2_score, 13)

    @patch("src.utils.validators.director_or_admin")
    @patch("src.utils.validators.match_exists")
    @patch("src.utils.validators.match_is_finished")
    @patch("src.utils.validators.team_has_five_players")
    @patch("src.utils.validators.is_author_of_tournament")
    def test_update_match_score_winner_mr12(
        self,
        mock_is_author,
        mock_team_has_five,
        mock_match_is_finished,
        mock_match_exists,
        mock_director_admin,
    ):
        """Test update_match_score with MR12 format that decides a winner."""
        mock_director_admin.return_value = None
        mock_match_exists.return_value = self.match
        mock_match_is_finished.return_value = None
        mock_team_has_five.return_value = None
        mock_is_author.return_value = None

        self.match.match_format = MatchFormat.MR12
        self.match.team1_score = 12
        self.match.team2_score = 11
        for i in range(5):
            self.team1.players.append(MagicMock(played_games=0, won_games=0))
            self.team2.players.append(MagicMock(played_games=0, won_games=0))

        result = update_match_score(self.db, self.match_id, "team1", self.director_user)
        self.assertTrue(result.is_finished)
        self.assertEqual(result.team1_score, 13)
        self.assertEqual(result.team2_score, 11)

    @patch("src.utils.validators.director_or_admin")
    @patch("src.utils.validators.match_exists")
    @patch("src.utils.validators.match_is_finished")
    @patch("src.utils.validators.team_has_five_players")
    @patch("src.utils.validators.is_author_of_tournament")
    def test_update_match_score_no_winner_added(
        self,
        mock_is_author,
        mock_team_has_five,
        mock_match_is_finished,
        mock_match_exists,
        mock_director_admin,
    ):
        """Test update_match_score when no winner is
        decided yet (MR15 or MR12 still ongoing)."""
        mock_director_admin.return_value = None
        mock_match_exists.return_value = self.match
        mock_match_is_finished.return_value = None
        mock_team_has_five.return_value = None
        mock_is_author.return_value = None

        for i in range(5):
            self.team1.players.append(MagicMock(played_games=0, won_games=0))
            self.team2.players.append(MagicMock(played_games=0, won_games=0))

        result = update_match_score(self.db, self.match_id, "team1", self.director_user)
        self.assertFalse(result.is_finished)
        self.assertEqual(result.team1_score, 1)

    @patch("src.crud.match.send_email_notification")
    def test_generate_matches_round_robin_no_players(self, mock_send_email):
        """Test generate_matches with ROUND_ROBIN format and no players."""
        self.tournament.tournament_format = TournamentFormat.ROUND_ROBIN
        self.tournament.current_stage = Stage.GROUP_STAGE
        self.db.bulk_save_objects = MagicMock()

        generate_matches(self.db, self.tournament)
        self.db.bulk_save_objects.assert_called_once()
        mock_send_email.assert_not_called()

    @patch("src.crud.match.send_email_notification")
    def test_generate_matches_single_elimination_no_players(self, mock_send_email):
        """Test generate_matches SINGLE_ELIMINATION with no players."""
        self.tournament.tournament_format = TournamentFormat.SINGLE_ELIMINATION
        self.db.bulk_save_objects = MagicMock()

        generate_matches(self.db, self.tournament)
        self.db.bulk_save_objects.assert_called_once()
        mock_send_email.assert_not_called()

    @patch("src.crud.match.send_email_notification")
    @patch("src.utils.validators.director_or_admin")
    @patch("src.utils.validators.match_exists")
    @patch("src.utils.validators.match_is_finished")
    @patch("src.utils.validators.match_has_started")
    @patch("src.utils.validators.is_author_of_tournament")
    def test_update_match_invalid_start_time(
        self,
        mock_is_author,
        mock_match_has_started,
        mock_match_is_finished,
        mock_match_exists,
        mock_director_or_admin,
        mock_send_email,
    ):
        """Test update_match with start_time outside tournament range or in the past."""
        mock_director_or_admin.return_value = None
        mock_match_exists.return_value = self.match
        mock_is_author.return_value = None
        mock_match_is_finished.return_value = None
        mock_match_has_started.return_value = None
        mock_send_email.return_value = None

        # Set start_time outside tournament range
        invalid_start = self.tournament.end_date + timedelta(days=10)
        update_data = MatchUpdate(start_time=invalid_start)
        with self.assertRaises(HTTPException) as ctx:
            update_match(self.db, self.match_id, update_data, self.director_user)
        self.assertIn("Invalid start time", ctx.exception.detail)

    @patch("src.crud.match.generate_matches")
    @patch("src.utils.validators.tournament_exists")
    def test_check_tournament_progress_and_update_stage(
        self, mock_tournament_exists, mock_generate_matches
    ):
        mock_tournament_exists.return_value = self.tournament

        self.db.begin_nested = MagicMock()
        self.db.refresh = MagicMock()
        self.db.commit = MagicMock()

        self.match.match_format = MatchFormat.MR15
        self.match.team1_score = 15
        self.match.team2_score = 13
        self.match.is_finished = False

        with (
            patch("src.crud.match._check_for_winner_for_mr15", return_value=self.team2),
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.match_exists", return_value=self.match),
            patch("src.utils.validators.match_is_finished", return_value=None),
            patch("src.utils.validators.team_has_five_players", return_value=None),
            patch("src.utils.validators.is_author_of_tournament", return_value=None),
        ):
            update_match_score(
                db=self.db,
                match_id=self.match_id,
                team_to_upvote_score="team1",
                current_user=self.director_user,
            )

        self.db.begin_nested.assert_called_once()
        self.db.commit.assert_called()
        self.db.refresh.assert_called()

    def test_match_team_prizes_final(self):
        """Test awarding prizes in _match_team_prizes when match is final."""
        from src.crud.match import _mark_match_as_finished, _match_team_prizes

        prize1 = MagicMock(place=1, team_id=None, team=MagicMock())
        prize2 = MagicMock(place=2, team_id=None, team=MagicMock())
        self.tournament.prize_cuts = [prize1, prize2]

        self.match.stage = Stage.FINAL
        self.match.is_finished = False
        self.match.team1_score = 16
        self.match.team2_score = 14
        self.match.winner_team_id = None

        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        _mark_match_as_finished(self.db, self.match, self.team1_id)
        _match_team_prizes(self.db, self.match)

        self.db.commit.assert_called()
        self.db.refresh.assert_called()

        self.assertEqual(prize1.team_id, self.team1_id)

    def test_update_match_no_changes(self):
        """Test update_match when no changes are provided
        (no start_time, stage, team1_name, team2_name)."""

        with (
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.match_exists", return_value=self.match),
            patch("src.utils.validators.match_is_finished", return_value=None),
            patch("src.utils.validators.match_has_started", return_value=None),
            patch("src.utils.validators.is_author_of_tournament", return_value=None),
        ):

            match_update = MatchUpdate()
            self.db.commit = MagicMock()
            self.db.refresh = MagicMock()

            result = update_match(
                self.db, self.match_id, match_update, self.director_user
            )

            self.assertEqual(result.id, self.match_id)
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once()

    def test_validate_match_update_already_finished(self):
        """Test update_match when match_is_finished validator fails."""
        with (
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.match_exists", return_value=self.match),
            patch(
                "src.utils.validators.match_is_finished",
                side_effect=HTTPException(status_code=400, detail="Match finished"),
            ),
            patch("src.utils.validators.match_has_started", return_value=None),
            patch("src.utils.validators.is_author_of_tournament", return_value=None),
        ):
            match_update = MatchUpdate(stage=Stage.SEMI_FINAL)
            with self.assertRaises(HTTPException) as ctx:
                update_match(self.db, self.match_id, match_update, self.director_user)
            self.assertIn("Match finished", ctx.exception.detail)

    def test_validate_match_update_already_started(self):
        """Test update_match when match_has_started validator fails."""
        with (
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.match_exists", return_value=self.match),
            patch("src.utils.validators.match_is_finished", return_value=None),
            patch(
                "src.utils.validators.match_has_started",
                side_effect=HTTPException(status_code=400, detail="Match has started"),
            ),
            patch("src.utils.validators.is_author_of_tournament", return_value=None),
        ):
            match_update = MatchUpdate(stage=Stage.SEMI_FINAL)
            with self.assertRaises(HTTPException) as ctx:
                update_match(self.db, self.match_id, match_update, self.director_user)
            self.assertIn("Match has started", ctx.exception.detail)

    def test_validate_match_score_update_not_enough_players(self):
        """Test update_match_score when a team doesn't have 5 players."""
        with (
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.match_exists", return_value=self.match),
            patch("src.utils.validators.is_author_of_tournament", return_value=None),
            patch("src.utils.validators.match_is_finished", return_value=None),
            patch(
                "src.utils.validators.team_has_five_players",
                side_effect=HTTPException(
                    status_code=400, detail="Team must have 5 players"
                ),
            ),
        ):

            with self.assertRaises(HTTPException) as ctx:
                update_match_score(self.db, self.match_id, "team1", self.director_user)
            self.assertIn("Team must have 5 players", ctx.exception.detail)

    def test_validate_match_score_update_not_authorized(self):
        """Test update_match_score when is_author_of_tournament fails."""
        with (
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.match_exists", return_value=self.match),
            patch("src.utils.validators.match_is_finished", return_value=None),
            patch("src.utils.validators.team_has_five_players", return_value=None),
            patch(
                "src.utils.validators.is_author_of_tournament",
                side_effect=HTTPException(status_code=403, detail="Not author"),
            ),
        ):
            with self.assertRaises(HTTPException) as ctx:
                update_match_score(self.db, self.match_id, "team1", self.director_user)
            self.assertIn("Not author", ctx.exception.detail)

    def test_generate_matches_one_off_match(self):
        """Test generate_matches with ONE_OFF_MATCH format."""
        self.tournament.tournament_format = TournamentFormat.ONE_OFF_MATCH
        self.db.bulk_save_objects = MagicMock()

        generate_matches(self.db, self.tournament)
        self.db.bulk_save_objects.assert_called_once()

    def test_validate_and_update_start_time_valid(self):
        """Test _validate_and_update_start_time with a valid start_time."""
        from src.crud.match import _validate_and_update_start_time

        valid_start = self.tournament.start_date + timedelta(days=1)
        match_update = MatchUpdate(start_time=valid_start)
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        with patch("src.crud.match.send_email_notification") as mock_send:
            _validate_and_update_start_time(
                self.match, match_update, "%B %d, %Y at %H:%M"
            )

            mock_send.assert_called_once()

    def test_check_for_winner_for_mr15_no_winner(self):
        """Test _check_for_winner_for_mr15 when no winner conditions are met."""
        from src.crud.match import _check_for_winner_for_mr15

        self.match.match_format = MatchFormat.MR15

        self.match.team1_score = 10
        self.match.team2_score = 10

        self.db.flush = MagicMock()
        self.db.refresh = MagicMock()

        result = _check_for_winner_for_mr15(self.db, self.match)

        self.db.flush.assert_called()
        self.db.refresh.assert_called()
        self.assertIsNone(result)

    def test_check_for_winner_for_mr12_no_winner(self):
        """Test _check_for_winner_for_mr12 when no winner conditions are met."""
        from src.crud.match import _check_for_winner_for_mr12

        self.match.match_format = MatchFormat.MR12
        self.match.team1_score = 5
        self.match.team2_score = 5

        self.db.flush = MagicMock()
        self.db.refresh = MagicMock()

        result = _check_for_winner_for_mr12(self.db, self.match)
        self.db.flush.assert_called()
        self.db.refresh.assert_called()
        self.assertIsNone(result)

    def test_mark_match_as_finished_no_players(self):
        """Test _mark_match_as_finished when winner or loser team has no players."""
        from src.crud.match import _mark_match_as_finished

        self.team1.players = []
        self.team2.players = []

        self.db.flush = MagicMock()
        self.db.refresh = MagicMock()

        _mark_match_as_finished(self.db, self.match, self.team1_id)

        self.db.flush.assert_called()
        self.db.refresh.assert_called()

    def test_handle_finished_match_non_final_non_robin(self):
        """Test _handle_finished_match when stage is
        not final and format is not ROUND_ROBIN."""
        from src.crud.match import _handle_finished_match

        self.match.is_finished = True
        self.match.stage = Stage.SEMI_FINAL
        self.tournament.tournament_format = TournamentFormat.SINGLE_ELIMINATION

        losing_team = self.team2

        _handle_finished_match(self.db, self.match, losing_team)
        self.assertIsNone(losing_team.tournament_id)

    def test_check_tournament_progress_not_all_finished(self):
        """Test _check_tournament_progress when not all matches are finished."""
        from src.crud.match import _check_tournament_progress

        another_match_id = uuid4()
        another_match = Match(
            id=another_match_id,
            match_format=MatchFormat.MR15,
            start_time=datetime.now(timezone.utc) + timedelta(days=2),
            is_finished=False,
            stage=Stage.QUARTER_FINAL,
            team1_id=self.team1_id,
            team2_id=self.team2_id,
            team1_score=0,
            team2_score=0,
            tournament_id=self.tournament_id,
            team1=self.team1,
            team2=self.team2,
            tournament=self.tournament,
        )
        self.tournament.matches.append(another_match)

        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        _check_tournament_progress(self.db, self.match)

    def test_check_tournament_progress_already_finished_stage(self):
        """Test _check_tournament_progress when tournament is already FINISHED."""
        from src.crud.match import _check_tournament_progress

        self.tournament.current_stage = Stage.FINISHED
        self.match.is_finished = True

        with (
            patch("src.crud.match._update_current_stage") as mock_update_stage,
            patch("src.crud.match.generate_matches") as mock_generate,
        ):
            _check_tournament_progress(self.db, self.match)
            mock_update_stage.assert_not_called()
            mock_generate.assert_not_called()

    def test_update_current_stage_group_stage(self):
        """Test _update_current_stage when current_stage is GROUP_STAGE."""
        from src.crud.match import _update_current_stage

        self.tournament.current_stage = Stage.GROUP_STAGE

        self.db.begin_nested = MagicMock()
        self.db.flush = MagicMock()
        self.db.refresh = MagicMock()

        with (
            patch(
                "src.utils.validators.tournament_exists", return_value=self.tournament
            ),
            patch("src.crud.team.leave_top_teams_from_robin_round") as mock_leave_top,
        ):
            _update_current_stage(self.db, self.tournament_id)

            mock_leave_top.assert_called_once()
            self.db.begin_nested.assert_called_once()
            self.db.flush.assert_called()

            self.db.refresh.assert_called()

    def test_match_team_prizes_unknown_place(self):
        """Test _match_team_prizes with a prize having place not 1 or 2."""
        from src.crud.match import _mark_match_as_finished, _match_team_prizes

        prize_unknown = MagicMock(place=3, team_id=None, team=MagicMock())
        self.tournament.prize_cuts.append(prize_unknown)

        self.match.stage = Stage.FINAL
        self.match.is_finished = False
        self.match.team1_score = 16
        self.match.team2_score = 14
        self.match.winner_team_id = None

        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        _mark_match_as_finished(self.db, self.match, self.team1_id)
        _match_team_prizes(self.db, self.match)

        self.db.commit.assert_called()
        self.db.refresh.assert_called()
        self.assertIsNone(prize_unknown.team_id)

    def test_update_score_else_team2(self):
        """Test _update_score else part by incrementing team2 score."""
        from src.crud.match import _update_score

        self.match.team1_score = 0
        self.match.team2_score = 0
        _update_score(self.match, "team2")
        self.assertEqual(self.match.team2_score, 1)
        self.assertEqual(self.match.team1_score, 0)

    def test_check_for_winner_for_mr15_team2_wins_high_score(self):
        """Test _check_for_winner_for_mr15 elif
        part for team2 winning with >=19 points."""
        from src.crud.match import _check_for_winner_for_mr15

        self.match.match_format = MatchFormat.MR15
        self.match.team1_score = 18
        self.match.team2_score = 20
        self.db.flush = MagicMock()
        self.db.refresh = MagicMock()

        with patch("src.crud.match._mark_match_as_finished") as mock_mark:
            result = _check_for_winner_for_mr15(self.db, self.match)
            mock_mark.assert_called_once_with(self.db, self.match, self.match.team2_id)
            self.assertEqual(result, self.match.team1)

    def test_check_for_winner_for_mr12_team2_wins(self):
        """Test _check_for_winner_for_mr12 elif
        part where team2 wins with >=16 points."""
        from src.crud.match import _check_for_winner_for_mr12

        self.match.match_format = MatchFormat.MR12
        self.match.team1_score = 14
        self.match.team2_score = 16
        self.db.flush = MagicMock()
        self.db.refresh = MagicMock()

        with patch("src.crud.match._mark_match_as_finished") as mock_mark:
            result = _check_for_winner_for_mr12(self.db, self.match)
            mock_mark.assert_called_once_with(self.db, self.match, self.match.team2_id)
            self.assertEqual(result, self.match.team1)

    def test_update_match_set_team2_name(self):
        """Test update_match when team2_name is provided to cover that if condition."""

        mock_player = MagicMock(user_id=uuid4())
        self.team2.players.append(mock_player)

        with (
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.match_exists", return_value=self.match),
            patch("src.utils.validators.match_is_finished", return_value=None),
            patch("src.utils.validators.match_has_started", return_value=None),
            patch("src.utils.validators.is_author_of_tournament", return_value=None),
            patch("src.utils.validators.team_exists", return_value=self.team2),
            patch("src.crud.match.send_email_notification") as mock_send,
        ):
            mock_query = MagicMock()
            self.db.query.return_value = mock_query
            mock_query.filter.return_value = mock_query
            mock_query.first.return_value = self.team2

            self.team2.name = "Team 2"
            self.team2.logo = "team2_logo.png"

            match_update = MatchUpdate(team2_name="Team 2")
            self.db.commit = MagicMock()
            self.db.refresh = MagicMock()

            result = update_match(
                self.db, self.match_id, match_update, self.director_user
            )

            self.assertEqual(result.id, self.match_id)
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called()

            mock_send.assert_called()

    def test_get_pairs_robin_round_multiple_teams(self):
        """Test _get_pairs_robin_round with more than 2
        teams to ensure for team2 in teams[i+1:] runs."""
        from src.crud.match import _get_pairs_robin_round

        team3_id = uuid4()
        team3 = Team(id=team3_id, name="Team 3", players=[])
        self.tournament.teams = [self.team1, self.team2, team3]
        self.tournament.tournament_format = TournamentFormat.ROUND_ROBIN
        self.tournament.current_stage = Stage.GROUP_STAGE

        pairs, first_match_datetime = _get_pairs_robin_round(self.tournament)

        self.assertEqual(len(pairs), 3)
        self.assertIn((self.team1, self.team2), pairs)
        self.assertIn((self.team1, team3), pairs)
        self.assertIn((self.team2, team3), pairs)

    def test_generate_matches_with_three_teams_round_robin(self):
        """Test generate_matches with ROUND_ROBIN and three teams."""
        from src.crud.match import generate_matches

        team3_id = uuid4()
        team3 = Team(id=team3_id, name="Team 3", players=[])
        self.tournament.teams = [self.team1, self.team2, team3]
        self.tournament.tournament_format = TournamentFormat.ROUND_ROBIN
        self.tournament.current_stage = Stage.GROUP_STAGE

        self.db.bulk_save_objects = MagicMock()
        with patch("src.crud.match.send_email_notification") as mock_send:
            generate_matches(self.db, self.tournament)

            self.db.bulk_save_objects.assert_called_once()

            mock_send.assert_not_called()

    def test_check_for_winner_mr12_team1_wins_with_exact_score(self):
        """Test _check_for_winner_for_mr12 when team1 wins with exactly 13 points."""
        from src.crud.match import _check_for_winner_for_mr12

        self.match.team1_score = 13
        self.match.team2_score = 11

        with patch("src.crud.match._mark_match_as_finished") as mock_mark:
            result = _check_for_winner_for_mr12(self.db, self.match)
            mock_mark.assert_called_once_with(self.db, self.match, self.team1_id)
            self.assertEqual(result, self.match.team2)

    def test_check_for_winner_mr15_team1_wins_high_score(self):
        """Test _check_for_winner_for_mr15 when team1 wins with high score (>=19)."""
        from src.crud.match import _check_for_winner_for_mr15

        self.match.team1_score = 19
        self.match.team2_score = 17

        with patch("src.crud.match._mark_match_as_finished") as mock_mark:
            result = _check_for_winner_for_mr15(self.db, self.match)
            mock_mark.assert_called_once_with(self.db, self.match, self.team1_id)
            self.assertEqual(result, self.match.team2)

    def test_check_for_winner_mr15_team2_wins_normal_score(self):
        """Test _check_for_winner_for_mr15 when team2 wins with normal score (>=16)."""
        from src.crud.match import _check_for_winner_for_mr15

        self.match.team1_score = 14
        self.match.team2_score = 16

        with patch("src.crud.match._mark_match_as_finished") as mock_mark:
            result = _check_for_winner_for_mr15(self.db, self.match)
            mock_mark.assert_called_once_with(self.db, self.match, self.team2_id)
            self.assertEqual(result, self.match.team1)

    def test_handle_finished_match_final_stage(self):
        """Test _handle_finished_match when match is final stage."""
        from src.crud.match import _handle_finished_match

        self.match.is_finished = True
        self.match.stage = Stage.FINAL

        with patch("src.crud.match._match_team_prizes") as mock_prizes:
            _handle_finished_match(self.db, self.match, self.team2)
            mock_prizes.assert_called_once_with(self.db, self.match)

    def test_update_team1_in_match(self):
        """Test update_match when updating team1."""

        mock_player = MagicMock(user_id=uuid4())

        new_team = Team(
            id=uuid4(),
            name="New Team 1",
            logo="new_logo.png",
            played_games=0,
            won_games=0,
            tournament_id=self.tournament_id,
            players=[mock_player],
        )

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = new_team
        self.db.query.return_value = mock_query

        with (
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.match_exists", return_value=self.match),
            patch("src.utils.validators.match_is_finished", return_value=None),
            patch("src.utils.validators.match_has_started", return_value=None),
            patch("src.utils.validators.is_author_of_tournament", return_value=None),
            patch("src.utils.validators.team_exists", return_value=new_team),
            patch("src.crud.match.send_email_notification") as mock_send,
        ):
            match_update = MatchUpdate(team1_name="New Team 1")

            self.match.team1 = Team(
                id=self.team1_id,
                name="Old Team 1",
                logo="old_logo.png",
                played_games=0,
                won_games=0,
            )
            self.match.team2 = Team(
                id=self.team2_id,
                name="Team 2",
                logo="logo2.png",
                played_games=0,
                won_games=0,
            )

            result = update_match(
                self.db, self.match_id, match_update, self.director_user
            )

            self.assertEqual(result.team1_name, "New Team 1")
            mock_send.assert_called()
            self.db.commit.assert_called_once()

    def test_get_pairs_single_elimination_even_teams(self):
        """Test _get_pairs_single_elimination with even number of teams."""
        from src.crud.match import _get_pairs_single_elimination

        team3 = Team(id=uuid4(), name="Team 3")
        team4 = Team(id=uuid4(), name="Team 4")
        self.tournament.teams = [self.team1, self.team2, team3, team4]

        pairs, _ = _get_pairs_single_elimination(self.tournament)

        self.assertEqual(len(pairs), 2)
        for pair in pairs:
            self.assertEqual(len(pair), 2)

    def test_generate_matches_with_end_hour_overflow(self):
        """Test generate_matches when current_time exceeds END_HOUR."""
        import src.crud.constants as c
        from src.crud.match import generate_matches

        self.tournament.teams = [self.team1, self.team2]

        self.tournament.start_date = datetime.now(timezone.utc).replace(
            hour=c.END_HOUR + 1
        )

        mock_player = MagicMock(
            user_id=uuid4(), user=MagicMock(email="test@example.com")
        )
        self.team1.players = [mock_player]
        self.team2.players = [mock_player]

        self.tournament.tournament_format = TournamentFormat.SINGLE_ELIMINATION
        self.tournament.current_stage = Stage.QUARTER_FINAL

        with patch(
            "src.crud.match.send_email_notification", return_value=None
        ) as mock_send:
            generate_matches(self.db, self.tournament)
            mock_send.assert_called()

            matches = self.db.query(Match).all()
            for match in matches:
                self.assertEqual(match.start_time.hour, c.START_HOUR)
                self.assertTrue(
                    match.start_time.date() > self.tournament.start_date.date()
                )

    def test_generate_matches_with_player_notifications(self):
        """Test generate_matches with players having user_ids for notifications."""
        from src.crud.match import generate_matches

        self.tournament.teams = [self.team1, self.team2]

        self.tournament.tournament_format = TournamentFormat.SINGLE_ELIMINATION
        self.tournament.current_stage = Stage.QUARTER_FINAL

        mock_user = MagicMock(email="player@example.com")
        mock_player = MagicMock(user_id=uuid4(), user=mock_user)

        self.team1.players = [mock_player]
        self.team2.players = [mock_player]

        with patch("src.crud.match.send_email_notification") as mock_send:
            generate_matches(self.db, self.tournament)

            self.assertEqual(mock_send.call_count, 2)
            first_call = mock_send.call_args_list[0]
            self.assertEqual(first_call.kwargs["email"], "player@example.com")
            self.assertEqual(first_call.kwargs["subject"], "Match Created")

    def test_check_for_winner_mr12_team1_wins_overtime(self):
        """Test _check_for_winner_for_mr12 when team1 wins in overtime (>=16 points)."""
        from src.crud.match import _check_for_winner_for_mr12

        self.match.team1_score = 16
        self.match.team2_score = 12

        with patch("src.crud.match._mark_match_as_finished") as mock_mark:
            result = _check_for_winner_for_mr12(self.db, self.match)
            mock_mark.assert_called_once_with(self.db, self.match, self.team1_id)
            self.assertEqual(result, self.match.team2)

    def test_check_for_winner_mr12_team2_exact_score_win(self):
        """Test _check_for_winner_for_mr12 when team2 wins with exactly 13 points."""
        from src.crud.match import _check_for_winner_for_mr12

        self.match.team1_score = 11
        self.match.team2_score = 13

        with patch("src.crud.match._mark_match_as_finished") as mock_mark:
            result = _check_for_winner_for_mr12(self.db, self.match)
            mock_mark.assert_called_once_with(self.db, self.match, self.team2_id)
            self.assertEqual(result, self.match.team1)

    def test_generate_matches_next_day_scheduling(self):
        """Test generate_matches when matches overflow to next day."""
        import src.crud.constants as c
        from src.crud.match import generate_matches

        team3 = Team(id=uuid4(), name="Team 3", players=[])
        team4 = Team(id=uuid4(), name="Team 4", players=[])
        self.tournament.teams = [self.team1, self.team2, team3, team4]

        self.tournament.tournament_format = TournamentFormat.ROUND_ROBIN
        self.tournament.current_stage = Stage.GROUP_STAGE

        start_time = datetime(2024, 12, 8, c.END_HOUR - 1, 0, tzinfo=timezone.utc)
        self.tournament.start_date = start_time
        self.tournament.end_date = start_time + timedelta(days=5)

        with patch("src.crud.match.send_email_notification"):
            generate_matches(self.db, self.tournament)

            saved_matches = self.db.bulk_save_objects.call_args[0][0]

            next_day_match = None
            for match in saved_matches:
                if match.start_time.day > start_time.day:
                    next_day_match = match
                    break

            self.assertIsNotNone(
                next_day_match, "Should have a match scheduled for next day"
            )
            self.assertEqual(next_day_match.start_time.hour, 11)
            self.assertEqual(next_day_match.start_time.day, start_time.day + 1)

    def test_update_match_score_tie_game(self):
        """Test updating match score when game is tied."""
        with (
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.match_exists", return_value=self.match),
            patch("src.utils.validators.match_is_finished", return_value=None),
            patch("src.utils.validators.team_has_five_players", return_value=None),
            patch("src.utils.validators.is_author_of_tournament", return_value=None),
        ):
            self.match.team1_score = 14
            self.match.team2_score = 14

            result = update_match_score(
                self.db, self.match_id, "team1", self.director_user
            )

            self.assertEqual(result.team1_score, 15)
            self.assertEqual(result.team2_score, 14)
            self.assertFalse(result.is_finished)

    def test_handle_finished_match_round_robin(self):
        """Test handling finished match in round robin tournament."""
        self.tournament.tournament_format = TournamentFormat.ROUND_ROBIN
        losing_team = self.team2

        from src.crud.match import _handle_finished_match

        _handle_finished_match(self.db, self.match, losing_team)

        self.assertIsNotNone(losing_team.tournament_id)
