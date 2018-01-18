from pygame import KEYDOWN, KEYUP, event


class KeyboardController:
    def __init__(self, screen):
        self.screen = screen

    def get_events(self):
        events = {
            'keydown': [],
            'keyup': []
        }
        for i in event.get([KEYDOWN, KEYUP]):
            # print(i.type, i.key)
            if i.type == KEYDOWN:
                events['keydown'].append(i.key)
            else:
                events['keyup'].append(i.key)

        # print(events)
        return events
