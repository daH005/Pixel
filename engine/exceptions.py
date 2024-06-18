__all__ = (
    'ExitFromGame',
    'MapObjectCannotBeCreated',
)


class ExitFromGame(Exception):
    pass


class MapObjectCannotBeCreated(Exception):
    pass
