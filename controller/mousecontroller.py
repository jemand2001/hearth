#!/usr/bin/env python3
from pygame import (MOUSEBUTTONDOWN, MOUSEBUTTONUP,
                    MOUSEMOTION, QUIT, event, mouse)


class MouseController:
    def __init__(self, screen):
        self.screen = screen

    def get_events(self):
        events = {}
        for i in event.get([MOUSEBUTTONDOWN,
                            MOUSEBUTTONUP,
                            MOUSEMOTION,
                            QUIT]):
            if i.type == MOUSEBUTTONDOWN:
                mousepos = mouse.get_pos()
                events['mousebuttondown'] = mousepos
            elif i.type == MOUSEBUTTONUP:
                mousepos = mouse.get_pos()
                events['mousebuttonup'] = mousepos
            elif i.type == MOUSEMOTION:
                mousepos = mouse.get_pos()
                events['mousemotion'] = mousepos
            elif i.type == QUIT:
                events['QUIT'] = QUIT

        return events


if __name__ == '__main__':
    init()
    s = display.set_mode([1366, 768])
    mc = MouseController(s)
    while 1:
        myevents = mc.get_events()
        for j in myevents:
            print(j, events[j])
