import pygame
from os import path
from .go import GameObject
from game.data import IMG_PATH


class BoardGO(GameObject):
    def __init__(self, screen, img):
        bg_img = img.lower() + '.png'
        pathtoimage = path.join(IMG_PATH, 'screens', bg_img)
        GameObject.__init__(self, screen, pathtoimage)


class CardGO(GameObject):
    def __init__(self, screen, cname, initpos=(0, 0)):
        c_img = cname.lower() + '.png'
        pathtoimage = path.join(IMG_PATH, 'cards', c_img)

        GameObject.__init__(self, screen, pathtoimage, initpos=initpos)
