from enum import Enum

__all__ = (
    'Color',
)


class Color(tuple[int, int, int], Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    GRAY = (100, 100, 100)
    BLUE = (0, 191, 255)
    GOLD = (255, 215, 0)
