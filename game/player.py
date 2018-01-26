# from card.hero import Hero
from card.deck import Deck, Hand
from .data import CLASSES as c
from .error import ManaError, TimeError


class Player:
    def __init__(self, pclass, deck, events, mana=0):
        """pclass: class of the player (int)
        deck: the deck of the player
        events: the global EventQueue
        mana: the amount of mana the player starts with"""
        # super(self).__init__()
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
        self.board = None
        self.eventqueue = events
        self.on = False
        # print self.deck.deck

    def play_card(self, index, target='board'):
        if not self.on:
            raise TimeError('Tried to play a card outside own turn!')
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
        if self.on is True:
            raise TimeError('Turn started during own turn!')
        self.on = True
        # on_start_of_turn effects
        self.do_effect_on_trigger('on_turn_start')
        self.mana = min((self.mana+1, 10))
        self.actualmana = self.mana
        self.hand.draw(1)

    def end_turn(self):
        if not self.on:
            raise TimeError('Turn ended outside own turn!')
        self.on = False
        self.do_effect_on_trigger('on_turn_end')

    def collect_by_attribute(self, attribute):
        res = []
        for i in self.battlefield['minions']:
            if i.exists_prop(attribute):
                res.append(i)
        return res

    def do_effect_on_trigger(self, trigger):
        items = self.collect_by_attribute(trigger)
        for i in items:
            effect = i.get_prop(trigger)
            effect.do_effect(i, self)

    def register_board(self, board):
        """board: global board instance.
        NOTE: only use once
        (in hearthstone.game.board.Board.__init__ or
        hearthstone.game.game.Game.__init__)!"""
        self.board = board
        self.get_enemy = self.board.get_enemy

    @property
    def battlefield_list(self):
        temp_bf = self.battlefield['minions'][:]
        temp_bf.append(self.hero)
        return tuple(temp_bf)

    # battlefield_list = property(_get_battlefield)
