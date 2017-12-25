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
        self.hand = Hand(self.deck)
        self.mana = self.actualmana = mana

        self.battlefield = {
            'hero': self.hero,
            'minions': []
        }

    def play_card(self, index, target='board'):
        c = self.hand[index]
        if c.mana < self.actualmana:
            c.play(self, target)
            self.actualmana -= c.mana
        else:
            raise ManaError('Not enough mana!')
