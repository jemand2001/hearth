from .card import HealthCard, AttackCard
from game.data import TYPES
from .effects import make_effect
import pdb


class Hero(HealthCard, AttackCard):
    def __init__(self, name, mana=0, cardclass='', hp=30, effect=''):
        """
        mana:   cost in mana (int)
        effect: spell effect (func, I guess)"""
        ctype = TYPES.index('hero')
        assert type(ctype) == int, ctype
        #pdb.set_trace()
        HealthCard.__init__(self, name, mana, hp,
                            ctype, cardclass)
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
        self.register_player(player)

    def register_player(self, player):
        """register the player the hero belongs to."""
        self.player = player

    def copy(self):
        new_card = Hero(self.name,
                        self.cost,
                        self.cardclass)
        return self._copy(new_card)

    def die(self):
        raise NotImplementedError('The game should end now. '
                                  'This is not implemented!')
