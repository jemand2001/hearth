from .game import Game
from .events import *
from .board import *
from .default_deck import make_def_deck
from card.deck import *


def make_game(**contents):
    """contents: initial parameters of the game (dict)
    including game board state, hands, ... (any number of these)
    returns {
    'game': <Game instance>
    'players': [<Player player1>, <Player player2>]
    'queue': <EventQueue instance>
    }"""
    if 'eventqueue' in contents:
        event_q = contents['eventqueue']
    else:
        event_q = EventQueue()
    if 'player1' in contents:
        p1 = contents['player1']
        player1 = create_player(p1['pclass'], p1['deck'], event_q)
        player1_side = p1['minions']
    else:
        pclass = randint(0, 1)
        deck = make_def_deck(pclass)
        player1 = create_player(pclass, deck, event_q)
        player1_side = None
    if 'player2' in contents:
        p2 = contents['player1']
        player2 = create_player(p2['pclass'], p2['deck'], event_q)
        player2_side = p2['minions']
    else:
        pclass = randint(0, 1)
        deck = make_def_deck(pclass)
        player2 = create_player(pclass, deck, event_q)
        player2_side = None
    board = create_board(player1, player2, player1_side, player2_side)
    game = Game(player1, player2, board)
    return {
        'game': game,
        'players': [player1, player2],
        'queue': event_q
    }


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
    if player2_side is not None:
        player2.minions = player2_side[]
    return b
