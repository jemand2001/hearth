from card.deck import Deck
from random import randint


def make_def_deck(pclass):
    """generates a random deck for the class pclass"""
    d = {}
    for i in range(30):
        cname = 'card{0}'.format(str(i))
        d[cname] = {
            'type': randint(0, 1),
            'mana': i % 10
        }
        d[cname]['cclass'] = pclass
        if d[cname]['type'] == 0:
            d[cname]['effect'] = '5_dmg'
        else:
            d[cname]['hp'] = randint(0, 10)
            d[cname]['dmg'] = randint(0, 10)
    return Deck(pclass, d)
