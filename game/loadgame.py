from .game import Game
from .events import *
from .board import *
from .default_deck import make_def_deck
from .data import CLASSES
from .player import Player
from card.deck import *
from random import randint


def make_game(contents=None):
    """contents: initial parameters of the game (dict)
    including game board state, hands, ... (any number of these)
    format:
    {
    'player1': {'minions': [...], 'pclass': n,
    \t'deck': [...], 'hero': {attributes}},
    ...
    }
    returns: {
    'game': <Game instance>
    'players': [<Player player1>, <Player player2>]
    'queue': <EventQueue instance>
    }"""
    #assert False, contents
    if contents is None:
        contents = {}
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
        p2 = contents['player2']
        player2 = create_player(p2['pclass'], p2['deck'], event_q)
        player2_side = p2['minions']
        assert player2_side != []
    else:
        pclass = randint(0, 1)
        deck = make_def_deck(pclass)
        player2 = create_player(pclass, deck, event_q)
        player2_side = None
    board = create_board(player1, player2, player1_side, player2_side)
    game = Game(player1, player2, board)
    return {
        'game': game,
        'players': (player1, player2),
        'queue': event_q,
        'board': board
    }


def create_player(pclass, deck, eventqueue, hand=None, hero=None):
    """creates a Player instance of that class, with that deck."""
    if hero is None:
        hero = CLASSES[CLASSES.keys()[pclass]]
    else:
        hero = make_hero(pclass, hero['name'], hero['maxhp'], hero['hp'])
    p = Player(pclass, deck, eventqueue)
    if hand is not None:
        p.hand.hand = hand
    return p


def create_board(player1, player2, player1_side=None, player2_side=None):
    """creates a Board instance for these players"""
    b = Board(player1, player2)
    if player1_side is not None:
        the_side = []
        for i in player1_side:
            if isinstance(i, Minion):
                the_side.append(i)
            elif isinstance(i, dict):
                the_side.append(make_minion_from_dict(i))
        player1.minions = the_side
    if player2_side is not None:
        the_side = []
        for i in player2_side:
            if isinstance(i, Minion):
                the_side.append(i)
            elif isinstance(i, dict):
                the_side.append(make_minion_from_dict(i))
        player2.minions = the_side
    return b


def make_hero(pclass, name, maxhp, hp=None):
    h = Hero(name=name, hp=maxhp)
    if hp is not None:
        h.setprop('hp', hp)


def make_spell(cclass, name, mana, hp, effect):
    return Spell(name, mana, effect, cclass)


def make_minion(name,
                mana,
                maxhp=1,
                hp=None,
                dmg=0,
                cclass=None,
                abilities=None,
                source='deck'):
    new_minion = Minion(name,
                        mana,
                        maxhp,
                        dmg,
                        cclass,
                        abilities,
                        source)
    if hp is not None:
        new_minion.set_prop('hp', hp)
    return new_minion


def make_minion_from_dict(attributes):
    name = attributes['name']
    mana = attributes['cost']
    maxhp = attributes['maxhp']
    try:
        cclass = attributes['cclass']
    except KeyError:
        cclass = None
    try:
        hp = attributes['hp']
    except KeyError:
        hp = maxhp
    dmg = attributes['dmg']
    try:
        abilities = attributes['abilities']
    except KeyError:
        abilities = None
    try:
        source = attributes['source']
    except KeyError:
        source = 'limbo'
    return make_minion(name,
                       mana,
                       maxhp,
                       hp,
                       dmg,
                       cclass,
                       abilities,
                       source)
