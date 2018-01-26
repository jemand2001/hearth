import random
from game.error import FriendlyEnemyError, TargetError
# from .card import TYPES
from .card import HealthCard
# from .minion import Minion
# from .hero import Hero
# from .spell import Spell


class Effect:
    """the class managing effects"""
    def __init__(self, effect):
        """effect: string describing the effect.
        e.g. '10_dmg' => deal 10 damage to target"""

        # if a card executes multiple effects at once
        # they're separated by a comma (',')
        if ',' in effect:
            myeffect = effect.split(',')
            myeffects = []
            for i in myeffect:
                new_effect = Effect(i)
                myeffects.append(new_effect)
            self.effect = myeffects
        else:
            self._parse_effect(effect)

        self.numtriggered = 0

    def _parse_effect(self, myeffect):
        """parse the myeffect string"""
        self.effect = {}
        if myeffect == '':
            return
        parts = myeffect.split('_')
        if 'dmg' in parts or 'heal' in parts:
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
                amount = 99999999L
            self.effect['type'] = parts[1]
            self.effect['amount'] = amount
            if len(parts) == 3:
                self.effect['targets'] = parts[3]
            elif len(parts) > 3:
                self.effect['targets'] = parts[3]
                self.effect['target_mod'] = parts[4:]
            else:
                self.effect['targets'] = 'any'

    def change_side(self, target):  # like: mind control
        """change the target's side"""
        pass

    def _select_target(self, card, player, target):
        if self.effect['targets'] == 'self':
            if card.ctype == 'spell':
                return player.hero
            else:
                return card
        aplayer = player.get_enemy(player)
        the_targets = self.effect['targets']
        if the_targets == 'all':
            if not self.effect.has_key('target_mod') or not self.effect['target_mod']:
                return player.board.battlefield
            else:
                target_mod = self.effect['target_mod']
                if target_mod == ['friendly',]:
                    return player.battlefield_list
                elif target_mod == ['enemy',]:
                    return aplayer.battlefield_list
        elif the_targets == 'any':
            if not self.effect.has_key('target_mod'):
                return target
            else:
                target_mod = self.effect['target_mod']
                if target_mod == ['friendly',] and target in player.battlefield_list:
                    return target
                elif target_mod == ['enemy',] and target in aplayer.battlefield_list:
                    return target
                else:
                    raise FriendlyEnemyError('this effect can only work'
                                             ' on the other side!')
        if 'minion' in self.effect['target_mod']:
            if the_targets == 'any':
                if target.ctype != 'minion':
                    raise TargetError()

                if ((('enemy' in self.effect['target_mod']
                      and target in player.battlefield['minions'])
                     or ('friendly' in self.effect['target_mod']
                         and target in aplayer.battlefield['minions']))):
                    raise FriendlyEnemyError('can only be used on the other side')
                return target
            elif the_targets == 'all':
                if 'friendly' in self.effect['target_mod']:
                    return player.battlefield['minions']
                elif 'enemy' in self.effect['target_mod']:
                    return aplayer.battlefield['minions']
                return player.board.minions
        elif 'hero' in self.effect['target_mod']:
            if the_targets == 'any':
                if target.ctype != 'hero':
                    raise TargetError('this can only work on hero cards')
                else:
                    return target
            elif the_targets == 'all':
                if 'friendly' in self.effect['target_mod']:
                    return player.hero
                elif 'enemy' in self.effect['target_mod']:
                    return aplayer.hero
                return player.board.heroes

    def do_effect(self, card, player, target='board'):
        """player: Player that the card this effect is caused by belongs to
        player: Player that the card this effect is caused by belongs to
        target: the effect's target card"""
        self.numtriggered += 1
        board = player.board
        # do something according to what self.effect says
        if self.effect == {}:
            return

        if isinstance(self.effect, list):
            for i in self.effect:
                i.do_effect(card, player, target)
                return

        if 'amount' in self.effect.keys() and card.ctype == 'spell':
            amount = self.effect['amount'] + player.spellpower
        else:
            amount = self.effect['amount']

        assert amount > 0

        # targets = self.effect['targets']
        # targets.extend(self.effect['target_mod'])
        # if 'random' in targets:

        target = self._select_target(card, player, target)

        if self.effect['type'] == 'heal':
            if isinstance(target, HealthCard):
                target.get_healed(amount)
            elif isinstance(target, (tuple, list)):
                for i in target:
                    i.get_healed(amount)
            # assert False, 'just healed someone!'
        elif self.effect['type'] == 'dmg':
            if isinstance(target, HealthCard):
                target.get_damaged(amount)
            elif isinstance(target, (tuple, list)):
                for i in target:
                    i.get_damaged(amount)
            # assert False, 'just hurt someone!'
