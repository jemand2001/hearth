from .card import Card, TYPES
from .effects import make_effect


class Spell(Card):
    def __init__(self, name, mana, effect, cclass='*'):
        """
        mana:   cost in mana (int)
        effect: spell effect (str)"""
        Card.__init__(self, name, mana, TYPES.index('spell'), cclass)
        self.register_prop('effect', make_effect(effect))

    def play(self, player, target):
        self.get_prop('effect').do_effect(self, player, target)
        self.set_prop('in_hand', False)
        self.set_prop('in_graveyard', True)

    def copy(self):
        new_card = Spell(self.name,
                         self.cost,
                         TYPES.index(self.ctype),
                         self.cardclass)
        return self._copy(new_card)
