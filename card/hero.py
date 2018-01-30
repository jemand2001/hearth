from .card import HealthCard, AttackCard, TYPES
from .effects import make_effect


class Hero(HealthCard, AttackCard):
    def __init__(self, name, mana=0, cardclass='', hp=30, effect=''):
        """
        mana:   cost in mana (int)
        effect: spell effect (func, I guess)"""
        HealthCard.__init__(self, name, mana, TYPES.index('hero'), cardclass)
        self.register_prop('effect', make_effect(effect))
        self.register_prop('tophp', hp)
        self.register_prop('hp', hp)

    def play(self, board, player, target):
        # do effect...
        self.get_prop('effect').do_effect(self, board, player, target)

        player.battlefield['hero'] = self
        player.health = self.get_prop('hp')
        self.change_prop('in_hand', False)
        self.change_prop('in_battlefield', True)

    def copy(self):
        new_card = Hero(self.name,
                        self.cost,
                        TYPES.index(self.ctype),
                        self.cardclass)
        return self._copy(new_card)

    def die(self):
        raise NotImplementedError('The game should end now. '
                                  'This is not implemented!')
