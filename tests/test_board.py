from ..board import Board
from ..player import *


def test_create_players():
    """should be in a test_player.py, but also fits here."""
    global p1, p2
    p1 = Player(0)
    p2 = Player(1)
    
def test_start_game():
    global b
    b = Board(p1, p2)
