import pygame
from os import path
from .go import GameObject
from game.data import IMG_PATH


class BoardGO(GameObject):
    def __init__(self, screen, img):
        bg_img = img + '.png'
        pathtoimage = path.join(IMG_PATH, 'screens', bg_img)
        GameObject.__init__(self, screen, pathtoimage)


class CardGO(GameObject):
    def __init__(self, screen, cname):
        c_img = cname + '.png'
        pathtoimage = path.join(IMG_PATH, 'cards', c_img)

        GameObject.__init__(self, screen, pathtoimage)
