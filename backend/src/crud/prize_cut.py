from uuid import UUID

from src.models import PrizeCut


def create_prize_cuts_for_tournament(db, db_tournament, new_prize_pool: int) -> None:
    """
    Create prize cuts for a tournament.

    Args:
        db (Session): The database session.
        db_tournament (Tournament): The tournament object.
        new_prize_pool (int): The new prize pool amount.

    Returns:
        None
    """
    prize_cut1 = _create_prize_cut(1, round(0.7 * new_prize_pool), db_tournament.id)
    prize_cut2 = _create_prize_cut(2, round(0.3 * new_prize_pool), db_tournament.id)

    db.add(prize_cut1)
    db.add(prize_cut2)


def delete_prize_cuts_for_tournament(db, db_tournament) -> None:
    """
    Delete prize cuts for a tournament.

    Args:
        db (Session): The database session.
        db_tournament (Tournament): The tournament object.

    Returns:
        None
    """
    db.query(PrizeCut).filter(PrizeCut.tournament_id == db_tournament.id).delete()


def _create_prize_cut(place: int, prize_cut: float, tournament_id: UUID) -> PrizeCut:
    """
    Create a prize cut object.

    Args:
        place (int): The place of the prize cut.
        prize_cut (float): The amount of the prize cut.
        tournament_id (UUID): The ID of the tournament.

    Returns:
        PrizeCut: The prize cut object.
    """
    db_prize = PrizeCut(
        place=place, prize_cut=prize_cut, tournament_id=tournament_id, team_id=None
    )

    return db_prize
