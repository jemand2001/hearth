# #!/usr/bin/env python3
import random


random.seed(0)


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


def create_decks(Deck):
    global d1, d2
    d1 = Deck(0, deck1)
    d2 = Deck(1, deck2)


def test_create_decks(deck):
    create_decks(deck)


def create_players(Player, Board):
    global p1, p2, myboard
    p1 = Player(0, d1)
    p2 = Player(1, d2)
    myboard = Board(p1, p2)
    p1.board = myboard
    p2.board = myboard


def test_create_players(player, board):
    create_players(player, board)


def game_start_p1(Spell):
    special_card1 = Spell('I\'m special', 0, '10_dmg', '*')
    p1.start_game()
    p1.deck.put_card_on_index(special_card1, len(p1.deck))
    p1.begin_turn()
    p1.play_card(-1, p2.hero)


def game_start_p2(Spell):
    special_card2 = Spell('I\'m special too', 0, '10_heal', '*')
    p2.start_game(start=False)
    p2.deck.put_card_on_index(special_card2, len(p2.deck))
    p2.begin_turn()
    p2.play_card(-1, p2.hero)


def test_game_start(spell):
    # do 1 turn as p1
    game_start_p1(spell)

    # then 1 turn as p2
    game_start_p2(spell)


def round2_p1(Minion):
    special_card1 = Minion('I\'m also special', 0, 5, 5, '*',
                           (('battlecry', '1_dmg_to_self'),))

    p1.deck.put_card_on_index(special_card1, len(p1.deck))
    p1.begin_turn()
    p1.play_card(-1)
    # assert 0, special_card1.properties
    assert special_card1 in p1.battlefield['minions']
    assert p1.battlefield['minions'][0] is special_card1
    assert special_card1.get_prop('hp') == 4


def test_round2(minion):
    round2_p1(minion)
