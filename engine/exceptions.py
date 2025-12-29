__all__ = (
    'ExitFromGame',
    'MapObjectCannotBeCreated',
    'PlayerWasNotCreated',
)


class ExitFromGame(Exception):
    pass


class MapObjectCannotBeCreated(Exception):
    pass


class PlayerWasNotCreated(Exception):
    pass
