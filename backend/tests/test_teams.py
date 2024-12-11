from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from src.crud.team import (
    create_team,
    create_teams_lst_for_tournament,
    get_team,
    get_teams,
    leave_top_teams_from_robin_round,
    update_team,
)
from src.models import Match, Team, Tournament, User
from src.models.enums import MatchFormat, Role, Stage
from src.schemas.team import TeamCreate, TeamUpdate
from src.utils.pagination import PaginationParams


class TeamServiceShould(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db = MagicMock(spec=Session)
        self.user_id = uuid4()
        self.admin_id = uuid4()
        self.director_id = uuid4()
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

        self.team = Team(
            id=self.team_id,
            name="Test Team",
            logo="test_logo.png",
            played_games=10,
            won_games=5,
            tournament_id=self.tournament_id,
        )

        self.tournament = Tournament(
            id=self.tournament_id,
            title="Test Tournament",
            start_date=datetime.now(),
            end_date=datetime.now(),
            current_stage=Stage.GROUP_STAGE,
        )

        self.pagination = PaginationParams(offset=0, limit=10)

    def test_get_teams_with_all_filters(self):
        """Test get_teams with all filters applied."""

        mock_team_query = MagicMock()
        mock_team_query.filter.return_value = mock_team_query
        mock_team_query.all.return_value = [self.team]

        mock_player_query = MagicMock()
        mock_player_query.group_by.return_value = mock_player_query
        mock_player_query.all.return_value = [(self.team_id, 5)]

        call_count = 0

        def side_effect(*args):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_team_query
            return mock_player_query

        self.db.query.side_effect = side_effect

        result = get_teams(
            self.db,
            self.pagination,
            search="Test",
            is_available="false",
            has_space="true",
            sort_by="desc",
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test Team")
        mock_team_query.filter.assert_called()
        self.assertEqual(call_count, 2)

    def test_get_teams_no_filters(self):
        """Test get_teams without any filters."""
        mock_query = MagicMock()
        mock_query.all.return_value = [self.team]
        self.db.query.return_value = mock_query

        result = get_teams(self.db, self.pagination)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test Team")

    @patch("src.utils.validators.director_or_admin")
    @patch("src.utils.validators.team_name_unique")
    @patch("src.utils.s3.s3_service.upload_file")
    def test_create_team_success(
        self, mock_upload_file, mock_team_name_unique, mock_director_or_admin
    ):
        """Test creating a team successfully."""
        mock_director_or_admin.return_value = None
        mock_team_name_unique.return_value = None
        mock_upload_file.return_value = "new_logo_url"

        team_create = TeamCreate(name="New Team")
        logo = MagicMock(spec=UploadFile)

        def mock_add(team):
            team.id = uuid4()
            team.name = "New Team"
            team.logo = "new_logo_url"
            team.played_games = 0
            team.won_games = 0

        self.db.add = MagicMock(side_effect=mock_add)

        result = create_team(self.db, team_create, logo, self.director_user)

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.name, "New Team")
        self.assertEqual(result.logo, "new_logo_url")

    @patch("src.utils.validators.team_exists")
    def test_get_team_with_matches_success(self, mock_team_exists):
        """Test get_team with match history successfully."""
        mock_team_exists.return_value = self.team

        opponent_team = Team(id=uuid4(), name="Opponent Team")
        match = Match(
            id=uuid4(),
            match_format=MatchFormat.MR15,
            start_time=datetime.now(),
            is_finished=True,
            stage=Stage.FINAL,
            team1_id=self.team_id,
            team2_id=opponent_team.id,
            team1=self.team,
            team2=opponent_team,
            winner_team_id=self.team_id,
            tournament=self.tournament,
            tournament_id=self.tournament_id,
            team1_score=16,
            team2_score=14,
        )

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [match]
        self.db.query.return_value = mock_query

        result = get_team(self.db, self.team_id)

        self.assertEqual(result.id, self.team_id)
        self.assertEqual(result.name, "Test Team")
        self.assertEqual(result.logo, "test_logo.png")
        self.assertEqual(result.tournament_id, self.tournament_id)

        self.assertEqual(result.team_stats["matches_played"], 10)
        self.assertEqual(result.team_stats["matches_won"], 5)
        self.assertEqual(result.team_stats["tournaments_won"], 1)
        self.assertEqual(
            result.team_stats["tournaments_played"], 0
        )  # Това е 0 според резултата
        self.assertEqual(
            result.team_stats["most_often_played_opponent"], opponent_team.name
        )
        self.assertEqual(result.team_stats["best_opponent"], opponent_team.name)
        self.assertEqual(result.team_stats["worst_opponent"], opponent_team.name)

        self.assertEqual(result.team_stats["match_win_loss_ratio"]["wins"], 5)
        self.assertEqual(result.team_stats["match_win_loss_ratio"]["losses"], 5)
        self.assertEqual(result.team_stats["match_win_loss_ratio"]["ratio"], "50%")

        self.assertEqual(result.team_stats["tournament_win_loss_ratio"]["won"], 1)
        self.assertEqual(result.team_stats["tournament_win_loss_ratio"]["played"], 0)
        self.assertEqual(result.team_stats["tournament_win_loss_ratio"]["ratio"], "0%")

        self.assertEqual(len(result.matches), 1)
        match_response = result.matches[0]
        self.assertEqual(match_response.team1_name, "Test Team")
        self.assertEqual(match_response.team2_name, "Opponent Team")
        self.assertEqual(match_response.team1_score, 16)
        self.assertEqual(match_response.team2_score, 14)
        self.assertEqual(match_response.winner_id, self.team_id)

        self.assertEqual(result.players, [])
        self.assertEqual(result.prize_cuts, [])

    @patch("src.utils.validators.team_exists")
    @patch("src.utils.validators.director_or_admin")
    @patch("src.utils.validators.team_name_unique")
    @patch("src.utils.s3.s3_service.delete_file")
    @patch("src.utils.s3.s3_service.upload_file")
    def test_update_team_success(
        self,
        mock_upload_file,
        mock_delete_file,
        mock_team_name_unique,
        mock_director_or_admin,
        mock_team_exists,
    ):
        """Test updating a team successfully."""
        mock_team_exists.return_value = self.team
        mock_director_or_admin.return_value = None
        mock_team_name_unique.return_value = None
        mock_upload_file.return_value = "new_logo_url"

        team_update = TeamUpdate(name="Updated Team")
        logo = MagicMock(spec=UploadFile)

        result = update_team(
            self.db, self.team_id, team_update, logo, self.director_user
        )

        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.name, "Updated Team")
        mock_delete_file.assert_called_once_with("test_logo.png")

    def test_create_teams_lst_for_tournament_success(self):
        """Test creating teams list for tournament successfully."""
        team_names = ["Team 1", "Team 2"]

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query

        mock_query.first.side_effect = [
            None,
            None,
            None,
            None,
        ]
        self.db.query.return_value = mock_query

        create_teams_lst_for_tournament(self.db, team_names, self.tournament_id)

        self.assertEqual(self.db.add.call_count, 2)

        self.db.flush.assert_called()
        mock_query.filter.call_count >= 2

        calls = self.db.add.call_args_list
        for call in calls:
            created_team = call[0][0]
            self.assertIsInstance(created_team, Team)
            self.assertEqual(created_team.tournament_id, self.tournament_id)
            self.assertIn(created_team.name, team_names)

    def test_create_teams_lst_existing_team_in_tournament(self):
        """Test creating teams list fails when team is in another tournament."""
        existing_team = Team(
            id=uuid4(),
            name="Existing Team",
            tournament_id=uuid4(),  # Already in a tournament
        )

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = existing_team
        self.db.query.return_value = mock_query

        with self.assertRaises(HTTPException) as context:
            create_teams_lst_for_tournament(
                self.db, ["Existing Team"], self.tournament_id
            )

        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "already participates in another tournament", context.exception.detail
        )

    def test_leave_top_teams_from_robin_round(self):
        """Test leave_top_teams_from_robin_round successful execution."""
        team1 = Team(id=uuid4(), name="Team 1", tournament_id=self.tournament_id)
        team2 = Team(id=uuid4(), name="Team 2", tournament_id=self.tournament_id)
        team3 = Team(id=uuid4(), name="Team 3", tournament_id=self.tournament_id)

        match1 = Match(
            team1=team1,
            team2=team2,
            team1_score=16,
            team2_score=14,
            winner_team_id=team1.id,
            tournament=self.tournament,
            tournament_id=self.tournament_id,
        )
        match2 = Match(
            team1=team1,
            team2=team3,
            team1_score=16,
            team2_score=10,
            winner_team_id=team1.id,
            tournament=self.tournament,
            tournament_id=self.tournament_id,
        )
        match3 = Match(
            team1=team2,
            team2=team3,
            team1_score=16,
            team2_score=12,
            winner_team_id=team2.id,
            tournament=self.tournament,
            tournament_id=self.tournament_id,
        )

        self.tournament.teams = [team1, team2, team3]
        self.tournament.matches = [match1, match2, match3]

        leave_top_teams_from_robin_round(self.db, self.tournament)

        self.assertEqual(team1.tournament_id, self.tournament_id)
        self.assertEqual(team2.tournament_id, self.tournament_id)
        self.assertIsNone(team3.tournament_id)
        self.db.flush.assert_called()

    def test_get_team_no_matches(self):
        """Test get_team when team has no match history."""
        with patch("src.utils.validators.team_exists", return_value=self.team):
            mock_query = MagicMock()
            mock_query.filter.return_value = mock_query
            mock_query.all.return_value = []
            self.db.query.return_value = mock_query

            result = get_team(self.db, self.team_id)

            self.assertEqual(result.id, self.team_id)
            self.assertEqual(result.name, "Test Team")
            self.assertEqual(result.logo, "test_logo.png")
            self.assertEqual(result.tournament_id, self.tournament_id)

            self.assertEqual(result.team_stats["tournaments_played"], 0)
            self.assertEqual(result.team_stats["tournaments_won"], 0)
            self.assertEqual(result.team_stats["matches_played"], 10)
            self.assertEqual(result.team_stats["matches_won"], 5)

            win_loss_ratio = result.team_stats["match_win_loss_ratio"]
            self.assertEqual(win_loss_ratio["ratio"], "0%")
            self.assertEqual(win_loss_ratio["wins"], 0)
            self.assertEqual(win_loss_ratio["losses"], 0)

            tournament_ratio = result.team_stats["tournament_win_loss_ratio"]
            self.assertEqual(tournament_ratio["ratio"], "0%")
            self.assertEqual(tournament_ratio["won"], 0)
            self.assertEqual(tournament_ratio["played"], 0)

            self.assertIsNone(result.team_stats["most_often_played_opponent"])
            self.assertIsNone(result.team_stats["best_opponent"])
            self.assertIsNone(result.team_stats["worst_opponent"])

            self.assertEqual(result.matches, [])
            self.assertEqual(result.players, [])
            self.assertEqual(result.prize_cuts, [])

    def test_create_team_no_logo(self):
        """Test creating a team without a logo."""
        with (
            patch("src.utils.validators.director_or_admin", return_value=None),
            patch("src.utils.validators.team_name_unique", return_value=None),
        ):
            team_create = TeamCreate(name="New Team")

            def mock_add(team):
                team.id = uuid4()
                team.name = "New Team"
                team.logo = None
                team.played_games = 0
                team.won_games = 0

            self.db.add = MagicMock(side_effect=mock_add)

            result = create_team(self.db, team_create, None, self.director_user)

            self.db.add.assert_called_once()
            self.assertEqual(result.name, "New Team")
            self.assertIsNone(result.logo)

    def test_update_team_no_changes(self):
        """Test updating a team with no changes provided."""
        with (
            patch("src.utils.validators.team_exists", return_value=self.team),
            patch("src.utils.validators.director_or_admin", return_value=None),
        ):
            team_update = TeamUpdate()

            result = update_team(
                self.db, self.team_id, team_update, None, self.director_user
            )

            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once()
            self.assertEqual(result.name, "Test Team")

    def test_get_teams_with_no_results(self):
        """Test get_teams returns empty list when no teams match filters."""
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = []
        self.db.query.return_value = mock_query

        result = get_teams(
            self.db,
            self.pagination,
            search="Nonexistent",
            is_available="true",
        )

        self.assertEqual(result, [])

    def test_create_teams_lst_existing_team_no_tournament(self):
        """Test creating teams list with existing team not in tournament."""
        existing_team = Team(id=uuid4(), name="Existing Team", tournament_id=None)

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = existing_team
        self.db.query.return_value = mock_query

        create_teams_lst_for_tournament(self.db, ["Existing Team"], self.tournament_id)

        self.assertEqual(existing_team.tournament_id, self.tournament_id)

        self.db.add.assert_not_called()

        mock_query.filter.assert_called_once()
        self.db.query.assert_called_once_with(Team)

    def test_get_teams_with_lost_matches(self):
        """Test get_teams with a team that has lost matches."""
        team1 = Team(id=uuid4(), name="Losing Team", played_games=5, won_games=2)

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [team1]
        self.db.query.return_value = mock_query

        mock_player_counts = [(team1.id, 5)]
        mock_player_query = MagicMock()
        mock_player_query.group_by.return_value.all.return_value = mock_player_counts

        call_count = 0

        def side_effect(*args):
            nonlocal call_count
            call_count += 1
            return mock_player_query if call_count == 2 else mock_query

        self.db.query.side_effect = side_effect

        result = get_teams(self.db, self.pagination, sort_by="desc")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Losing Team")

        self.assertEqual(result[0].game_win_ratio, "40%")  # 2/5 * 100

    def test_get_teams_with_finished_tournament(self):
        """Test get_teams for teams that participated in finished tournaments."""
        team = Team(id=uuid4(), name="Tournament Team", played_games=5, won_games=2)

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [team]
        self.db.query.return_value = mock_query

        mock_player_counts = [(team.id, 5)]
        mock_player_query = MagicMock()
        mock_player_query.group_by.return_value.all.return_value = mock_player_counts

        call_count = 0

        def side_effect(*args):
            nonlocal call_count
            call_count += 1
            return mock_player_query if call_count == 2 else mock_query

        self.db.query.side_effect = side_effect

        result = get_teams(self.db, self.pagination)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Tournament Team")

    def test_get_teams_with_full_roster(self):
        """Test get_teams filtering for teams with full rosters (10 or more players)."""
        team_full = Team(id=uuid4(), name="Full Team", played_games=5, won_games=2)

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [team_full]

        mock_player_counts = [(team_full.id, 10)]
        mock_player_query = MagicMock()
        mock_player_query.group_by.return_value = mock_player_query
        mock_player_query.all.return_value = mock_player_counts

        call_count = 0

        def side_effect(*args):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_query
            return mock_player_query

        self.db.query.side_effect = side_effect

        result = get_teams(self.db, self.pagination, has_space="false")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Full Team")

        call_count = 0

        result_with_space = get_teams(self.db, self.pagination, has_space="true")

        self.assertEqual(len(result_with_space), 0)

    def test_get_teams_with_available_space(self):
        """Test get_teams filtering for teams with
        available space (less than 10 players)."""
        team = Team(id=uuid4(), name="Team With Space", played_games=5, won_games=2)

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [team]

        mock_player_counts = [(team.id, 8)]
        mock_player_query = MagicMock()
        mock_player_query.group_by.return_value = mock_player_query
        mock_player_query.all.return_value = mock_player_counts

        call_count = 0

        def side_effect(*args):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_query
            return mock_player_query

        self.db.query.side_effect = side_effect

        result = get_teams(self.db, self.pagination, has_space="true")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Team With Space")

        call_count = 0

        result_full = get_teams(self.db, self.pagination, has_space="false")

        self.assertEqual(len(result_full), 0)

    @patch("src.utils.validators.team_exists")
    def test_tournaments_played_when_match_finished(self, mock_team_exists):
        """Test counting tournaments played when a
        match's tournament stage is finished."""
        mock_team_exists.return_value = self.team

        finished_tournament = Tournament(
            id=uuid4(),
            title="Finished Tournament",
            current_stage=Stage.FINISHED,
        )

        opponent_team = Team(id=uuid4(), name="Opponent Team")
        match = Match(
            id=uuid4(),
            team1=self.team,
            team2=opponent_team,
            winner_team_id=self.team_id,
            tournament=finished_tournament,
            tournament_id=finished_tournament.id,
            match_format=MatchFormat.MR15,
            start_time=datetime.now(),
            is_finished=True,
            stage=Stage.FINISHED,
            team1_id=self.team_id,
            team2_id=opponent_team.id,
            team1_score=16,
            team2_score=14,
        )

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [match]
        self.db.query.return_value = mock_query

        result = get_team(self.db, self.team_id)

        self.assertEqual(result.team_stats["tournaments_played"], 1)
