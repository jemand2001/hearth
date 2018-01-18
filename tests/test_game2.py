import random


random.seed(0)


def create_game(Game, deck1, deck2):
    global mygame
    p1 = {'name': 'some guy',
          'class': 1,
          'deck': deck1}

    p2 = {'name': 'some dude',
          'class': 0,
          'deck': deck2}

    mygame = Game(p1, p2)
    mygame.start()


def test_create_game(game, the_deck1, the_deck2):
    create_game(game, the_deck1, the_deck2)
