from enum import IntEnum

__all__ = (
    'ZIndex'
)


class ZIndex(IntEnum):

    TREE = -100
    BACKGROUND = -10
    MOVING_OBJECT = 5
    OVERLAY = 9
    WEB = 10
    BLOCK = 12
    HINT = 100
