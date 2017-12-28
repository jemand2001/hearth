from .card import Card, TYPES
from .effects import Effect


class Minion(Card):
    def __init__(self, name, mana, hp, dmg, cclass, abilities):
        """
        mana: cost in mana (int)
        hp:   health points (int)
        dmg:  damage (int)
        abilities: effects that happen when something happens (str=str)"""
        Card.__init__(self, name, mana, TYPES.index('minion'), cclass)
        self.register_prop('tophp', hp)
        self.register_prop('hp', hp)
        self.register_prop('dmg', dmg)
        if abilities != ():
            for i in abilities:
                self.register_prop(i[0], Effect(i[1]))

    def attack(self, target):
        if self.getprop('dmg') == 0:
            raise ValueError('this minion can\'t attack!')
        if 'on_attack' in self.properties.keys():
            print('wah!')

    def play(self, board, player, target):
        self.summon(board, player, 'hand')
        if ('battlecry' in self.properties.keys() and (
                self.get_prop('in_hand') is True)):
            print('WAAAH!')

    def summon(self, board, player, from_where):
        if from_where == 'hand':
            self.change_prop('in_hand', False)
        elif from_where == 'deck':
            self.change_prop('in_deck', False)
        self.change_prop('on_battlefield', True)
        self.register_prop('board', board)
        self.register_prop('player', player)
        player.battlefield['minions'].append(self)

    def get_damaged(self, amount):
        self.change_prop('hp', -amount)
        if self.exists_prop('on_dmg'):
            # V This call is incomplete!
            self.get_prop('on_dmg').do_effect(self.ctype,
                                              self.get_prop('board'),
                                              self.get_prop('player'))
        if self.get_prop('hp') <= 0:
            self.die()

    def get_healed(self, amount):
        self.change_prop('hp', amount)
        if self.get_prop('hp') > self.get_prop('tophp'):
            self.set_prop('hp', self.get_prop('tophp'))

    def die(self):
        if self.exists_prop('deathrattle'):
            self.get_prop('deathrattle').do_effect(self.ctype,
                                                   self.board,
                                                   self.get_prop('player'))
