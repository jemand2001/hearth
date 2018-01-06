#!/usr/bin/env python3
import pygame


class MouseController:
    def __init__(self, screen):
        self.screen = screen

    def get_events(self):
        events = {}
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                events['mousebuttondown'] = mousepos
            elif event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()
                events['mousebuttonup'] = mousepos
            elif event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
                events['mousemotion'] = mousepos

        return events


if __name__ == '__main__':
    pygame.init()
    s = pygame.display.set_mode([1366, 768])
    mc = MouseController(s)
    while 1:
        events = mc.get_events()
        for i in events.keys():
            print(i, events[i])
