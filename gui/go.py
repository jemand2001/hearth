import pygame


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
        if debug or (not self.image):
            rect = list(pos1)
            rect.extend(pos2)
            pygame.draw.rect(self.screen, color, rect, 5)

        if self.image:
            pos_x, pos_y = pos1

            rect = self.image.get_rect()
            rect.x = pos_x
            rect.y = pos_y
            self.screen.blit(self.image, rect)


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
    pygame.init()
    s = pygame.display.set_mode([1366, 768])
    #s.fill((255, 255, 255))
    mygo = GameObject(s, 'little_friend.png')

    while 1:
        mygo.draw((10, 20), (200, 300), color=(255, 255, 255, 255), debug=True)
        pygame.display.flip()
