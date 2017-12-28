from .card import Card, TYPES
from .effects import Effect


class Spell(Card):
    def __init__(self, name, mana, effect, cclass):
        """
        mana:   cost in mana (int)
        effect: spell effect (str)"""
        Card.__init__(self, name, mana, TYPES.index('spell'), cclass)
        self.register_prop('effect', Effect(effect))

    def play(self, board, player, target):
        # TODO: need to add a register of effects and how they work
        self.get_prop('effect').do_effect(self.ctype, board, player, target)
        self.change_prop('in_hand', False)
        self.change_prop('in_graveyard', True)
