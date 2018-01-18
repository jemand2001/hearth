from .testpygame import mouse


def test_getmouse():
    assert mouse.get_pos() == (0, 0)
