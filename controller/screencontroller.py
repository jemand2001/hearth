import pygame
from gui.main import BoardGO, CardGO, HeroGO
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
        cards = 0
        for i in elements:
            if isinstance(i, Hero):
                initpos = (
                    self.res[0] / 2,
                    750
                )
                new_go = HeroGO(self.screen, i.name, initpos)
                self.game_objects[i] = new_go
            else:
                cards += 1
                init_x = 100 + cards * 200
                init_y = 850
                new_go = CardGO(self.screen, i.name, initpos=(init_x, init_y))
                self.game_objects[i] = new_go
            print('Created CardGO:', new_go)
        # print(len(elements))
        # print(len(self.game_objects.values()))

    def draw(self):
        self.screen.fill(BLACK) 
        screen = self.game_objects['screen']
        screen.draw()
        for i in self.game_objects.values():
            if isinstance(i, (CardGO, HeroGO)):
                i.draw(debug=self.debug)
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
    special_card = Spell('../test/little_friend', 0, '10_dmg', '*')
    vplayer.deck.put_card_on_index(special_card, len(vplayer.deck))
    vplayer.start_game()

    elements = vplayer.hand[:]
    elements.append(vplayer.hero)

    # print(elements)

    sc = ScreenController(elements, debug=True)

    while 1:
        sc.draw()
