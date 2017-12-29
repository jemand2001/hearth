from ..card.hero import Hero
from ..card.deck import Deck, Hand
from ..data import CLASSES
from ..error import ManaError


c = {}
for i in CLASSES.keys():
    c[i] = CLASSES[i]


class Player:
    def __init__(self, pclass, deck, hp=None, mana=0):
        """pclass: class of the player (int)"""
        if hp is None:
            self.health = c[list(c.keys())[pclass]][1]

        self.pclass = list(c.keys())[pclass]
        self.hero = c[list(c.keys())[pclass]][0]
        self.deck = deck
        self.mana = self.actualmana = mana
        self.spellpower = 0

        self.battlefield = {
            'hero': self.hero,
            'minions': []
        }

    def play_card(self, index, target='board'):
        c = self.hand[index]
        if c.cost <= self.actualmana:
            c.play(self.board, self, target)
            self.actualmana -= c.cost
        else:
            raise ManaError('Not enough mana(%i < %i)!' % (c.cost,
                                                           self.actualmana))

    def start_game(self, start=True):
        if start:
            self.hand = Hand(self.deck)
        else:
            self.hand = Hand(self.deck, 4)

    def begin_turn(self):
        # on_start_of_turn effects
        for i in self.battlefield['minions']:
            if i.exists_prop('on_turn_start'):
                effect = i.get_prop('on_turn_start')
                i.get_prop('on_turn_start').do_effect(i.ctype,
                                                      self.board,
                                                      self)

        self.mana = min((self.mana+1, 10))
        self.actualmana = self.mana
        self.hand.draw()
