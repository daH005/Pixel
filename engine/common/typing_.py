from typing import TypeAlias

from engine.common.colors import Color

__all__ = (
    'XYTupleType',
    'SizeTupleType',
    'ColorTupleType',
)

XYTupleType: TypeAlias = tuple[int, int]
SizeTupleType: TypeAlias = tuple[int, int]
ColorTupleType: TypeAlias = tuple[int, int, int] | tuple[int, int, int, float] | Color
