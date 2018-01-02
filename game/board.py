from error import FriendlyEnemyError


class Board:
    def __init__(self, p1, p2):
        self.players = [p1, p2]

    def get_enemy(self, p):
        if p is self.players[0]:
            return self.players[1]
        else:
            return self.players[0]

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
