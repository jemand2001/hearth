from ..error import *
from .card import Card


class Effect:
    def __init__(self, effect):
        """effect: string describing the effect.
        e.g. '10_dmg' => deal 10 damage to target"""

        # if a card executes multiple effects at once
        # they're separated by a comma (',')
        if ',' in effect:
            e = effect.split(',')
            myeffects = []
            for i in e:
                new_effect = Effect(i)
                myeffects.append(new_effect)
            self.effect = myeffects
        else:
            self.parse_effect(effect)

    def parse_effect(self, e):
        self.effect = {}
        if e == '':
            return
        parts = e.split('_')
        if 'dmg' in parts or 'heal' in parts:
            #################
            # damaging effect
            # pattern:
            # 'x_dmg[
            #        _to_any_[friendly|enemy]|
            #            all[friendly|enemy][minions|heros]|
            #                 [friendly|enemy](minions|heros)|
            #                 (frienly|enemy)hero|]|
            #            self'
            # x = amount; target defaults to any
            #################
            amount = int(parts[0])
            self.effect['type'] = parts[1]
            self.effect['amount'] = amount
            if len(parts) > 2:
                if parts[3] == 'all':
                    self.effect['targets'] = parts[3]
                    if len(parts) > 3:
                        self.effect['targets'] += parts[4]
                        if len(parts) == 5:
                            self.effect['targets'] += parts[5]

                elif parts[3] == 'any':
                    self.effect['validtargets'] = parts[3]
                    if len(parts) > 3:
                        self.effect['validtargets'] += parts[4]

                        if len(parts) == 5:
                            self.effect['validtargets'] += parts[5]

                elif parts[3] == 'self':
                    self.effect['targets'] = 'self'

            else:
                self.effect['validtargets'] = 'any'

    def change_side(self, target):  # like: mind control
        pass

    def do_effect(self, card, board, player, target='board'):
        """board: Board instance (the only one in the game, i'd hope)
        player: Player that the card this effect is caused by belongs to
        target: the effect's target card"""
        # do something according to what self.effect says
        if self.effect == {}:
            return

        if isinstance(self.effect, list):
            for i in self.effect:
                i.do_effect(card, board, player, target)
                return

        if 'amount' in self.effect.keys() and card.ctype == 'spell':
            amount = self.effect['amount'] + player.spellpower
        else:
            amount = self.effect['amount']

        # assert 0, self.effect

        if self.effect['type'] == 'dmg':
            if 'targets' in self.effect.keys():
                if self.effect['targets'] == 'self':
                    if card.ctype == 'spell':
                        player.hero.get_damaged(amount)
                    else:
                        card.get_damaged(amount)

                elif self.effect['targets'] == 'all':
                    for aplayer in board.players:
                        aplayer.hero.get_damaged(amount)
                        for i in aplayer.battlefield['minions']:
                            i.get_damaged(amount)

                elif self.effect['targets'][:11] == 'allfriendly':
                    if self.effect['targets'][11:] == '':
                        for i in player.battlefield:
                            i.get_damaged(amount)

                    elif self.effect['targets'][11:] == 'minions':
                        for i in player.battlefield['minions']:
                            i.get_damaged(amount)

                    elif self.effect['targets'][11:] == 'hero':
                        player.hero.get_damaged(amount)

                elif self.effect['targets'][:8] == 'allenemy':
                    aplayer = board.get_enemy(player)
                    if self.effect['targets'][8:] == '':
                        aplayer.hero.get_damaged(amount)
                        for i in aplayer.battlefield['minions']:
                            i.get_damaged(amount)

                    elif self.effect['targets'][8:] == 'minions':
                        for i in aplayer.battlefield['minions']:
                            i.get_damaged(amount)

                    elif self.effect['targets'][8:] == 'hero':
                        aplayer.hero.get_damaged(amount)

            elif 'validtargets' in self.effect.keys():
                # if not isinstance(target, Card):
                #     raise TargetError('this effect has to be directed!')

                if self.effect['validtargets'] == 'any':
                    target.get_damaged(amount)

                elif self.effect['targets'][:11] == 'anyfriendly':
                    if ((self.effect['targets'][11:] == 'minions'
                         and target in player.battlefield['minions'])):
                        target.get_damaged(amount)

                    elif (target is player.hero
                          or target in player.battlefield['minions']):
                        target.get_damaged(amount)

                    else:
                        raise FriendlyEnemyError('This effect can only work'
                                                 ' on friendly characters.')

                elif self.effect['targets'][:8] == 'anyenemy':
                    aplayer = board.get_enemy(player)
                    if self.effect['targets'][8:] == '':
                        if target is aplayer.hero:
                            aplayer.hero.get_damaged(amount)
                        else:
                            for i in aplayer.battlefield['minions']:
                                if target is i:
                                    i.get_damaged(amount)

        elif self.effect['type'] == 'heal':
            if 'targets' in self.effect.keys():
                if self.effect['targets'] == 'self':
                    if card.ctype == 'spell':
                        player.hero.get_healed(amount)
                    else:
                        card.get_healed(amount)
                elif self.effect['targets'] == 'all':
                    for aplayer in board.players:
                        aplayer.hero.get_healed(amount)
                        for i in aplayer.battlefield['minions']:
                            i.get_healed(amount)

                elif self.effect['targets'][:11] == 'allfriendly':
                    if self.effect['targets'][11:] == '':
                        for i in player.battlefield:
                            i.get_healed(amount)

                    elif self.effect['targets'][11:] == 'minions':
                        for i in player.battlefield['minions']:
                            i.get_healed(amount)

                    elif self.effect['targets'][11:] == 'hero':
                        player.hero.get_healed(amount)

                elif self.effect['targets'][:8] == 'allenemy':
                    aplayer = board.get_enemy(player)
                    if self.effect['targets'][8:] == '':
                        aplayer.hero.get_healed(amount)
                        for i in aplayer.battlefield['minions']:
                            i.get_healed(amount)

                    elif self.effect['targets'][8:] == 'minions':
                        for i in aplayer.battlefield['minions']:
                            i.get_healed(amount)

                    elif self.effect['targets'][8:] == 'hero':
                        aplayer.hero.get_healed(amount)

            elif 'validtargets' in self.effect.keys():
                # if not isinstance(target, Card):
                #     raise TargetError('this effect has to be directed!')

                if self.effect['validtargets'] == 'any':
                    target.get_healed(amount)

                elif self.effect['targets'][:11] == 'anyfriendly':
                    if ((self.effect['targets'][11:] == 'minions'
                         and target in player.battlefield['minions'])):
                        target.get_healed(amount)

                    elif (target is player.hero
                          or target in player.battlefield['minions']):
                        target.get_healed(amount)

                    else:
                        raise FriendlyEnemyError('This effect can only work'
                                                 ' on friendly characters.')

                elif self.effect['targets'][:11] == 'anyenemy':
                    aplayer = board.get_enemy(player)
                    if self.effect['targets'][8:] == '':
                        if target is aplayer.hero:
                            aplayer.hero.get_healed(amount)
                        else:
                            for i in aplayer.battlefield['minions']:
                                if target is i:
                                    i.get_healed(amount)
