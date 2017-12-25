from ..card.card import Hero
from ..card.deck import Deck, Hand
from ..data import CLASSES
from ..error import ManaError


class Player:
    def __init__(self, pclass, deck, hp=None, mana=0):
        """pclass: class of the player (int)"""
        if hp is None:
            self.health = CLASSES[list(CLASSES.keys())[pclass]][1]

        self.pclass = list(CLASSES.keys())[pclass]
        self.hero = CLASSES[list(CLASSES.keys())[pclass]][0]
        self.deck = deck
        self.mana = self.actualmana = mana

        self.battlefield = {
            'hero': self.hero,
            'minions': []
        }

    def play_card(self, index, target='board'):
        c = self.hand[index]
        if c.cost <= self.actualmana:
            c.play(self, target)
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
                # do effect(effect)?
                print('TURN HAS STARTED!')

        self.mana += 1
        self.hand.draw()
