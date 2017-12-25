import pygame


class GameObject:
    gameobjects = []

    def __init__(self, screen, pathtoimage=''):
        self.image = pathtoimage
        gameobjects.append(self)
        self.screen = screen

    def draw(self, pos1, pos2, color=(0, 0, 0, 255)):
        rect = list(pos1)
        rect.extend(pos2)
        pygame.draw.rect(self.screen, color, rect, .1)


class Text:
    def __init__(self, screen, font):
        """screen: pygame screen object on which to render
        font: pygame font object"""
        self.screen = screen
        self.font = font

    def draw(self, pos, value, color=(0, 0, 0, 255)):
        surf = self.font.render(value, 1, color)
        self.screen.blit(surf, pos)


if __name__ == '__main__':
    s = pygame.display.set_mode([1366, 768])
    mygo = GameObject(s)
