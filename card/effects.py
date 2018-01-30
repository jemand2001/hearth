import random
from game.error import FriendlyEnemyError, TargetError
# from .card import TYPES
from .card import HealthCard


def make_effect(effect):
    if effect == '':
        return
    if 'dmg' in effect or 'heal' in effect:
        the_effect = HealthEffect(effect)
    elif 'changeside' in effect:
        the_effect = ChangeSide(effect)
    else:
        raise TypeError('This effect doesn\'t exist.')
    return the_effect


class Effect:
    """the class managing effects"""
    def __init__(self, effect):
        """effect: string describing the effect.
        e.g. '10_dmg' => deal 10 damage to target"""
        """
        if 'dmg' in effect or 'heal' in effect:
            EffectClass = HealthEffect
        elif 'change_sides' in effect:
            EffectClass = ChangeSide
        """
        # if a card executes multiple effects at once
        # they're separated by a comma (',')
        if ',' in effect:
            myeffect = effect.split(',')
            myeffects = []
            for i in myeffect:
                new_effect = make_effect(i)
                myeffects.append(new_effect)
            self.effect = myeffects
        else:
            # otherwise, the effect is just parsed, as-is
            self.parse_effect(effect)
        self.numtriggered = 0

    def parse_effect(self, myeffect):
        """parse the myeffect string"""
        if myeffect == '':
            return
        self.effect = {}
        parts = myeffect.split('_')
        self._parse_effect(parts)
        
    def _select_target(self, card, player, target):
        mytarget = None
        if self.effect['targets'] == 'self':
            if card.ctype == 'spell':
                mytarget = player.hero
            else:
                mytarget = card
        aplayer = player.get_enemy(player)
        the_targets = self.effect['targets']
        if 'target_mod' in self.effect:
            target_mod = self.effect['target_mod']
        else:
            target_mod = []
        if the_targets == 'all':
            if not target_mod or target_mod in (['minion'], ['hero']):
                mytarget = player.board.battlefield
            elif target_mod == ['friendly', ]:
                mytarget = player.battlefield_list
            elif target_mod == ['enemy', ]:
                mytarget = aplayer.battlefield_list
        elif the_targets == 'any':
            if not target_mod or target_mod in (['minion'], ['hero']):
                mytarget = target
            elif ((target_mod == ['friendly', ]
                   and target in player.battlefield_list)):
                mytarget = target
            elif ((target_mod == ['enemy', ]
                   and target in aplayer.battlefield_list)):
                mytarget = target
            else:
                raise FriendlyEnemyError('this effect can only work'
                                         ' on the other side!')
        if 'minion' in target_mod:
            if the_targets == 'any':
                if target.ctype != 'minion':
                    raise TargetError('wrong card type')
                if ((('enemy' in target_mod
                      and target in player.battlefield['minions'])
                     or ('friendly' in target_mod
                         and target in aplayer.battlefield['minions']))):
                    raise FriendlyEnemyError('can only be used on the other side')
                mytarget = target
            elif the_targets == 'all':
                if 'friendly' in target_mod:
                    mytarget = player.battlefield['minions']
                elif 'enemy' in target_mod:
                    mytarget = aplayer.battlefield['minions']
                mytarget = player.board.minions
        elif 'hero' in target_mod:
            if the_targets == 'any':
                if target.ctype != 'hero':
                    raise TargetError('this can only work on hero cards')
                else:
                    mytarget = target
            elif the_targets == 'all':
                if 'friendly' in target_mod:
                    mytarget = player.hero
                elif 'enemy' in target_mod:
                    mytarget = aplayer.hero
                else:
                    mytarget = player.board.heroes
        return mytarget

    def do_effect(self, card, player, target='board'):
        """player: Player that the card this effect is caused by belongs to
        player: Player that the card this effect is caused by belongs to
        target: the effect's target card"""
        self.numtriggered += 1
        # do something according to what self.effect says
        if self.effect == {}:
            return

        if isinstance(self.effect, list):
            for i in self.effect:
                i.do_effect(card, player, target)
                return
        realtarget = self._select_target(card, player, target)
        if self.effect['type'] in ('heal', 'dmg'):
            HealthEffect._do_effect(self, card, player, realtarget)
        elif self.effect['type'] == 'changeside':
            ChangeSide._do_effect(self, card, player, realtarget)


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
        if 'amount' in self.effect.keys() and card.ctype == 'spell':
            amount = self.effect['amount'] + player.spellpower
        else:
            amount = self.effect['amount']
        if self.effect['type'] == 'heal':
            if isinstance(realtarget, HealthCard):
                realtarget.get_healed(amount)
            elif isinstance(realtarget, (tuple, list)):
                for i in realtarget:
                    i.get_healed(amount)
        elif self.effect['type'] == 'dmg':
            if isinstance(realtarget, HealthCard):
                realtarget.get_damaged(amount)
            elif isinstance(realtarget, (tuple, list)):
                for i in realtarget:
                    i.get_damaged(amount)


class ChangeSide(Effect):
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
            self.effect['targets'] = parts[3]
        elif len(parts) > 3:
            self.effect['targets'] = parts[3]
            self.effect['target_mod'] = parts[4:]
        else:
            self.effect['targets'] = 'any'
        self.effect['target_mod'].append('minion')

    def _do_effect(self, card, player, realtarget):
        """change the target's side"""
        if isinstance(realtarget, (tuple, list)):
            for i in realtarget:
                self._do_effect(card, player, realtarget)
        else:
            tplayer = realtarget.player
            tplayer.remove_minion(realtarget)
            tplayer.aplayer.add_minion(realtarget)
