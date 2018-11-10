from importlib import import_module

from game.error import FriendlyEnemyError, TargetError
from utils import str2dict
from . import TYPES


def make_effect(effect):
    if isinstance(effect, dict):
        return _from_dict(effect)
    if effect == '':
        return
    if ',' in effect:
        the_effect = MultiEffect(effect)
    elif 'if' in effect:
        the_effect = CondEffect(effect)
    elif 'dmg' in effect or 'heal' in effect:
        the_effect = HealthEffect(effect)
    elif 'changeside' in effect:
        the_effect = ChangeSideEffect(effect)
    elif 'summon' in effect:
        the_effect = SummonEffect(effect, 'minion')
    elif 'destroy' in effect:
        the_effect = DestroyEffect(effect)
    else:
        raise TypeError('This effect doesn\'t exist.')
    return the_effect


class Effect:
    """the parent class for all effects"""
    def __init__(self, effect, *types):
        """effect: string describing the effect.
        e.g. '10_dmg' => deal 10 damage to target
        """
        self.ctypes = []
        for i in types:
            path = 'card.' + i.lower()
            ctype = import_module(path, i.capitalize())
            self.ctypes.append(ctype)
        if isinstance(effect, dict):
            self.effect = effect
        else:
            self.effect = {}
            self.parse_effect(effect)
        self.numtriggered = 0

    def parse_effect(self, myeffect):
        """parse the myeffect string"""
        if myeffect == '':
            return
        parts = myeffect.split('_')
        self._parse_effect(parts)

    def _select_target(self, card, player, target):
        my_target = None
        if self.effect['targets'] == 'self':
            if TYPES[card.ctype] == 'spell':
                my_target = player.hero
            else:
                my_target = card
        aplayer = player.get_enemy(player)
        the_targets = self.effect['targets']
        if 'target_mod' in self.effect:
            target_mod = self.effect['target_mod']
        else:
            target_mod = []
        if the_targets == 'all':
            if not target_mod or target_mod in (['minion'], ['hero']):
                my_target = player.board.battlefield
            elif target_mod == ['friendly', ]:
                my_target = player.battlefield_list
            elif target_mod == ['enemy', ]:
                my_target = aplayer.battlefield_list
        elif the_targets == 'any':
            if not target_mod or target_mod in (['minion'], ['hero']):
                my_target = target
            elif ((target_mod == ['friendly', ]
                   and target in player.battlefield_list)):
                my_target = target
            elif ((target_mod == ['enemy', ]
                   and target in aplayer.battlefield_list)):
                my_target = target
            else:
                raise FriendlyEnemyError('this effect can only work'
                                         ' on the other side!')
        if 'minion' in target_mod:
            if the_targets == 'any':
                if TYPES[target.ctype] != 'minion':
                    raise TargetError('wrong card type')
                if ((('enemy' in target_mod
                      and target in player.battlefield['minions'])
                     or ('friendly' in target_mod
                         and target in aplayer.battlefield['minions']))):
                    raise FriendlyEnemyError('can only be used'
                                             ' on the other side')
                my_target = target
            elif the_targets == 'all':
                if 'friendly' in target_mod:
                    my_target = player.battlefield['minions']
                elif 'enemy' in target_mod:
                    my_target = aplayer.battlefield['minions']
                my_target = player.board.minions
        elif 'hero' in target_mod:
            if the_targets == 'any':
                if TYPES[target.ctype] != 'hero':
                    raise TargetError('this can only work on hero cards')
                else:
                    my_target = target
            elif the_targets == 'all':
                if 'friendly' in target_mod:
                    my_target = player.hero
                elif 'enemy' in target_mod:
                    my_target = aplayer.hero
                else:
                    my_target = player.board.heroes
        return my_target

    def do_effect(self, card, player, target='board'):
        """player: Player that the card this effect is caused by belongs to
        player: Player that the card this effect is caused by belongs to
        target: the effect's target card"""
        self.numtriggered += 1
        # do something according to what self.effect says
        if self.effect == {}:
            return
        if 'effects' in self.effect:
            for i in self.effect['effects']:
                i.do_effect(card, player, target)
        else:
            realtarget = self._select_target(card, player, target)
            self._do_effect(card, player, realtarget)

    @property
    def deconst(self):
        return self.effect


class HealthEffect(Effect):
    def _parse_effect(self, parts):
        #################
        # damaging effect
        # pattern:
        # 'x_dmg[
        #        _to_any_[friendly|enemy]|
        #            all[friendly|enemy]_[minion|hero]|
        #               (frienly|enemy)hero]|
        #            random[...]
        #            self'
        # x = amount; target defaults to any
        #################
        self.effect['type'] = 'health'
        amount = int(parts[0])
        if amount == -1:
            amount = 99999999
        self.effect['type'] = parts[1]
        self.effect['amount'] = amount
        self.effect['target_mod'] = []
        if len(parts) == 3:
            self.effect['targets'] = parts[3]
        elif len(parts) > 3:
            self.effect['targets'] = parts[3]
            self.effect['target_mod'] = parts[4:]
        else:
            self.effect['targets'] = 'any'

    def _do_effect(self, card, player, realtarget):
        #print('HealthEffect triggered', self.effect)
        if 'amount' in self.effect.keys() and TYPES[card.ctype] == 'spell':
            amount = self.effect['amount'] + player.spellpower
        else:
            amount = self.effect['amount']
        if self.effect['type'] == 'heal':
            if realtarget.ctype in ('minion', 'hero'):
                realtarget.get_healed(amount)
            elif isinstance(realtarget, (tuple, list)):
                for i in realtarget:
                    i.get_healed(amount)
        elif self.effect['type'] == 'dmg':
            if realtarget.ctype in ('minion', 'hero'):
                realtarget.get_damaged(amount)
            elif isinstance(realtarget, (tuple, list)):
                for i in realtarget:
                    i.get_damaged(amount)


