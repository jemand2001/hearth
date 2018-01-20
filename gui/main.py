# import pygame
from os import path
from game.data import IMG_PATH
from .go import GameObject


class BoardGO(GameObject):
    def __init__(self, screen, img='', color=(0, 0, 0, 0)):
        if img:
            bg_img = img.lower() + '.png'
            pathtoimage = path.join(IMG_PATH, 'screens', bg_img)
            GameObject.__init__(self, screen, pathtoimage, centered=False)
        else:
            GameObject.__init__(self, screen, '', centered=False, color=color)


class CardGO(GameObject):
    def __init__(self, screen, cname, initpos=(0, 0)):
        c_img = cname.lower() + '.png'
        pathtoimage = path.join(IMG_PATH, 'cards', c_img)

        GameObject.__init__(self, screen, pathtoimage, initpos=initpos)


class HeroGO(GameObject):
    def __init__(self, screen, hname, initpos=(0, 0)):
        h_img = hname.lower() + '.png'
        pathtoimage = path.join(IMG_PATH, 'cards', 'heroes', h_img)

        GameObject.__init__(self, screen, pathtoimage, initpos=initpos)
