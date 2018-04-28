from .game import Game
from .events import *
from .board import *
from .default_deck import make_def_deck
from card.deck import *


def make_game(**contents):
    """contents: initial parameters of the game
    including game board state, hands, ... (any number of these)"""
    if 'eventqueue' in contents:
        event_q = contents['eventqueue']
    else:
        event_q = EventQueue()
    if 'player1' in contents:
        p1 = contents['player1']
        player1 = create_player(p1['pclass'], p1['deck'], event_q)
    else:
        pclass = randint(0, 1)
        deck = make_def_deck(pclass)
        player1 = create_player(pclass, deck, event_q)
    if 'player2' in contents:
        p2 = contents['player1']
        player2 = create_player(p2['pclass'], p2['deck'], event_q)
    else:
        pclass = randint(0, 1)
        deck = make_def_deck(pclass)
        player2 = create_player(pclass, deck, event_q)
    


def create_player(pclass, deck, eventqueue, hand=None):
    """creates a Player instance of that class, with that deck.""" 
    my_deck = create_deck(deck, pclass)
    p = Player(pclass, my_dack, eventqueue)
    if hand is not None:
        p.hand.hand = hand
    return p


def create_board(player1, player2, player1_side=None, player2_side=None):
    """creates a Board instance for these players"""
    b = Board(player1, player2)
    if player1_side is not None:
        player1.minions = player1_side[]
    return b
