from card.effects import make_effect


def test_create_effect():
    e = 'if hp = 10: 10_dmg_to_self'
    my_effect = make_effect(e)
    assert my_effect.effect['condition'] == ['hp', '=', '10']
