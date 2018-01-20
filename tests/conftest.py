import pytest
import random


@pytest.fixture(scope='session')
def hero():
    from card.hero import Hero as Hero
    return Hero


@pytest.fixture(scope='session')
def player():
    from game.player import Player
    return Player


@pytest.fixture(scope='session')
def minion():
    from card.minion import Minion as Minion
    return Minion


@pytest.fixture(scope='session')
def spell():
    from card.spell import Spell as Spell
    return Spell


@pytest.fixture(scope='session')
def deck():
    from card.deck import Deck
    return Deck


@pytest.fixture(scope='session')
def hand():
    from card.deck import Hand
    return Hand


"""
@pytest.fixture(scope='session')
def error():
    from game.error import *
"""


@pytest.fixture(scope='session')
def board():
    from game.board import Board
    return Board


@pytest.fixture(scope='session')
def game():
    from game.game import Game
    return Game


@pytest.fixture(scope='session')
def eventqueue():
    from game.events import EventQueue
    return EventQueue


@pytest.fixture(scope='session')
def the_deck1():
    deck1 = {}
    for i in range(30):
        cname = 'card{0}'.format(str(i))
        deck1[cname] = {
            'type': random.randint(0, 1),
            'mana': random.randint(0, 10)
        }
        deck1[cname]['cclass'] = 0

        if deck1[cname]['type'] == 0:
            deck1[cname]['effect'] = '5_dmg'
        else:
            deck1[cname]['hp'] = random.randint(0, 10)
            deck1[cname]['dmg'] = random.randint(0, 10)
    return deck1


@pytest.fixture(scope='session')
def the_deck2():
    deck2 = {}
    for i in range(30):
        cname = 'card{0}'.format(str(i))
        deck2[cname] = {
            'type': random.randint(0, 1),
            'mana': i % 10
        }
        deck2[cname]['cclass'] = 1

        if deck2[cname]['type'] == 0:
            deck2[cname]['effect'] = '5_dmg'
        else:
            deck2[cname]['hp'] = random.randint(0, 10)
            deck2[cname]['dmg'] = random.randint(0, 10)

    return deck2
