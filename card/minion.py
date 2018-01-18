from .card import HealthCard, AttackCard, TYPES
from .effects import Effect


class Minion(HealthCard, AttackCard):
    def __init__(self, name, mana, hp=0, dmg=0, cclass=None, abilities={}):
        """
        mana: cost in mana (int)
        hp:   health points (int)
        dmg:  damage (int)
        abilities: effects that happen when something happens ((str,str))"""
        HealthCard.__init__(self, name, mana, TYPES.index('minion'), cclass)
        self.register_prop('tophp', hp)
        self.register_prop('hp', hp)
        self.register_prop('dmg', dmg)
        if abilities != {}:
            for i in abilities.keys():
                self.register_prop(i, Effect(abilities[i]))

    def play(self, player, target):
        self.summon(player, 'hand')
        if self.exists_prop('battlecry'):
            self.get_prop('battlecry').do_effect(self, player, target)

    def summon(self, player, from_where):
        board = player.board
        if from_where == 'hand':
            self.change_prop('in_hand', False)
        elif from_where == 'deck':
            self.change_prop('in_deck', False)
        self.change_prop('on_battlefield', True)
        self.register_prop('board', board)
        self.register_prop('player', player)
        player.battlefield['minions'].append(self)

    def copy(self):
        new_card = Minion(self.name,
                          self.cost,
                          TYPES.index(self.ctype),
                          self.cardclass)

        return self._copy(new_card)
