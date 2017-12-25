import pygame
from .go import GameObject


class BoardGO(GameObject):
    def __init__(self, screen):
        GameObject.__init__(self, screen)
