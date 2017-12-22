from card import Hero


#CLASSES = ('warrior', 'mage')
CLASSES = {'warrior': Hero()}


class Player:
    def __init__(self, pclass):
        """pclass: class of the player (int)"""
        self.pclass = CLASSES.keys()[pclass]
        self.hero   = CLASSES[CLASSES.keys()[pclass]]
