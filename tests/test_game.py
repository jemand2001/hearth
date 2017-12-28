#!/usr/bin/env python3
import random
from ..player.player import Player
from ..card.hero import *
from ..card.minion import *
from ..card.spell import *
from ..card.deck import Deck, Hand
from ..error import *
from ..board import Board


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


def create_decks():
    global d1, d2
    d1 = Deck(0, deck1)
    d2 = Deck(1, deck2)


def test_create_decks():
    create_decks()


def create_players():
    global p1, p2, myboard
    p1 = Player(0, d1)
    p2 = Player(1, d2)
    myboard = Board(p1, p2)


def test_create_players():
    create_players()


def test_game_start():
    special_card1 = Spell('I\'m special', 0, '10_dmg', '*')
    special_card2 = Spell('I\'m special too', 0, '10_heal', '*')

    # do 1 turn as p1
    p1.start_game()
    p1.deck.put_card_on_index(special_card1, len(p1.deck))
    p1.begin_turn()
    p1.play_card(myboard, -1, p2.hero)

    # then 1 turn as p2
    p2.start_game(start=False)
    p2.deck.put_card_on_index(special_card2, len(p2.deck))
    p2.begin_turn()
    p2.play_card(myboard, -1, p2.hero)
    if p2.hero.get_prop('hp') != 30:
        raise Error('')