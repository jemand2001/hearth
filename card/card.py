# from ..data import CLASSES
# from .effects import Effect


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
