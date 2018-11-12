import random
from .board import Board
from .player import Player
from .events import EventQueue


class Game(object):
    def __init__(self, p1, p2, board=None):
        """p1, p2: dict
        \tformat: {
        \t\t'name': name,
        \t\t'class': pclass (as in data.CLASSES),
        \t\t'deck': deck (in a format understandable by Deck.__init__)}"""
        self.events = EventQueue()
        self.players = []
        """
        if not isinstance(p1, Player):
            self.players[p1['name']] = self.create_player(p1)
        else:
            self.players[p1.name] = p1
        if not isinstance(p2, Player):
            self.players[p2['name']] = self.create_player(p2)
        else:
            self.players[p2.name] = p2
        """
        if not isinstance(p1, Player):
            self.players.append(self.create_player(p1))
        else:
            self.players.append(p1)
        if not isinstance(p2, Player):
            self.players.append(self.create_player(p1))
        else:
            self.players.append(p2)
        if board is None:
            self.board = Board(self.players[p1['name']],
                               self.players[p2['name']])
        else:
            self.board = board
        self.has_started = False

    def create_player(self, player):
        if isinstance(player, Player):
            return player
        player1 = Player(
            player['class'],
            player['deck'],
            self.events
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
        startplayer_num = random.choice(enumerate(self.players))
        self.startplayer = self.players[startplayer_num]
        self.startplayer.start_game()
        self.otherplayer = self.board.get_enemy(self.startplayer)
        self.otherplayer.start_game(False)
        self.has_started = True


    def save(self):
        player1 = self.players[0]
        player2 = self.players[1]
        savestate = {
            'player1': {
                'minions': [],
                'pclass': player1.pclass_num,
                'deck': player1.deck.deconst,
                'hero': None
            },
            'player2': {
                'minions': [],
                'pclass': player2.pclass_num,
                'deck': player2.deck.deconst,
                'hero': None,
            }
        }
        if self.has_started:
            savestate['player1']['hand'] = player1.hand.deconst
            savestate['player2']['hand'] = player2.hand.deconst
        for i in player1.minions:
            savestate['player1']['minions'].append(i.deconst)
        for i in player2.minions:
            savestate['player2']['minions'].append(i.deconst)
        return savestate
