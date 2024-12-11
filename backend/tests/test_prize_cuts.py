from datetime import datetime
import unittest
from unittest.mock import MagicMock
from uuid import uuid4

from sqlalchemy.orm import Session
from src.crud.prize_cut import (
    create_prize_cuts_for_tournament,
    delete_prize_cuts_for_tournament,
)
from src.models import PrizeCut, Tournament


class PrizeCutServiceShould(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db = MagicMock(spec=Session)
        self.tournament_id = uuid4()
        self.tournament = Tournament(
            id=self.tournament_id,
            title="Test Tournament",
            prize_pool=10000,
            start_date=datetime.now(),
            end_date=datetime.now(),
        )

    def test_create_prize_cut_success(self):
        """Test creating a single prize cut successfully."""
        from src.crud.prize_cut import _create_prize_cut

        # Arrange
        place = 1
        prize_amount = 7000

        # Act
        result = _create_prize_cut(place, prize_amount, self.tournament_id)

        # Assert
        self.assertIsInstance(result, PrizeCut)
        self.assertEqual(result.place, place)
        self.assertEqual(result.prize_cut, prize_amount)
        self.assertEqual(result.tournament_id, self.tournament_id)
        self.assertIsNone(result.team_id)

    def test_create_prize_cuts_for_tournament_success(self):
        """Test creating all prize cuts for a tournament with correct proportions."""
        # Arrange
        prize_pool = 10000
        expected_first_place = 7000
        expected_second_place = 3000

        # Act
        create_prize_cuts_for_tournament(self.db, self.tournament, prize_pool)

        # Assert
        self.assertEqual(self.db.add.call_count, 2)

        call_args_list = self.db.add.call_args_list
        first_prize = call_args_list[0][0][0]
        second_prize = call_args_list[1][0][0]

        self.assertEqual(first_prize.place, 1)
        self.assertEqual(first_prize.prize_cut, expected_first_place)
        self.assertEqual(first_prize.tournament_id, self.tournament_id)

        # Check second place prize
        self.assertEqual(second_prize.place, 2)
        self.assertEqual(second_prize.prize_cut, expected_second_place)
        self.assertEqual(second_prize.tournament_id, self.tournament_id)

    def test_create_prize_cuts_with_odd_prize_pool(self):
        """Test creating prize cuts with a prize pool that doesn't divide evenly."""
        # Arrange
        prize_pool = 9999
        expected_first_place = round(0.7 * prize_pool)
        expected_second_place = round(0.3 * prize_pool)

        # Act
        create_prize_cuts_for_tournament(self.db, self.tournament, prize_pool)

        # Assert
        call_args_list = self.db.add.call_args_list
        first_prize = call_args_list[0][0][0]
        second_prize = call_args_list[1][0][0]

        self.assertEqual(first_prize.prize_cut, expected_first_place)
        self.assertEqual(second_prize.prize_cut, expected_second_place)

        self.assertEqual(first_prize.prize_cut + second_prize.prize_cut, prize_pool)

    def test_delete_prize_cuts_for_tournament_success(self):
        """Test deleting all prize cuts for a tournament."""
        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()
        self.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter

        # Act
        delete_prize_cuts_for_tournament(self.db, self.tournament)

        # Assert
        self.db.query.assert_called_once_with(PrizeCut)
        mock_query.filter.assert_called_once()
        mock_filter.delete.assert_called_once()

    def test_create_prize_cuts_verifies_proportions(self):
        """Test that prize cuts are correctly proportioned (70/30 split)."""
        # Arrange
        prize_pools_to_test = [10000, 25000, 75000, 999999]

        for prize_pool in prize_pools_to_test:
            with self.subTest(prize_pool=prize_pool):

                self.db.add.reset_mock()

                # Act
                create_prize_cuts_for_tournament(self.db, self.tournament, prize_pool)

                # Assert
                call_args_list = self.db.add.call_args_list
                first_prize = call_args_list[0][0][0]
                second_prize = call_args_list[1][0][0]

                actual_first_proportion = first_prize.prize_cut / prize_pool
                actual_second_proportion = second_prize.prize_cut / prize_pool

                self.assertAlmostEqual(actual_first_proportion, 0.7, places=2)
                self.assertAlmostEqual(actual_second_proportion, 0.3, places=2)
