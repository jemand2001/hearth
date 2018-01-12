import pygame


class KeyboardController:
    def __init__(self, screen):
        self.screen = screen

    def get_events(self):
        events = {
            'keydown': [],
            'keyup': []
        }
        for event in event.get([KEYDOWN, KEYUP]):
            if event.type = KEYDOWN:
                events['keydown'].append(event.key)
            else:
                events['keyup'].append(event.key)

        return events
