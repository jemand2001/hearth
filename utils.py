from card.effects import HealthEffect, ChangeSideEffect, SummonEffect, DestroyEffect, MultiEffect, CondEffect


def str2dict(s):
    """
    parse a string to a dictionary.
    pattern: '{<key1>:<value1>|<key2>:<value2>|...}'
    """
    if s[0] != '{' or s[-1] != '}':
        raise SyntaxError('Invalid Syntax!')

    if ':' not in s:
        return {}
    res = {}
    my_str = s.strip('{}')
    items = my_str.split('|')
    for i in items:
        if ':' not in i:
            raise SyntaxError('Invalid Syntax!')
        key, value = i.split(':')
        key = key.strip()
        value = value.strip()
        res[key] = value
    return res


def str2tuple(mystr):
    if '|' not in mystr:
        return mystr
    my_str.strip('()')
    return tuple(my_str.split('|'))


def str2things(mystr):
    """
    convert a string to a different type
    """
    res = None
    if '|' in mystr:
        try:
            res = str2dict(mystr)
        except SyntaxError:
            res = str2tuple(mystr)
    else:
        try:
            res = int(mystr)
        except SyntaxError:
            res = mystr
    return res


def dict2str(d):
    """convert a dictionary to a string
    to be understood by str2dict"""
    res = '{'
    for i in enumerate(d):
        key, value = d.items()[i]
        res += '%s:%s' % (key, value)
        if i < len(d):
            res += '|'
    res += '}'
    return res


def _from_dict(effect):
    if effect['type'] == 'health':
        the_effect = HealthEffect(effect)
    elif effect['type'] == 'changeside':
        the_effect = ChangeSideEffect(effect)
    elif effect['type'] == 'summon':
        the_effect = SummonEffect(effect)
    elif effect['type'] == 'destroy':
        the_effect = DestroyEffect(effect)
    elif effect['type'] == 'multi':
        the_effect = MultiEffect(effect)
    elif effect['type'] == 'cond':
        the_effect = CondEffect(effect)
    else:
        raise TypeError('This effect doesn\'t exist.')
    return the_effect