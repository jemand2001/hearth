from ..error import *


class Effect:
    def __init__(self, effect):
        """effect: string describing the effect.
        e.g. '10_dmg' => deal 10 damage to target"""
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
            #                 (frienly|enemy)hero|]'
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
            else:
                self.effect['validtargets'] = 'any'

    def change_side(self, target):  # like: mind control
        pass

    def do_effect(self, ctype, board, player, target='board'):
        """board: Board instance (the only one in the game, i'd hope)
        player: Player that the card this effect is caused by belongs to
        target: the effect's target card"""
        # do something according to what self.effect says
        if self.effect == {}:
            return

        if 'amount' in self.effect.keys() and ctype == 'spell':
            amount = self.effect['amount'] + player.spellpower
        else:
            amount = self.effect['amount']

        if self.effect['type'] == 'dmg':
            if 'targets' in self.effect.keys():
                if self.effect['targets'] == 'all':
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
                    if self.effect['targets'][8:] == '':
                        for aplayer in board.players:
                            if aplayer is not player:
                                aplayer.hero.get_damaged(amount)
                                for i in aplayer.battlefield['minions']:
                                    i.get_damaged(amount)

                    elif self.effect['targets'][8:] == 'minions':
                        for aplayer in board.players:
                            if aplayer is not player:
                                for i in aplayer.battlefield['minions']:
                                    i.get_damaged(amount)

                    elif self.effect['targets'][8:] == 'hero':
                        for aplayer in board.players:
                            if aplayer is not player:
                                aplayer.hero.get_damaged(amount)

            elif 'validtargets' in self.effect.keys():
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

                elif self.effect['targets'][:11] == 'anyenemy':
                    pass

        elif self.effect['type'] == 'heal':
            pass
