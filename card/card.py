# from ..data import CLASSES


TYPES = ('spell', 'minion', 'hero',)


class Card:
    def __init__(self, name, mana, cardtype, cardclass):
        """
        mana:       cost in mana      (int)
        cardtype:   type of the card  (int)
        """
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

    def use(self, player, target):
        """target: target card (provided by GUI//mouse controller)"""
        self.play(player, target)


class Minion(Card):
    def __init__(self, name, mana, hp, dmg, cclass, abilities):
        """
        mana: cost in mana (int)
        hp:   health points (int)
        dmg:  damage (int)
        abilities: effects that happen when something happens (str=str)"""
        Card.__init__(self, name, mana, TYPES.index('minion'), cclass)
        self.register_prop('hp', hp)
        self.register_prop('dmg', dmg)
        if abilities != ():
            for i in abilities:
                self.register_prop(i[0], i[1])

    def attack(self, target):
        if self.getprop('dmg') == 0:
            raise ValueError('this minion can\'t attack!')
        if 'on_attack' in self.properties.keys():
            print('wah!')

    def play(self, player, target):
        if ('battlecry' in self.properties.keys() and (
                self.get_prop('in_hand') is True)):
            print('WAAAH!')

        self.summon(player, 'hand')

    def summon(self, player, from_where):
        if from_where == 'hand':
            self.change_prop('in_hand', False)
        elif from_where == 'deck':
            self.change_prop('in_deck', False)
        self.change_prop('on_battlefield', True)
        player.battlefield['minions'].append(self)


class Spell(Card):
    def __init__(self, name, mana, effect, cclass):
        """
        mana:   cost in mana (int)
        effect: spell effect (str)"""
        Card.__init__(self, name, mana, TYPES.index('spell'), cclass)
        self.register_prop('effect', effect)

    def play(self, player, target):
        # TODO: need to add a register of effects and how they work
        self.change_prop('in_hand', False)
        self.change_prop('in_graveyard', True)


class Hero(Card):
    def __init__(self, name, mana=0, cardclass='', hp=30, effect=None):
        """
        mana:   cost in mana (int)
        effect: spell effect (func, I guess)"""
        Card.__init__(self, name, mana, TYPES.index('hero'), cardclass)
        self.register_prop('effect', None)
        self.register_prop('hp', hp)

    def play(self, player, target):
        # do effect...

        player.battlefield['hero'] = self
        player.health = self.get_prop('hp')
        self.change_prop('in_hand', False)
        self.change_prop('in_battlefield', True)
