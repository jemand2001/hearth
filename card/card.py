# from ..data import CLASSES
from .effects import Effect


TYPES = ('spell', 'minion', 'hero',)


class Card:
    def __init__(self, name, mana, cardtype, cardclass):
        """
        mana:       cost in mana      (int)
        cardtype:   type of the card  (int)
        """
        # self.board = board
        self.name = name
        self.cost = mana
        self.ctype = TYPES[cardtype]
        self.cardclass = cardclass
        self.properties = {}

    def register_prop(self, name, value):
        self.properties[name] = value

    def set_prop(self, name, value):
        if name in self.properties.keys():
            self.properties[name] = value
        else:
            raise KeyError('"%s" is not a valid property' % name)

    def change_prop(self, name, amount):
        if (not (isinstance(self.get_prop(name), int)
                 or isinstance(self.get_prop(name), float))):
            raise TypeError('prop %s can not be added to' % name)
        self.properties[name] += amount

    def get_prop(self, name):
        return self.properties[name]

    def exists_prop(self, name):
        return name in self.properties.keys()

    def use(self, board, player, target):
        """target: target card (provided by GUI//mouse controller)"""
        self.play(board, player, target)

    def copy(self):
        new_card = Card(self.name,
                        self.cost,
                        TYPES.index(self.ctype),
                        self.cardclass)
        for i in self.properties.keys():
            new_card.register_prop(i, self.get_prop(i))
        return new_card


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
