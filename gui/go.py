import pygame
import time


class GameObject:
    def __init__(self, screen, pathtoimage='', initpos=[0, 0]):
        self.image = pathtoimage
        # gameobjects.append(self)
        self.screen = screen
        try: # if pathtoimage:
            self.image = pygame.image.load(pathtoimage)
            self.irect = self.image.get_rect()
        except pygame.error:
            self.image = None
            self.initpos = initpos

    def draw(self, color=(0, 0, 0, 255), debug=False):
        if not self.image:
            
            rect = self.screen.get_rect()
            pygame.draw.rect(self.screen, color, rect, 1)
            return

        """
        if self.image:
            if pos2:
                pos_center_x = (pos1[0] + pos2[0]) / 2
                pos_center_y = (pos1[1] + pos2[1]) / 2

                pos_x = pos_center_x - (irect.width / 2)
                pos_y = pos_center_y - (irect.height / 2)

            else:
                pos_x, pos_y = pos1

            self.irect.x = pos_x
            self.irect.y = pos_y
#            self.irect.width = 500
            self.screen.blit(self.image, self.irect)
        """

        self.screen.blit(self.image, self.irect)

        if debug:
            pygame.draw.rect(self.screen, (255, 0, 0, 255), self.irect, 1)

    def move(self, direction):
        self.irect.move(direction)


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
            if i.type == pygame.KEYDOWN:
                if i.key in (pygame.K_LCTRL, pygame.K_RCTRL, pygame.KMOD_CTRL):
                    key_ctrl = True
                elif i.key == pygame.K_q:
                    key_q = True
            if i.type == pygame.QUIT or i.type == pygame.K_ESCAPE:
                import sys
                sys.exit()

        print('key_ctrl:', key_ctrl)
        print('key_q:', key_q)

        if key_ctrl == key_q == True:
            import sys
            sys.exit()
        mygo.draw(pos1=(10, 20), debug=True)
        pygame.display.flip()
