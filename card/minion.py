from .card import HealthCard, AttackCard, TYPES
from .effects import make_effect


class Minion(HealthCard, AttackCard):
    def __init__(self,
                 name,
                 mana,
                 hp=1,
                 dmg=0,
                 cclass=None,
                 abilities=None,
                 source='deck'):
        """
        mana:   cost in mana (int)
        hp:     health points (int)
        dmg:    damage (int)
        cclass: the class the minion belongs to (str)
        abilities: effects that happen when something happens ((str,str))"""
        if cclass is None:
            cclass = '*'
        if abilities is None:
            abilities = {}
        HealthCard.__init__(self, name, mana, hp,
                            TYPES.index('minion'), cclass, source)
        self.register_prop('dmg', dmg)

    def play(self, player, target):
        self.summon(player, 'hand')
        if self.exists_prop('battlecry'):
            self.get_prop('battlecry').do_effect(self, player, target)

    def summon(self, player, from_where):
        self.set_prop('in_hand', False)
        self.set_prop('in_deck', False)
        self.set_prop('on_battlefield', True)
        self.register_prop('board', player.board)
        self.register_player(player)
        player.add_minion(self)

    def register_player(self, player):
        """register this minion's player"""
        self.player = player

    def copy(self):
        new_card = Minion(self.name,
                          self.cost,
                          cclass=self.cardclass)
        return self._copy(new_card)

    def die(self):
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
        self.set_prop('player', value)

    @property
    def deconst(self):
        res = self._deconst
        return res
