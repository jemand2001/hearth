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
    p1.register_board(myboard)
    p2.register_board(myboard)


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
    assert p2.hero.get_prop('hp') == 20


def game_start_p2(Spell):
    special_card2 = Spell('I\'m special too', 0, '10_heal', '*')
    assert len(p2.deck) == 30
    p2.start_game(start=False)
    p2.deck.put_card_on_index(special_card2, len(p2.deck))
    p2.begin_turn()
    p2.play_card(-1, p2.hero)
    p2.end_turn()
    assert p2.hero.get_prop('hp') == 30


def test_game_start(spell):
    # do 1 turn as p1
    game_start_p1(spell)

    # then 1 turn as p2
    game_start_p2(spell)


def turn2_p1(Minion):
    special_card1 = Minion('I\'m also special', 0, 5, 5, '*',
                           {'battlecry': '1_dmg_to_self'})

    p1.deck.put_card_on_index(special_card1, len(p1.deck))
    p1.begin_turn()
    p1.play_card(-1)
    p1.end_turn()
    assert special_card1 in p1.battlefield['minions']
    assert p1.battlefield['minions'][0] is special_card1
    assert special_card1.get_prop('hp') == 4


def turn2_p2(Minion):
    special_card2 = Minion('Me too', 0, 5, 5, '*',
                           {'on_turn_start': '1_dmg_to_all',
                            'on_turn_end': '1_heal_to_all_friendly'})
    p2.deck.put_card_on_index(special_card2, len(p1.deck))
    p2.begin_turn()
    p2.play_card(-1)
    p2.end_turn()
    assert p2.battlefield['minions'][0].get_prop('on_turn_start').numtriggered == 0
    # assert 


def test_turn2(minion):
    turn2_p1(minion)
    turn2_p2(minion)
    assert p1.hero.get_prop('hp') == p2.hero.get_prop('hp') == 30
    assert not p2.on
    assert not p1.on


def turn3(hero):
    p1.begin_turn()
    p1.end_turn()
    p2.begin_turn()
    m1 = p2.battlefield['minions'][0]
    e1 = m1.get_prop('on_turn_start')
    assert e1.numtriggered == 1
    targets = e1._select_target(m1, p2, 'myboard')
    bf = myboard.battlefield
    assert targets == bf
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


def test_turn3(hero):
    turn3(hero)


def turn4_p1(Spell):
    special_card1 = Spell('special card', 0, '29_dmg_to_all_enemy_hero')
    special_card2 = Spell('another one!', 0, '1_heal_to_all_enemy')
    p1.deck.put_card_on_index(special_card1, len(p1.deck))
    p1.deck.put_card_on_index(special_card2, len(p1.deck) - 1)
    p1.begin_turn()
    p1.play_card(-1)
    p1.hand.draw()
    p1.play_card(-1)
    p1.end_turn()
    assert p2.hero.get_prop('hp') == 2


def turn4_p2(Spell):
    special_card2 = Spell('other special card',
                          3,
                          '-1_heal_to_all_friendly,1_dmg_to_all_enemy')
    assert special_card2.get_prop('effect').effect[0].effect['amount'] == 99999999
    p2.deck.put_card_on_index(special_card2, len(p1.deck))
    p2.begin_turn()
    assert p2.hand[-1] is special_card2
    p2.play_card(-1)
    p2.end_turn()
    assert p2.hero.get_prop('hp') == p2.hero.get_prop('tophp')
    assert p1.hero.get_prop('hp') == 28


def test_turn4(spell):
    turn4_p1(spell)
    turn4_p2(spell)


def turn5_p1(Spell):
    special_card1 = Spell('special card numero 1 bgzhillion',
                          0,
                          'changeside')
    the_minion = p2.minions[0]
    p1.deck.put_card_on_index(special_card1, len(p1.deck))
    p1.begin_turn()
    p1.play_card(-1, the_minion)
    p1.end_turn()
    assert p1.minions[-1] is the_minion


def turn5_p2(Minion):
    special_card2 = Minion('I\'m BADASS',
                           mana=5,
                           hp=10,
                           dmg=0,
                           abilities={'on_turn_end': 'changeside_of_self'})
    p2.deck.put_card_on_index(special_card2, len(p1.deck))
    p2.begin_turn()
    p2.play_card(-1)
    p2.end_turn()
    assert p1.minions[-1] is special_card2


def test_turn5(spell, minion):
    turn5_p1(spell)
    turn5_p2(minion)
    for i in myboard.minions:
        assert type(i.get_prop('hp')) == int


def turn6_p1(Spell, Minion):
    special_card1 = Spell('Summoning Great things!',
                          5,
                          effect="summon_Great things_5_100_0_*_{}")
    greatthing = Minion('Great things', 5, 100, 0)
    e = special_card1.get_prop('effect')
    m = e.effect['minion']
    assert m.name == 'Great things'
    assert m.properties == greatthing.properties
    p1.deck.put_card_on_index(special_card1, len(p1.deck))
    p1.begin_turn()
    assert p1.hand[-1] is special_card1
    p1.play_card(-1)
    assert e.numtriggered == 1
    assert m.get_prop('on_battlefield')
    bfnames = []
    for i in myboard.minions:
        bfnames.append(i.name)
    assert p1.minions[-1] is m, (bfnames)
    p1.end_turn()
    assert p2.minions[-1] is special_card2


def turn6_p2(Spell):
    special_card2 = Spell('Destroy something!',
                          0,
                          effect='destroy')
    p2.deck.put_card_on_index(special_card2, len(p1.deck))
    p2.begin_turn()
    p2.play_card(-1)
    p2.end_turn()
    assert p1.minions[-1] is special_card2


def test_turn6(spell, minion):
    turn6_p1(spell, minion)
    turn6_p2(spell)
