from ..card import *


def test_createcard():
    global c, d
    c = Card(5, 0, hp=10, abilities=(('on_turn_end', 'destroy_all')))
    d = Card(0,0)

def test_use():
    c.use(d)
