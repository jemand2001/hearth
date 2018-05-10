from game.loadgame import make_game
from game.game import Game
from game.player import Player
from game.events import *
from card.deck import *
from game.board import *


def test_load_game_1():
    the_game = make_game()
    assert isinstance(the_game['game'], Game)
    assert isinstance(the_game['players'], list)
    assert isinstance(the_game['players'][0], Player)
    assert isinstance(the_game['players'][1], Player)
    assert isinstance(the_game['queue'], EventQueue)
    assert isinstance(the_game['board'], Board)


def test_load_game_2():
    game_state = {
        'player1': {
            'minions': [],
            'pclass': 0,
            'deck': [Spell('CRAZY!', 0, '10_dmg'),],
            'hero': {'pclass': 1, 'name': 'WUT', 'maxhp': 200, 'hp': 5}
        },
        'player2': {
            'minions': [Minion('Blah', 1, 10, 0)],
            'pclass': 1,
            'deck': []
        }
    }
    the_game = make_game(game_state)
    player1, player2 = the_game['players']
    #print(player2.battlefield)
    assert player2.minions != []

def test_load_game_dict():
    game_state = {
        'player1': {
            'minions': [],
            'pclass': 0,
            'deck': {'CRAZY!': {'type': 0, 'mana':0, 'effect': '10_dmg', 'cclass': '*'}},
            'hero': {'pclass': 1, 'name': 'WUT', 'maxhp': 200, 'hp': 5}
        },
        'player2': {
            'minions': [
                {
                    'type': 1,
                    'name': 'Blah',
                    'cost':1,
                    'hp': 10,
                    'maxhp':10,
                    'dmg': 0,
                    'cclass': '*'
                }
            ],
            'pclass': 1,
            'deck': []
        }
    }
    the_game = make_game(game_state)
    player1, player2 = the_game['players']
    #print(player2.battlefield)
    assert player2.minions != []
