from enum import IntEnum

__all__ = (
    'ZIndex'
)


class ZIndex(IntEnum):

    TREE = -100
    BACKGROUND = -10
    MOVING_OBJECT = 5
    OVERLAY = 9
    BLOCK = 10
    HINT = 100
