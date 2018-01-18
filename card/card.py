TYPES = ('spell', 'minion', 'hero',)


class Card:
    def __init__(self, name, mana, cardtype, cardclass):
        """
        name:     name of the card (str)
        mana:     cost in mana     (int)
        cardtype: type of the card (int)
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

    def _copy(self, new_card):
        for i in self.properties:
            new_card.register_prop(i, self.get_prop(i))
        return new_card

class HealthCard(Card):
    def get_damaged(self, amount):
        self.change_prop('hp', -amount)
        if self.exists_prop('on_dmg'):
            # V This call is incomplete!
            self.get_prop('on_dmg').do_effect(self,
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
            self.get_prop('deathrattle').do_effect(
                self,
                self.get_prop('player').board,
                self.get_prop('player'))

class AttackCard(Card):
    def attack(self, target):
        if self.get_prop('dmg') == 0:
            raise ValueError('this minion can\'t attack!')
        if self.exists_prop('on_attack'):
            # print('wah!')
            self.get_prop('on_attack').do_effect(
                self,
                self.get_prop('player').board,
                self.get_prop('player'))

        target.get_damaged(self.get_prop('dmg'))
