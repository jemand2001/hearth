# #!/usr/bin/env python3
import random


random.seed(0)


def create_decks(Deck, deck1, deck2):
    global d1, d2
    d1 = Deck(0, deck1)
    d2 = Deck(1, deck2)


def test_create_decks(deck, the_deck1, the_deck2):
    create_decks(deck, the_deck1, the_deck2)
    # assert False, d1.deck


def create_event_queue(EventQueue):
    global the_events
    the_events = EventQueue


def test_event_queue(eventqueue):
    create_event_queue(eventqueue)


def create_players(Player, Board):
    global p1, p2, myboard
    p1 = Player(0, d1, the_events)
    p2 = Player(1, d2, the_events)
    myboard = Board(p1, p2)
    p1.board = myboard
    p2.board = myboard


def test_create_players(player, board):
    create_players(player, board)


def game_start_p1(Spell):
    special_card1 = Spell('I\'m special', 0, '10_dmg', '*')
    assert len(p1.deck) == 30
    p1.start_game()
    p1.deck.put_card_on_index(special_card1, len(p1.deck))
    p1.begin_turn()
    p1.play_card(-1, p2.hero)
    p1.end_turn()


def game_start_p2(Spell):
    special_card2 = Spell('I\'m special too', 0, '10_heal', '*')
    assert len(p2.deck) == 30
    p2.start_game(start=False)
    p2.deck.put_card_on_index(special_card2, len(p2.deck))
    p2.begin_turn()
    p2.play_card(-1, p2.hero)
    p1.end_turn()


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
    p2.end_turn()
    assert p2.battlefield['minions'][0].get_prop('on_turn_start').numtriggered == 0


def test_round2(minion):
    round2_p1(minion)
    round2_p2(minion)


def test_round3():
    p1.begin_turn()
    p1.end_turn()
    p2.begin_turn()
    assert p2.battlefield['minions'][0].get_prop('on_turn_start').numtriggered == 1
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
