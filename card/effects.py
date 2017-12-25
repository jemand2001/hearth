

class Effect:
    def __init__(self, effect):
        """effect: string describing the effect.
        e.g. '10_dmg' => deal 10 damage to target"""
        self.parse_effect(effect)

    def parse_effect(self, effect):
        self.effect = {}
        parts = e.split('_')
        if 'dmg' in parts:
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
            self.effect['type'] = dmg
            self.effect['amount'] = amount
            if len(parts) > 2:
                if parts[3] == 'all':
                    self.effect['targets'] = parts[3] + parts[4]

    def damage(self, target, amount):
        target.change_prop('hp', amount)

    def change_side(self, target):  # like: mind control
        pass

    def do_effect(self, target='board'):
        # do something according to what self.effect says
        if self.effect['type'] == 'dmg':
            if ('targets' in self.effect.keys()
                or 'validtargets' in self.effect.keys()):
