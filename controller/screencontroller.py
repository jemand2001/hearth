import pygame
from gui.main import BoardGO, CardGO
from card.hero import Hero
from card.spell import Spell
from card.minion import Minion


BLACK = (0, 0, 0, 255)


class ScreenController:
    def __init__(self, elements, res=(1920, 1014), img='test', debug=False):
        """elements: list of Card instances"""

        self.debug = debug
        self.res = res

        pygame.init()
        self.screen = pygame.display.set_mode(self.res)

        self.game_objects = {
            'screen': BoardGO(self.screen, img)
        }
        for i in elements:
            if isinstance(i, Hero):
                initpos = (
                    self.res[0] / 2,
                    700
                )
                new_go = CardGO(self.screen, i.name, initpos)
                self.game_objects[i] = new_go
            else:
                cards = 0
                for j in self.game_objects.keys():
                    if not isinstance(i, Hero):
                        cards += 1
                init_x = 100 + cards * 100
                init_y = 800
                new_go = CardGO(self.screen, i.name, initpos=(init_x, init_y))
                self.game_objects[i] = new_go
            # print('Created CardGO:', new_go)

    def draw(self):
        self.screen.fill(BLACK)
        for i in self.game_objects.values():
            i.draw()
        pygame.display.flip()


if __name__ == '__main__':
    import random
    from game.player import Player

    random.seed(0)

    deck1 = []
    for i in range(30):
        cname = 'somecard'
        c = {
            'type': random.randint(0, 1),
            'mana': random.randint(0, 10)
        }
        c['cclass'] = 0

        if c['type'] == 0:
            c['effect'] = '5_dmg'
        else:
            c['hp'] = random.randint(0, 10)
            c['dmg'] = random.randint(0, 10)
        deck1.append((cname, c))

    # print(deck1)

    vplayer = Player(0, deck1)
    vplayer.start_game()

    elements = vplayer.hand[:]
    elements.append(vplayer.hero)

    sc = ScreenController(elements, debug=True)

    while 1:
        sc.draw()
