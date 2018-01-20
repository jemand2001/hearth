

class EventQueue:
    def __init__(self):
        self.events = []

    def add_event(self, event, eventargs=None):
        if eventargs is None:
            eventargs = {}
        if isinstance(event, str):
            self.events.append(GameEvent(event, eventargs))
        elif isinstance(event, GameEvent):
            self.events.append(event)

    def get(self):
        """really primitive"""
        return self.events

    def dequeue(self):
        return self.events.pop(0)


class GameEvent:
    def __init__(self, etype, args=None):
        if args is None:
            args = {}
        self.type = etype
        for i in args.keys():
            # this actually works! VVV
            exec 'self.%s = x' % i in {'self': self, 'x': args[i]}

    def __repr__(self):
        mydata = {'type': self.type}
        mydata.update(self.__dict__)
        return str(mydata)


if __name__ == '__main__':
    eventq = EventQueue()
    gevent = GameEvent('cardplayed', {'cname': 'something'})

    eventq.add_event(event=gevent)
    eventq.add_event(event='thingdied')

    print eventq.get()
