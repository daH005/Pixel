from enum import IntEnum

__all__ = (
    'SceneKey',
)


class SceneKey(IntEnum):
    HOME = 0
    LEVELS_MENU = 1
    LEVEL = 2
    LEVEL_PAUSE = 3
    LEVEL_LOSING = 4
    LEVEL_COMPLETION = 5
