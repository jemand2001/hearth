

class EventQueue:
    def __init__(self):
        self.events = []

    def add_event(self, event, eventargs={}):
        if isinstance(event, str):
            self.events.append(GameEvent(event, eventargs))
        elif isinstance(event, GameEvent):
            self.events.append(event)

    def get(self):
        return self.events

class GameEvent:
    def __init__(self, etype, args={}):
        self.type = etype
        for i in args.keys():
            # this actually works!
            exec 'self.%s = x' % i in {'self': self, 'x': args[i]}


if __name__ == '__main__':
    eq = EventQueue()
    ge = GameEvent('cardplayed', {'cname': 'something'})

    eq.add_event(event=ge)
    eq.add_event(event='thingdied')

    print eq.get()
