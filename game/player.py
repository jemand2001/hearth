from card.hero import Hero
from card.deck import Deck, Hand
from .data import CLASSES as c
from .error import ManaError, TimeError


class Player:
    def __init__(self, pclass, deck, mana=0):
        """pclass: class of the player (int)"""
        self.pclass = list(c.keys())[pclass]
        self.hero = c[list(c.keys())[pclass]][0].copy()
        if isinstance(deck, Deck):
            self.deck = deck
        else:
            self.deck = Deck(pclass, deck)
        self.mana = self.actualmana = mana
        self.spellpower = 0

        self.battlefield = {
            'hero': self.hero,
            'minions': []
        }

    def play_card(self, index, target='board'):
        if not self.on:
            raise TimeError('Tried to play a card outside own turn!')
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
        self.on = True
        for i in self.collect_by_trigger('on_turn_start'):
            effect = i.get_prop('on_turn_start')
            effect.do_effect(i,
                             self.board,
                             self)
        self.mana = min((self.mana+1, 10))
        self.actualmana = self.mana
        self.hand.draw()

    def end_turn(self):
        self.on = False
        for i in self.collect_by_trigger('on_turn_end'):
            effect = i.get_prop('on_turn_end')
            effect.do_effect(i,
                             self.board,
                             self)

    def collect_by_trigger(self, trigger):
        res = []
        for i in self.battlefield['minions']:
            if i.exists_prop(trigger):
                res.append(i)
        return res
