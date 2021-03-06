from .error import FriendlyEnemyError


class Board(object):
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        player1.register_board(self)
        player2.register_board(self)

    def get_all_players(self):
        return self.players

    def get_enemy(self, player):
        # there should only ever be two players in self.players,
        # so this should always work
        if len(self.players) > 2:
            raise FriendlyEnemyError('There are too many players (%i>2)!'
                                     % len(self.players))

        for i in self.players:
            if i is not player:
                return i

    @property
    def battlefield(self):
        res = []
        for i in self.players:
            res.extend(i.battlefield_list)
        return tuple(res)

    @property
    def minions(self):
        res = []
        for i in self.players:
            res.extend(i.battlefield['minions'])
        return tuple(res)

    @property
    def heroes(self):
        res = []
        for i in self.players:
            res.append(i.hero)
        return tuple(res)
