import random
from board import Board
from player.player import Player, CLASSES


class Game:
    def __init__(self, p1, p2):
        """p1, p2: dict
        \tformat: {
        \t\t'name': name,
        \t\t'class': pclass (as in data.CLASSES),
        \t\t'deck': deck (in a format understandable by Deck.__init__)}"""
        self.players = {}
        self.players[p1['name']] = self.create_player(p1)
        self.players[p2['name']] = self.create_player(p2)
        self.board = Board(self.players[p1['name']],
                           self.players[p2['name']])

    def create_player(self, player):
        player1 = Player(
            player['class'],
            player['deck']
        )
        if 'mana' in player.keys():
            player1.mana = player1.actualmana = player['mana']
        return player1

    def turn(self):
        pass

    def start(self):
        startplayer_name = random.choice(self.players.keys())
        self.startplayer = self.players[startplayer_name]

        self.startplayer.start_game()

        self.otherplayer = self.board.get_enemy(self.startplayer)
