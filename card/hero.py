from .card import Card, TYPES
from .effects import Effect


class Hero(Card):
    def __init__(self, name, mana=0, cardclass='', hp=30, effect=''):
        """
        mana:   cost in mana (int)
        effect: spell effect (func, I guess)"""
        Card.__init__(self, name, mana, TYPES.index('hero'), cardclass)
        self.register_prop('effect', Effect(effect))
        self.register_prop('tophp', hp)
        self.register_prop('hp', hp)

    def play(self, board, player, target):
        # do effect...
        self.get_prop('effect').do_effect(board, player, target)
        player.battlefield['hero'] = self
        player.health = self.get_prop('hp')
        self.change_prop('in_hand', False)
        self.change_prop('in_battlefield', True)

    def get_damaged(self, amount):
        self.change_prop('hp', -amount)
        if self.get_prop('hp') <= 0:
            self.die()

    def get_healed(self, amount):
        self.change_prop('hp', amount)
        if self.get_prop('hp') > self.get_prop('tophp'):
            self.set_prop('hp', self.get_prop('tophp'))

    def die(self):
        # TODO: The game should end here. I need to implement this!
        pass
