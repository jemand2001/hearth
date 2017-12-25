#!/usr/bin/env python3
import random
from ..player.player import Player
from ..card.card import *
from ..card.deck import Deck, Hand


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
    global p1, p2
    p1 = Player(0, d1)
    p2 = Player(1, d2)


def test_create_players():
    create_players()


def test_game_start():
    special_card1 = Spell('I\'m special', 0, '10dmg', '*')

    # do 1 turn as p1
    p1.start_game()
    p1.deck.put_card_on_index(special_card1, len(p1.deck))
    p1.begin_turn()
    p1.play_card(-1, p2)
    # then 1 turn as p2
    p2.start_game(start=False)
