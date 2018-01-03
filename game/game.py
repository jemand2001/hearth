import random
from .board import Board
from .player import Player
from .data import CLASSES


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
        self.startplayer.start_turn()
        # now i need some mechanic to get all the actions & stuff
        # i'll work on gui system now
        self.startplayer.end_turn()

        self.otherplayer.start_turn()
        self.otherplayer.end_turn()

    def start(self):
        startplayer_name = random.choice(self.players.keys())
        self.startplayer = self.players[startplayer_name]
        self.startplayer.start_game()
        self.otherplayer = self.board.get_enemy(self.startplayer)
        self.otherplayer.start_game(False)
