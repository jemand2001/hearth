import pygame
import time


class GameObject:
    def __init__(self, screen, pathtoimage='', initpos=[0, 0], color=(0, 0, 0, 0), centered=True):
        self.pathtoimage = pathtoimage

        self.initpos = initpos
        self.screen = screen
        try:
            self.image = pygame.image.load(pathtoimage)
            self.irect = self.image.get_rect()
            if centered:
                self.irect.x = initpos[0] - (self.irect.width/2)
                self.irect.y = initpos[1] - (self.irect.height/2)
            else:
                self.irect.x, self.irect.y = self.initpos

        except pygame.error:
            self.color=color
            self.image = None

        self.goal = None
        self.speed = .2

    def draw(self, color=(0, 0, 0, 255), debug=False):
        if not self.image:
            if self.color != (0, 0, 0, 0):
                color = self.color

            rect = self.screen.get_rect()
            pygame.draw.rect(self.screen, color, rect, 1)
            return

        self.screen.blit(self.image, self.irect)

        if debug:
            pygame.draw.rect(self.screen, (255, 0, 0, 255), self.irect, 1)

        if self.goal is not None:
            # move toward there
            amount = (
                int((self.irect.x - self.goal[0]) * self.speed),
                int((self.irect.y - self.goal[1]) * self.speed)
            )
            self.move(amount)

    def move(self, direction):
        self.irect.move(direction)

    def set_pos(self, pos, center=True):
        if center:
            self.irect.center = pos
        else:
            self.irect.x, self.irect.y = pos

    def get_pos(self, centered=True):
        if centered:
            return self.irect.center
        else:
            return self.irect.x, self.irect.y

    def set_goal(self, pos, centered=True):
        if centered:
            pos = pos[0] - (self.irect.width/2), pos[1] - (self.irect.height/2)

        self.goal = pos


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

    # print('KEY Q: {}'.format(pygame.K_q))
    # print('KEY Ctrl: {}'.format(pygame.K_LCTRL))

    key_q = key_ctrl = esc = 0

    while 1:
        for i in pygame.event.get():
            # print('event:', i)
            if i.type == pygame.KEYDOWN:
                # print(i.key)
                
                if i.key in (pygame.K_LCTRL, pygame.K_RCTRL, pygame.KMOD_CTRL):
                    key_ctrl = 50
                elif i.key == pygame.K_q:
                    key_q = 50
            if i.type == pygame.QUIT or i.type == pygame.K_ESCAPE:
                import sys
                sys.exit()

        # print('key_ctrl:', key_ctrl)
        # print('key_q:', key_q)

        if key_ctrl > 0:
            if key_q > 0:
                import sys
                sys.exit()
        else:
            key_ctrl -= 1
        if key_q > 0:
            key_q -= 1
        mygo.set_pos((10, 20), center=False)
        mygo.draw(debug=True)
        pygame.display.flip()
