import pytest


@pytest.fixture(scope='session')
def hero():
    from ..card.hero import Hero as Hero
    return Hero


@pytest.fixture(scope='session')
def player():
    from ..player.player import Player
    return Player


@pytest.fixture(scope='session')
def minion():
    from ..card.minion import Minion as Minion
    return Minion


@pytest.fixture(scope='session')
def spell():
    from ..card.spell import Spell as Spell
    return Spell


@pytest.fixture(scope='session')
def deck():
    from ..card.deck import Deck, Hand
    return Deck


@pytest.fixture(scope='session')
def error():
    from ..error import *


@pytest.fixture(scope='session')
def board():
    from ..board import Board
    return Board


@pytest.fixture(scope='session')
def game():
    from ..game import Game
    return Game
