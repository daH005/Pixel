from typing import TypeAlias
from pygame.rect import Rect

from engine.common.colors import Color
from engine.common.float_rect import FloatRect

__all__ = (
    'XYTupleType',
    'SizeTupleType',
    'ColorTupleType',
    'AnyRectType',
    'CameraBoundingLineType',
    'CameraBoundingLinesType',
)

XYTupleType: TypeAlias = tuple[int, int]
SizeTupleType: TypeAlias = tuple[int, int]
ColorTupleType: TypeAlias = tuple[int, int, int] | tuple[int, int, int, float] | Color

AnyRectType: TypeAlias = Rect | FloatRect

CameraBoundingLineType: TypeAlias = tuple[int, int, int]
CameraBoundingLinesType: TypeAlias = list[CameraBoundingLineType]
