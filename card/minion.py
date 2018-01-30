from .card import HealthCard, AttackCard, TYPES
from .effects import make_effect


class Minion(HealthCard, AttackCard):
    def __init__(self, name, mana, hp=0, dmg=0, cclass=None, abilities=None):
        """
        mana: cost in mana (int)
        hp:   health points (int)
        dmg:  damage (int)
        abilities: effects that happen when something happens ((str,str))"""
        if abilities is None:
            abilities = {}
        HealthCard.__init__(self, name, mana, TYPES.index('minion'), cclass)
        self.register_prop('tophp', hp)
        self.register_prop('hp', hp)
        self.register_prop('dmg', dmg)
        for i in abilities.keys():
            self.register_prop(i, make_effect(abilities[i]))

    def play(self, player, target):
        self.summon(player, 'hand')
        if self.exists_prop('battlecry'):
            self.get_prop('battlecry').do_effect(self, player, target)

    def summon(self, player, from_where):
        board = player.board
        if from_where == 'hand':
            self.set_prop('in_hand', False)
        elif from_where == 'deck':
            self.set_prop('in_deck', False)
        self.set_prop('on_battlefield', True)
        self.register_prop('board', board)
        self.register_prop('player', player)
        player.add_minion(self)

    def copy(self):
        new_card = Minion(self.name,
                          self.cost,
                          TYPES.index(self.ctype),
                          self.cardclass)
        return self._copy(new_card)

    def die(self):
        if self.exists_prop('deathrattle'):
            self.get_prop('deathrattle').do_effect(
                self,
                self.get_prop('player').board,
                self.get_prop('player'))
        self.get_prop('player').kill_minion(self)

    @property
    def player(self):
        return self.get_prop('player')
