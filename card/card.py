from player import Player


TYPES = ('spell', 'creature', 'hero',)


class Card:
    def __init__(self, mana, cardtype, cardclass, **properties):
        """
        mana:       cost in mana      (int)
        cardtype:   type of the card  (int)
        properties: set of properties (e.g. hp, ...)
        """
        self.cost = mana
        self.ctype = TYPES[cardtype]
        self.cardclass = cardclass
        self.properties = properties

    def use(self, target):
        """target: target card (provided by GUI controller)"""
        pass

class Spell(Card):
    def __init__(self, mana, effect):
        """
        mana:   cost in mana (int)
        effect: spell effect (func, I guess)"""
        Card.__init__(self, mana, 0, effect=effect)

class Hero(Card):
    def __init__(self, mana=0, cardclass='', effect=None):
        """
        mana:   cost in mana (int)
        effect: spell effect (func, I guess)"""
        Card.__init__(self, mana, 0, effect=effect, )
