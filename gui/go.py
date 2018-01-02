import pygame
import time


class GameObject:
    # gameobjects = []

    def __init__(self, screen, pathtoimage=''):
        self.image = pathtoimage
        # gameobjects.append(self)
        self.screen = screen
        if pathtoimage:
            self.image = pygame.image.load(pathtoimage)
        else:
            self.image = None

    def draw(self, pos1, pos2=(), color=(0, 0, 0, 255), debug=False):
        if not self.image:
            rect = list(pos1)
            rect.extend(pos2)
            pygame.draw.rect(self.screen, color, rect, 1)
            return

        if self.image:
            irect = self.image.get_rect()
            if pos2:
                pos_center_x = (pos1[0] + pos2[0]) / 2
                pos_center_y = (pos1[1] + pos2[1]) / 2

                pos_x = pos_center_x - (irect.width / 2)
                pos_y = pos_center_y - (irect.height / 2)

            else:
                pos_x, pos_y = pos1

            irect.x = pos_x
            irect.y = pos_y
            self.screen.blit(self.image, irect)

        self.screen.blit(self.image, irect)

        if debug:
            pygame.draw.rect(self.screen, (255, 0, 0, 255), irect, 1)


class Text:
    def __init__(self, screen, font, size):
        """screen: pygame screen object on which to render
        font: ttf font file"""
        self.screen = screen
        self.font = pygame.font.Font(font, size)

    def draw(self, pos, value, color=(0, 0, 0, 255)):
        surf = self.font.render(value, 1, color)
        self.screen.blit(surf, pos)


if __name__ == '__main__':
    from os import path
    from game.data import IMG_PATH
    pygame.init()
    s = pygame.display.set_mode([1366, 768])
    # s.fill((255, 255, 255))
    testpath = path.join(IMG_PATH, 'test', 'little_friend2.png')
    mygo = GameObject(s, testpath)

    while 1:
        key_q = key_ctrl = esc = False
        for i in pygame.event.get():
            # print('event:', i)
            if i.type == pygame.K_LCTRL or i.type == pygame.K_RCTRL:
                key_ctrl = True
            elif i.type == pygame.K_q:
                key_q = True
            if i.type == pygame.QUIT or i.type == pygame.K_ESCAPE:
                import sys
                sys.exit()

        if key_ctrl and key_q:
            import sys
            sys.exit()
        mygo.draw(pos1=(10, 20), debug=True)
        pygame.display.flip()
