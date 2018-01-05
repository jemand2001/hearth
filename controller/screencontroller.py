import pygame
from gui.main import BoardGO, CardGO


BLACK = (0, 0, 0, 255)


class ScreenController:
    def __init__(self, elements, res=(1920, 1000), img='', debug=False):
        """elements: list of Card instances"""

        self.debug = debug
        self.res = res

        pygame.init()
        self.screen = pygame.display.set_mode(self.res)

        self.game_objects = {
            'screen': BoardGO(self.screen, img)
        }
        for i in elements:
            new_go = CardGO(self.screen, i.name)
            self.game_objects[i] = new_go
            print('Created CardGO:', new_go)

    def draw(self):
        self.screen.fill(BLACK)
        for i in self.game_objects.values():
            i.draw()


if __name__ == '__main__':
    import random
    from game.player import Player

    random.seed(0)

    deck1 = []
    for i in range(30):
        cname = 'somecard'
        c = {}
        # TODO: Translate the stuff below here!
        deck1.append((cname, c))
        """
        deck1[cname] = {
            'type': random.randint(0, 1),
            'mana': random.randint(0, 10)
        }
        deck1[cname]['cclass'] = 0

        if deck1[cname]['type'] == 0:
            deck1[cname]['effect'] = '5_dmg'
        else:
            deck1[cname]['hp'] = random.randint(0, 10)
            deck1[cname]['dmg'] = random.randint(0, 10)
    deck2 = {}
    for i in range(30):
        cname = 'somecard'
        deck2[cname] = {
            'type': random.randint(0, 1),
            'mana': i % 10
        }
        deck2[cname]['cclass'] = 1

        if deck2[cname]['type'] == 0:
            deck2[cname]['effect'] = '5_dmg'
        else:
            deck2[cname]['hp'] = random.randint(0, 10)
            deck2[cname]['dmg'] = random.randint(0, 10)"""

    vplayer = Player(0, deck1)
    vplayer.start_game()

    sc = ScreenController(vplayer.hand, debug=True)

    while 1:
        sc.draw()
