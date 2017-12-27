

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
