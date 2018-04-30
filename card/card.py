TYPES = ('spell', 'minion', 'hero',)


class Card:
    def __init__(self, name, mana, cardtype, cardclass, source='deck'):
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
        self.register_prop('in_deck', False)
        self.register_prop('in_hand', False)
        self.register_prop('in_graveyard', False)
        if source == 'deck':
            self.set_prop('in_deck', True)
        elif source == 'hand':
            self.set_prop('in_hand', True)
        self.register_prop('source', source)

    def register_prop(self, name, default):
        self.properties[name] = default

    def set_prop(self, name, value):
        if name in self.properties.keys():
            self.properties[name] = value
        else:
            raise KeyError('"%s" is not an existing property' % name)

    def change_prop(self, name, amount):
        # assert False, amount
        if not isinstance(self.get_prop(name), (int, float, long)):
            raise TypeError('prop %s can not be added to' % name)
        self.properties[name] += amount
        print('Changing property \"%s\" of %s (new value: %s)'
              % (name, str(self), self.get_prop(name)))

    def get_prop(self, name):
        return self.properties[name]

    def exists_prop(self, name):
        return name in self.properties

    def _copy(self, new_card):
        for i in self.properties:
            new_card.register_prop(i, self.get_prop(i))
        return new_card


class PermanentCard(Card):
    def __init__(self, name, mana, cardtype, cardclass, source='deck'):
        Card.__init__(self, name, mana, cardtype, cardclass, source)
        self.register_prop('on_battlefield', False)


class HealthCard(PermanentCard):
    def get_damaged(self, amount):
        print('damaging %s by %d' % (str(self), amount))
        self.change_prop('hp', -amount)
        if self.exists_prop('on_dmg'):
            # V This call is incomplete!
            self.get_prop('on_dmg').do_effect(self,
                                              self.get_prop('player'))
        if self.get_prop('hp') <= 0:
            self.die()

    def get_healed(self, amount):
        print('healing %s by %d' % (str(self), amount))
        self.change_prop('hp', amount)
        if self.get_prop('hp') > self.get_prop('tophp'):
            self.set_prop('hp', self.get_prop('tophp'))

    def set_hp(self, hp):
        self.set_prop('hp', hp)


class AttackCard(PermanentCard):
    def attack(self, target):
        if self.get_prop('dmg') == 0:
            raise ValueError('this minion can\'t attack!')
        if self.exists_prop('on_attack'):
            # print('wah!')
            self.get_prop('on_attack').do_effect(
                self,
                self.get_prop('player'))

        target.get_damaged(self.get_prop('dmg'))
