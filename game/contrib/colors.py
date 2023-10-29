from typing import TypeAlias
from enum import Enum

__all__ = (
    'ColorTupleType',
    'Color',
)

ColorTupleType: TypeAlias = tuple[int, int, int] | tuple[int, int, int, float]


class Color(tuple, Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    GRAY = (100, 100, 100)
    BLUE = (0, 191, 255)
    GOLD = (255, 215, 0)


if __name__ == '__main__':
    print(Color.BLUE[0])
