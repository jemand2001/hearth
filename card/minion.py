from .card import HealthCard, AttackCard
from . import TYPES
from game.error import PermissionError


class Minion(HealthCard, AttackCard):
    def __init__(self,
                 name,
                 mana,
                 hp=1,
                 dmg=0,
                 cklass=None,
                 abilities=None,
                 source='deck'):
        """
        mana:   cost in mana (int)
        hp:     health points (int)
        dmg:    damage (int)
        cclass: the class the minion belongs to (str)
        abilities: effects that happen when something happens ((str,str))"""
        if cklass is None:
            cklass = '*'
        HealthCard.__init__(self, name, mana, hp,
                            TYPES.index('minion'), cklass, abilities, source)
        self.register_prop('dmg', dmg)
        self.reason_died = None

    def play(self, player, target):
        self.summon(player, 'hand')
        if self.exists_prop('battlecry'):
            self.get_prop('battlecry').do_effect(self, player, target)

    def summon(self, player, from_where):
        self.set_prop('in_hand', False)
        self.set_prop('in_deck', False)
        self.set_prop('on_battlefield', True)
        self.register_prop('board', player.board)
        self.register_prop('source', from_where)
        self.register_player(player)
        player.add_minion(self)

    def register_player(self, player):
        """register this minion's player"""
        self.player = player

    def copy(self):
        new_card = Minion(self.name,
                          self.cost,
                          cklass=self.klass)
        return self._copy(new_card)

    def die(self, reason):
        self.reason_died = reason
        if self.exists_prop('deathrattle'):
            self.get_prop('deathrattle').do_effect(
                self,
                self.player.board,
                self.player)
        self.player.kill_minion(self)

    @property
    def player(self):
        return self.get_prop('player')

    @player.setter
    def player(self, value):
        if not self.exists_prop('player'):
            self.set_prop('player', value)
        else:
            raise PermissionError('Tried changing owner?')
