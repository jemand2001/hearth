from game.error import FriendlyEnemyError
# from .card import Card


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

        self.numtriggered = 0

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
            if len(parts) > 3:
                if parts[3] == 'all':
                    self.effect['targets'] = parts[3]
                    if len(parts) > 4:
                        self.effect['targets'] += parts[4]
                        if len(parts) == 6:
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

    def specify_target(self):
        if 'targets' in self.effect.keys():
            if self.effect['targets'] == 'self':
                target = 'self'
            elif self.effect['targets'] == 'all':
                target = 'all'
            elif self.effect['targets'][:11] == 'allfriendly':
                target = 'allfriendly'
                if self.effect['targets'][11:] == 'minions':
                    target += 'minions'
                elif self.effect['targets'][11:] == 'hero':
                    target += 'hero'
            elif self.effect['targets'][:8] == 'allenemy':
                target = 'allenemy'
                if self.effect['targets'][8:] == 'minions':
                    target += 'minions'
                elif self.effect['targets'][8:] == 'hero':
                    target += 'hero'
        elif 'validtargets' in self.effect.keys():
            if self.effect['validtargets'] == 'any':
                target = 'any'
            elif self.effect['validtargets'][:11] == 'anyfriendly':
                target = 'anyfriendly'
                if self.effect['validtargets'][11:] == 'minions':
                    target += 'minions'
                elif self.effect['validtargets'][11:] == 'hero':
                    target += 'hero'
            elif self.effect['validtargets'][:8] == 'anyenemy':
                target = 'anyenemy'
                if self.effect['validtargets'][8:] == 'minions':
                    target += 'minions'
                elif self.effect['validtargets'][8:] == 'hero':
                    target += 'hero'
        return target

    def do_effect(self, card, player, target='board'):
        self.numtriggered += 1
        """player: Player that the card this effect is caused by belongs to
        player: Player that the card this effect is caused by belongs to
        target: the effect's target card"""
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

        if (('targets' in self.effect.keys() or
             'validtargets' in self.effect.keys())):
            targets = self.specify_target()
        else:
            targets = None

        aplayer = board.get_enemy(player)

        # assert 0, self.effect

        if ((targets[:11] == 'anyfriendly'
             and target is not player.hero
             and target not in player.battlefield['minions'])
                or targets[:8] == 'anyenemy'
                and (target is not aplayer.hero
                     and target not in aplayer.battlefield['minions'])):
            raise FriendlyEnemyError('This effect can only work'
                                     ' on the other side.')

        if self.effect['type'] == 'dmg':
            if targets == 'self':
                if card.ctype == 'spell':
                    player.hero.get_damaged(amount)
                else:
                    card.get_damaged(amount)
            elif targets == 'all':
                for theplayer in board.players:
                    theplayer.hero.get_damaged(amount)
                    for i in theplayer.battlefield['minions']:
                        i.get_damaged(amount)
            elif targets == 'allfriendly':
                player.hero.get_damaged(amount)
                for i in player.battlefield['minions']:
                    i.get_damaged(amount)
            elif targets == 'allfriendlyminions':
                for i in player.battlefield['minions']:
                    i.get_damaged(amount)
            elif target == 'allfriendlyhero':
                player.hero.get_damaged(amount)
            elif targets == 'allenemy':
                aplayer.hero.get_damaged(amount)
                for i in aplayer.battlefield['minions']:
                    i.get_damaged(amount)
            elif targets == 'allenemyminions':
                for i in aplayer.battlefield['minions']:
                    i.get_damaged(amount)
            elif targets == 'allenemyhero':
                aplayer.hero.get_damaged(amount)

            if targets == 'any':
                target.get_damaged(amount)
            elif ((targets == 'anyfriendlyminion'
                   and target in player.battlefield['minions'])):
                target.get_damaged(amount)
            elif (targets == 'anyfriendly'
                  and (target is player.hero
                       or target in player.battlefield['minions'])):
                target.get_damaged(amount)

            elif targets == 'anyenemy':
                if target is aplayer.hero:
                    aplayer.hero.get_damaged(amount)
                elif target in aplayer.battlefield['minions']:
                    target.get_damaged(amount)
            elif targets == 'anyenemyminion':
                if target in aplayer.battlefield['minions']:
                    target.get_damaged(amount)

        elif self.effect['type'] == 'heal':
            if amount == -1:
                # full heal
                amount = 99999999L

            if targets == 'self':
                if card.ctype == 'spell':
                    player.hero.get_healed(amount)
                else:
                    card.get_healed(amount)
            elif targets == 'all':
                for theplayer in board.players:
                    theplayer.hero.get_healed(amount)
                    for i in theplayer.battlefield['minions']:
                        i.get_healed(amount)
            elif targets == 'allfriendly':
                player.hero.get_healed(amount)
                for i in player.battlefield['minions']:
                    i.get_healed(amount)
            elif targets == 'allfriendlyminions':
                for i in player.battlefield['minions']:
                    i.get_healed(amount)
            elif target == 'allfriendlyhero':
                player.hero.get_healed(amount)
            elif targets == 'allenemy':
                aplayer.hero.get_healed(amount)
                for i in aplayer.battlefield['minions']:
                    i.get_healed(amount)
            elif targets == 'allenemyminions':
                for i in aplayer.battlefield['minions']:
                    i.get_healed(amount)
            elif targets == 'allenemyhero':
                aplayer.hero.get_healed(amount)

            if targets == 'any':
                target.get_healed(amount)
            elif ((targets == 'anyfriendlyminion'
                   and target in player.battlefield['minions'])):
                target.get_healed(amount)
            elif (targets == 'anyfriendly'
                  and (target is player.hero
                       or target in player.battlefield['minions'])):
                target.get_healed(amount)

            elif targets == 'anyenemy':
                if target is aplayer.hero:
                    aplayer.hero.get_healed(amount)
                elif target in aplayer.battlefield['minions']:
                    target.get_healed(amount)
            elif targets == 'anyenemyminion':
                if target in aplayer.battlefield['minions']:
                    target.get_healed(amount)
