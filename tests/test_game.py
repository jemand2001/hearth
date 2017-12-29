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
                           {'battlecry': '1_dmg_to_self'})

    p1.deck.put_card_on_index(special_card1, len(p1.deck))
    p1.begin_turn()
    p1.play_card(-1)
    p1.end_turn()
    assert special_card1 in p1.battlefield['minions']
    assert p1.battlefield['minions'][0] is special_card1
    assert special_card1.get_prop('hp') == 4


def round2_p2(Minion):
    special_card2 = Minion('Me too', 0, 5, 5, '*',
                           {'on_turn_start': '1_dmg_to_all',
                            'on_turn_end': '1_heal_to_all_friendly'})
    p2.deck.put_card_on_index(special_card2, len(p1.deck))
    p2.begin_turn()
    p2.play_card(-1)
    p1.end_turn()


def test_round2(minion):
    round2_p1(minion)
    round2_p2(minion)


def test_round3():
    p1.begin_turn()
    p1.end_turn()
    p2.begin_turn()
    assert p1.hero.get_prop('hp') == 29
    assert p2.hero.get_prop('hp') == 29
    for i in p1.battlefield['minions']:
        assert i.get_prop('hp') == 3
    for i in p2.battlefield['minions']:
        assert i.get_prop('hp') == 4
    p2.end_turn()
    assert p1.hero.get_prop('hp') == 29
    assert p2.hero.get_prop('hp') == 30
    for i in p2.battlefield['minions']:
        assert i.get_prop('hp') == 5


def round4_p1(Spell):
    special_card1 = Spell('special card', 0, '29_dmg_to_all_enemy_hero')
    p1.deck.put_card_on_index(special_card1, len(p1.deck))
    p1.begin_turn()
    p1.play_card(-1)
    p1.end_turn()
    assert p2.hero.get_prop('hp') == 1


def round4_p2(Spell):
    special_card2 = Spell('other special card',
                          3,
                          '-1_heal_to_all_friendly,1_dmg_to_all_enemy')
    p2.deck.put_card_on_index(special_card2, len(p1.deck))
    p2.begin_turn()
    p2.play_card(-1)
    p2.end_turn()
    assert p2.hero.get_prop('hp') == p2.hero.get_prop('tophp')
    assert p1.hero.get_prop('hp') == 28


def test_round4(spell):
    round4_p1(spell)
    round4_p2(spell)
