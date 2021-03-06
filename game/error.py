

class Error(Exception):
    def __init__(self, value):
        Exception.__init__(self, value)
        self.value = value

    def __str__(self):
        return repr(self.value)


class ManaError(Error):
    pass


class FriendlyEnemyError(Error):
    pass


class TargetError(Error):
    pass


class TimeError(Error):
    pass


class ConditionError(Error):
    pass


class PermissionError(Error):
    pass


class FatalError(Error):
    pass