class ChangeSideEffect(Effect):
    def _parse_effect(self, parts):
        #################
        # side-changing effect
        # pattern:
        # 'changeside_of_any[friendly|enemy]|
        #                all[friendly|enemy]|
        #                random[...]|
        #                self'
        #################
        self.effect['type'] = 'changeside'
        self.effect['target_mod'] = []
        if len(parts) == 3:
            self.effect['targets'] = parts[2]
        elif len(parts) > 3:
            self.effect['targets'] = parts[2]
            self.effect['target_mod'] = parts[3:]
        else:
            self.effect['targets'] = 'any'
        self.effect['target_mod'].append('minion')

    def _do_effect(self, card, player, realtarget):
        """change the target's side"""
        # print('ChangeSideEffect triggered', self.effect)
        if isinstance(realtarget, (tuple, list)):
            for i in realtarget:
                self._do_effect(card, player, i)
        else:
            tplayer = realtarget.player
            tplayer.remove_minion(realtarget)
            tplayer.aplayer.add_minion(realtarget)


class SummonEffect(Effect):
    def _parse_effect(self, parts):
        #################
        # summoning effect (single minion)
        # pattern:
        # 'summon_<name>_<mana>_<hp>_<dmg>_<class>_<abilities>[_for_(friendly|enemy)]'
        # types:
        # str_int_int_int_str_dict
        #################
        self.effect['type'] = 'summon'
        Minion = self.ctypes[0].Minion
        name = parts[1]
        i, j, k = parts[2:5]
        mana = int(i)
        hp = int(j)
        dmg = int(k)
        cclass = parts[5]
        abilities = str2dict(parts[6])
        self.effect['targets'] = 'all'
        if len(parts) > 7:
            self.effect['target_mod'] = [parts[-1], 'hero']
        else:
            self.effect['target_mod'] = ['friendly', 'hero']
        self.effect['minion'] = Minion(name=name,
                                       mana=mana,
                                       hp=hp,
                                       dmg=dmg,
                                       cclass=cclass,
                                       abilities=abilities,
                                       source='effect')

    def _do_effect(self, card, player, realtarget):
        """summon the specified minion"""
        # print('SummonEffect triggered', self.effect)
        self.effect['minion'].summon(realtarget.player, 'effect')


class DestroyEffect(Effect):
    def _parse_effect(self, parts):
        #################
        # destroying effect
        # pattern:
        # 'destroy[_all|any|random][_friendly|enemy]'
        #################
        self.effect['type'] = 'destroy'
        parts.sort()
        if parts[0] in ('any', 'all'):
            self.effect['targets'] = parts.pop(0)
        elif parts[-1] == 'random':
            self.effect['targets'] = parts.pop(-1)
        else:
            self.effect['targets'] = 'any'
        self.effect['target_mod'] = []
        if parts[-1] != 'destroy':
            self.effect['target_mod'].append(parts[-1])

    def _do_effect(self, card, player, realtarget):
        """destroy target minion"""
        # print('DestroyEffect triggered', self.effect)
        realtarget.die()


############
#
# Special forms of effects that are detatched from the actual effects
#
############


class MultiEffect:
    """in case you want to execute multiple effects at once"""
    def __init__(self, effect):
        """multiple effects are separated by a comma (',')
        """
        self.effect = {}
        myeffect = effect.split(',')
        myeffects = []
        for i in myeffect:
            new_effect = make_effect(i)
            myeffects.append(new_effect)
        self.effect['type'] = 'multi'
        self.effect['effects'] = myeffects
        self.numtriggered = 0

    def do_effect(self, card, player, target='board'):
        # print('MultiEffect triggered!' + str(self.effect) + '\n{{{')
        self.numtriggered += 1
        for i in self.effect['effects']:
            i.do_effect(card, player, target)
        # print('}}}')


class CondEffect:
    """in case you want to only execute an effect on a condition"""
    def __init__(self, effect):
        self.effect = {}
        condition, effect = effect.split(':', 1)
        condition = condition.strip()
        effect = effect.strip()
        self.parse_condition(condition)
        self.effect['effect'] = make_effect(effect)
        self.effect['type'] = 'cond'
        self.numtriggered = 0

    def parse_condition(self, condition):
        self.effect['condition'] = condition[3:].split()

    def eval_condition(self):
        c = False
        if 'condition' not in self.effect:
            c = True
        return c

    def do_effect(self, card, player, target='board'):
        self.numtriggered += 1
        print('CondEffect triggered --')
        if self.eval_condition():
            print('successfully', self.effect)
            self.effect['effect'].do_effect(card, player, target='board')
        else:
            print('unsuccessfully', self.effect)
            #raise ConditionError('The conditions have not been met!')


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