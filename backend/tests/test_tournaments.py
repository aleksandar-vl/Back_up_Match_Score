from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.crud.tournament import (
    _calculate_tournament_end_date,
    _get_author_filter,
    _get_format_filter,
    _get_period_filter,
    _get_search_filter,
    _get_status_filter,
    _get_tournament_current_stage,
    create_tournament,
    get_tournament,
    get_tournaments,
    update_tournament,
)
from src.models import Match, Team, Tournament, User
from src.models.enums import MatchFormat, Role, Stage, TournamentFormat
from src.schemas.tournament import TournamentCreate, TournamentUpdate
from src.utils.pagination import PaginationParams
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)


class TournamentServiceShould(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user_id = uuid4()
        self.admin_id = uuid4()
        self.director_id = uuid4()
        self.team1_id = uuid4()
        self.team2_id = uuid4()
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

        self.team1 = Team(
            id=self.team1_id,
            name="Team 1",
            logo="logo1.png",
            played_games=5,
            won_games=3,
            tournament_id=self.tournament_id,
        )

        self.team2 = Team(
            id=self.team2_id,
            name="Team 2",
            logo="logo2.png",
            played_games=5,
            won_games=2,
            tournament_id=self.tournament_id,
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
            teams=[self.team1, self.team2],
            matches=[],
            prize_cuts=[],
        )

        self.pagination = PaginationParams(offset=0, limit=10)

    def test_get_tournaments_with_all_filters(self):
        """Test get_tournaments with all possible filters applied."""
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [self.tournament]
        self.db.query.return_value = mock_query

        result = get_tournaments(
            db=self.db,
            pagination=self.pagination,
            period="present",
            status="active",
            tournament_format=TournamentFormat.SINGLE_ELIMINATION,
            search="Test",
            author_id=self.director_id,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.tournament_id)
        mock_query.filter.assert_called()
        mock_query.order_by.assert_called_once()

    def test_get_tournaments_no_filters(self):
        """Test get_tournaments without any filters."""
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [self.tournament]
        self.db.query.return_value = mock_query

        result = get_tournaments(db=self.db, pagination=self.pagination)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.tournament_id)
        mock_query.options.assert_called_once()

    def test_get_tournament_success(self):
        """Test get_tournament successfully retrieves a tournament."""
        self.db.query.return_value.filter.return_value.first.return_value = (
            self.tournament
        )

        result = get_tournament(self.db, self.tournament_id)

        self.assertEqual(result.id, self.tournament_id)
        self.assertEqual(result.title, "Test Tournament")
        self.assertEqual(result.tournament_format, TournamentFormat.SINGLE_ELIMINATION)

    def test_get_tournament_not_found(self):
        """Test get_tournament raises exception when tournament not found."""
        self.db.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(HTTPException) as context:
            get_tournament(self.db, uuid4())

        self.assertEqual(context.exception.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, "Tournament not found")

    @patch("src.crud.tournament.crud_match.generate_matches")
    @patch("src.crud.tournament.crud_team.create_teams_lst_for_tournament")
    @patch("src.crud.tournament.crud_prize_cut.create_prize_cuts_for_tournament")
    def test_create_tournament_success(
        self, mock_create_prize_cuts, mock_create_teams, mock_generate_matches
    ):
        """Test create_tournament successfully creates a tournament."""
        tournament_create = TournamentCreate(
            title="New Tournament",
            tournament_format=TournamentFormat.SINGLE_ELIMINATION,
            start_date=datetime.now(timezone.utc) + timedelta(days=2),
            prize_pool=1000,
            team_names=["Team 1", "Team 2", "Team 3", "Team 4"],
        )

        self.db.query.return_value.filter.return_value.first.return_value = None

        def mock_add(tournament):
            tournament.id = uuid4()
            tournament.matches = []
            tournament.teams = []
            tournament.prize_cuts = []

        self.db.add.side_effect = mock_add

        mock_create_prize_cuts.return_value = None
        mock_create_teams.return_value = None
        mock_generate_matches.return_value = None

        result = create_tournament(
            db=self.db, tournament=tournament_create, current_user=self.director_user
        )

        self.assertEqual(result.title, "New Tournament")
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        mock_create_prize_cuts.assert_called_once()
        mock_create_teams.assert_called_once()
        mock_generate_matches.assert_called_once()

    def test_create_tournament_duplicate_teams(self):
        """Test create_tournament fails with duplicate team names."""
        tournament_create = TournamentCreate(
            title="New Tournament",
            tournament_format=TournamentFormat.SINGLE_ELIMINATION,
            start_date=datetime.now(timezone.utc) + timedelta(days=2),
            prize_pool=1000,
            team_names=["Team 1", "Team 1", "Team 2", "Team 3"],
        )

        with self.assertRaises(HTTPException) as context:
            create_tournament(
                db=self.db,
                tournament=tournament_create,
                current_user=self.director_user,
            )

        self.assertEqual(context.exception.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail, "There is a duplicate team in the tournament list"
        )

    def test_create_tournament_existing_title(self):
        """Test create_tournament fails with existing tournament title."""
        tournament_create = TournamentCreate(
            title="Test Tournament",
            tournament_format=TournamentFormat.SINGLE_ELIMINATION,
            start_date=datetime.now(timezone.utc) + timedelta(days=2),
            prize_pool=1000,
            team_names=["Team 1", "Team 2", "Team 3", "Team 4"],
        )

        self.db.query.return_value.filter.return_value.first.return_value = (
            self.tournament
        )

        with self.assertRaises(HTTPException) as context:
            create_tournament(
                db=self.db,
                tournament=tournament_create,
                current_user=self.director_user,
            )

        self.assertEqual(context.exception.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail, "Tournament with this title already exists"
        )

    def test_create_tournament_invalid_start_date(self):
        """Test create_tournament fails with start date in the past."""
        tournament_create = TournamentCreate(
            title="New Tournament",
            tournament_format=TournamentFormat.SINGLE_ELIMINATION,
            start_date=datetime.now(timezone.utc) - timedelta(days=1),
            prize_pool=1000,
            team_names=["Team 1", "Team 2", "Team 3", "Team 4"],
        )

        self.db.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(HTTPException) as context:
            create_tournament(
                db=self.db,
                tournament=tournament_create,
                current_user=self.director_user,
            )

        self.assertEqual(context.exception.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail, "Start date must be at least 1 day in the future"
        )

    def test_update_tournament_success(self):
        """Test update_tournament successfully updates tournament details."""
        tournament_update = TournamentUpdate(
            title="Updated Tournament",
            end_date=datetime.now(timezone.utc) + timedelta(days=7),
            prize_pool=2000,
        )

        self.tournament.teams = []
        self.tournament.matches = []
        self.tournament.prize_cuts = []
        self.tournament.title = "Old Tournament"
        self.tournament.director_id = self.director_user.id

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.side_effect = [self.tournament, self.tournament, None]
        self.db.query.return_value = mock_query

        mock_transaction = MagicMock()
        self.db.begin_nested.return_value = mock_transaction
        self.db.begin_nested.return_value.__enter__.return_value = None
        self.db.begin_nested.return_value.__exit__.return_value = None

        with (
            patch(
                "src.crud.tournament.crud_prize_cut.delete_prize_cuts_for_tournament"
            ) as mock_delete_cuts,
            patch(
                "src.crud.tournament.crud_prize_cut.create_prize_cuts_for_tournament"
            ) as mock_create_cuts,
        ):
            mock_delete_cuts.return_value = None
            mock_create_cuts.return_value = None

            result = update_tournament(
                db=self.db,
                tournament_id=self.tournament_id,
                tournament=tournament_update,
                current_user=self.director_user,
            )

        self.assertEqual(result.title, "Updated Tournament")

        self.db.begin_nested.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        mock_delete_cuts.assert_called_once()
        mock_create_cuts.assert_called_once()

        self.assertEqual(self.tournament.title, "Updated Tournament")
        self.assertEqual(self.tournament.prize_pool, 2000)

    def test_update_tournament_not_authorized(self):
        """Test update_tournament fails when user is not authorized."""
        tournament_update = TournamentUpdate(title="Updated Tournament")

        with self.assertRaises(HTTPException) as context:
            update_tournament(
                db=self.db,
                tournament_id=self.tournament_id,
                tournament=tournament_update,
                current_user=self.current_user,
            )

        self.assertEqual(context.exception.status_code, HTTP_403_FORBIDDEN)

    def test_get_period_filter_past(self):
        """Test _get_period_filter for past tournaments."""
        filters = _get_period_filter("past")
        self.assertEqual(len(filters), 1)

    def test_get_period_filter_present(self):
        """Test _get_period_filter for present tournaments."""
        filters = _get_period_filter("present")
        self.assertEqual(len(filters), 1)

    def test_get_period_filter_future(self):
        """Test _get_period_filter for future tournaments."""
        filters = _get_period_filter("future")
        self.assertEqual(len(filters), 1)

    def test_get_status_filter_active(self):
        """Test _get_status_filter for active tournaments."""
        filters = _get_status_filter("active")
        self.assertEqual(len(filters), 1)

    def test_get_status_filter_finished(self):
        """Test _get_status_filter for finished tournaments."""
        filters = _get_status_filter("finished")
        self.assertEqual(len(filters), 1)

    def test_get_format_filter(self):
        """Test _get_format_filter for specific tournament format."""
        filters = _get_format_filter(TournamentFormat.SINGLE_ELIMINATION)
        self.assertEqual(len(filters), 1)

    def test_get_search_filter(self):
        """Test _get_search_filter for title search."""
        filters = _get_search_filter("Test")
        self.assertEqual(len(filters), 1)

    def test_get_author_filter(self):
        """Test _get_author_filter for specific director."""
        filters = _get_author_filter(self.director_id)
        self.assertEqual(len(filters), 1)

    def test_get_tournament_current_stage_round_robin(self):
        """Test _get_tournament_current_stage for round robin format."""
        stage = _get_tournament_current_stage(TournamentFormat.ROUND_ROBIN.value, 4)
        self.assertEqual(stage, Stage.GROUP_STAGE)

    def test_get_tournament_current_stage_one_off(self):
        """Test _get_tournament_current_stage for one off match format."""
        stage = _get_tournament_current_stage(TournamentFormat.ONE_OFF_MATCH.value, 2)
        self.assertEqual(stage, Stage.FINAL)

    def test_get_tournament_current_stage_invalid_teams(self):
        """Test _get_tournament_current_stage with invalid number of teams."""
        with self.assertRaises(HTTPException) as context:
            _get_tournament_current_stage(TournamentFormat.SINGLE_ELIMINATION.value, 3)
        self.assertEqual(context.exception.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail,
            "Invalid number of teams for single " "elimination - must be 4, 8 or 16",
        )

    def test_validate_tournament_title_length(self):
        """Test validation for tournament title length when updating."""
        from unittest.mock import patch

        from fastapi import HTTPException
        from src.crud.tournament import update_tournament
        from src.schemas.tournament import TournamentUpdate
        from starlette.status import HTTP_400_BAD_REQUEST

        self.tournament.director_id = self.director_user.id

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.filter.return_value.first.return_value = self.tournament
        self.db.query.return_value = mock_query

        invalid_update = TournamentUpdate.model_construct(
            title="", end_date=None, prize_pool=None
        )

        with patch(
            "src.schemas.tournament.TournamentUpdate.model_validate",
            return_value=invalid_update,
        ):
            with self.assertRaises(HTTPException) as context:
                update_tournament(
                    self.db, self.tournament_id, invalid_update, self.director_user
                )

            self.assertEqual(context.exception.status_code, HTTP_400_BAD_REQUEST)
            self.assertEqual(context.exception.detail, "Title must not be empty")

    def test_calculate_tournament_end_date_round_robin(self):
        """Test _calculate_tournament_end_date for round robin
        format with correct days calculation."""
        start_date = datetime(2024, 12, 1, 12, 0, tzinfo=timezone.utc)
        format = TournamentFormat.ROUND_ROBIN
        current_stage = Stage.GROUP_STAGE
        total_teams = 4

        result = _calculate_tournament_end_date(
            start_date, format, current_stage, total_teams
        )

        expected_end = start_date + timedelta(days=3)
        expected_end = expected_end.replace(hour=23, minute=59, second=59)

        self.assertEqual(result.date(), expected_end.date())
        self.assertEqual(result.hour, expected_end.hour)
        self.assertEqual(result.minute, expected_end.minute)
        self.assertEqual(result.second, expected_end.second)

        # Очакваме 4-ти декември (1-ви + 3 дни)
        self.assertEqual(result.strftime("%Y-%m-%d"), "2024-12-04")

    def test_get_tournament_current_stage_invalid_one_off_teams(self):
        """Test _get_tournament_current_stage fails with
        invalid number of teams for one off match."""
        with self.assertRaises(HTTPException) as context:
            _get_tournament_current_stage(TournamentFormat.ONE_OFF_MATCH.value, 3)

        self.assertEqual(context.exception.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail,
            "Invalid number of teams for one off match - must be 2",
        )

    def test_get_tournament_current_stage_invalid_round_robin_teams(self):
        """Test _get_tournament_current_stage fails with
        invalid number of teams for round robin."""
        with self.assertRaises(HTTPException) as context:
            _get_tournament_current_stage(TournamentFormat.ROUND_ROBIN.value, 3)

        self.assertEqual(context.exception.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            context.exception.detail,
            "Invalid number of teams for round robin - must be 4 or 5",
        )

    def test_get_tournament_current_stage_single_elimination(self):
        """Test _get_tournament_current_stage returns correct stages
        for different number of teams in single elimination."""
        stage = _get_tournament_current_stage(
            TournamentFormat.SINGLE_ELIMINATION.value, 4
        )
        self.assertEqual(stage, Stage.SEMI_FINAL)

        stage = _get_tournament_current_stage(
            TournamentFormat.SINGLE_ELIMINATION.value, 8
        )
        self.assertEqual(stage, Stage.QUARTER_FINAL)

    def test_get_tournament_current_stage_invalid_single_elimination(self):
        """Test _get_tournament_current_stage fails for
        invalid number of teams in single elimination."""
        invalid_numbers = [2, 3, 5, 6, 7, 9, 16]

        for num in invalid_numbers:
            with self.assertRaises(HTTPException) as context:
                _get_tournament_current_stage(
                    TournamentFormat.SINGLE_ELIMINATION.value, num
                )

            self.assertEqual(context.exception.status_code, HTTP_400_BAD_REQUEST)
            self.assertEqual(
                context.exception.detail,
                "Invalid number of teams for single elimination - must be 4, 8 or 16",
            )

    def test_get_tournament_with_teams(self):
        """Test get_tournament correctly collects unique teams from matches."""
        match1 = Match(
            id=uuid4(),
            team1=self.team1,
            team2=self.team2,
            team1_id=self.team1_id,
            team2_id=self.team2_id,
            match_format=MatchFormat.MR15,
            start_time=datetime.now(timezone.utc),
            is_finished=False,
            stage=Stage.QUARTER_FINAL,
            tournament_id=self.tournament_id,
            tournament=self.tournament,
            team1_score=0,
            team2_score=0,
        )

        team3_id = uuid4()
        team3 = Team(id=team3_id, name="Team 3")
        match2 = Match(
            id=uuid4(),
            team1=self.team1,
            team2=team3,
            team1_id=self.team1_id,
            team2_id=team3_id,
            match_format=MatchFormat.MR15,
            start_time=datetime.now(timezone.utc),
            is_finished=False,
            stage=Stage.QUARTER_FINAL,
            tournament_id=self.tournament_id,
            tournament=self.tournament,
            team1_score=0,
            team2_score=0,
        )

        self.tournament.matches = [match1, match2]
        self.tournament.teams = [self.team1, self.team2]

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.filter.return_value.first.return_value = self.tournament
        self.db.query.return_value = mock_query

        result = get_tournament(self.db, self.tournament_id)

        self.assertEqual(len(result.teams), 2)
        team_names = {team.name for team in result.teams}
        self.assertEqual(team_names, {"Team 1", "Team 2"})
